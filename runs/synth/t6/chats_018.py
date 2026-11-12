"""t6 entries 0171–0180 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0171",
        """
c: hey can i get 2 breakfast sandwiches on a bagel w avocado
c: pickup for dev
c: card
b: Got it, Dev: 2 breakfast sandwiches on a bagel with avocado, for pickup, paying by card. Is that right?
c: yes
c: oh wait just 1 sandwich actually
""",
        "P P P C M",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "bagel",
                ["2 breakfast sandwiches on a bagel w avocado", "just 1 sandwich"],
                [add("avocado", "w avocado")],
            )
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0172",
        """
c: HELLO
c: A LARGE BBQ CHICKEN PIZZA
c: A WATER, A COKE AND AN ICED TEA
c: FOR PICKUP
""",
        "S P P P",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["A LARGE BBQ CHICKEN PIZZA"]),
            I("water", 1, None, ["A WATER"]),
            I("coke", 1, None, ["A COKE"]),
            I("iced_tea", 1, None, ["AN ICED TEA"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
    ),
    X(
        "syn-t6-0173",
        """
c: morning
c: some cinnamon raisin bagels
c: 2 small americanos
c: in 15 min
c: cash
""",
        "S P P P P",
        items=[
            I("bagel", None, "cinnamon_raisin", ["some cinnamon raisin bagels"]),
            I("americano", 2, "small", ["2 small americanos"]),
        ],
        time=("relative", "in 15 min", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0174",
        """
c: is the cappuccino extra foamy? ☕
b: We can make it extra foamy if you'd like!
c: nah normal is fine 😊 a medium cappuccino n same as last time, asap, pickup for rosa
""",
        "Q P",
        items=[
            I("cappuccino", 1, "medium", ["a medium cappuccino"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0175",
        """
c: Do you still take orders until 11?
b: Yes, we're open until 11 pm.
c: Great: a medium cheese pizza, a large margherita and 2 large Hawaiians for pickup. Name is Marcus, paying cash.
c: Actually, drop the Hawaiians.
""",
        "D P M",
        items=[
            I("cheese_pizza", 1, "medium", ["a medium cheese pizza"]),
            I("margherita_pizza", 1, "large", ["a large margherita"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="paying cash",
        name="Marcus",
    ),
    X(
        "syn-t6-0176",
        """
c: HI
c: ONE COFFEE AND PASTRY DEAL WITH A DRIP COFFEE AND A CROISSANT, PLUS 2 PLAIN CROISSANTS ON THEIR OWN
c: PICKUP AT 2:30 FOR TOM
""",
        "S P P",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["ONE COFFEE AND PASTRY DEAL WITH A DRIP COFFEE AND A CROISSANT"],
                combo={"drink": "drip_coffee", "pastry": "croissant"},
            ),
            I("croissant", 2, "plain", ["2 PLAIN CROISSANTS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 2:30", "14:30"),
        name="Tom",
        name_q="TOM",
    ),
    X(
        "syn-t6-0177",
        """
c: hey good morning
c: 3 coffees w vanilla, a small americano n one of those
c: pickup for nico
""",
        "S P P",
        items=[
            I("drip_coffee", 3, None, ["3 coffees w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("americano", 1, "small", ["a small americano"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t6-0178",
        """
c: hey 🍕
c: 5 large meat lovers, 3 of them no cheese
c: n 3 diet cokes 🥤
c: deliver to 833 cedar hill blvd apt 18c, card 💳
""",
        "S P P P",
        items=[
            I("meat_lovers_pizza", 2, "large", ["5 large meat lovers"]),
            I(
                "meat_lovers_pizza",
                3,
                "large",
                ["5 large meat lovers", "3 of them no cheese"],
                [rm("cheese", "no cheese")],
            ),
            I("diet_coke", 3, None, ["3 diet cokes"]),
        ],
        method="delivery",
        method_q="deliver to 833 cedar hill blvd",
        addr={
            "raw": "833 cedar hill blvd apt 18c",
            "number": "833",
            "street": "cedar hill blvd",
            "unit": "apt 18c",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0179",
        """
c: hi
c: 2 medium hawaiians no ham, thick crust
c: for friday at 8
c: card
""",
        "S P P P",
        items=[
            I(
                "hawaiian_pizza",
                2,
                "medium",
                ["2 medium hawaiians no ham, thick crust"],
                [rm("ham", "no ham"), add("crust_thick", "thick crust")],
            )
        ],
        time=("clock_time", "at 8", "20:00"),
        day=("weekday", "fri", "friday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0180",
        """
c: WHAT FLAVORS OF SHAKES DO YOU HAVE
b: Vanilla, chocolate or strawberry.
c: CHOCOLATE ONE AND A REGULAR FRY AT 7, CASH
""",
        "Q P",
        items=[
            I("milkshake", 1, "chocolate", ["CHOCOLATE ONE"]),
            I("fries", 1, "regular", ["A REGULAR FRY"]),
        ],
        time=("clock_time", "AT 7", "19:00"),
        pay="cash",
        pay_q="CASH",
    ),
]
