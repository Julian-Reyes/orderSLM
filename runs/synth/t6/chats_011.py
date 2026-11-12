"""t6 entries 0101–0110 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t6-0101",
        """
c: yo
c: can i order for friday
c: is the iced tea sweetened
b: I can't confirm that here, sorry.
c: ok whatever, an iced tea n a coke
c: card
""",
        "S P Q P P",
        items=[
            I("iced_tea", 1, None, ["an iced tea"]),
            I("coke", 1, None, ["a coke"]),
        ],
        time=("ambiguous", "for friday"),
        day=("weekday", "fri", "friday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0102",
        """
c: a large hawaiian w eggplant pls
c: n a 20 oz diet coke
c: pickup, maya, card
""",
        "P P P",
        items=[
            I("hawaiian_pizza", 1, "large", ["a large hawaiian w eggplant"], [offmod("w eggplant")]),
            I("diet_coke", 1, "bottle_20oz", ["a 20 oz diet coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t6-0103",
        """
c: Hi, I'd like to schedule an order for the 16th at 7 pm: 2 single cheeseburgers.
c: Delivery to 723 Sycamore Pl, and I'll pay by card.
""",
        "P P",
        items=[I("cheeseburger", 2, "single", ["2 single cheeseburgers"])],
        method="delivery",
        method_q="Delivery to 723 Sycamore Pl",
        time=("clock_time", "at 7 pm", "19:00"),
        day=("date", None, 16, "the 16th"),
        addr={"raw": "723 Sycamore Pl", "number": "723", "street": "Sycamore Pl"},
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0104",
        """
c: hiii
c: can i get a blueberry muffin for monday
c: pickup at 8:30
c: tara, cash
""",
        "S P P P",
        items=[I("muffin", 1, "blueberry", ["a blueberry muffin"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8:30", "08:30"),
        day=("weekday", "mon", "monday"),
        pay="cash",
        pay_q="cash",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t6-0105",
        """
c: hey can i get a medium veggie w bbq sauce
c: its for tomorrow
c: pickup at 12:30
""",
        "P P P",
        items=[
            I("veggie_pizza", 1, "medium", ["a medium veggie w bbq sauce"], [add("bbq_sauce", "w bbq sauce")])
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:30", "12:30"),
        day=("tomorrow", "tomorrow"),
    ),
    X(
        "syn-t6-0106",
        """
c: Hi, two medium veggie pizzas with olive oil, please.
c: For Monday at 7:30, delivered to 54 Cedar Hill Dr.
""",
        "P P",
        items=[
            I(
                "veggie_pizza",
                2,
                "medium",
                ["two medium veggie pizzas with olive oil"],
                [add("olive_oil", "with olive oil")],
            )
        ],
        method="delivery",
        method_q="delivered to 54 Cedar Hill Dr",
        time=("clock_time", "at 7:30", "19:30"),
        day=("weekday", "mon", "Monday"),
        addr={"raw": "54 Cedar Hill Dr", "number": "54", "street": "Cedar Hill Dr"},
    ),
    X(
        "syn-t6-0107",
        """
c: HEY
c: CAN YOU PUT BACON ON A VEGGIE BURGER?
b: Yes, bacon is an add-on for the veggie burger.
c: LOL OK
c: ONE VEGGIE BURGER WITH BACON, NO ONIONS
c: FOR WEDNESDAY
""",
        "S Q S P P",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["ONE VEGGIE BURGER WITH BACON, NO ONIONS"],
                [add("bacon", "WITH BACON"), rm("onion", "NO ONIONS")],
            )
        ],
        time=("ambiguous", "FOR WEDNESDAY"),
        day=("weekday", "wed", "WEDNESDAY"),
    ),
    X(
        "syn-t6-0108",
        """
c: hey 🍓 2 strawberry shakes pls
c: deliver to 231 riverside rd
c: cash 💵
c: actually just 1 shake 🙏
""",
        "P P P M",
        items=[I("milkshake", 1, "strawberry", ["2 strawberry shakes", "just 1 shake"])],
        method="delivery",
        method_q="deliver to 231 riverside rd",
        addr={"raw": "231 riverside rd", "number": "231", "street": "riverside rd"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0109",
        """
c: Hi, a Sprite for pickup at 5:30, please. Name is Eli, paying cash.
b: Got it, Eli: 1 Sprite for pickup at 5:30, paying cash. Is that right?
c: Yes.
c: Actually, swap the Sprite for 3 Cokes.
""",
        "P C M",
        items=[I("coke", 3, None, ["swap the Sprite for 3 Cokes"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 5:30", "17:30"),
        pay="cash",
        pay_q="paying cash",
        name="Eli",
    ),
    X(
        "syn-t6-0110",
        """
c: Hi, I'd like 2 breakfast sandwiches, one of them without egg.
c: Also 2 plain bagels with cream cheese.
c: And 2 banana nut muffins.
c: Pickup at 1:30 for Jordan. Card.
""",
        "P P P P",
        items=[
            I("breakfast_sandwich", 1, None, ["2 breakfast sandwiches"]),
            I(
                "breakfast_sandwich",
                1,
                None,
                ["2 breakfast sandwiches", "one of them without egg"],
                [rm("egg", "without egg")],
            ),
            I(
                "bagel",
                2,
                "plain",
                ["2 plain bagels with cream cheese"],
                [add("cream_cheese", "with cream cheese")],
            ),
            I("muffin", 2, "banana_nut", ["2 banana nut muffins"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 1:30", "13:30"),
        pay="card",
        pay_q="Card",
        name="Jordan",
    ),
]
