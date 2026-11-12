"""t6 entries 0011–0020 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0011",
        """
c: CAN I GET SOME SMALL LATTES WITH HAZELNUT AND SKIM MILK
c: AND 2 CHOCOLATE CHIP MUFFINS
c: PAYING CASH
""",
        "P P P",
        items=[
            I(
                "latte",
                None,
                "small",
                ["SOME SMALL LATTES WITH HAZELNUT AND SKIM MILK"],
                [add("hazelnut_syrup", "WITH HAZELNUT"), sub("whole_milk", "skim_milk", "SKIM MILK")],
            ),
            I("muffin", 2, "chocolate_chip", ["2 CHOCOLATE CHIP MUFFINS"]),
        ],
        pay="cash",
        pay_q="PAYING CASH",
    ),
    X(
        "syn-t6-0012",
        """
c: hi ☀️ for tomorrow at 9:30 can i get a small cappuccino w almond milk n 2 everything bagels? paying cash, ill need change for a 20 💵
""",
        "P",
        items=[
            I(
                "cappuccino",
                1,
                "small",
                ["a small cappuccino w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
            I("bagel", 2, "everything", ["2 everything bagels"]),
        ],
        time=("clock_time", "at 9:30", "09:30"),
        day=("tomorrow", "tomorrow"),
        pay="cash",
        pay_q=["paying cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t6-0013",
        """
c: Hello, do you have any pizza combo deals?
b: We don't have combo deals, sorry. Everything is ordered separately.
c: Okay. Then a large pepperoni and 4 iced teas. Deliver to 39 Sycamore Blvd, apt 10B. I'll pay by card.
""",
        "Q P",
        items=[
            I("pepperoni_pizza", 1, "large", ["a large pepperoni"]),
            I("iced_tea", 4, None, ["4 iced teas"]),
        ],
        method="delivery",
        method_q="Deliver to 39 Sycamore Blvd",
        addr={
            "raw": "39 Sycamore Blvd, apt 10B",
            "number": "39",
            "street": "Sycamore Blvd",
            "unit": "apt 10B",
        },
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0014",
        """
c: hii 🍔
c: 4 double cheeseburgers pls
c: 3 of them no tomato 🍅🚫
c: n 3 orders of onion rings
c: pickup 🚗
c: card 💳
""",
        "S P P P P P",
        items=[
            I("cheeseburger", 1, "double", ["4 double cheeseburgers"]),
            I(
                "cheeseburger",
                3,
                "double",
                ["4 double cheeseburgers", "3 of them no tomato"],
                [rm("tomato", "no tomato")],
            ),
            I("onion_rings", 3, None, ["3 orders of onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0015",
        """
c: HI I WANT TO ORDER FOR OCTOBER 30TH
c: 2 REGULAR FRIES AND A LEMONADE, PICKUP AT 12:30
c: CARD
""",
        "P P P",
        items=[
            I("fries", 2, "regular", ["2 REGULAR FRIES"]),
            I("lemonade", 1, None, ["A LEMONADE"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 12:30", "12:30"),
        day=("date", 10, 30, "OCTOBER 30TH"),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0016",
        """
c: hey can i put in an order for thursday
c: a medium americano
c: n 3 cinnamon raisin bagels w tomato
c: pickup, name eli, card
""",
        "P P P P",
        items=[
            I("americano", 1, "medium", ["a medium americano"]),
            I(
                "bagel",
                3,
                "cinnamon_raisin",
                ["3 cinnamon raisin bagels w tomato"],
                [add("tomato", "w tomato")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for thursday"),
        day=("weekday", "thu", "thursday"),
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t6-0017",
        """
c: yo
c: 1 breakfast sandwich
c: for tmrw
c: 7:45
c: pickup, sam, card
""",
        "S P P P P",
        items=[I("breakfast_sandwich", 1, None, ["1 breakfast sandwich"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "7:45", "07:45"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t6-0018",
        """
c: Hello, I'd like to order a hot chocolate with vanilla for pickup on Wednesday at 10:15. The name is Eli and I'll pay by card.
""",
        "P",
        items=[
            I(
                "hot_chocolate",
                1,
                None,
                ["a hot chocolate with vanilla"],
                [add("vanilla_syrup", "with vanilla")],
            )
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 10:15", "10:15"),
        day=("weekday", "wed", "Wednesday"),
        pay="card",
        pay_q="pay by card",
        name="Eli",
    ),
    X(
        "syn-t6-0019",
        """
c: hi can i get 3 muffins for pickup, name luis
c: paying cash, have a 20
""",
        "P P",
        items=[I("muffin", 3, None, ["3 muffins"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q=["paying cash", "have a 20"],
        change=2000,
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t6-0020",
        """
c: lazy sunday lol
c: need food asap
c: 2 veggie burgers
c: pickup
c: card
c: thx
""",
        "S P P P P S",
        items=[I("veggie_burger", 2, None, ["2 veggie burgers"])],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
]
