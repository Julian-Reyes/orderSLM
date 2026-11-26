"""The 60 sim1 scenario cards (live-sim@0.1), written by Claude in the session on 2026-11-26. Each card's target is the
order this customer wants; the plan says how they talk. Evaluation-only (never training or generation input).

    uv run python runs/live-sim/build_cards.py   # → data/sim1/cards.jsonl, then `make live-sim ARGS=check`
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "data" / "sim1" / "cards.jsonl"
TZ = {"corner-patty": "-05:00", "halfmoon-pizza": "-06:00", "morning-crumb": "-08:00"}


def I(item, variant=None, q=1, mods=(), combo=()):  # noqa: E743
    return {
        "menu_item_id": item,
        "variant_id": variant,
        "quantity": q,
        "modifications": list(mods),
        "combo_selections": [{"slot_id": s, "menu_item_id": m, "variant_id": v} for s, m, v in combo],
    }


def rm(x):
    return {"kind": "remove", "modifier_id": x}


def add(x, amount="normal"):
    return {"kind": "add", "modifier_id": x, "amount": amount}


def sub(old, new):
    return {"kind": "substitute", "modifier_id": old, "replacement_modifier_id": new}


CARDS = []


def card(
    biz,
    day,
    at,
    persona,
    style,
    plan,
    items,
    method,
    pay,
    *,
    time=None,
    ahead=0,
    addr=None,
    change=None,
    name=None,
    careless=False,
):
    CARDS.append(
        {
            "id": f"sim1-{len(CARDS) + 1:03d}",
            "business_id": biz,
            "start_at": f"2026-12-{day:02d}T{at}:00{TZ[biz]}",
            "persona": persona,
            "style": style,
            "plan": plan,
            "checks_summary": not careless,
            "target": {
                "items": items,
                "method": method,
                "days_ahead": ahead,
                "time": time,
                "address": addr,
                "payment": pay,
                "change_for_cents": change,
                "name": name,
            },
        }
    )


CP, HP, MC = "corner-patty", "halfmoon-pizza", "morning-crumb"

# ---- Corner Patty (11:00-22:00, New York)
card(
    CP,
    1,
    "12:10",
    "office worker on lunch break",
    "plain",
    "Says everything in the first message.",
    [I("cheeseburger", "single", 2), I("fries", "large"), I("coke", q=2)],
    "pickup",
    "card",
    name="Mike",
)
card(
    CP,
    1,
    "18:05",
    "tired parent",
    "lowercase, no punctuation",
    "Asks for 'the cheeseburger combo, no pickles' and a coke, delivery; picks onion rings and lemonade for the "
    "combo only when asked; pays cash and needs change for a $20.",
    [
        I(
            "cheeseburger_combo",
            mods=[rm("pickle")],
            combo=[("side", "onion_rings", None), ("drink", "lemonade", None)],
        ),
        I("coke"),
    ],
    "delivery",
    "cash",
    addr="418 Maple Ave",
    change=2000,
)
card(
    CP,
    2,
    "16:40",
    "college student",
    "casual, typos",
    "First message: the two burgers. Second message: pickup at 6:30 for Dana, card.",
    [I("bacon_burger", mods=[add("jalapeno")]), I("veggie_burger", mods=[rm("onion")])],
    "pickup",
    "card",
    time="18:30",
    name="Dana",
)
card(
    CP,
    2,
    "19:20",
    "group dinner organizer",
    "chatty",
    "Starts with 2 double cheeseburgers, 2 regular fries, 2 sprites; then 'actually make it 3 of each'.",
    [I("cheeseburger", "double", 3), I("fries", "regular", 3), I("sprite", q=3)],
    "delivery",
    "card",
    addr="77 Birch St Apt 4",
)
card(
    CP,
    3,
    "14:15",
    "teenager",
    "short messages",
    "Asks for '2 milkshakes' with no flavor; says chocolate when asked; pickup, cash, name Lee.",
    [I("milkshake", "chocolate", 2)],
    "pickup",
    "cash",
    name="Lee",
)
card(
    CP,
    3,
    "12:00",
    "busy nurse",
    "plain",
    "Orders everything in one message, pickup at 12:15.",
    [I("veggie_burger", mods=[add("avocado")]), I("fries", "regular"), I("lemonade")],
    "pickup",
    "card",
    time="12:15",
    careless=True,
)
card(
    CP,
    4,
    "17:30",
    "couple ordering for two",
    "two quick messages",
    "One combo with fries and a coke, another combo with onion rings and a sprite; pickup, card, name Tom.",
    [
        I("cheeseburger_combo", combo=[("side", "fries", None), ("drink", "coke", None)]),
        I("cheeseburger_combo", combo=[("side", "onion_rings", None), ("drink", "sprite", None)]),
    ],
    "pickup",
    "card",
    name="Tom",
)
card(
    CP,
    4,
    "20:10",
    "night-shift worker",
    "abbreviations",
    "Two bacon burgers with no tomato and onion rings, delivery, card.",
    [I("bacon_burger", q=2, mods=[rm("tomato")]), I("onion_rings")],
    "delivery",
    "card",
    addr="9 Harbor Rd",
    careless=True,
)
card(
    CP,
    5,
    "13:45",
    "regular customer",
    "friendly",
    "A cheeseburger with extra cheese and a coke, pickup at 7:45 tonight, cash, name Priya.",
    [I("cheeseburger", "single", mods=[add("cheese", "extra")]), I("coke")],
    "pickup",
    "cash",
    time="19:45",
    name="Priya",
)
card(
    CP,
    3,
    "15:00",
    "planning a team lunch",
    "plain",
    "Orders for tomorrow at 1pm: 4 single cheeseburgers and 4 regular fries, pickup, card, name Sam.",
    [I("cheeseburger", "single", 4), I("fries", "regular", 4)],
    "pickup",
    "card",
    time="13:00",
    ahead=1,
    name="Sam",
)
card(
    CP,
    1,
    "13:30",
    "indecisive customer",
    "casual",
    "Orders a cheeseburger with no onions, large fries and a coke; next message 'actually sprite not coke'; "
    "pickup, card.",
    [I("cheeseburger", "single", mods=[rm("onion")]), I("fries", "large"), I("sprite")],
    "pickup",
    "card",
)
card(
    CP,
    2,
    "12:50",
    "regular who assumes the bot knows them",
    "casual",
    "Opens with 'can i get my usual'; when asked, says a bacon burger and onion rings; pickup, cash, name Rob.",
    [I("bacon_burger"), I("onion_rings")],
    "pickup",
    "cash",
    name="Rob",
)
card(
    CP,
    5,
    "18:40",
    "family dinner",
    "long message plus a follow-up",
    "Two bacon burgers (one with no onion), a veggie burger, 3 regular fries, onion rings, 2 cokes, a lemonade; "
    "delivery, card.",
    [
        I("bacon_burger"),
        I("bacon_burger", mods=[rm("onion")]),
        I("veggie_burger"),
        I("fries", "regular", 3),
        I("onion_rings"),
        I("coke", q=2),
        I("lemonade"),
    ],
    "delivery",
    "card",
    addr="1200 Elm St",
)
card(
    CP,
    4,
    "14:20",
    "two friends",
    "emoji",
    "A vanilla and a strawberry milkshake and large fries, pickup at 3pm.",
    [I("milkshake", "vanilla"), I("milkshake", "strawberry"), I("fries", "large")],
    "pickup",
    "card",
    time="15:00",
    careless=True,
)
card(
    CP,
    1,
    "19:00",
    "hungry gamer",
    "plain",
    "A cheeseburger combo with bacon added, fries and a coke, plus onion rings, delivery, paying cash (no change "
    "needed).",
    [
        I(
            "cheeseburger_combo",
            mods=[add("bacon")],
            combo=[("side", "fries", None), ("drink", "coke", None)],
        ),
        I("onion_rings"),
    ],
    "delivery",
    "cash",
    addr="55 Pine St",
)
card(
    CP,
    2,
    "11:40",
    "careful eater",
    "polite",
    "First asks 'do you have gluten free buns?'; whatever the answer, orders a veggie burger and a sprite; "
    "pickup, card, name Jo.",
    [I("veggie_burger"), I("sprite")],
    "pickup",
    "card",
    name="Jo",
)
card(
    CP,
    3,
    "20:30",
    "student",
    "lowercase",
    "Two cheeseburgers, no pickles and no onions on both, delivery, card.",
    [I("cheeseburger", "single", 2, mods=[rm("pickle"), rm("onion")])],
    "delivery",
    "card",
    addr="300 Oak Blvd Unit 12",
    careless=True,
)
card(
    CP,
    4,
    "12:30",
    "budget-minded",
    "plain",
    "Orders 2 cheeseburgers, regular fries and onion rings; then 'drop the onion rings'; pickup, cash, name Ana.",
    [I("cheeseburger", "single", 2), I("fries", "regular")],
    "pickup",
    "cash",
    name="Ana",
)
card(
    CP,
    5,
    "15:30",
    "planner",
    "plain",
    "Two veggie burgers and two lemonades for pickup at 6; then changes to 6:30; card, name Kai.",
    [I("veggie_burger", q=2), I("lemonade", q=2)],
    "pickup",
    "card",
    time="18:30",
    name="Kai",
)
card(
    CP,
    1,
    "21:00",
    "late-night regular",
    "heavy abbreviations",
    "'2 cb dbl w bacon, lg fry, 2 sprites, deliv 64 cedar ct, card' in one message.",
    [I("cheeseburger", "double", 2, mods=[add("bacon")]), I("fries", "large"), I("sprite", q=2)],
    "delivery",
    "card",
    addr="64 Cedar Ct",
    careless=True,
)

# ---- Halfmoon Pizza (12:00-23:00, Chicago)
card(
    HP,
    1,
    "18:00",
    "dad picking up dinner",
    "plain",
    "Everything up front: 2 large pepperoni, pickup, card, Jake.",
    [I("pepperoni_pizza", "large", 2)],
    "pickup",
    "card",
    name="Jake",
)
card(
    HP,
    1,
    "19:10",
    "roommates",
    "casual",
    "'a margherita and garlic knots' with no size; says medium when asked; delivery; cash, change for $30.",
    [I("margherita_pizza", "medium"), I("garlic_knots")],
    "delivery",
    "cash",
    addr="812 Lake St",
    change=3000,
)
card(
    HP,
    2,
    "17:20",
    "regular",
    "friendly",
    "A large hawaiian on thin crust and a 2 liter coke, pickup at 7, card, name Rita.",
    [I("hawaiian_pizza", "large", mods=[add("crust_thin")]), I("coke", "two_liter")],
    "pickup",
    "card",
    time="19:00",
    name="Rita",
)
card(
    HP,
    2,
    "20:45",
    "night owl",
    "lowercase",
    "An extra large supreme with no olives and breadsticks, delivery, card.",
    [I("supreme_pizza", "extra_large", mods=[rm("olives")]), I("breadsticks")],
    "delivery",
    "card",
    addr="45 River Rd",
    careless=True,
)
card(
    HP,
    3,
    "13:15",
    "indecisive",
    "casual",
    "A medium cheese pizza with mushrooms; then 'make it a large'; pickup, cash, name Ben.",
    [I("cheese_pizza", "large", mods=[add("mushrooms")])],
    "pickup",
    "cash",
    name="Ben",
)
card(
    HP,
    3,
    "16:00",
    "party host",
    "plain",
    "Orders for Saturday at 6pm: 2 large meat lovers and 2 garlic knots, delivery, card.",
    [I("meat_lovers_pizza", "large", 2), I("garlic_knots", q=2)],
    "delivery",
    "card",
    time="18:00",
    ahead=2,
    addr="990 Summit Ave",
)
card(
    HP,
    4,
    "12:05",
    "lunch break",
    "short",
    "A medium bbq chicken and two 20oz diet cokes, pickup at 12:30, card, name Nina.",
    [I("bbq_chicken_pizza", "medium"), I("diet_coke", "bottle_20oz", 2)],
    "pickup",
    "card",
    time="12:30",
    name="Nina",
)
card(
    HP,
    4,
    "18:30",
    "kid with a parent's phone",
    "emoji",
    "A small veggie pizza with extra cheese, pickup, card, name Leo.",
    [I("veggie_pizza", "small", mods=[add("cheese", "extra")])],
    "pickup",
    "card",
    name="Leo",
    careless=True,
)
card(
    HP,
    5,
    "19:30",
    "family night",
    "several short messages",
    "A large pepperoni, a large cheese, a medium hawaiian, 2 garlic knots, a 2 liter sprite; delivery, card.",
    [
        I("pepperoni_pizza", "large"),
        I("cheese_pizza", "large"),
        I("hawaiian_pizza", "medium"),
        I("garlic_knots", q=2),
        I("sprite", "two_liter"),
    ],
    "delivery",
    "card",
    addr="15 Grove St Apt 3B",
)
card(
    HP,
    5,
    "17:00",
    "office party",
    "plain",
    "Asks for 'some pepperoni pizzas'; when asked, 3 mediums; pickup at 8:15pm, card, name Omar.",
    [I("pepperoni_pizza", "medium", 3)],
    "pickup",
    "card",
    time="20:15",
    name="Omar",
)
card(
    HP,
    1,
    "14:30",
    "picky eater",
    "plain",
    "A large cheese pizza with sausage and mushrooms, delivery, card; corrects the summary if anything is off.",
    [I("cheese_pizza", "large", mods=[add("sausage"), add("mushrooms")])],
    "delivery",
    "card",
    addr="23 Fifth Ave",
)
card(
    HP,
    2,
    "13:00",
    "solo lunch",
    "short",
    "A personal pepperoni and a water, pickup, cash, name Zoe.",
    [I("pepperoni_pizza", "personal"), I("water")],
    "pickup",
    "cash",
    name="Zoe",
    careless=True,
)
card(
    HP,
    3,
    "18:50",
    "new in town",
    "polite",
    "First asks 'do you deliver to evanston?'; then orders a large margherita and an iced tea can, delivery, card.",
    [I("margherita_pizza", "large"), I("iced_tea", "can")],
    "delivery",
    "card",
    addr="610 Church St",
)
card(
    HP,
    4,
    "20:00",
    "changes their mind",
    "casual",
    "2 large cheese pizzas and breadsticks; then 'actually no breadsticks'; pickup, card, name Ivy.",
    [I("cheese_pizza", "large", 2)],
    "pickup",
    "card",
    name="Ivy",
)
card(
    HP,
    5,
    "15:45",
    "movie night",
    "plain",
    "Two medium hawaiians and two dr pepper cans, pickup at 9pm, card, name Max.",
    [I("hawaiian_pizza", "medium", 2), I("dr_pepper", "can", 2)],
    "pickup",
    "card",
    time="21:00",
    name="Max",
)
card(
    HP,
    1,
    "21:15",
    "spicy food fan",
    "plain",
    "A large pepperoni with jalapenos and onions, delivery, cash with change for $50.",
    [I("pepperoni_pizza", "large", mods=[add("jalapenos"), add("onions")])],
    "delivery",
    "cash",
    addr="400 State St",
    change=5000,
)
card(
    HP,
    2,
    "12:40",
    "celiac",
    "polite",
    "A small margherita on gluten free crust, pickup, card, name Sara.",
    [I("margherita_pizza", "small", mods=[add("crust_gluten_free")])],
    "pickup",
    "card",
    name="Sara",
    careless=True,
)
card(
    HP,
    3,
    "17:10",
    "two kids' parent",
    "plain",
    "'2 pizzas, one pepperoni one cheese, both large' and a 2 liter coke, pickup at 6:45, card, name Eli.",
    [I("pepperoni_pizza", "large"), I("cheese_pizza", "large"), I("coke", "two_liter")],
    "pickup",
    "card",
    time="18:45",
    name="Eli",
)
card(
    HP,
    4,
    "16:20",
    "planning ahead",
    "plain",
    "For tomorrow at 12:30: a large veggie and a large bbq chicken, pickup, card, name Ava.",
    [I("veggie_pizza", "large"), I("bbq_chicken_pizza", "large")],
    "pickup",
    "card",
    time="12:30",
    ahead=1,
    name="Ava",
)
card(
    HP,
    5,
    "22:00",
    "late-night regular",
    "heavy abbreviations",
    "'lg pep x2 + knots, deliv 88 oak pl, cash, change for 50' in one message.",
    [I("pepperoni_pizza", "large", 2), I("garlic_knots")],
    "delivery",
    "cash",
    addr="88 Oak Pl",
    change=5000,
    careless=True,
)

# ---- Morning Crumb Café (07:00-15:00, Los Angeles; pickup needs a name)
card(
    MC,
    1,
    "08:00",
    "commuter",
    "plain",
    "A medium latte with oat milk and a plain croissant, pickup, card, Mia.",
    [I("latte", "medium", mods=[sub("whole_milk", "oat_milk")]), I("croissant", "plain")],
    "pickup",
    "card",
    name="Mia",
)
card(
    MC,
    1,
    "09:05",
    "remote worker",
    "casual",
    "'2 cappuccinos' with no size; says small when asked; pickup at 9:30, cash, name Theo.",
    [I("cappuccino", "small", 2)],
    "pickup",
    "cash",
    time="09:30",
    name="Theo",
)
card(
    MC,
    2,
    "07:40",
    "early riser",
    "short",
    "A large drip coffee and 2 blueberry muffins, pickup, card, Ana.",
    [I("drip_coffee", "large"), I("muffin", "blueberry", 2)],
    "pickup",
    "card",
    name="Ana",
    careless=True,
)
card(
    MC,
    2,
    "07:30",
    "student before class",
    "casual",
    "Asks for 'the coffee and pastry combo'; picks a medium latte and a chocolate croissant when asked; pickup at 8, "
    "card, name Ruth.",
    [I("coffee_pastry_combo", combo=[("drink", "latte", "medium"), ("pastry", "croissant", "chocolate")])],
    "pickup",
    "card",
    time="08:00",
    name="Ruth",
)
card(
    MC,
    3,
    "10:15",
    "working from home",
    "plain",
    "Two everything bagels with cream cheese and a medium americano; asks for delivery first, then picks it up when "
    "told it's pickup only; card, name Fern.",
    [I("bagel", "everything", 2, mods=[add("cream_cheese")]), I("americano", "medium")],
    "pickup",
    "card",
    name="Fern",
)
card(
    MC,
    3,
    "08:20",
    "changes their mind",
    "casual",
    "A medium latte; then 'make it a large with vanilla'; pickup, card, name Jon.",
    [I("latte", "large", mods=[add("vanilla_syrup")])],
    "pickup",
    "card",
    name="Jon",
)
card(
    MC,
    4,
    "09:40",
    "vegetarian",
    "polite",
    "A breakfast sandwich on a croissant with no bacon and with avocado, and a small hot chocolate; pickup, cash, "
    "name Cleo.",
    [I("breakfast_sandwich", "croissant", mods=[rm("bacon"), add("avocado")]), I("hot_chocolate", "small")],
    "pickup",
    "cash",
    name="Cleo",
)
card(
    MC,
    4,
    "13:30",
    "office assistant",
    "plain",
    "For tomorrow at 7:30am: 6 medium drip coffees and 6 banana nut muffins, pickup, card, name Lena.",
    [I("drip_coffee", "medium", 6), I("muffin", "banana_nut", 6)],
    "pickup",
    "card",
    time="07:30",
    ahead=1,
    name="Lena",
)
card(
    MC,
    5,
    "08:45",
    "ordering for coworkers",
    "several short messages",
    "A small latte with almond milk, a medium cappuccino, 2 almond croissants, a sesame bagel with butter; "
    "pickup, card, name Gus.",
    [
        I("latte", "small", mods=[sub("whole_milk", "almond_milk")]),
        I("cappuccino", "medium"),
        I("croissant", "almond", 2),
        I("bagel", "sesame", mods=[add("butter")]),
    ],
    "pickup",
    "card",
    name="Gus",
)
card(
    MC,
    5,
    "11:10",
    "sweet tooth",
    "emoji",
    "A large hot chocolate with extra whipped cream and a chocolate chip muffin, pickup, card, name Pia.",
    [I("hot_chocolate", "large", mods=[add("whipped_cream", "extra")]), I("muffin", "chocolate_chip")],
    "pickup",
    "card",
    name="Pia",
    careless=True,
)
card(
    MC,
    1,
    "07:55",
    "sleepy",
    "vague",
    "Asks for 'the thing with egg'; when asked, the breakfast sandwich on an english muffin; adds a small drip "
    "coffee; pickup, cash, name Hal.",
    [I("breakfast_sandwich", "english_muffin"), I("drip_coffee", "small")],
    "pickup",
    "cash",
    name="Hal",
)
card(
    MC,
    2,
    "10:30",
    "allergy-aware",
    "polite",
    "First asks 'is the almond croissant made with real almonds?'; then orders 2 plain croissants and a large "
    "americano; pickup, card, name Ida.",
    [I("croissant", "plain", 2), I("americano", "large")],
    "pickup",
    "card",
    name="Ida",
)
card(
    MC,
    3,
    "12:15",
    "lunch run",
    "casual",
    "A medium latte, a blueberry muffin and a plain bagel; then 'skip the bagel'; pickup, card, name Ned.",
    [I("latte", "medium"), I("muffin", "blueberry")],
    "pickup",
    "card",
    name="Ned",
)
card(
    MC,
    4,
    "09:20",
    "planner",
    "plain",
    "A large cappuccino with hazelnut and a plain croissant with butter for 10:00; then changes to 10:30; pickup, "
    "card, name Ola.",
    [I("cappuccino", "large", mods=[add("hazelnut_syrup")]), I("croissant", "plain", mods=[add("butter")])],
    "pickup",
    "card",
    time="10:30",
    name="Ola",
)
card(
    MC,
    5,
    "08:05",
    "team breakfast",
    "short",
    "3 medium drip coffees and 3 blueberry muffins, pickup, card, name Dot.",
    [I("drip_coffee", "medium", 3), I("muffin", "blueberry", 3)],
    "pickup",
    "card",
    name="Dot",
    careless=True,
)
card(
    MC,
    1,
    "11:50",
    "regular",
    "plain",
    "A small americano with whole milk and a cinnamon raisin bagel with butter; pickup, cash, name Vic.",
    [I("americano", "small", mods=[add("whole_milk")]), I("bagel", "cinnamon_raisin", mods=[add("butter")])],
    "pickup",
    "cash",
    name="Vic",
)
card(
    MC,
    2,
    "13:05",
    "two friends",
    "casual",
    "'2 lattes, one oat one regular, both medium'; pickup, card, name Bea.",
    [I("latte", "medium", mods=[sub("whole_milk", "oat_milk")]), I("latte", "medium")],
    "pickup",
    "card",
    name="Bea",
)
card(
    MC,
    3,
    "10:50",
    "pays cash",
    "plain",
    "A small drip coffee and a chocolate croissant for 11:15, cash, change for a $20, name Rex.",
    [I("drip_coffee", "small"), I("croissant", "chocolate")],
    "pickup",
    "cash",
    time="11:15",
    change=2000,
    name="Rex",
)
card(
    MC,
    4,
    "07:15",
    "knows what they want",
    "plain",
    "The combo with a large americano and a blueberry muffin, plus a plain bagel with cream cheese; pickup, card, "
    "name Una.",
    [
        I("coffee_pastry_combo", combo=[("drink", "americano", "large"), ("pastry", "muffin", "blueberry")]),
        I("bagel", "plain", mods=[add("cream_cheese")]),
    ],
    "pickup",
    "card",
    name="Una",
    careless=True,
)
card(
    MC,
    5,
    "12:30",
    "texter",
    "emoji, abbreviations",
    "'lg hot choc + 2 everything bagels w cc, pickup 1pm, card, name wes' in one message.",
    [I("hot_chocolate", "large"), I("bagel", "everything", 2, mods=[add("cream_cheese")])],
    "pickup",
    "card",
    time="13:00",
    name="Wes",
    careless=True,
)

assert len(CARDS) == 60
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("".join(json.dumps(c) + "\n" for c in CARDS))
print(f"wrote {len(CARDS)} cards to {OUT}")
