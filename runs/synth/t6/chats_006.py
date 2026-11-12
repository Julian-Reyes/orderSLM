"""t6 entries 0051–0060 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0051",
        """
c: Hi, I'd like 2 large americanos and a banana nut muffin for pickup. Name is Ben.
c: I'll pay by card.
c: Actually, instead of the americanos, could I get 3 croissants with butter?
""",
        "P P M",
        items=[
            I("croissant", 3, None, ["3 croissants with butter"], [add("butter", "with butter")]),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="pay by card",
        name="Ben",
    ),
    X(
        "syn-t6-0052",
        """
c: hey can i get 2 medium veggie pizzas w jalapenos
c: for pickup tmrw
c: name rosa
""",
        "P P P",
        items=[
            I(
                "veggie_pizza",
                2,
                "medium",
                ["2 medium veggie pizzas w jalapenos"],
                [add("jalapenos", "w jalapenos")],
            )
        ],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "tmrw"),
        day=("tomorrow", "tmrw"),
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0053",
        """
c: hi can i get a large cocoa w vanilla n oat milk + 3 house coffees
c: pickup for june, paying cash
""",
        "P P",
        items=[
            I(
                "hot_chocolate",
                1,
                "large",
                ["a large cocoa w vanilla n oat milk"],
                [add("vanilla_syrup", "w vanilla"), sub("whole_milk", "oat_milk", "oat milk")],
            ),
            I("drip_coffee", 3, None, ["3 house coffees"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="paying cash",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t6-0054",
        """
c: can i grab a banana nut n a medium latte w whip
b: Do you mean a banana nut muffin?
c: yep the muffin. asap for pickup, name ivy
""",
        "P P",
        items=[
            I("muffin", 1, "banana_nut", ["a banana nut", "the muffin"]),
            I("latte", 1, "medium", ["a medium latte w whip"], [add("whipped_cream", "w whip")]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("asap", "asap", None),
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t6-0055",
        """
c: hey 👋 3 cokes pls
c: deliver to 44 brookside ct 🏠
c: card 💳
c: wait no cokes, make it 3 large fries instead 🍟
""",
        "P P P M",
        items=[I("fries", 3, "large", ["make it 3 large fries"])],
        method="delivery",
        method_q="deliver to 44 brookside ct",
        addr={"raw": "44 brookside ct", "number": "44", "street": "brookside ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0056",
        """
c: Hello, I'd like to order for Saturday evening.
c: An extra large margherita with stuffed crust.
c: A 20 oz Sprite and a 2 liter Dr Pepper.
c: Delivered to 229 Bayview St at 6:30.
c: I'll pay cash and need change for a 50.
""",
        "P P P P P",
        items=[
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["An extra large margherita with stuffed crust"],
                [add("crust_stuffed", "with stuffed crust")],
            ),
            I("sprite", 1, "bottle_20oz", ["A 20 oz Sprite"]),
            I("dr_pepper", 1, "two_liter", ["a 2 liter Dr Pepper"]),
        ],
        method="delivery",
        method_q="Delivered to 229 Bayview St",
        time=("clock_time", "at 6:30", "18:30"),
        day=("weekday", "sat", "Saturday"),
        addr={"raw": "229 Bayview St", "number": "229", "street": "Bayview St"},
        pay="cash",
        pay_q=["pay cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t6-0057",
        """
c: 3 small caps w almond milk
c: tmrw at 7:15
c: card
""",
        "P P P",
        items=[
            I(
                "cappuccino",
                3,
                "small",
                ["3 small caps w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            )
        ],
        time=("clock_time", "at 7:15", "07:15"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0058",
        """
c: hey can i get a cheeseburger no cheese for pickup at 6, name ben, cash
c: lol yes i know a cheeseburger w no cheese
c: actually make it thursday at 6 not today
""",
        "P S M",
        items=[I("cheeseburger", 1, None, ["a cheeseburger no cheese"], [rm("cheese", "no cheese")])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "thu", "thursday"),
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0059",
        """
c: can i get a few medium veggie pizzas delivered? 🍕 paying card 💳
""",
        "P",
        items=[I("veggie_pizza", None, "medium", ["a few medium veggie pizzas"])],
        method="delivery",
        method_q="delivered",
        pay="card",
        pay_q="paying card",
    ),
    X(
        "syn-t6-0060",
        """
c: ugh long thursday
c: 2 bacon burgers pls
c: deliver to 856 juniper st
c: cash
c: thank u
""",
        "S P P P S",
        items=[I("bacon_burger", 2, None, ["2 bacon burgers"])],
        method="delivery",
        method_q="deliver to 856 juniper st",
        addr={"raw": "856 juniper st", "number": "856", "street": "juniper st"},
        pay="cash",
        pay_q="cash",
    ),
]
