"""t6 entries 0061–0070 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0061",
        """
c: hey
c: any deals?
b: No deals right now, sorry. Everything is ordered on its own.
c: ok 2 orders of breadsticks n a medium cheese pizza
c: deliver to 8443 riverside terrace at 7
c: cash, change for a 50
""",
        "S Q P P P",
        items=[
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I("cheese_pizza", 1, "medium", ["a medium cheese pizza"]),
        ],
        method="delivery",
        method_q="deliver to 8443 riverside terrace",
        time=("clock_time", "at 7", "19:00"),
        addr={"raw": "8443 riverside terrace", "number": "8443", "street": "riverside terrace"},
        pay="cash",
        pay_q=["cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t6-0062",
        """
c: hi ☀️
c: 4 croissants, 3 of them w butter 🧈 + a sesame bagel
c: pickup for dev, card 💳
""",
        "S P P",
        items=[
            I("croissant", 1, None, ["4 croissants"]),
            I("croissant", 3, None, ["4 croissants", "3 of them w butter"], [add("butter", "w butter")]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0063",
        """
c: hey for tmrw at 8 can i get a small latte w hazelnut n oat milk, a banana nut muffin n 2 large coffees w caramel, pickup for rosa, paying cash w a 20
""",
        "P",
        items=[
            I(
                "latte",
                1,
                "small",
                ["a small latte w hazelnut n oat milk"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "oat_milk", "oat milk")],
            ),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
            I("drip_coffee", 2, "large", ["2 large coffees w caramel"], [add("caramel_syrup", "w caramel")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "08:00"),
        day=("tomorrow", "tmrw"),
        pay="cash",
        pay_q=["paying cash", "w a 20"],
        change=2000,
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0064",
        """
c: hi! 4 breakfast sandwiches n 3 small cappuccinos w skim milk 🥪☕
c: + a croissant, paying card 💳
b: Got it! Is this for pickup, and what name should I put it under?
c: oh actually skip the croissant 🙏
""",
        "P P M",
        items=[
            I("breakfast_sandwich", 4, None, ["4 breakfast sandwiches"]),
            I(
                "cappuccino",
                3,
                "small",
                ["3 small cappuccinos w skim milk"],
                [sub("whole_milk", "skim_milk", "w skim milk")],
            ),
        ],
        pay="card",
        pay_q="paying card",
    ),
    X(
        "syn-t6-0065",
        """
c: hey 👋 can i order for monday
c: a hot chocolate, a croissant n 2 large coffees ☕
""",
        "P P",
        items=[
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
            I("croissant", 1, None, ["a croissant"]),
            I("drip_coffee", 2, "large", ["2 large coffees"]),
        ],
        time=("ambiguous", "for monday"),
        day=("weekday", "mon", "monday"),
    ),
    X(
        "syn-t6-0066",
        """
c: can i get a sprite delivered tmrw at noon to 794 sunset pl, next to the laundromat 🥤
""",
        "P",
        items=[I("sprite", 1, None, ["a sprite"])],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at noon", "12:00"),
        day=("tomorrow", "tmrw"),
        addr={
            "raw": "794 sunset pl, next to the laundromat",
            "number": "794",
            "street": "sunset pl",
            "reference": "next to the laundromat",
        },
    ),
    X(
        "syn-t6-0067",
        """
c: hey 🍕 can i get some meat lovers, no ham but add grilled chicken
c: deliver to 53 thornton way unit 13a
c: card 💳
""",
        "P P P",
        items=[
            I(
                "meat_lovers_pizza",
                None,
                None,
                ["some meat lovers, no ham but add grilled chicken"],
                [rm("ham", "no ham"), add("grilled_chicken", "add grilled chicken")],
            )
        ],
        method="delivery",
        method_q="deliver to 53 thornton way",
        addr={
            "raw": "53 thornton way unit 13a",
            "number": "53",
            "street": "thornton way",
            "unit": "unit 13a",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0068",
        """
c: hi!
c: a personal pepperoni w grilled chicken n a large margherita
c: 2 small veggie pizzas w bbq sauce n thick crust
c: 2 cokes n a 20 oz iced tea
c: pickup at 6:30, name ana, card
""",
        "S P P P P",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "personal",
                ["a personal pepperoni w grilled chicken"],
                [add("grilled_chicken", "w grilled chicken")],
            ),
            I("margherita_pizza", 1, "large", ["a large margherita"]),
            I(
                "veggie_pizza",
                2,
                "small",
                ["2 small veggie pizzas w bbq sauce n thick crust"],
                [add("bbq_sauce", "w bbq sauce"), add("crust_thick", "thick crust")],
            ),
            I("coke", 2, None, ["2 cokes"]),
            I("iced_tea", 1, "bottle_20oz", ["a 20 oz iced tea"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 6:30", "18:30"),
        pay="card",
        pay_q="card",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t6-0069",
        """
c: CAN I GET SOME CHOCOLATE CHIP MUFFINS
c: AND 3 HOT CHOCOLATES WITH ALMOND MILK AND 3 MEDIUM CAPPUCCINOS WITH VANILLA AND OAT MILK
c: IN ABOUT 20 MINUTES
""",
        "P P P",
        items=[
            I("muffin", None, "chocolate_chip", ["SOME CHOCOLATE CHIP MUFFINS"]),
            I(
                "hot_chocolate",
                3,
                None,
                ["3 HOT CHOCOLATES WITH ALMOND MILK"],
                [sub("whole_milk", "almond_milk", "WITH ALMOND MILK")],
            ),
            I(
                "cappuccino",
                3,
                "medium",
                ["3 MEDIUM CAPPUCCINOS WITH VANILLA AND OAT MILK"],
                [add("vanilla_syrup", "WITH VANILLA"), sub("whole_milk", "oat_milk", "OAT MILK")],
            ),
        ],
        time=("relative", "IN ABOUT 20 MINUTES", None),
    ),
    X(
        "syn-t6-0070",
        """
c: 2 small americanos for fri at 9
c: actually nvm friday, can i get them today asap
""",
        "P M",
        items=[I("americano", 2, "small", ["2 small americanos"])],
        time=("asap", "asap", None),
    ),
]
