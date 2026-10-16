"""Teacher labels for synthetic chats (spec §7, §4): every customer message's intent + the order after the last
message, in one call per chat, then finalized in code (core/finalize).

Automatic consistency checks drop a label when: the JSON doesn't match the contract (schema/label.py), the
intents don't cover each customer message once in order, finalize fails, or a grounding check fails (evidence
quote not in the cited customer message, unknown menu ids; checks.py). The card is then compared with the label:
a disagreement is not a drop but a flag for the label audit (spec §11d).
"""

import json
from collections import Counter
from importlib.resources import files
from typing import Any

from pydantic import ValidationError

from orderslm.checks import Issue, check_all
from orderslm.core.finalize import FINALIZE_VERSION, finalize_order
from orderslm.extractors.teacher import conversation_prompt, portable_schema
from orderslm.llm.types import ChatMessage, ChatRequest
from orderslm.schema.conversation import Conversation, Role
from orderslm.schema.extraction import DecisionState, ExtractionOutput, ItemProposal, ModificationKind
from orderslm.schema.label import TeacherLabel
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.routing import LABEL_DESCRIPTIONS
from orderslm.schema.synthetic import LabeledConversation, PlannedItem, SynthCard

LABEL_PROMPT_VERSION = "teacher-label@0.4"  # 0.2: answering a size question is PLACE_ORDER; 0.3 (p3 audit): PLACE vs MODIFY by "adds vs changes", answers take the request's label, garbled text is UNKNOWN with no items; 0.4: an answer keeps its own request's label, additions after a confirm are MODIFY
TEACHER = "openai/gpt-6-luna@low"  # Julian, 2026-10-15 (docs/TEACHER_BAKEOFF.md)
MAX_OUTPUT_TOKENS = 16000


def prompt_text(version: str = LABEL_PROMPT_VERSION) -> str:
    text = (files("orderslm.extractors") / "prompts" / f"{version}.md").read_text()
    labels = "\n".join(f"- `{label.value}`: {desc}" for label, desc in LABEL_DESCRIPTIONS.items())
    return text.replace("{label_descriptions}", labels)


def build_request(conversation: Conversation, menu: MenuCatalog) -> ChatRequest:
    schema = portable_schema(TeacherLabel)
    system = (
        prompt_text()
        + "\n# JSON schema\nThe output must be one JSON object valid against this schema:\n"
        + json.dumps(schema, separators=(",", ":"))
        + "\n"
    )
    user = (
        conversation_prompt(menu.extractor_view(), conversation)
        + "\n\nReturn the intents and the order after the last message as one JSON object."
    )
    return ChatRequest(
        system=system,
        messages=[ChatMessage(role="user", content=user)],
        json_schema=schema,
        schema_name="teacher_label",
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )


def _customer_evidence(output: ExtractionOutput, conversation: Conversation) -> list[Issue]:
    roles = {m.index: m.role for m in conversation.messages}
    return [
        Issue("EVIDENCE_NOT_CUSTOMER", path, f"message {e.message_index} is not a customer message")
        for path, e in output.iter_evidence()
        if roles.get(e.message_index) is not Role.customer
    ]


def parse_label(
    text: str, conversation: Conversation, menu: MenuCatalog, teacher: str
) -> tuple[LabeledConversation | None, str | None]:
    """(label, None) or (None, drop reason). Never raises."""
    try:
        label = TeacherLabel.model_validate(json.loads(text))
    except (ValueError, ValidationError) as e:
        return None, f"invalid_contract: {str(e)[:300]}"
    got = [i.message_index for i in label.intents]
    if got != conversation.customer_indices():
        return None, f"intents_mismatch: {got} vs customer messages {conversation.customer_indices()}"
    try:
        extraction = finalize_order(label.order, menu, conversation.language)
    except (ValueError, ValidationError) as e:
        return None, f"finalize: {str(e)[:300]}"
    issues = check_all(extraction, conversation, menu) + _customer_evidence(extraction, conversation)
    if issues:
        return None, "check_failed: " + "; ".join(f"{i.code} {i.path}" for i in issues[:5])
    return (
        LabeledConversation(
            conversation_id=conversation.id,
            teacher=teacher,
            label_prompt_version=LABEL_PROMPT_VERSION,
            finalize_version=FINALIZE_VERSION,
            intents=label.intents,
            extraction=extraction if extraction.items else None,
        ),
        None,
    )


# ---------------------------------------------------------------- card vs label


def _planned_key(p: PlannedItem) -> tuple[str, int]:
    if p.off_menu_text is not None:
        return "off_menu", p.quantity
    if p.halves is not None:
        return "halves:" + "+".join(sorted(p.halves)), p.quantity
    return str(p.menu_item_id), p.quantity


def _line_key(line: ItemProposal) -> tuple[str, int | None]:
    if line.unmatched_text is not None:
        return "off_menu", line.quantity
    if line.halves is not None:
        return "halves:" + "+".join(sorted(h.menu_item_id for h in line.halves)), line.quantity
    return str(line.menu_item_id), line.quantity


def _mods(remove: set, add: set, substitute: set) -> tuple[frozenset, frozenset]:
    """A substitute (a → b) counts the same as removing a and adding b: "no ketchup, add mustard instead"."""
    return frozenset(remove | {a for a, _ in substitute}), frozenset(add | {b for _, b in substitute})


def _planned_detail(p: PlannedItem, menu: MenuCatalog) -> tuple[Any, ...]:
    variant = p.variant_id
    if variant is None and p.menu_item_id is not None:
        item = menu.item(p.menu_item_id)
        variant = item.default_variant_id if item is not None else None
    return (
        _planned_key(p),
        variant,
        _mods(set(p.remove), set(p.add), set(p.substitute.items())),
        frozenset(p.combo.items()),
    )


def _line_detail(line: ItemProposal) -> tuple[Any, ...]:
    mods = line.modifications
    return (
        _line_key(line),
        line.variant_id,
        _mods(
            {m.modifier_id for m in mods if m.kind is ModificationKind.remove},
            {m.modifier_id for m in mods if m.kind is ModificationKind.add and m.modifier_id},
            {
                (m.modifier_id, m.replacement_modifier_id)
                for m in mods
                if m.kind is ModificationKind.substitute
            },
        ),
        frozenset((s.slot_id, s.menu_item_id) for s in line.combo_selections),
    )


def card_agreement(card: SynthCard, label: LabeledConversation, menu: MenuCatalog) -> dict[str, Any]:
    """Where the teacher's label disagrees with what the card asked the generator to write. A disagreement means
    the generator didn't follow the card or the teacher misread the chat: both are reasons to look (§11d)."""
    lines = label.extraction.items if label.extraction else []
    items_ok = Counter(_planned_key(p) for p in card.items) == Counter(_line_key(x) for x in lines)
    details_ok = Counter(_planned_detail(p, menu) for p in card.items) == Counter(
        _line_detail(x) for x in lines
    )
    seen = {i.primary for i in label.intents} | {i.secondary for i in label.intents if i.secondary}
    missing_labels = [x.value for x in card.expected_labels if x not in seen]
    decision = label.extraction.customer_decision.state if label.extraction else None
    decision_ok = True
    if card.scenario.value == "cancellation":
        decision_ok = decision is DecisionState.cancelled
    # correction_after_confirmation has no decision check: a customer may confirm again after the change.
    flags = []
    if not items_ok:
        flags.append("items")
    elif not details_ok:
        flags.append("item_details")
    if missing_labels:
        flags.append("labels")
    if not decision_ok:
        flags.append("decision")
    return {"flags": flags, "missing_labels": missing_labels, "items_ok": items_ok, "details_ok": details_ok}
