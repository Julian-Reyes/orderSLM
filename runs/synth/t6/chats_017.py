"""t6 entries 0161–0170 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0161",
        """
c: hey
c: 6 small americanos, 4 of em w hazelnut
c: a breakfast sandwich w tomato n a sesame bagel
c: 3 large hot chocolates w caramel
c: pickup for june, card
""",
        "S P P P P",
        items=[
            I("americano", 2, "small", ["6 small americanos"]),
            I(
                "americano",
                4,
                "small",
                ["6 small americanos", "4 of em w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich w tomato"], [add("tomato", "w tomato")]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
            I(
                "hot_chocolate",
                3,
                "large",
                ["3 large hot chocolates w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t6-0162",
        """
c: Hi, can I get a Coke delivered tomorrow at 1:30? I'll pay cash.
""",
        "P",
        items=[I("coke", 1, None, ["a Coke"])],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 1:30", "13:30"),
        day=("tomorrow", "tomorrow"),
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t6-0163",
        """
c: 2 large supremes no sauce n 2 large hawaiians
c: 4 cans of iced tea n the usual
c: deliver to 256 cedar hill rd unit 26a
""",
        "P P P",
        items=[
            I("supreme_pizza", 2, "large", ["2 large supremes no sauce"], [rm("tomato_sauce", "no sauce")]),
            I("hawaiian_pizza", 2, "large", ["2 large hawaiians"]),
            I("iced_tea", 4, "can", ["4 cans of iced tea"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="deliver to 256 cedar hill rd",
        addr={
            "raw": "256 cedar hill rd unit 26a",
            "number": "256",
            "street": "cedar hill rd",
            "unit": "unit 26a",
        },
    ),
    X(
        "syn-t6-0164",
        """
c: 3 personal meat lovers no cheese thick crust
c: 3 personal margheritas
c: a diet coke n one of those
c: pickup
""",
        "P P P P",
        items=[
            I(
                "meat_lovers_pizza",
                3,
                "personal",
                ["3 personal meat lovers no cheese thick crust"],
                [rm("cheese", "no cheese"), add("crust_thick", "thick crust")],
            ),
            I("margherita_pizza", 3, "personal", ["3 personal margheritas"]),
            I("diet_coke", 1, None, ["a diet coke"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t6-0165",
        """
c: do u have oat milk?
b: Yes, oat milk and almond milk.
c: ok a small latte w oat milk, a hot chocolate, a banana nut muffin n the one i always get
c: pickup at 10 for marcus
""",
        "Q P P",
        items=[
            I(
                "latte",
                1,
                "small",
                ["a small latte w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10", "10:00"),
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t6-0166",
        """
c: hey
c: medium hot chocolate asap for pickup, dev, card
c: actually swap that for 2 large cappuccinos
""",
        "S P M",
        items=[I("cappuccino", 2, "large", ["swap that for 2 large cappuccinos"])],
        method="pickup",
        method_q="for pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0167",
        """
c: Good morning!
c: Hump day already, can you believe it?
c: I'd like 2 small lattes.
c: With caramel and skim milk, please.
c: I'll pay by card.
""",
        "S S P P P",
        items=[
            I(
                "latte",
                2,
                "small",
                ["2 small lattes", "With caramel and skim milk"],
                [add("caramel_syrup", "With caramel"), sub("whole_milk", "skim_milk", "skim milk")],
            )
        ],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0168",
        """
c: 3 medium caps
c: w hazelnut
c: n almond milk
c: for 1pm
c: actually make it saturday at 9 instead
""",
        "P P P P M",
        items=[
            I(
                "cappuccino",
                3,
                "medium",
                ["3 medium caps", "w hazelnut", "n almond milk"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "almond_milk", "almond milk")],
            )
        ],
        time=("clock_time", "at 9", "09:00"),
        day=("weekday", "sat", "saturday"),
    ),
    X(
        "syn-t6-0169",
        """
c: Hello.
c: I'd like to place a small order for tomorrow.
c: Just one Coke.
c: At 12:15.
c: I'll pay by card.
""",
        "S P P P P",
        items=[I("coke", 1, None, ["one Coke"])],
        time=("clock_time", "At 12:15", "12:15"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0170",
        """
c: whats in the coffee n pastry deal?
b: A drip coffee, latte or americano with a croissant or a muffin.
c: ok one deal w a drip coffee n a blueberry muffin, plus 2 plain bagels n 2 choc chip muffins. pickup at 11 for grace, cash
""",
        "Q P",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["one deal w a drip coffee n a blueberry muffin"],
                combo={"drink": "drip_coffee", "pastry": ("muffin", "blueberry")},
            ),
            I("bagel", 2, "plain", ["2 plain bagels"]),
            I("muffin", 2, "chocolate_chip", ["2 choc chip muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 11", "11:00"),
        pay="cash",
        pay_q="cash",
        name="Grace",
        name_q="grace",
    ),
]
