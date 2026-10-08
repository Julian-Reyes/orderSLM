"""Scenario cards for Source A, the Claude-written evaluation chats (spec §7, docs/SPLITS.md).

A card says what one conversation must contain: business, situation, the router labels it must
exercise, tricky-case tags, writing style and features, fulfillment, a persona and a short brief.
Claude writes exactly one conversation per card. Cards are split dev/test up front, so a test
conversation never shares a card (or its situation instance) with a dev one.

Coverage is by construction (fixed per-split quotas per situation); everything else (style,
persona, variants, fulfillment, business within what the situation allows) comes from a seeded RNG.
Cards added after the first review (SUPPLEMENT) are appended with their own RNG stream, so earlier
cards never change.
Dev cards: data/dev/cards.jsonl. Test cards: data/test/cards.jsonl (sealed like the test split).

    uv run python -m orderslm.data.cards summary            # dev only
    ORDERSLM_UNSEAL_TEST="author Source A" uv run python -m orderslm.data.cards generate
"""

import argparse
import json
import random
from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field

from orderslm.menus import load_menus
from orderslm.schema.annotation import Scenario, WritingStyle
from orderslm.schema.common import ID_PATTERN, Strict
from orderslm.schema.conversation import Split
from orderslm.schema.routing import RouterLabel

from .splits import split_dir

CARDS_FILE = "cards.jsonl"
SEED = 20261007
L = RouterLabel
S = Scenario


class Feature(StrEnum):
    typos = "typos"
    abbreviations = "abbreviations"
    emoji = "emoji"
    burst = "burst"  # several short messages in a row
    all_caps = "all_caps"


class ScenarioCard(Strict):
    id: str = Field(pattern=ID_PATTERN)
    split: Split
    business_id: str = Field(pattern=ID_PATTERN)
    situation: str
    variant: str | None = Field(
        default=None, description="situation-specific twist, e.g. the_usual, cold_food"
    )
    expected_labels: list[RouterLabel] = Field(
        min_length=1, description="labels that must appear (primary or secondary)"
    )
    scenarios: list[Scenario] = Field(min_length=1)
    style: WritingStyle
    features: list[Feature]
    fulfillment: Literal["delivery", "pickup", "unstated", "not_applicable"]
    customer_messages: int = Field(ge=1, le=12, description="target number of customer messages")
    persona: str
    brief: str


@dataclass(frozen=True)
class Situation:
    labels: tuple[RouterLabel, ...]
    scenarios: tuple[Scenario, ...]
    counts: tuple[int, int]  # (dev, test) in the first batch; SUPPLEMENT adds more
    brief: str  # may use {variant}
    messages: tuple[int, int]  # customer message range
    order: bool = True  # builds an order (so fulfillment applies)
    variants: tuple[str, ...] = ()
    businesses: tuple[str, ...] | None = None  # None = any allowed in the split


COMBO_MENUS = ("corner-patty", "morning-crumb", "lucky-lime")

SITUATIONS: dict[str, Situation] = {
    "simple_order": Situation(
        (L.PLACE_ORDER,),
        (S.simple_order,),
        (8, 17),
        "Places a complete order quickly: items, how they get it, and payment.",
        (1, 3),
    ),
    "multi_message_order": Situation(
        (L.PLACE_ORDER,),
        (S.multi_message_order,),
        (8, 17),
        "Builds the order across several messages, adding items and details one at a time.",
        (3, 6),
    ),
    "correction": Situation(
        (L.PLACE_ORDER, L.MODIFY_ORDER),
        (S.correction,),
        (6, 12),
        "Changes something already ordered before confirming: {variant}.",
        (2, 5),
        variants=(
            "change a size",
            "change a quantity",
            "swap one item for another",
            "remove an item",
            "change pickup to delivery or back",
            "change the time",
        ),
    ),
    "correction_after_confirmation": Situation(
        (L.PLACE_ORDER, L.CONFIRM_ORDER, L.MODIFY_ORDER),
        (S.correction_after_confirmation, S.contextual_yes),
        (4, 8),
        "Confirms the business's summary, then changes something right after: {variant}.",
        (3, 5),
        variants=("add one more item", "change a size", "change the address", "switch payment method"),
    ),
    "cancellation": Situation(
        (L.PLACE_ORDER, L.CANCEL_ORDER),
        (S.cancellation,),
        (4, 8),
        "Starts an order, then cancels the whole thing ({variant}).",
        (2, 4),
        variants=("changed their mind", "found it too expensive", "plans changed", "ordered somewhere else"),
    ),
    "contextual_yes": Situation(
        (L.PLACE_ORDER, L.CONFIRM_ORDER),
        (S.contextual_yes,),
        (4, 8),
        "Answers the business's summary with a bare 'yes'-type reply ({variant}); only the context makes it a confirmation.",
        (2, 4),
        variants=("yes", "yep thats it", "ok sounds good", "👍", "correct"),
    ),
    "two_requests": Situation(
        (L.PLACE_ORDER,),
        (S.two_requests,),
        (5, 10),
        "One message both adds to the order and asks a {variant}.",
        (1, 4),
        variants=("menu question", "delivery question", "payment question"),
    ),
    "ambiguous_reference": Situation(
        (L.PLACE_ORDER, L.MODIFY_ORDER),
        (S.ambiguous_reference,),
        (4, 8),
        "Refers to something vaguely: '{variant}'. Gold marks it ambiguous where it can't be resolved.",
        (2, 5),
        variants=("one of them", "the usual", "same as last time", "that one", "the other one"),
    ),
    "off_menu": Situation(
        (L.PLACE_ORDER,),
        (S.off_menu,),
        (4, 8),
        "Asks for something the menu doesn't have ({variant}) alongside real items.",
        (1, 4),
        variants=(
            "an item from another cuisine",
            "a size that doesn't exist",
            "a topping or add-on not offered",
            "a brand-name drink not on the menu",
        ),
    ),
    "missing_info": Situation(
        (L.PLACE_ORDER,),
        (S.missing_info,),
        (4, 10),
        "Leaves something required out and stops: {variant}.",
        (1, 3),
        variants=(
            "no size",
            "no pickup/delivery",
            "delivery without an address",
            "no payment method",
            "a vague time like 'around 7 or 8'",
            "an unclear quantity like 'some'",
        ),
    ),
    "half_and_half": Situation(
        (L.PLACE_ORDER,),
        (S.half_and_half,),
        (3, 6),
        "Orders a half-and-half pizza ({variant}).",
        (1, 4),
        variants=("two recipe pizzas", "different toppings on each half", "with the size left out"),
        businesses=("halfmoon-pizza",),
    ),
    "combo": Situation(
        (L.PLACE_ORDER,),
        (S.combo,),
        (3, 6),
        "Orders a combo and {variant}.",
        (1, 4),
        variants=("picks every choice", "forgets one choice", "upsizes a choice"),
        businesses=COMBO_MENUS,
    ),
    "menu_question": Situation(
        (L.MENU_QUESTION,),
        (S.menu_question,),
        (3, 6),
        "Asks about the menu ({variant}), maybe orders after.",
        (1, 3),
        order=False,
        variants=("ingredients or allergens", "sizes", "prices", "what's popular", "vegetarian options"),
    ),
    "delivery_question": Situation(
        (L.DELIVERY_QUESTION,),
        (S.delivery_question,),
        (2, 5),
        "Asks about {variant}.",
        (1, 3),
        order=False,
        variants=("the delivery area", "the delivery fee", "opening hours", "whether pickup is possible"),
    ),
    "payment_question": Situation(
        (L.PAYMENT_QUESTION,),
        (S.payment_question,),
        (2, 5),
        "Asks how to pay ({variant}).",
        (1, 3),
        order=False,
        variants=("card at the door", "cash and change", "paying online"),
    ),
    "payment_claim": Situation(
        (L.PAYMENT_CLAIM,),
        (S.payment_claim,),
        (2, 5),
        "Says they already paid ({variant}); the claim stays unverified.",
        (1, 3),
        variants=("during an order", "after the order was placed", "with a screenshot mention"),
    ),
    "status_question": Situation(
        (L.ORDER_STATUS,),
        (S.status_question,),
        (2, 5),
        "Asks where an order placed earlier is ({variant}).",
        (1, 3),
        order=False,
        variants=("politely", "impatient", "asks for an ETA"),
    ),
    "order_problem": Situation(
        (L.ORDER_PROBLEM,),
        (S.order_problem,),
        (2, 5),
        "Complains about a received order: {variant}.",
        (1, 4),
        order=False,
        variants=("missing item", "wrong item", "cold food", "very late", "allergy concern"),
    ),
    "refund_request": Situation(
        (L.REFUND_REQUEST,),
        (S.refund_request,),
        (2, 4),
        "Asks for money back after a problem ({variant}).",
        (1, 3),
        order=False,
        variants=("item never arrived", "charged twice", "wrong order"),
    ),
    "human_request": Situation(
        (L.HUMAN_REQUEST,),
        (S.human_request,),
        (2, 5),
        "Asks to talk to a real person ({variant}).",
        (1, 3),
        order=False,
        variants=("frustrated with the bot", "large catering order", "complicated allergy question"),
    ),
    "small_talk": Situation(
        (L.SMALL_TALK,),
        (S.small_talk,),
        (2, 4),
        "Only chit-chat ({variant}); no request.",
        (1, 2),
        order=False,
        variants=("greeting", "thanks after a meal", "compliment"),
    ),
    "out_of_scope": Situation(
        (L.OUT_OF_SCOPE,),
        (S.out_of_scope,),
        (2, 4),
        "Asks something unrelated to ordering here ({variant}).",
        (1, 2),
        order=False,
        variants=("a job application", "a different business", "general trivia"),
    ),
    "implicit_category": Situation(
        (L.PLACE_ORDER,),
        (S.implicit_category,),
        (0, 0),
        "Orders without naming the menu category: {variant}. Gold maps each mention to the item it means, "
        "or marks it ambiguous if the chat never settles it.",
        (2, 4),
        variants=(
            "a drink by a casual word instead of its name ('pop', 'something fizzy', 'something warm')",
            "items by name only, without category words",
            "a vague request like 'something sweet' or 'something to snack on', settled with the business's help",
        ),
    ),
    "unclear": Situation(
        (L.UNKNOWN,),
        (S.unclear_message,),
        (2, 4),
        "Sends something too unclear to interpret ({variant}).",
        (1, 2),
        order=False,
        variants=("a stray character", "a garbled message", "an unexplained number"),
    ),
}

# Second batch (Julian's card review, 2026-10-08): +1 dev / +3 test for each rare label, and implicit
# category mentions for the menu-narrowing evaluation (spec §11e). Appended after the first batch.
SUPPLEMENT: dict[str, tuple[int, int]] = {
    "human_request": (1, 3),
    "order_problem": (1, 3),
    "status_question": (1, 3),
    "payment_claim": (1, 3),
    "out_of_scope": (1, 3),
    "refund_request": (1, 3),
    "unclear": (1, 3),
    "implicit_category": (4, 8),
}
SUPPLEMENT_SEED = f"{SEED}-supplement-2026-10-08"


def quota(name: str, split: Split) -> int:
    """Total cards per situation and split, over both batches."""
    k = split is Split.test
    return SITUATIONS[name].counts[k] + SUPPLEMENT.get(name, (0, 0))[k]


SECOND_REQUEST = {
    "menu question": L.MENU_QUESTION,
    "delivery question": L.DELIVERY_QUESTION,
    "payment question": L.PAYMENT_QUESTION,
}

# Optional extras layered on order cards, so non-order labels also show up mid-order.
EXTRAS = {
    "greets_first": ((L.SMALL_TALK,), (S.small_talk,), "Opens with a greeting before ordering."),
    "asks_menu_mid_order": ((L.MENU_QUESTION,), (), "Asks a menu question partway through."),
}
EXTRA_RATE = 0.3

STYLE_WEIGHTS = {
    WritingStyle.clean: 0.2,
    WritingStyle.texting: 0.3,
    WritingStyle.rapid_fire: 0.2,
    WritingStyle.shouty: 0.12,
    WritingStyle.emoji: 0.18,
}
PERSONAS = [
    "busy parent ordering for the family",
    "college student, late night",
    "office worker ordering lunch for a few coworkers",
    "regular customer who knows the menu",
    "first-time customer, a bit unsure",
    "older customer, polite and wordy",
    "teenager texting fast",
    "someone ordering for a party",
    "commuter picking up on the way home",
    "night-shift worker",
    "customer with a dietary restriction",
    "tourist new to the area",
]


def _features(style: WritingStyle, rng: random.Random) -> list[Feature]:
    f: set[Feature] = set()
    if style is WritingStyle.texting:
        f |= {Feature.abbreviations} | ({Feature.typos} if rng.random() < 0.7 else set())
    elif style is WritingStyle.rapid_fire:
        f |= {Feature.burst, Feature.abbreviations} | ({Feature.typos} if rng.random() < 0.5 else set())
    elif style is WritingStyle.shouty:
        f |= {Feature.all_caps} | ({Feature.typos} if rng.random() < 0.4 else set())
    elif style is WritingStyle.emoji:
        f |= {Feature.emoji} | ({Feature.abbreviations} if rng.random() < 0.5 else set())
    elif rng.random() < 0.2:
        f.add(Feature.typos)
    return sorted(f)


def _styles(n: int, rng: random.Random) -> list[WritingStyle]:
    """Exact-proportion style pool (largest remainder), shuffled."""
    raw = {s: w * n for s, w in STYLE_WEIGHTS.items()}
    counts = {s: int(v) for s, v in raw.items()}
    for s in sorted(raw, key=lambda s: raw[s] - counts[s], reverse=True)[: n - sum(counts.values())]:
        counts[s] += 1
    pool = [s for s, c in counts.items() for _ in range(c)]
    rng.shuffle(pool)
    return pool


def generate(seed: int = SEED) -> dict[Split, list[ScenarioCard]]:
    menus = load_menus(include_held_out=True)
    out: dict[Split, list[ScenarioCard]] = {Split.dev: [], Split.test: []}
    used: dict[Split, Counter] = {s: Counter() for s in out}  # balance businesses across batches
    variant_used: dict[Split, Counter] = {s: Counter() for s in out}
    # The supplement also spreads each situation over the menus (the first batch only balanced totals;
    # changing that would change its cards).
    batches = (
        (random.Random(seed), {name: sit.counts for name, sit in SITUATIONS.items()}, False),
        (random.Random(SUPPLEMENT_SEED.replace(str(SEED), str(seed))), SUPPLEMENT, True),
    )
    for rng, quotas, spread in batches:
        for k, split in enumerate((Split.dev, Split.test)):
            jobs = [name for name, counts in quotas.items() for _ in range(counts[k])]
            rng.shuffle(jobs)
            out[split] += _cards(
                split, jobs, rng, menus, used[split], variant_used[split], len(out[split]), spread
            )
    return out


def _cards(
    split: Split,
    jobs: list[str],
    rng: random.Random,
    menus: dict,
    used: Counter,
    variant_used: Counter,
    numbered_from: int,
    spread: bool,
) -> list[ScenarioCard]:
    allowed = sorted(b for b, m in menus.items() if split is Split.test or not m.held_out)
    styles = _styles(len(jobs), rng)
    cards: list[ScenarioCard] = []
    for n, (name, style) in enumerate(zip(jobs, styles, strict=True), start=numbered_from + 1):
        sit = SITUATIONS[name]
        options = [b for b in (sit.businesses or allowed) if b in allowed]
        load = {b: ((used[(name, b)],) if spread else ()) + (used[b],) for b in options}
        least = min(load.values())
        business = rng.choice([b for b in options if load[b] == least])
        used[business] += 1
        used[(name, business)] += 1
        variant = None
        if sit.variants:  # rotate variants evenly within a situation
            least_v = min(variant_used[(name, v)] for v in sit.variants)
            variant = rng.choice([v for v in sit.variants if variant_used[(name, v)] == least_v])
            variant_used[(name, variant)] += 1
        labels, scenarios, brief = (
            list(sit.labels),
            list(sit.scenarios),
            sit.brief.format(variant=variant),
        )
        if variant in SECOND_REQUEST:  # two_requests: the question is the message's secondary label
            labels.append(SECOND_REQUEST[variant])
        if sit.order and rng.random() < EXTRA_RATE:
            extra = rng.choice(sorted(EXTRAS))
            x_labels, x_scen, x_brief = EXTRAS[extra]
            labels += [lab for lab in x_labels if lab not in labels]
            scenarios += [s for s in x_scen if s not in scenarios]
            brief += " " + x_brief
        menu = menus[business]
        if not sit.order:
            fulfillment = "not_applicable"
        elif name == "missing_info" and variant == "no pickup/delivery":
            fulfillment = "unstated"
        elif name == "missing_info" and variant == "delivery without an address":
            fulfillment = "delivery" if menu.delivery.available else "pickup"
        elif not menu.delivery.available:
            fulfillment = rng.choice(["pickup", "pickup", "unstated"])
        else:
            fulfillment = rng.choice(["delivery", "delivery", "pickup", "pickup", "unstated"])
        if business == "morning-crumb" and fulfillment == "pickup":
            brief += " (Pickup needs a name here.)"
        lo, hi = sit.messages
        if style is WritingStyle.rapid_fire:
            lo, hi = lo + 1, hi + 2
        cards.append(
            ScenarioCard(
                id=f"a-{split.value}-{n:03d}",
                split=split,
                business_id=business,
                situation=name,
                variant=variant,
                expected_labels=labels,
                scenarios=scenarios,
                style=style,
                features=_features(style, rng),
                fulfillment=fulfillment,
                customer_messages=rng.randint(lo, hi),
                persona=rng.choice(PERSONAS),
                brief=brief,
            )
        )
    return cards


# ---------------------------------------------------------------- storage and summary


def cards_path(split: Split) -> Path:
    return split_dir(split) / CARDS_FILE


def write(cards: dict[Split, list[ScenarioCard]], *, force: bool = False) -> None:
    for split, items in cards.items():
        path = cards_path(split)
        if path.exists() and not force:
            raise FileExistsError(f"{path} exists; pass --force to regenerate")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(c.model_dump_json() + "\n" for c in items))


def load(split: Split) -> list[ScenarioCard]:
    path = cards_path(split)
    if not path.exists():
        return []
    return [ScenarioCard.model_validate_json(line) for line in path.read_text().splitlines() if line.strip()]


def summary(cards: list[ScenarioCard]) -> dict:
    def count(values) -> dict:
        return dict(sorted(Counter(values).items()))

    return {
        "cards": len(cards),
        "labels": count(lab.value for c in cards for lab in c.expected_labels),
        "menus": count(c.business_id for c in cards),
        "styles": count(c.style.value for c in cards),
        "features": count(f.value for c in cards for f in c.features),
        "tricky_cases": count(s.value for c in cards for s in c.scenarios),
        "situations": count(c.situation for c in cards),
        "fulfillment": count(c.fulfillment for c in cards),
        "customer_messages": count(c.customer_messages for c in cards),
    }


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate", help="write dev + test cards (test needs ORDERSLM_UNSEAL_TEST)")
    g.add_argument("--force", action="store_true")
    g.add_argument("--split", choices=["dev", "test"], action="append", help="default: both")
    s = sub.add_parser("summary")
    s.add_argument("--split", choices=["dev", "test"], action="append")
    args = ap.parse_args(argv)
    if args.cmd == "generate":
        chosen = {Split(x) for x in (args.split or ["dev", "test"])}
        write({s: cs for s, cs in generate().items() if s in chosen}, force=args.force)
    for split in (
        [Split(x) for x in (args.split or ["dev", "test"])]
        if args.cmd == "summary" or args.split
        else (Split.dev, Split.test)
    ):
        print(f"== {split.value}")
        print(json.dumps(summary(load(split)), indent=2))


if __name__ == "__main__":
    main()
