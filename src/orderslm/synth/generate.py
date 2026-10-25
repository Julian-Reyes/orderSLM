"""Writing a synthetic chat from a card (spec §7): one call per card to the card's generator model.

The generator sees the menu without prices and the card without ids (names only), and returns the messages.
Code adds the indices and timestamps (seeded from the card, starting at the card's start time), trims business
messages after the last customer message and removes a top-level `"type": "object"` the model echoes from the
schema (both logged in `repairs`), and drops chats that break a rule the label
can't repair: invalid JSON, no customer message, a business message that states a price.
"""

import json
import random
import re
from datetime import timedelta
from importlib.resources import files

from pydantic import ValidationError

from orderslm.extractors.teacher import portable_schema
from orderslm.llm.types import ChatMessage, ChatRequest
from orderslm.schema.conversation import Conversation, Message, Role, Source, Split
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.synthetic import GeneratedChat, SynthCard, SyntheticConversation

from .cards import FEATURE_TEXT, STYLE_TEXT, item_text

GENERATOR_PROMPT_VERSION = "synth-write@0.2"  # 0.2: steps in order, card address, no formal letters
MAX_OUTPUT_TOKENS = 4000
PRICE = re.compile(r"\$\s?\d|\b\d+\.\d{2}\b|\b\d+\s*(dollars?|bucks)\b", re.IGNORECASE)


def prompt_text(version: str = GENERATOR_PROMPT_VERSION) -> str:
    return (files("orderslm.synth") / "prompts" / f"{version}.md").read_text()


def menu_view(menu: MenuCatalog) -> str:
    """The menu for the generator: names, sizes, options, combos, hours and services. No prices, no ids."""
    mods = {m.id: m.name for m in menu.modifiers}
    lines = [
        f"{menu.name}. Open {menu.opens_at:%H:%M}-{menu.closes_at:%H:%M}. "
        f"{'Delivery and pickup' if menu.delivery.available else 'Pickup only, no delivery'}. "
        f"Payment: {', '.join(menu.accepts_payment)}."
    ]
    for item in menu.items:
        parts = [f"- {item.name} ({item.category})"]
        if item.variants:
            parts.append("sizes/flavors: " + ", ".join(v.name for v in item.variants))
        if item.ingredient_ids:
            parts.append("comes with: " + ", ".join(mods[m] for m in item.ingredient_ids))
        if item.addon_ids:
            parts.append("can add: " + ", ".join(mods[m] for m in item.addon_ids))
        if item.splittable:
            parts.append("half-and-half allowed")
        for slot in item.combo_slots:
            parts.append(f"{slot.name}: " + " / ".join(menu.item(c).name for c in slot.choices))  # type: ignore[union-attr]
        lines.append("; ".join(parts))
    return "\n".join(lines)


def card_view(card: SynthCard, menu: MenuCatalog) -> str:
    lines = [
        f"Persona: {card.persona}",
        f"Style: {STYLE_TEXT[card.style]}",
        "Features: " + (", ".join(FEATURE_TEXT[f] for f in card.features) or "none"),
        f"Customer messages: about {card.customer_messages}",
        f"What happens: {card.brief}",
    ]
    if card.items:
        lines.append("Final order: " + "; ".join(item_text(p, menu) for p in card.items))
    return "\n".join(lines)


def build_request(card: SynthCard, menu: MenuCatalog) -> ChatRequest:
    schema = portable_schema(GeneratedChat)
    system = (
        prompt_text()
        + "\n# JSON schema\nThe output must be one JSON object valid against this schema:\n"
        + json.dumps(schema, separators=(",", ":"))
        + "\n"
    )
    user = f"Menu:\n{menu_view(menu)}\n\nScenario card:\n{card_view(card, menu)}\n\nWrite the chat as one JSON object."
    return ChatRequest(
        system=system,
        messages=[ChatMessage(role="user", content=user)],
        json_schema=schema,
        schema_name="synthetic_chat",
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )


def _strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t
        t = t.rsplit("```", 1)[0]
    return t.strip()


def to_conversation(
    card: SynthCard, text: str, *, prompt_version: str = GENERATOR_PROMPT_VERSION
) -> tuple[SyntheticConversation | None, str | None]:
    """(conversation, None) or (None, drop reason). Never raises."""
    repairs = []
    try:
        raw = json.loads(_strip_fences(text))
        # DeepSeek flash sometimes appends the schema's own `"type": "object"` (t3 pilot: 2 of 10, 2026-10-25)
        if isinstance(raw, dict) and raw.get("type") == "object" and set(raw) == {"messages", "type"}:
            del raw["type"]
            repairs.append("removed_schema_type_key")
        chat = GeneratedChat.model_validate(raw)
    except (ValueError, ValidationError) as e:
        return None, f"invalid_output: {str(e)[:200]}"
    msgs = list(chat.messages)
    while msgs and msgs[-1].role is not Role.customer:  # the label is "after the last customer message"
        msgs.pop()
        repairs.append("trimmed_trailing_business_message")
    if not msgs:
        return None, "no_customer_message"
    for m in msgs:
        if m.role is Role.business and PRICE.search(m.text):
            return None, "business_states_price"
    rng = random.Random(card.id)
    at = card.start_at
    messages = []
    for i, m in enumerate(msgs):
        if i:
            prev = msgs[i - 1].role
            gap = (3, 40) if prev is m.role else ((20, 90) if m.role is Role.business else (15, 120))
            at = at + timedelta(seconds=rng.randint(*gap))
        messages.append(Message(index=i, role=m.role, text=m.text, sent_at=at))
    conv = Conversation(
        id=card.id,
        business_id=card.business_id,
        split=Split.synthetic,
        source=Source.synthetic,
        messages=messages,
    )
    return (
        SyntheticConversation(
            conversation=conv,
            card_id=card.id,
            generator=card.generator,
            generator_prompt_version=prompt_version,
            repairs=repairs,
        ),
        None,
    )
