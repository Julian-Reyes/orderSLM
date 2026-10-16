"""Scenario cards for synthetic training chats (spec §7, M4).

Code plans each card from (menu × persona × scenario × writing style) with a seeded RNG: the scenario mix comes
from fixed weights (exact proportions), the order a card ends with is picked from the menu, and the generator
model is assigned round-robin within each scenario, so every generator gets the same mix. Nothing here reads
Source A (its cards, chats or persona list): Source A is evaluation data only (CLAUDE.md).

The held-out menu is never used (it is test-only). Mega-menu cards (spec §11e) are not planned yet.
"""

import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from orderslm.menus import load_menu, load_menus
from orderslm.schema.annotation import Scenario, WritingStyle
from orderslm.schema.menu import MenuCatalog, MenuItem
from orderslm.schema.routing import RouterLabel
from orderslm.schema.synthetic import PlannedItem, SynthCard, SynthFeature

CARDS_VERSION = "synth-cards@0.5"  # 0.2: address picked by code, no item twice in one order; 0.3: unstated
# default size said explicitly, a greeting is no longer an expected SMALL_TALK label (often part of the order message);
# 0.4 (p3 review): no "regular one" wording (leaked into chats), address-gap cards no longer also say "never says
# pickup or delivery", a correction never swaps an item for itself, clearer payment-claim and unclear-message briefs;
# 0.5 (Julian, bulk): each non-order scenario weight 2 → 4 (non-order ≈ 35% of chats, was 22%) for the rare intents
L = RouterLabel
S = Scenario
F = SynthFeature


@dataclass(frozen=True)
class Plan:
    weight: int
    labels: tuple[RouterLabel, ...]
    messages: tuple[int, int]  # customer message range
    order: bool = True  # the chat ends with an order
    menus: tuple[str, ...] | None = None  # None = any training menu


PLANS: dict[Scenario, Plan] = {
    S.simple_order: Plan(14, (L.PLACE_ORDER,), (1, 3)),
    S.multi_message_order: Plan(10, (L.PLACE_ORDER,), (3, 6)),
    S.correction: Plan(9, (L.PLACE_ORDER, L.MODIFY_ORDER), (2, 5)),
    S.correction_after_confirmation: Plan(5, (L.PLACE_ORDER, L.CONFIRM_ORDER, L.MODIFY_ORDER), (3, 6)),
    S.cancellation: Plan(4, (L.PLACE_ORDER, L.CANCEL_ORDER), (2, 4)),
    S.missing_info: Plan(6, (L.PLACE_ORDER,), (1, 3)),
    S.contextual_yes: Plan(6, (L.PLACE_ORDER, L.CONFIRM_ORDER), (2, 4)),
    S.off_menu: Plan(4, (L.PLACE_ORDER,), (1, 3)),
    S.ambiguous_reference: Plan(4, (L.PLACE_ORDER,), (2, 4)),
    S.half_and_half: Plan(4, (L.PLACE_ORDER,), (1, 3), menus=("halfmoon-pizza",)),
    S.combo: Plan(5, (L.PLACE_ORDER,), (1, 3), menus=("corner-patty", "morning-crumb")),
    S.implicit_category: Plan(5, (L.PLACE_ORDER,), (1, 3)),
    S.two_requests: Plan(4, (L.PLACE_ORDER, L.MENU_QUESTION), (1, 3)),
    S.menu_question: Plan(4, (L.MENU_QUESTION,), (1, 3), order=False),
    S.delivery_question: Plan(4, (L.DELIVERY_QUESTION,), (1, 3), order=False),
    S.payment_question: Plan(4, (L.PAYMENT_QUESTION,), (1, 2), order=False),
    S.status_question: Plan(4, (L.ORDER_STATUS,), (1, 3), order=False),
    S.order_problem: Plan(4, (L.ORDER_PROBLEM,), (1, 3), order=False),
    S.refund_request: Plan(4, (L.REFUND_REQUEST,), (1, 3), order=False),
    S.payment_claim: Plan(4, (L.PAYMENT_CLAIM,), (1, 3), order=False),
    S.human_request: Plan(4, (L.HUMAN_REQUEST,), (1, 3), order=False),
    S.small_talk: Plan(4, (L.SMALL_TALK,), (1, 2), order=False),
    S.out_of_scope: Plan(4, (L.OUT_OF_SCOPE,), (1, 2), order=False),
    S.unclear_message: Plan(4, (L.UNKNOWN,), (1, 2), order=False),
}

NON_ORDER_BRIEFS: dict[Scenario, str] = {
    S.menu_question: "Only asks one or two questions about the menu (what comes on something, sizes, what's good, "
    "whether they have something). Does not order.",
    S.delivery_question: "Only asks about delivery or pickup (delivery area, fee, how long it takes, opening "
    "hours). Does not order.",
    S.payment_question: "Only asks how they can pay (cash, card, an app). Does not order.",
    S.status_question: "Placed an order earlier (not in this chat) and asks where it is or when it will arrive.",
    S.order_problem: "Got an earlier order (not in this chat) with a problem: the {item} was {problem}. "
    "Complains. Does not order anything new.",
    S.refund_request: "Got an earlier order (not in this chat) where the {item} was {problem}, and asks for "
    "their money back.",
    S.payment_claim: "Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent "
    "the money on the app') and asks whether the payment went through. Does not order anything new.",
    S.human_request: "Asks to talk to a person or the manager, with a short reason. Does not order.",
    S.small_talk: "Only greets, thanks the business or chats briefly. No request.",
    S.out_of_scope: "Asks something unrelated to ordering food (a job, parking, a lost item, the wifi, a "
    "donation). Does not order.",
    S.unclear_message: "Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a "
    "pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.",
}

STYLE_WEIGHTS = {
    WritingStyle.clean: 20,
    WritingStyle.texting: 30,
    WritingStyle.rapid_fire: 20,
    WritingStyle.shouty: 10,
    WritingStyle.emoji: 20,
}
STYLE_TEXT = {
    WritingStyle.clean: "clean, complete sentences",
    WritingStyle.texting: "casual texting: lowercase, few or no punctuation marks",
    WritingStyle.rapid_fire: "rapid-fire: several very short messages in a row",
    WritingStyle.shouty: "shouty: mostly ALL CAPS, exclamation marks",
    WritingStyle.emoji: "friendly, with emoji",
}
FEATURE_TEXT = {
    F.typos: "a few realistic typos",
    F.abbreviations: "texting abbreviations (u, pls, thx, rn, gonna, lemme)",
    F.emoji: "emoji",
    F.burst: "splits thoughts across several short messages",
    F.all_caps: "ALL CAPS",
    F.number_words: "numbers as words ('two', 'a couple of')",
    F.no_punctuation: "almost no punctuation",
}

# Written for synthetic data only (not Source A's persona list).
PERSONAS = [
    "nurse grabbing food between shifts",
    "dad ordering for two hungry kids",
    "grad student who forgot to eat",
    "construction worker on lunch break",
    "roommates splitting an order",
    "retired teacher, very polite",
    "gamer who doesn't want to leave the screen",
    "new parent ordering one-handed",
    "coach feeding a few players after practice",
    "someone hosting a last-minute movie night",
    "delivery driver ordering for themselves",
    "small-business owner ordering for the shop",
    "student who just finished an exam",
    "person working from home, in a hurry",
    "hungover customer on a Sunday",
    "picky eater who customizes everything",
    "customer trying the place for the first time",
    "regular who orders the same thing often",
    "couple deciding together over chat",
    "teen ordering with a parent's okay",
    "night owl ordering late",
    "office assistant ordering for a meeting",
    "fitness fan watching what they eat",
    "someone ordering for a sick friend",
]
NAMES = ["Maya", "Jordan", "Luis", "Priya", "Sam", "Keisha", "Tom", "Ana", "Dev", "Rosa", "Ben", "Leah", "Omar",
         "Grace", "Nico", "Tara", "Eli", "June", "Marcus", "Ivy"]  # fmt: skip
OFF_MENU = {
    "corner-patty": ["chicken nuggets", "a fish sandwich", "a hot dog", "a side salad", "mozzarella sticks"],
    "halfmoon-pizza": ["a calzone", "buffalo wings", "a caesar salad", "cannoli", "a meatball sub"],
    "morning-crumb": ["a smoothie", "a chai latte", "a breakfast burrito", "a scone", "a fruit cup"],
}
NOT_REMOVABLE_GROUPS = {"extra"}  # espresso shot
TIMES = ["asap", "a clock time (like 'at 6:30')", "a relative time (like 'in 20 min')"]
# Code picks the address: left to the generators, every pilot chat lived on "Maple" (p1 mini-pilot, 2026-10-16).
STREETS = ["Oak", "Birch", "Hawthorne", "Juniper", "Mission", "Lakeview", "Kensington", "Delancey", "Fulton", "Grant",
           "Harbor", "Ridgecrest", "Willow Creek", "Sycamore", "Orchard", "Prospect", "Union", "Cedar Hill", "Elm",
           "Franklin", "Magnolia", "Sunset", "Bayview", "Chestnut", "Larkin", "Quincy", "Riverside", "Spruce",
           "Thornton", "Vine", "Wexford", "Alder", "Brookside", "Clement", "Dover", "Easton", "Fairmont", "Glenwood",
           "Hollis", "Ivanhoe"]  # fmt: skip
SUFFIXES = ["St", "Ave", "Rd", "Blvd", "Dr", "Ln", "Ct", "Pl", "Way", "Terrace"]
LANDMARKS = [
    "blue door",
    "next to the laundromat",
    "side entrance",
    "across from the park",
    "above the bakery",
]
VAGUE = ["the usual", "one of those", "same as last time", "the one I always get", "that thing from before"]
PROBLEMS = ["missing", "cold", "the wrong one", "squashed", "undercooked"]
GENERATORS = (  # Julian, 2026-10-16: pilot 200 / 200 / 100
    ("deepseek/deepseek-flash@none", 2),
    ("google/gemini-3.1-flash-lite@minimal", 2),
    ("anthropic/claude-haiku-5-5@off-low", 1),
)


def _exact(weights: dict, n: int, rng: random.Random) -> list:
    """Exact-proportion pool (largest remainder), shuffled."""
    total = sum(weights.values())
    raw = {k: w * n / total for k, w in weights.items()}
    counts = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - counts[k], reverse=True)[: n - sum(counts.values())]:
        counts[k] += 1
    pool = [k for k, c in counts.items() for _ in range(c)]
    rng.shuffle(pool)
    return pool


def _pick_variant(item: MenuItem, rng: random.Random, state: bool) -> str | None:
    if not item.variants:
        return None
    if item.default_variant_id is None:
        return rng.choice(item.variants).id if state else None
    return rng.choice(item.variants).id if state and rng.random() < 0.5 else None


def _mods(menu: MenuCatalog, item: MenuItem, rng: random.Random, p: PlannedItem) -> None:
    exclusive = set(menu.exclusive_groups)

    def group(mid: str) -> str:
        m = menu.modifier(mid)
        return m.group if m else ""

    # Removable: not the core of the item (an espresso shot) and not a choice group (milk, crust).
    removable = [i for i in item.ingredient_ids if group(i) not in exclusive | NOT_REMOVABLE_GROUPS]
    if removable and rng.random() < 0.3:
        p.remove.append(rng.choice(removable))
    addons = [a for a in item.addon_ids if group(a) not in exclusive]
    if addons and rng.random() < 0.3:
        p.add.append(rng.choice([a for a in addons if a not in p.remove] or addons))
    swaps = [
        (ing, a)
        for a in item.addon_ids
        if group(a) in exclusive
        for ing in item.ingredient_ids
        if group(ing) == group(a) and ing not in p.remove
    ]
    if swaps and rng.random() < 0.25:
        old, new = rng.choice(swaps)
        p.substitute[old] = new
    elif not swaps:
        picks = [a for a in item.addon_ids if group(a) in exclusive]
        if picks and rng.random() < 0.2:  # e.g. a crust choice on a pizza
            p.add.append(rng.choice(picks))


def plan_item(
    menu: MenuCatalog,
    rng: random.Random,
    *,
    pool: list[MenuItem] | None = None,
    state_variant: bool = True,
    exclude: set[str] = frozenset(),  # type: ignore[assignment]
) -> PlannedItem:
    items = pool or [i for i in menu.items if i.available and not i.combo_slots]
    items = [i for i in items if i.id not in exclude] or items
    item = rng.choice(items)
    quantity = rng.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
    p = PlannedItem(
        menu_item_id=item.id, quantity=quantity, variant_id=_pick_variant(item, rng, state_variant)
    )
    for slot in item.combo_slots:
        p.combo[slot.id] = rng.choice(slot.choices)
    _mods(menu, item, rng, p)
    return p


def _half_and_half(menu: MenuCatalog, rng: random.Random) -> PlannedItem:
    pizzas = [i for i in menu.items if i.splittable]
    a, b = rng.sample(pizzas, 2)
    return PlannedItem(halves=[a.id, b.id], quantity=1, variant_id=rng.choice(a.variants).id)


def item_text(p: PlannedItem, menu: MenuCatalog) -> str:
    """How the card shows an item to the generator: names, never ids or prices."""

    def mname(mid: str) -> str:
        m = menu.modifier(mid)
        return m.name if m else mid

    if p.off_menu_text:
        return f"{p.quantity} × {p.off_menu_text} (not on the menu)"
    if p.halves:
        names = [menu.item(h).name for h in p.halves]  # type: ignore[union-attr]
        size = menu.item(p.halves[0]).variant(p.variant_id).name if p.variant_id else "no size stated"  # type: ignore[union-attr]
        return f"{p.quantity} × half-and-half pizza ({size}): half {names[0]}, half {names[1]}"
    item = menu.item(p.menu_item_id or "")
    assert item is not None
    text = f"{p.quantity} × {item.name}"
    if item.sold_as.value == "order":
        text = f"{p.quantity} order{'s' if p.quantity > 1 else ''} of {item.name}"
        text += f" ({item.pieces_per_order} pieces each)" if item.pieces_per_order else ""
    if p.variant_id:
        text += f" ({item.variant(p.variant_id).name})"  # type: ignore[union-attr]
    elif item.variants and item.default_variant_id is None:
        text += " (size/flavor not stated)"
    elif item.variants:
        text += " (the customer doesn't mention a size)"
    extras = [f"no {mname(m)}" for m in p.remove] + [f"add {mname(m)}" for m in p.add]
    extras += [f"{mname(new)} instead of {mname(old)}" for old, new in p.substitute.items()]
    for slot_id, choice in p.combo.items():
        extras.append(f"{slot_id}: {menu.item(choice).name}")  # type: ignore[union-attr]
    return text + (", " + ", ".join(extras) if extras else "")


def _items_text(items: list[PlannedItem], menu: MenuCatalog) -> str:
    return "; ".join(item_text(p, menu) for p in items)


def _address(rng: random.Random) -> str:
    number = rng.choice([rng.randint(1, 99), rng.randint(100, 999), rng.randint(1000, 9999)])
    text = f"{number} {rng.choice(STREETS)} {rng.choice(SUFFIXES)}"
    r = rng.random()
    if r < 0.3:
        text += f", {rng.choice(['apt', 'unit', '#'])} {rng.randint(1, 30)}{rng.choice(['', 'A', 'B', 'C'])}"
    elif r < 0.4:
        text += f" ({rng.choice(LANDMARKS)})"
    return text


def _start(menu: MenuCatalog, rng: random.Random) -> datetime:
    tz = ZoneInfo(menu.timezone)
    day = datetime(2026, 10, 1, tzinfo=tz) + timedelta(days=rng.randrange(28))
    opens = menu.opens_at.hour * 60 + menu.opens_at.minute + 20
    closes = menu.closes_at.hour * 60 + menu.closes_at.minute - 40
    if closes <= opens:
        closes += 24 * 60
    minute = rng.randrange(opens, closes)
    return (day + timedelta(minutes=minute)).astimezone(UTC)


def _features(style: WritingStyle, rng: random.Random) -> list[SynthFeature]:
    f: set[SynthFeature] = set()
    if style is WritingStyle.texting:
        f |= {F.abbreviations, F.no_punctuation} | ({F.typos} if rng.random() < 0.6 else set())
    elif style is WritingStyle.rapid_fire:
        f |= {F.burst} | ({F.abbreviations} if rng.random() < 0.6 else set())
    elif style is WritingStyle.shouty:
        f |= {F.all_caps} | ({F.typos} if rng.random() < 0.4 else set())
    elif style is WritingStyle.emoji:
        f |= {F.emoji} | ({F.abbreviations} if rng.random() < 0.4 else set())
    elif rng.random() < 0.2:
        f.add(F.typos)
    if rng.random() < 0.3:
        f.add(F.number_words)
    return sorted(f)


def _card(
    n: int, scenario: Scenario, style: WritingStyle, menu: MenuCatalog, rng: random.Random, batch: str
) -> SynthCard:
    plan = PLANS[scenario]
    labels = list(plan.labels)
    lo, hi = plan.messages
    msgs = rng.randint(lo, hi) + (2 if style is WritingStyle.rapid_fire else 0)
    brief: list[str] = []
    extras: list[str] = []
    items: list[PlannedItem] = []
    first_ask: PlannedItem | None = None
    fulfillment, payment, name, address = "not_applicable", "not_applicable", None, None

    if plan.order:
        if rng.random() < 0.25:
            extras.append("greets_first")
            msgs += 1
        if scenario not in (S.two_requests,) and rng.random() < 0.15:
            extras.append("asks_menu_mid_order")
            labels.append(L.MENU_QUESTION)
            msgs += 1
        gap = None
        if scenario is S.missing_info:
            gaps = ["payment", "fulfillment"] + (["address"] if menu.delivery.available else [])
            sizeable = [
                i for i in menu.items if i.variants and i.default_variant_id is None and not i.combo_slots
            ]
            gaps += ["size"] if sizeable else []
            gap = rng.choice(gaps)
        n_items = rng.choices([1, 2, 3], weights=[45, 35, 20])[0]
        if scenario is S.half_and_half:
            items.append(_half_and_half(menu, rng))
            n_items -= 1
        if scenario is S.combo:
            combos = [i for i in menu.items if i.combo_slots]
            items.append(plan_item(menu, rng, pool=combos))
            n_items -= 1
        if gap == "size":
            sizeable = [
                i for i in menu.items if i.variants and i.default_variant_id is None and not i.combo_slots
            ]
            items.append(plan_item(menu, rng, pool=sizeable, state_variant=False))
            n_items -= 1
        for _ in range(max(n_items, 0)):
            items.append(plan_item(menu, rng, exclude={p.menu_item_id for p in items if p.menu_item_id}))
        if scenario is S.off_menu:
            choices = OFF_MENU.get(menu.business_id) or sorted({x for v in OFF_MENU.values() for x in v})
            items.append(PlannedItem(off_menu_text=rng.choice(choices), quantity=1))

        # fulfillment, payment, name
        if menu.delivery.available:
            fulfillment = rng.choices(["delivery", "pickup", "unstated"], weights=[40, 40, 20])[0]
        else:
            fulfillment = rng.choices(["pickup", "unstated"], weights=[75, 25])[0]
        payment = rng.choices(["card", "cash", "unstated"], weights=[45, 30, 25])[0]
        if gap == "fulfillment":
            fulfillment = "unstated"
        if gap == "payment":
            payment = "unstated"
        if gap == "address":
            fulfillment = "delivery"
        if fulfillment == "pickup" and (menu.name_required_for_pickup or rng.random() < 0.5):
            name = rng.choice(NAMES)

        core = {
            S.simple_order: "Orders: {items}.",
            S.multi_message_order: "Builds the order over several messages, a thing or two at a time: {items}.",
            S.cancellation: "Orders: {items}. Then cancels the whole order before it is placed (the last "
            "customer message is the cancellation).",
            S.missing_info: "Orders: {items}.",
            S.contextual_yes: "Orders: {items}. The business reads the order back (no prices) and asks if it's "
            "right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up).",
            S.off_menu: "Orders: {items}. The item marked 'not on the menu' is asked for as if the customer "
            "thinks they have it; the chat ends before the business answers about it.",
            S.half_and_half: "Orders: {items}.",
            S.combo: "Orders: {items}. Picks every combo choice.",
            S.implicit_category: "Orders: {items}. Never uses category words: names items casually ('a coke', "
            "'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone.",
            S.two_requests: "Orders: {items}. In the same message as the first item, also asks a question about "
            "the menu.",
        }
        if scenario in (S.correction, S.correction_after_confirmation):
            target = items[0]
            if rng.random() < 0.5 and target.menu_item_id:
                first_ask = target.model_copy(update={"quantity": target.quantity % 4 + 1})
                change = f"changes the quantity to {target.quantity}"
            else:
                first_ask = plan_item(menu, rng, exclude={p.menu_item_id for p in items if p.menu_item_id})
                change = f"swaps it for {item_text(target, menu)}"
            if scenario is S.correction:
                brief.append(
                    f"First asks for {item_text(first_ask, menu)} (plus anything else below), then {change}. "
                    "Final order: {items}."
                )
            else:
                brief.append(
                    f"First orders {item_text(first_ask, menu)} (plus anything else below). The business reads "
                    f"the order back (no prices); the customer confirms, then {change}. Final order: {{items}}."
                )
        elif scenario is S.ambiguous_reference:
            brief.append(
                f"Refers to the first item vaguely at first ('{rng.choice(VAGUE)}'); the business asks which one, "
                "and the customer names it. Final order: {items}."
            )
        else:
            brief.append(core[scenario])
        if gap == "size":
            brief.append("Never says the size or flavor of the item marked 'not stated'.")
        if gap == "address":
            brief.append("Chooses delivery but never gives an address.")
        if fulfillment == "delivery" and gap != "address":
            address = _address(rng)
            brief.append(f"Wants delivery to {address} (written the way the customer would type it).")
        elif fulfillment == "delivery":
            pass  # the address gap sentence above already says delivery
        elif fulfillment == "pickup":
            brief.append("Will pick it up.")
        else:
            brief.append("Never says whether it's pickup or delivery.")
        if payment == "cash":
            brief.append(
                "Pays cash"
                + (", and asks for change for a bill (a 20 or a 50)." if rng.random() < 0.3 else ".")
            )
        elif payment == "card":
            brief.append("Pays by card.")
        else:
            brief.append("Never says how they'll pay.")
        if name:
            brief.append(f"Gives their name: {name}.")
        if rng.random() < 0.3:
            brief.append(f"Says when they want it: {rng.choice(TIMES)}.")
        if "greets_first" in extras:
            brief.insert(0, "Opens with a greeting before ordering.")
        if "asks_menu_mid_order" in extras:
            brief.append("Asks a menu question partway through.")
    else:
        sample = rng.choice([i for i in menu.items if not i.combo_slots])
        brief.append(
            NON_ORDER_BRIEFS[scenario].format(item=sample.name.lower(), problem=rng.choice(PROBLEMS))
        )

    text = " ".join(brief).replace("{items}", _items_text(items, menu))
    return SynthCard(
        id=f"syn-{batch}-{n:04d}",
        generator="unassigned",
        business_id=menu.business_id,
        scenario=scenario,
        extras=extras,
        expected_labels=list(dict.fromkeys(labels)),
        style=style,
        features=_features(style, rng),
        persona=rng.choice(PERSONAS),
        customer_messages=min(msgs, 12),
        fulfillment=fulfillment,  # type: ignore[arg-type]
        payment=payment,  # type: ignore[arg-type]
        customer_name=name,
        address=address,
        items=items,
        first_ask=first_ask,
        brief=text,
        start_at=_start(menu, rng),
    )


def _pattern(generators: tuple[tuple[str, int], ...]) -> list[str]:
    """(D, 2), (G, 2), (H, 1) → D, G, H, D, G: round-robin over the remaining weight."""
    left = dict(generators)
    out: list[str] = []
    while any(left.values()):
        for g, _ in generators:
            if left[g]:
                out.append(g)
                left[g] -= 1
    return out


def _supports(menu: MenuCatalog, scenario: Scenario) -> bool:
    """A scenario restricted to some menus also fits a menu (the mega-menu) that has what it needs."""
    if scenario is S.half_and_half:
        return sum(i.splittable for i in menu.items) >= 2
    if scenario is S.combo:
        return any(i.combo_slots for i in menu.items)
    return False


def plan_cards(
    n: int,
    *,
    seed: int,
    batch: str,
    generators: tuple[tuple[str, int], ...] = GENERATORS,
    business_ids: tuple[str, ...] | None = None,
) -> list[SynthCard]:
    """n cards. Generators are assigned in scenario order, so each scenario is split across them in the given
    ratio and the totals are exact when n is a multiple of the summed weights."""
    rng = random.Random(f"{CARDS_VERSION}-{seed}-{batch}")
    if business_ids is None:
        menus = {b: m for b, m in load_menus().items() if not m.held_out}
    else:
        menus = {b: load_menu(b) for b in business_ids}  # a held-out id is unknown here (KeyError): test-only
    scenarios = _exact({s: p.weight for s, p in PLANS.items()}, n, rng)
    styles = _exact(STYLE_WEIGHTS, n, rng)
    cards = []
    for i, (scenario, style) in enumerate(zip(scenarios, styles, strict=True), start=1):
        only = PLANS[scenario].menus
        allowed = tuple(
            b for b in sorted(menus) if only is None or b in only or _supports(menus[b], scenario)
        )
        cards.append(_card(i, scenario, style, menus[rng.choice(allowed)], rng, batch))
    order = list(PLANS)
    pattern = _pattern(generators)
    ranked = sorted(range(n), key=lambda i: (order.index(cards[i].scenario), i))
    for j, i in enumerate(ranked):
        cards[i] = cards[i].model_copy(update={"generator": pattern[j % len(pattern)]})
    return cards
