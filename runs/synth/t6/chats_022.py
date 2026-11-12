"""t6 entries 0216–0228 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t6-0216",
        """
c: 3 medium supremes no mushrooms w olive oil n thick crust 🍕
c: + a personal hawaiian, an order of garlic knots n a can of dr pepper, pickup, cash 💵
c: actually skip the hawaiian 🙅
""",
        "P P M",
        items=[
            I(
                "supreme_pizza",
                3,
                "medium",
                ["3 medium supremes no mushrooms w olive oil n thick crust"],
                [
                    rm("mushrooms", "no mushrooms"),
                    add("olive_oil", "w olive oil"),
                    add("crust_thick", "thick crust"),
                ],
            ),
            I("garlic_knots", 1, None, ["an order of garlic knots"]),
            I("dr_pepper", 1, "can", ["a can of dr pepper"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0217",
        """
c: hi
c: small cappuccino
c: w cinnamon on top
c: pickup
c: grace
c: card
""",
        "S P P P P P",
        items=[
            I(
                "cappuccino",
                1,
                "small",
                ["small cappuccino", "w cinnamon on top"],
                [offmod("w cinnamon on top")],
            )
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t6-0218",
        """
c: A medium BBQ chicken pizza with onions, an order of breadsticks and a 2 liter Dr Pepper for pickup, card.
c: Sorry, no Dr Pepper after all.
""",
        "P M",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "medium",
                ["A medium BBQ chicken pizza with onions"],
                [add("onions", "with onions")],
            ),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0219",
        """
c: hey
c: onion rings n 3 vanilla shakes for tmrw at 4:30
c: pickup, maya, card
""",
        "S P P",
        items=[
            I("onion_rings", 1, None, ["onion rings"]),
            I("milkshake", 3, "vanilla", ["3 vanilla shakes"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 4:30", "16:30"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t6-0220",
        """
c: 3 small lattes w hazelnut n a large americano for fri at 7:45, pickup for eli, card
""",
        "P",
        items=[
            I("latte", 3, "small", ["3 small lattes w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("americano", 1, "large", ["a large americano"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:45", "07:45"),
        day=("weekday", "fri", "fri"),
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t6-0221",
        """
c: hey ☀️
c: 3 small americanos + a medium latte w skim milk
c: cash 💵
c: oh only 2 americanos actually
""",
        "S P P M",
        items=[
            I("americano", 2, "small", ["3 small americanos", "only 2 americanos"]),
            I(
                "latte",
                1,
                "medium",
                ["a medium latte w skim milk"],
                [sub("whole_milk", "skim_milk", "w skim milk")],
            ),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0222",
        """
c: single cheeseburger w chili on it
c: n 2 cokes
c: cash
""",
        "P P P",
        items=[
            I("cheeseburger", 1, "single", ["single cheeseburger w chili on it"], [offmod("w chili on it")]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0223",
        """
c: Do your milkshakes come in strawberry?
b: Yes, vanilla, chocolate or strawberry.
c: Great, two strawberry milkshakes for pickup on Friday. Name is Dev, paying by card.
""",
        "Q P",
        items=[I("milkshake", 2, "strawberry", ["two strawberry milkshakes"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "on Friday"),
        day=("weekday", "fri", "Friday"),
        pay="card",
        pay_q="paying by card",
        name="Dev",
    ),
    X(
        "syn-t6-0224",
        """
c: yo
c: 2 sprites
c: for tmrw
c: pickup
c: eli
c: card
""",
        "S P P P P P",
        items=[I("sprite", 2, None, ["2 sprites"])],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tmrw"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t6-0225",
        """
c: do u guys have decaf?
b: Sorry, we don't have decaf on the menu.
c: ok a coffee then for pickup at 1, jordan
c: actually can u do tomorrow at 1 instead
""",
        "Q P M",
        items=[I("drip_coffee", 1, None, ["a coffee"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 1", "13:00"),
        day=("tomorrow", "tomorrow"),
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t6-0226",
        """
c: hey there
c: 4 single cheeseburgers, 1 of them no onions
c: n 4 sprites
c: pickup at 8:45 for tom
""",
        "S P P P",
        items=[
            I("cheeseburger", 3, "single", ["4 single cheeseburgers"]),
            I(
                "cheeseburger",
                1,
                "single",
                ["4 single cheeseburgers", "1 of them no onions"],
                [rm("onion", "no onions")],
            ),
            I("sprite", 4, None, ["4 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8:45", "20:45"),
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t6-0227",
        """
c: can i order for wed morning
b: Sure, we can take orders ahead. What would you like, and what time?
c: 4 coffees at 7:30, pickup for nico, card
""",
        "D P",
        items=[I("drip_coffee", 4, None, ["4 coffees"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:30", "07:30"),
        day=("weekday", "wed", "wed"),
        pay="card",
        pay_q="card",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t6-0228",
        """
c: a cheeseburger, a veggie burger n same as last time to 1697 cedar hill st 🙏
""",
        "P",
        items=[
            I("cheeseburger", 1, None, ["a cheeseburger"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="to 1697 cedar hill st",
        addr={"raw": "1697 cedar hill st", "number": "1697", "street": "cedar hill st"},
    ),
]
