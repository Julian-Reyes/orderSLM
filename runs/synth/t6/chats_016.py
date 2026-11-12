"""t6 entries 0151–0160 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0151",
        """
c: hi ☀️ can i get a bacon egg n cheese on a croissant + 4 cocoas
c: pickup at 9 for ben 🙂
c: card 💳
""",
        "P P P",
        items=[
            I("breakfast_sandwich", 1, "croissant", ["a bacon egg n cheese on a croissant"]),
            I("hot_chocolate", 4, None, ["4 cocoas"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0152",
        """
c: the usual pls
b: Sorry, I can't see past orders here. What would you like?
c: 2 veggie burgers
c: 3 regular fries n 2 orders of onion rings
c: 2 strawberry shakes + a single cheeseburger
c: deliver to 2562 mission pl, cash, change for a 100
""",
        "P P P P P",
        items=[
            I("veggie_burger", 2, None, ["2 veggie burgers"]),
            I("fries", 3, "regular", ["3 regular fries"]),
            I("onion_rings", 2, None, ["2 orders of onion rings"]),
            I("milkshake", 2, "strawberry", ["2 strawberry shakes"]),
            I("cheeseburger", 1, "single", ["a single cheeseburger"]),
        ],
        method="delivery",
        method_q="deliver to 2562 mission pl",
        addr={"raw": "2562 mission pl", "number": "2562", "street": "mission pl"},
        pay="cash",
        pay_q=["cash", "change for a 100"],
        change=10000,
    ),
    X(
        "syn-t6-0153",
        """
c: hey can i get 2 croissants w butter, a breakfast sandwich on an english muffin no cheddar
c: a small americano w hazelnut, a small latte w vanilla, a blueberry muffin n 3 coffees
c: pickup for keisha, paying cash, change for a 50
""",
        "P P P",
        items=[
            I("croissant", 2, None, ["2 croissants w butter"], [add("butter", "w butter")]),
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["a breakfast sandwich on an english muffin no cheddar"],
                [rm("cheddar", "no cheddar")],
            ),
            I(
                "americano",
                1,
                "small",
                ["a small americano w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("latte", 1, "small", ["a small latte w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
            I("drip_coffee", 3, None, ["3 coffees"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["paying cash", "change for a 50"],
        change=5000,
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t6-0154",
        """
c: hi
c: 3 xl hawaiians
c: no cheese on them
c: add red onions
c: pickup in 30 min
c: card
c: wait actually forget the hawaiians, just a personal cheese pizza w ground beef
""",
        "S P P P P P M",
        items=[
            I(
                "cheese_pizza",
                1,
                "personal",
                ["a personal cheese pizza w ground beef"],
                [add("beef", "w ground beef")],
            )
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 30 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0155",
        """
c: DO YOU HAVE A MEAL DEAL?
b: No meal deals, sorry. Everything is ordered on its own.
c: FINE, AN ORDER OF BREADSTICKS AND A 20 OZ DIET COKE FOR PICKUP, CARD
""",
        "Q P",
        items=[
            I("breadsticks", 1, None, ["AN ORDER OF BREADSTICKS"]),
            I("diet_coke", 1, "bottle_20oz", ["A 20 OZ DIET COKE"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0156",
        """
c: hey 🍔
c: 2 bacon burgers no cheese
c: + 2 sprites 🥤
c: its for monday lunch, pickup
c: ivy, card 💳
""",
        "S P P P P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers no cheese"], [rm("cheese", "no cheese")]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "monday lunch"),
        day=("weekday", "mon", "monday"),
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t6-0157",
        """
c: can i get a dr pepper for pickup tmrw at 1 🥤
c: name maya, cash 💵
c: actually nvm can i grab it today at 4 instead
""",
        "P P M",
        items=[I("dr_pepper", 1, None, ["a dr pepper"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 4", "16:00"),
        pay="cash",
        pay_q="cash",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t6-0158",
        """
c: A SMALL COFFEE AND A BLUEBERRY MUFFIN
c: AND 2 SMALL HOT CHOCOLATES NO WHIPPED CREAM WITH HAZELNUT
c: IN 20 MINUTES, PAYING CASH
b: Got it! Is this for pickup, and what name should it be under?
c: ACTUALLY NO HOT CHOCOLATES
""",
        "P P P M",
        items=[
            I("drip_coffee", 1, "small", ["A SMALL COFFEE"]),
            I("muffin", 1, "blueberry", ["A BLUEBERRY MUFFIN"]),
        ],
        time=("relative", "IN 20 MINUTES", None),
        pay="cash",
        pay_q="PAYING CASH",
    ),
    X(
        "syn-t6-0159",
        """
c: DO YOU HAVE HAZELNUT SYRUP?
b: Yes, we do!
c: GREAT. A CAPPUCCINO WITH HAZELNUT AND A BREAKFAST SANDWICH ON AN ENGLISH MUFFIN, NO BACON, ADD TOMATO
c: FOR PICKUP TOMORROW AT 8, NAME IS ROSA
""",
        "Q P P",
        items=[
            I(
                "cappuccino",
                1,
                None,
                ["A CAPPUCCINO WITH HAZELNUT"],
                [add("hazelnut_syrup", "WITH HAZELNUT")],
            ),
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["A BREAKFAST SANDWICH ON AN ENGLISH MUFFIN, NO BACON, ADD TOMATO"],
                [rm("bacon", "NO BACON"), add("tomato", "ADD TOMATO")],
            ),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        time=("clock_time", "AT 8", "08:00"),
        day=("tomorrow", "TOMORROW"),
        name="Rosa",
        name_q="ROSA",
    ),
    X(
        "syn-t6-0160",
        """
c: can i get an order of french fries delivered to 190 union way apt 11a
c: card
""",
        "P P",
        items=[I("fries", 1, None, ["an order of french fries"])],
        method="delivery",
        method_q="delivered to 190 union way",
        addr={"raw": "190 union way apt 11a", "number": "190", "street": "union way", "unit": "apt 11a"},
        pay="card",
        pay_q="card",
    ),
]
