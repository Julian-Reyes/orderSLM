"""t6 entries 0081–0090 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0081",
        """
c: veggie burger no tomato w mustard n same as last time for my bf 🍔 paying cash 💵
""",
        "P",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["veggie burger no tomato w mustard"],
                [rm("tomato", "no tomato"), add("mustard", "w mustard")],
            ),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t6-0082",
        """
c: Hi, could I get 2 BBQ chicken pizzas with pepperoni added at 7:15? I'll pay cash with a 50.
""",
        "P",
        items=[
            I(
                "bbq_chicken_pizza",
                2,
                None,
                ["2 BBQ chicken pizzas with pepperoni added"],
                [add("pepperoni", "with pepperoni added")],
            )
        ],
        time=("clock_time", "at 7:15", "19:15"),
        pay="cash",
        pay_q=["pay cash", "with a 50"],
        change=5000,
    ),
    X(
        "syn-t6-0083",
        """
c: HI
c: 6 VEGGIE BURGERS, 3 OF THEM WITH CHEESE
c: AND A CHEESEBURGER NO TOMATO WITH MUSTARD
c: DELIVER TO 9694 FRANKLIN CT
c: AT 7:30
c: CARD
""",
        "S P P P P P",
        items=[
            I("veggie_burger", 3, None, ["6 VEGGIE BURGERS"]),
            I(
                "veggie_burger",
                3,
                None,
                ["6 VEGGIE BURGERS", "3 OF THEM WITH CHEESE"],
                [add("cheese", "WITH CHEESE")],
            ),
            I(
                "cheeseburger",
                1,
                None,
                ["A CHEESEBURGER NO TOMATO WITH MUSTARD"],
                [rm("tomato", "NO TOMATO"), add("mustard", "WITH MUSTARD")],
            ),
        ],
        method="delivery",
        method_q="DELIVER TO 9694 FRANKLIN CT",
        time=("clock_time", "AT 7:30", "19:30"),
        addr={"raw": "9694 FRANKLIN CT", "number": "9694", "street": "FRANKLIN CT"},
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0084",
        """
c: can i get some sprites
c: cash
""",
        "P P",
        items=[I("sprite", None, None, ["some sprites"])],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0085",
        """
c: hey can i get a combo w onion rings n a coke
c: plus a double cheeseburger on its own
c: deliver to 223 cedar hill rd, card
""",
        "P P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["a combo w onion rings n a coke"],
                combo={"side": "onion_rings", "drink": "coke"},
            ),
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
        ],
        method="delivery",
        method_q="deliver to 223 cedar hill rd",
        addr={"raw": "223 cedar hill rd", "number": "223", "street": "cedar hill rd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0086",
        """
c: hey wanna order for tmrw lunch
c: a double cheeseburger n 2 sprites
c: pickup at 12:15 for sam, card
""",
        "P P P",
        items=[
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:15", "12:15"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t6-0087",
        """
c: hi can i set up an order for tomorrow
c: a medium coffee
c: n 2 breakfast sandwiches on a bagel no bacon
c: pickup at 7 for rosa
""",
        "P P P P",
        items=[
            I("drip_coffee", 1, "medium", ["a medium coffee"]),
            I(
                "breakfast_sandwich",
                2,
                "bagel",
                ["2 breakfast sandwiches on a bagel no bacon"],
                [rm("bacon", "no bacon")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "07:00"),
        day=("tomorrow", "tomorrow"),
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0088",
        """
c: hey can i get a strawberry shake, a single cheeseburger n a sprite delivered saturday at 8 to 7674 ivanhoe st
c: thx
""",
        "P S",
        items=[
            I("milkshake", 1, "strawberry", ["a strawberry shake"]),
            I("cheeseburger", 1, "single", ["a single cheeseburger"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 8", "20:00"),
        day=("weekday", "sat", "saturday"),
        addr={"raw": "7674 ivanhoe st", "number": "7674", "street": "ivanhoe st"},
    ),
    X(
        "syn-t6-0089",
        """
c: hi just need a coke for pickup tmrw
c: at 1:30
c: june, card
""",
        "P P P",
        items=[I("coke", 1, None, ["a coke"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 1:30", "13:30"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t6-0090",
        """
c: weird one but 3 xl pepperoni pizzas with no pepperoni n bbq sauce added lol
c: pickup thurs at 5:45
""",
        "P P",
        items=[
            I(
                "pepperoni_pizza",
                3,
                "extra_large",
                ["3 xl pepperoni pizzas with no pepperoni n bbq sauce added"],
                [rm("pepperoni", "no pepperoni"), add("bbq_sauce", "bbq sauce added")],
            )
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 5:45", "17:45"),
        day=("weekday", "thu", "thurs"),
    ),
]
