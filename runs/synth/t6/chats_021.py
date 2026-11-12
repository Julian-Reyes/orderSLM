"""t6 entries 0204–0215 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0204",
        """
c: r ur fries seasoned
b: They come lightly salted. We can make them without salt if you like.
c: ok
c: large fries delivered
c: for oct 17 at 1
""",
        "Q S P P",
        items=[I("fries", 1, "large", ["large fries"])],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 1", "13:00"),
        day=("date", 10, 17, "oct 17"),
    ),
    X(
        "syn-t6-0205",
        """
c: hey can i get that thing from before
b: Sorry, I can't see past orders here. What would you like?
c: 4 cans of iced tea, an xl meat lovers, 2 medium hawaiians no sauce w basil n an xl bbq chicken w pepperoni. deliver to 1320 union way above the bakery, card
""",
        "P P",
        items=[
            I("iced_tea", 4, "can", ["4 cans of iced tea"]),
            I("meat_lovers_pizza", 1, "extra_large", ["an xl meat lovers"]),
            I(
                "hawaiian_pizza",
                2,
                "medium",
                ["2 medium hawaiians no sauce w basil"],
                [rm("tomato_sauce", "no sauce"), add("basil", "w basil")],
            ),
            I(
                "bbq_chicken_pizza",
                1,
                "extra_large",
                ["an xl bbq chicken w pepperoni"],
                [add("pepperoni", "w pepperoni")],
            ),
        ],
        method="delivery",
        method_q="deliver to 1320 union way",
        addr={
            "raw": "1320 union way above the bakery",
            "number": "1320",
            "street": "union way",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0206",
        """
c: Hi, two veggie burgers, one with mustard.
c: And a Coke.
c: Delivered to 89 Dover Dr, unit 22C.
c: As soon as possible, please.
c: Card.
""",
        "P P P P P",
        items=[
            I("veggie_burger", 1, None, ["two veggie burgers"]),
            I(
                "veggie_burger",
                1,
                None,
                ["two veggie burgers", "one with mustard"],
                [add("mustard", "with mustard")],
            ),
            I("coke", 1, None, ["a Coke"]),
        ],
        method="delivery",
        method_q="Delivered to 89 Dover Dr",
        time=("asap", "As soon as possible", None),
        addr={"raw": "89 Dover Dr, unit 22C", "number": "89", "street": "Dover Dr", "unit": "unit 22C"},
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t6-0207",
        """
c: bacon burger w avocado
c: onion rings
c: 2 lemonades
c: card
c: actually fries instead of the onion rings
""",
        "P P P P M",
        items=[
            I("bacon_burger", 1, None, ["bacon burger w avocado"], [add("avocado", "w avocado")]),
            I("fries", 1, None, ["fries instead of the onion rings"]),
            I("lemonade", 2, None, ["2 lemonades"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0208",
        """
c: Good evening.
c: Do you have thick crust?
b: Yes, thick crust is available on any pizza.
c: Then a medium veggie pizza with thick crust for Thursday at 7, please.
c: Delivered to 93 Thornton Blvd #19A, paying by card.
""",
        "S Q P P",
        items=[
            I(
                "veggie_pizza",
                1,
                "medium",
                ["a medium veggie pizza with thick crust"],
                [add("crust_thick", "with thick crust")],
            )
        ],
        method="delivery",
        method_q="Delivered to 93 Thornton Blvd #19A",
        time=("clock_time", "at 7", "19:00"),
        day=("weekday", "thu", "Thursday"),
        addr={"raw": "93 Thornton Blvd #19A", "number": "93", "street": "Thornton Blvd", "unit": "#19A"},
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t6-0209",
        """
c: 3 bagels
c: for wed
c: at 7:30
c: pickup priya
c: card
""",
        "P P P P P",
        items=[I("bagel", 3, None, ["3 bagels"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:30", "07:30"),
        day=("weekday", "wed", "wed"),
        pay="card",
        pay_q="card",
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t6-0210",
        """
c: hey 👋
c: single cheeseburger no ketchup, a lemonade n onion rings, delivery on monday 🙏 card
""",
        "S P",
        items=[
            I("cheeseburger", 1, "single", ["single cheeseburger no ketchup"], [rm("ketchup", "no ketchup")]),
            I("lemonade", 1, None, ["a lemonade"]),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        method="delivery",
        method_q="delivery",
        time=("ambiguous", "on monday"),
        day=("weekday", "mon", "monday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0211",
        """
c: 2 small veggies, 1 no cheese
c: 2 medium supremes no pepperoni + a personal margherita no olive oil
c: a 20 oz iced tea
c: deliver to 28 riverside dr, cash
""",
        "P P P P",
        items=[
            I("veggie_pizza", 1, "small", ["2 small veggies"]),
            I("veggie_pizza", 1, "small", ["2 small veggies", "1 no cheese"], [rm("cheese", "no cheese")]),
            I(
                "supreme_pizza",
                2,
                "medium",
                ["2 medium supremes no pepperoni"],
                [rm("pepperoni", "no pepperoni")],
            ),
            I(
                "margherita_pizza",
                1,
                "personal",
                ["a personal margherita no olive oil"],
                [rm("olive_oil", "no olive oil")],
            ),
            I("iced_tea", 1, "bottle_20oz", ["a 20 oz iced tea"]),
        ],
        method="delivery",
        method_q="deliver to 28 riverside dr",
        addr={"raw": "28 riverside dr", "number": "28", "street": "riverside dr"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0212",
        """
c: 3 bagels
c: tmrw 8:45
c: pickup jordan
c: cash, change for a 20
""",
        "P P P P",
        items=[I("bagel", 3, None, ["3 bagels"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "8:45", "08:45"),
        day=("tomorrow", "tmrw"),
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t6-0213",
        """
c: 4 cans of iced tea
c: delivery sunday at 5
c: card
c: actually can u bring it now instead, asap
""",
        "P P P M",
        items=[I("iced_tea", 4, "can", ["4 cans of iced tea"])],
        method="delivery",
        method_q="delivery",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0214",
        """
c: a supreme no olives
c: add red onions
c: n a coke
c: deliver to 116 chestnut ln, card
""",
        "P P P P",
        items=[
            I(
                "supreme_pizza",
                1,
                None,
                ["a supreme no olives", "add red onions"],
                [rm("olives", "no olives"), add("red_onions", "add red onions")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="deliver to 116 chestnut ln",
        addr={"raw": "116 chestnut ln", "number": "116", "street": "chestnut ln"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0215",
        """
c: Hi, I'd like one bottled water for pickup on Thursday. Name is Ben, paying by card.
""",
        "P",
        items=[I("water", 1, None, ["one bottled water"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "on Thursday"),
        day=("weekday", "thu", "Thursday"),
        pay="card",
        pay_q="paying by card",
        name="Ben",
    ),
]
