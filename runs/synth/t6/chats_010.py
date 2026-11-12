"""t6 entries 0091–0100 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0091",
        """
c: hey 🍕 a pepperoni pizza n that thing from before
c: deliver to 93 clement ct #14c
c: card 💳
""",
        "P P P",
        items=[
            I("pepperoni_pizza", 1, None, ["a pepperoni pizza"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="deliver to 93 clement ct #14c",
        addr={"raw": "93 clement ct #14c", "number": "93", "street": "clement ct", "unit": "#14c"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0092",
        """
c: hey
c: 2 small margheritas w spinach, thick crust
c: n 2 large bbq chicken, no bbq sauce on those
c: for pickup tomorrow
c: at 5:30
""",
        "S P P P P",
        items=[
            I(
                "margherita_pizza",
                2,
                "small",
                ["2 small margheritas w spinach, thick crust"],
                [add("spinach", "w spinach"), add("crust_thick", "thick crust")],
            ),
            I(
                "bbq_chicken_pizza",
                2,
                "large",
                ["2 large bbq chicken, no bbq sauce"],
                [rm("bbq_sauce", "no bbq sauce")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 5:30", "17:30"),
        day=("tomorrow", "tomorrow"),
    ),
    X(
        "syn-t6-0093",
        """
c: HELLO
c: ONE VEGGIE BURGER NO PICKLES
c: DELIVERED TO 83 DELANCEY RD TOMORROW AT 1:15
""",
        "S P P",
        items=[I("veggie_burger", 1, None, ["ONE VEGGIE BURGER NO PICKLES"], [rm("pickle", "NO PICKLES")])],
        method="delivery",
        method_q="DELIVERED TO 83 DELANCEY RD",
        time=("clock_time", "AT 1:15", "13:15"),
        day=("tomorrow", "TOMORROW"),
        addr={"raw": "83 DELANCEY RD", "number": "83", "street": "DELANCEY RD"},
    ),
    X(
        "syn-t6-0094",
        """
c: can i get a medium meat lovers for pickup on tuesday
c: at 6:45
c: leah, card
""",
        "P P P",
        items=[I("meat_lovers_pizza", 1, "medium", ["a medium meat lovers"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6:45", "18:45"),
        day=("weekday", "tue", "tuesday"),
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t6-0095",
        """
c: Hi, does the veggie burger come with pickles?
b: Yes, it comes with lettuce, tomato, onion, pickles and mayo.
c: Okay, then 2 veggie burgers without pickles, please.
c: It's for Thursday, delivered to 812 Ivanhoe Ave.
""",
        "Q P P",
        items=[
            I(
                "veggie_burger",
                2,
                None,
                ["2 veggie burgers without pickles"],
                [rm("pickle", "without pickles")],
            )
        ],
        method="delivery",
        method_q="delivered to 812 Ivanhoe Ave",
        time=("ambiguous", "for Thursday"),
        day=("weekday", "thu", "Thursday"),
        addr={"raw": "812 Ivanhoe Ave", "number": "812", "street": "Ivanhoe Ave"},
    ),
    X(
        "syn-t6-0096",
        """
c: hey
c: 2 milkshakes for tmrw night at 8
c: deliver to 34 fulton blvd
c: cash
""",
        "S P P P",
        items=[I("milkshake", 2, None, ["2 milkshakes"])],
        method="delivery",
        method_q="deliver to 34 fulton blvd",
        time=("clock_time", "at 8", "20:00"),
        day=("tomorrow", "tmrw"),
        addr={"raw": "34 fulton blvd", "number": "34", "street": "fulton blvd"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0097",
        """
c: hey
c: a coffee
c: n the usual
c: asap
c: pickup, ben
""",
        "S P P P P",
        items=[
            I("drip_coffee", 1, None, ["a coffee"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0098",
        """
c: hi 🙂 for tmrw at 7:45 pls
c: a large cappuccino, 2 breakfast sandwiches w tomato n 2 coffees ☕
c: pickup for sam, card 💳
""",
        "P P P",
        items=[
            I("cappuccino", 1, "large", ["a large cappuccino"]),
            I(
                "breakfast_sandwich",
                2,
                None,
                ["2 breakfast sandwiches w tomato"],
                [add("tomato", "w tomato")],
            ),
            I("drip_coffee", 2, None, ["2 coffees"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:45", "07:45"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t6-0099",
        """
c: good morning ☀️
c: is the cocoa made w real chocolate?
b: Yes, our hot chocolate is made with real chocolate.
c: yum 😋 one cocoa then, no whipped cream
""",
        "S Q P",
        items=[
            I(
                "hot_chocolate",
                1,
                None,
                ["one cocoa then, no whipped cream"],
                [rm("whipped_cream", "no whipped cream")],
            )
        ],
    ),
    X(
        "syn-t6-0100",
        """
c: HAPPY WEDNESDAY!!
c: I NEED AN ORDER OF GARLIC KNOTS
c: AND A 2 LITER DR PEPPER
c: DELIVER TO 2507 FRANKLIN WAY
c: THANKS
""",
        "S P P P S",
        items=[
            I("garlic_knots", 1, None, ["AN ORDER OF GARLIC KNOTS"]),
            I("dr_pepper", 1, "two_liter", ["A 2 LITER DR PEPPER"]),
        ],
        method="delivery",
        method_q="DELIVER TO 2507 FRANKLIN WAY",
        addr={"raw": "2507 FRANKLIN WAY", "number": "2507", "street": "FRANKLIN WAY"},
    ),
]
