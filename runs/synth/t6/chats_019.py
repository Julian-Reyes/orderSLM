"""t6 entries 0181–0190 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t6-0181",
        """
c: bacon burger
c: w coleslaw on it
c: deliver to 877 delancey terrace
c: at 9
c: card
""",
        "P P P P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger", "w coleslaw on it"], [offmod("w coleslaw on it")])
        ],
        method="delivery",
        method_q="deliver to 877 delancey terrace",
        time=("clock_time", "at 9", "21:00"),
        addr={"raw": "877 delancey terrace", "number": "877", "street": "delancey terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0182",
        """
c: same as last time pls
b: Sorry, I can't see past orders here. What would you like?
c: 4 sesame bagels
c: 2 medium caps w skim
c: 2 large americanos w caramel n almond milk
c: 2 small lattes w skim, pickup for keisha
""",
        "P P P P P",
        items=[
            I("bagel", 4, "sesame", ["4 sesame bagels"]),
            I(
                "cappuccino",
                2,
                "medium",
                ["2 medium caps w skim"],
                [sub("whole_milk", "skim_milk", "w skim")],
            ),
            I(
                "americano",
                2,
                "large",
                ["2 large americanos w caramel n almond milk"],
                [add("caramel_syrup", "w caramel"), add("almond_milk", "almond milk")],
            ),
            I("latte", 2, "small", ["2 small lattes w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t6-0183",
        """
c: ugh mondays 😩
c: are ur onion rings crispy?
b: We can make them extra crispy if you like!
c: ok 2 cheeseburgers no onions + an order of onion rings, pickup for tom 🙏
""",
        "S Q P",
        items=[
            I("cheeseburger", 2, None, ["2 cheeseburgers no onions"], [rm("onion", "no onions")]),
            I("onion_rings", 1, None, ["an order of onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t6-0184",
        """
c: hey
c: 2 small margheritas no olive oil
c: 2 waters
c: deliver to 75 dover ave
c: card
c: oh can u make it tomorrow at 6:30 instead of now
""",
        "S P P P P M",
        items=[
            I(
                "margherita_pizza",
                2,
                "small",
                ["2 small margheritas no olive oil"],
                [rm("olive_oil", "no olive oil")],
            ),
            I("water", 2, None, ["2 waters"]),
        ],
        method="delivery",
        method_q="deliver to 75 dover ave",
        time=("clock_time", "at 6:30", "18:30"),
        day=("tomorrow", "tomorrow"),
        addr={"raw": "75 dover ave", "number": "75", "street": "dover ave"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0185",
        """
c: Hi, I'd like a cheeseburger combo with onion rings and a Coke.
c: And one extra lemonade on the side.
c: Delivery to 40 Prospect Ct, apt 24C. Cash, I'll need change for a 50.
""",
        "P P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["a cheeseburger combo with onion rings and a Coke"],
                combo={"side": "onion_rings", "drink": "coke"},
            ),
            I("lemonade", 1, None, ["one extra lemonade"]),
        ],
        method="delivery",
        method_q="Delivery to 40 Prospect Ct",
        addr={"raw": "40 Prospect Ct, apt 24C", "number": "40", "street": "Prospect Ct", "unit": "apt 24C"},
        pay="cash",
        pay_q=["Cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t6-0186",
        """
c: can i get 2 coffee n pastry deals w a medium americano n a croissant each, plus a blueberry muffin, pickup for dev
""",
        "P",
        items=[
            I(
                "coffee_pastry_combo",
                2,
                None,
                ["2 coffee n pastry deals w a medium americano n a croissant each"],
                combo={"drink": ("americano", "medium"), "pastry": "croissant"},
            ),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0187",
        """
c: r u open on tuesdays? 🤔
b: Yes, we're open every day from 11 am to 10 pm.
c: cool 😎 then a coke for pickup tuesday at 5
""",
        "D P",
        items=[I("coke", 1, None, ["a coke"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 5", "17:00"),
        day=("weekday", "tue", "tuesday"),
    ),
    X(
        "syn-t6-0188",
        """
c: Good morning.
c: Two hot chocolates without whipped cream for Friday at 9:30, please.
c: Pickup under Priya, paying by card.
""",
        "S P P",
        items=[
            I(
                "hot_chocolate",
                2,
                None,
                ["Two hot chocolates without whipped cream"],
                [rm("whipped_cream", "without whipped cream")],
            )
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 9:30", "09:30"),
        day=("weekday", "fri", "Friday"),
        pay="card",
        pay_q="paying by card",
        name="Priya",
    ),
    X(
        "syn-t6-0189",
        """
c: hiii ☀️
c: a medium latte w whipped cream n a medium hot chocolate w almond milk for sunday 🙏
c: cash, change for a 20 💵
""",
        "S P P",
        items=[
            I(
                "latte",
                1,
                "medium",
                ["a medium latte w whipped cream"],
                [add("whipped_cream", "w whipped cream")],
            ),
            I(
                "hot_chocolate",
                1,
                "medium",
                ["a medium hot chocolate w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
        ],
        time=("ambiguous", "for sunday"),
        day=("weekday", "sun", "sunday"),
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t6-0190",
        """
c: Is your lemonade homemade?
b: Sorry, I can't confirm that here.
c: Okay. Two lemonades and a veggie burger with no tomato, topped with chili, in about 30 minutes. I'll pay cash.
""",
        "Q P",
        items=[
            I("lemonade", 2, None, ["Two lemonades"]),
            I(
                "veggie_burger",
                1,
                None,
                ["a veggie burger with no tomato, topped with chili"],
                [rm("tomato", "with no tomato"), offmod("topped with chili")],
            ),
        ],
        time=("relative", "in about 30 minutes", None),
        pay="cash",
        pay_q="pay cash",
    ),
]
