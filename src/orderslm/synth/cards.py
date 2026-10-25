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
# Targeted batch (M6 error review, docs/STUDENT_ERRORS.md): patterns the students miss and the training data barely
# has. Written from those pattern descriptions, never from dev chats (Source A is evaluation only).
TARGETS_VERSION = "synth-targets@0.1"
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
# Toppings / add-ins none of the training menus has (checked against modifier names and aliases in tests).
OFF_MENU_ADDONS = {
    "corner-patty": ["a fried egg", "grilled mushrooms", "sriracha", "coleslaw", "chili"],
    "halfmoon-pizza": ["capers", "arugula", "eggplant", "truffle oil", "shrimp"],
    "morning-crumb": ["coconut milk", "matcha powder", "honey", "cinnamon", "lavender syrup"],
}
TARGET_WEIGHTS = {  # Julian, 2026-10-25: 600 chats, same writers and teacher as M4
    "split_lines": 10,  # the same dish on two lines ("4 cheeseburgers, 2 no onion"): 1 of 1,865 training answers
    "big_order": 10,  # 4–6 lines, half with a clarifying question midway: 10 of 1,865
    "modify_last": 16,  # a change in the last customer message (MODIFY_ORDER): 2.9% of training rows
    "size_unstated": 6,  # an item whose size is never said
    "unclear": 6,  # UNKNOWN: 14 training rows
    "trivia": 4,  # general-knowledge questions (OUT_OF_SCOPE, read as MENU_QUESTION)
    "bare_time": 4,  # "at 8:30" with no am/pm, meaning the later one
    "offmenu_addon": 4,  # a topping the menu doesn't have, on a menu item
}
# Kinds of change in the 160 modify_last chats, weighted toward what all three students got wrong on dev (Julian,
# 2026-10-25: "the whole point is to help the students on what they got wrong"): size changes ("make the fries
# large"), option swaps ("make the latte oat milk"), time/payment changes, removals, additions after confirming.
MODIFY_KIND_WEIGHTS = {
    "size": 30,
    "option_swap": 25,
    "time": 10,
    "payment": 10,
    "remove_item": 18,
    "add_mod": 15,
    "add_item": 15,  # only after a confirmation (before one, a new item is more ordering, not a change)
    "swap_item": 13,
    "remove_mod": 12,
    "quantity": 12,
}
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


def _split(menu: MenuCatalog, rng: random.Random, items: list[PlannedItem]) -> None:
    """Make one dish two lines: N of it, K of them with one change (a removal or an add-on)."""

    def changeable(i: MenuItem) -> bool:
        return bool(i.ingredient_ids or i.addon_ids) and not i.combo_slots

    pool = [i for i in menu.items if i.available and changeable(i)]
    base = plan_item(menu, rng, pool=pool, exclude={p.menu_item_id for p in items if p.menu_item_id})
    item = menu.item(base.menu_item_id or "")
    assert item is not None
    total = rng.choice([2, 3, 4, 4, 5, 6])
    k = rng.randint(1, total - 1)
    plain = base.model_copy(update={"quantity": total - k, "remove": [], "add": [], "substitute": {}})
    changed = plain.model_copy(update={"quantity": k, "remove": [], "add": []})
    probe = PlannedItem(menu_item_id=item.id, quantity=1)
    for _ in range(20):  # _mods draws at random; keep the first draw with one removal or one add-on
        probe = PlannedItem(menu_item_id=item.id, quantity=1)
        _mods(menu, item, rng, probe)
        if probe.remove or probe.add:
            break
    if probe.remove:
        changed.remove.append(probe.remove[0])
    elif probe.add:
        changed.add.append(probe.add[0])
    else:
        changed.add.append(rng.choice(item.addon_ids or item.ingredient_ids))
    items.insert(0, changed)
    items.insert(0, plain)


def _modify_last(
    menu: MenuCatalog, rng: random.Random, items: list[PlannedItem], kind: str, payment: str
) -> tuple[str, str]:
    """The change in the last customer message, of an assigned kind (MODIFY_KIND_WEIGHTS); `items` becomes the final
    order, and gets an item the change can apply to when it has none. Returns (what the customer says first, the
    change). "time" and "payment" kinds change a detail instead of an item."""
    exclusive = set(menu.exclusive_groups)
    taken = {p.menu_item_id for p in items if p.menu_item_id}

    def group(mid: str) -> str:
        m = menu.modifier(mid)
        return m.group if m else ""

    def mname(mid: str) -> str:
        m = menu.modifier(mid)
        return m.name if m else mid

    def holder(fits) -> tuple[PlannedItem, MenuItem]:
        """An order line whose item fits, else a new one added to the order."""
        for p in items:
            item = menu.item(p.menu_item_id) if p.menu_item_id and not p.combo else None
            if item and fits(item, p):
                return p, item
        pool = [i for i in menu.items if i.available and not i.combo_slots and fits(i, None)]
        p = plan_item(menu, rng, pool=pool, exclude=taken)
        p.remove, p.add, p.substitute = [], [], {}
        items.append(p)
        return p, menu.item(p.menu_item_id)  # type: ignore[return-value]

    changed = "First orders the items below, but with the earlier version of the changed one."
    if kind == "size":
        p, item = holder(lambda i, p: len(i.variants) >= 2)
        if p.variant_id is None:
            p.variant_id = rng.choice(item.variants).id
        old = rng.choice([v for v in item.variants if v.id != p.variant_id])
        new = item.variant(p.variant_id)
        return (
            changed,
            f"changes the size of the {item.name} from {old.name} to {new.name} (like 'make it a {new.name.split()[0].lower()}').",
        )  # type: ignore[union-attr]
    if kind == "option_swap":

        def swaps(i: MenuItem) -> list[tuple[str | None, str]]:
            """(the ingredient it replaces, the option): milk swaps out whole milk; a crust (no crust ingredient on
            the pizza menu) is a pick, so it replaces nothing."""
            out: list[tuple[str | None, str]] = []
            for a in i.addon_ids:
                if group(a) in exclusive:
                    same = [ing for ing in i.ingredient_ids if group(ing) == group(a)]
                    out += [(ing, a) for ing in same if ing != a] if same else [(None, a)]
            return out

        p, item = holder(lambda i, p: bool(swaps(i)))
        old, new = rng.choice(swaps(item))
        if old is None:
            p.add = [x for x in p.add if group(x) != group(new)] + [new]
            return (
                changed,
                f"asks for the {item.name} with {mname(new)} (like 'make it {mname(new).lower()}').",
            )
        p.remove = [r for r in p.remove if r != old]
        p.substitute = {old: new}
        return changed, f"asks for the {item.name} with {mname(new)} instead of {mname(old)}."
    if kind == "add_mod":
        p, item = holder(lambda i, p: any(group(a) not in exclusive for a in i.addon_ids))
        a = rng.choice([a for a in item.addon_ids if group(a) not in exclusive])
        if a not in p.add:
            p.add.append(a)
        return changed, f"adds {mname(a)} to the {item.name}."
    if kind == "remove_mod":

        def removable(i: MenuItem) -> list[str]:
            return [r for r in i.ingredient_ids if group(r) not in exclusive | NOT_REMOVABLE_GROUPS]

        p, item = holder(lambda i, p: bool(removable(i)))
        r = rng.choice(removable(item))
        if r not in p.remove:
            p.remove.append(r)
        p.substitute.pop(r, None)
        return changed, f"asks for the {item.name} without {mname(r)}."
    if kind == "remove_item":
        dropped = plan_item(menu, rng, exclude=taken)
        return (
            f"First orders the items below plus {item_text(dropped, menu)}.",
            f"removes the {item_text(dropped, menu)} from the order.",
        )
    if kind == "add_item":
        added = plan_item(menu, rng, exclude=taken)
        items.append(added)
        return (
            "First orders the items below except the one added at the end.",
            f"adds {item_text(added, menu)} (not asked for before).",
        )
    if kind == "quantity":
        p, item = holder(lambda i, p: True)
        before = p.quantity % 4 + 1
        return changed, f"changes the {item.name} from {before} to {p.quantity}."
    if kind == "swap_item":
        p, item = holder(lambda i, p: True)
        old = plan_item(menu, rng, exclude=taken | {p.menu_item_id})
        return (
            f"First orders the items below, but {item_text(old, menu)} instead of {item_text(p, menu)}.",
            f"swaps the {item_text(old, menu)} for {item_text(p, menu)}.",
        )
    if kind == "payment" and payment in ("card", "cash"):
        before = "cash" if payment == "card" else "card"
        return (
            f"First orders the items below and says they'll pay by {before}.",
            f"switches the payment to {payment} instead of {before}.",
        )
    # "time" (and "payment" when the card has no payment to change)
    h, m = rng.choice([(12, 0), (12, 30), (13, 15), (18, 0), (18, 30), (19, 0), (19, 45)])
    later = (h * 60 + m + rng.choice([30, 45, 60])) % (24 * 60)
    return (
        f"First orders the items below for a clock time ({h:02d}:{m:02d}, said the way a customer would).",
        f"moves the time to {later // 60:02d}:{later % 60:02d} (like 'can you make it X instead').",
    )


def _bare_time(menu: MenuCatalog, rng: random.Random) -> tuple[datetime, str]:
    """A start late in the opening hours and a time 30–90 min later, said on a 12-hour clock without am/pm."""
    tz = ZoneInfo(menu.timezone)
    day = datetime(2026, 10, 1, tzinfo=tz) + timedelta(days=rng.randrange(28))
    closes = menu.closes_at.hour * 60 + menu.closes_at.minute
    start = rng.randrange(max(closes - 240, menu.opens_at.hour * 60 + 60), closes - 100)
    at = start + rng.choice([30, 45, 60, 75, 90])
    at -= at % 15
    h, m = divmod(at, 60)
    said = f"{(h - 1) % 12 + 1}:{m:02d}" if m else f"{(h - 1) % 12 + 1}"
    sentence = f"Says when they want it as a bare clock time with no am/pm: 'at {said}' (meaning {h:02d}:{m:02d} today)."
    return (day + timedelta(minutes=start)).astimezone(UTC), sentence


def _card(
    n: int,
    scenario: Scenario,
    style: WritingStyle,
    menu: MenuCatalog,
    rng: random.Random,
    batch: str,
    target: str | None = None,
    modify_kind: str | None = None,
) -> SynthCard:
    """target (a TARGET_WEIGHTS key) adds a targeted pattern, modify_kind (MODIFY_KIND_WEIGHTS) the change for
    "modify_last"; without a target, the random draws are as before."""
    plan = PLANS[scenario]
    labels = list(plan.labels)
    lo, hi = plan.messages
    msgs = rng.randint(lo, hi) + (2 if style is WritingStyle.rapid_fire else 0)
    brief: list[str] = []
    extras: list[str] = []
    items: list[PlannedItem] = []
    first_ask: PlannedItem | None = None
    fulfillment, payment, name, address = "not_applicable", "not_applicable", None, None
    start_at: datetime | None = None  # set early only for target "bare_time"

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
            if target == "size_unstated" and sizeable:
                gap = "size"
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
        if target == "split_lines":
            _split(menu, rng, items)
        if target == "big_order":
            while len(items) < rng.randint(4, 6):
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
        if modify_kind == "payment" and payment == "unstated":  # a payment change needs a payment to change
            payment = rng.choice(["card", "cash"])
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
        if target == "modify_last":
            confirmed = scenario is S.correction_after_confirmation
            first, change = _modify_last(menu, rng, items, modify_kind or "quantity", payment)
            first += " "
            if confirmed:
                first += "The business reads the order back (no prices) and the customer confirms. "
            brief.append(
                first
                + f"Then, in the very last customer message, {change} Their other details come before that change; "
                "nothing comes after it. Final order: {items}."
            )
        elif scenario in (S.correction, S.correction_after_confirmation):
            target_item = items[0]
            if rng.random() < 0.5 and target_item.menu_item_id:
                first_ask = target_item.model_copy(update={"quantity": target_item.quantity % 4 + 1})
                change = f"changes the quantity to {target_item.quantity}"
            else:
                first_ask = plan_item(menu, rng, exclude={p.menu_item_id for p in items if p.menu_item_id})
                change = f"swaps it for {item_text(target_item, menu)}"
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
        if modify_kind == "payment" and payment in ("card", "cash"):
            pass  # the change sentence says both payments
        elif payment == "cash":
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
        if target == "split_lines":
            brief.append(
                "The first two lines are the same item: says them as one request with a count and how many get "
                "the change (like '4 burgers, 2 of them no onions')."
            )
        if target == "bare_time":
            start_at, time_sentence = _bare_time(menu, rng)
            brief.append(time_sentence)
        elif modify_kind not in ("time", "payment") and rng.random() < 0.3:
            brief.append(f"Says when they want it: {rng.choice(TIMES)}.")
        if target == "offmenu_addon":
            host = next(
                (p for p in items if p.menu_item_id and menu.item(p.menu_item_id).addon_ids),  # type: ignore[union-attr]
                None,
            )
            if host is None:  # only drinks so far: add a dish that takes add-ons
                takes = [i for i in menu.items if i.available and i.addon_ids and not i.combo_slots]
                host = plan_item(
                    menu, rng, pool=takes, exclude={p.menu_item_id for p in items if p.menu_item_id}
                )
                items.append(host)
            addon = rng.choice(OFF_MENU_ADDONS[menu.business_id])
            host_name = menu.item(host.menu_item_id or "").name  # type: ignore[union-attr]
            brief.append(
                f"Asks for {addon} on the {host_name}, as if the place has it (it isn't on the menu)."
            )
        if "greets_first" in extras:
            brief.insert(0, "Opens with a greeting before ordering.")
        if "asks_menu_mid_order" in extras:
            brief.append("Asks a menu question partway through.")
    else:
        sample = rng.choice([i for i in menu.items if not i.combo_slots])
        if target == "trivia":
            brief.append(
                "Asks one or two general-knowledge or trivia questions that have nothing to do with the restaurant "
                "(history, geography, sports, a fun fact, settling a bet). Does not order."
            )
        else:
            brief.append(
                NON_ORDER_BRIEFS[scenario].format(item=sample.name.lower(), problem=rng.choice(PROBLEMS))
            )

    text = " ".join(brief).replace("{items}", _items_text(items, menu))
    if target == "modify_last":
        labels.append(L.MODIFY_ORDER)
    if target:
        extras.append(f"target:{target}")
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
        start_at=start_at if target == "bare_time" else _start(menu, rng),  # drawn last, as before targets
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


TARGET_SCENARIOS: dict[str, tuple[Scenario, ...]] = {
    "split_lines": (S.simple_order, S.multi_message_order),
    "big_order": (S.multi_message_order, S.ambiguous_reference),
    "modify_last": (S.correction, S.correction_after_confirmation),
    "size_unstated": (S.missing_info,),
    "unclear": (S.unclear_message,),
    "trivia": (S.out_of_scope,),
    "bare_time": (S.simple_order, S.multi_message_order),
    "offmenu_addon": (S.simple_order, S.multi_message_order),
}


def plan_targeted_cards(
    n: int,
    *,
    seed: int,
    batch: str,
    generators: tuple[tuple[str, int], ...] = GENERATORS,
) -> list[SynthCard]:
    """n cards for the targeted batch (TARGET_WEIGHTS over the three training menus), generators assigned in target
    order as in plan_cards."""
    rng = random.Random(f"{TARGETS_VERSION}-{seed}-{batch}")
    menus = {b: m for b, m in load_menus().items() if not m.held_out}
    targets = _exact(TARGET_WEIGHTS, n, rng)
    styles = _exact(STYLE_WEIGHTS, n, rng)
    kinds = iter(_exact(MODIFY_KIND_WEIGHTS, targets.count("modify_last"), rng))
    cards = []
    for i, (target, style) in enumerate(zip(targets, styles, strict=True), start=1):
        kind = next(kinds) if target == "modify_last" else None
        scenario = rng.choice(TARGET_SCENARIOS[target])
        if kind == "add_item":  # a new item is a change only once the order was confirmed
            scenario = S.correction_after_confirmation
        allowed = sorted(menus)
        if kind == "option_swap":  # milk (bakery) or crust (pizza): the burger place has no such choice
            allowed = [b for b in allowed if menus[b].exclusive_groups]
        menu = menus[rng.choice(allowed)]
        cards.append(_card(i, scenario, style, menu, rng, batch, target=target, modify_kind=kind))
    order = list(TARGET_WEIGHTS)
    pattern = _pattern(generators)
    ranked = sorted(range(n), key=lambda i: (order.index(cards[i].extras[-1].removeprefix("target:")), i))
    for j, i in enumerate(ranked):
        cards[i] = cards[i].model_copy(update={"generator": pattern[j % len(pattern)]})
    return cards
