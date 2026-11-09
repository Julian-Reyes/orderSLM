"""t5 entries 0131–0160 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0131",
        """
c: some cans of dr pepper and 2 xl cheese pizzas
c: delivery
""",
        "P P",
        items=[
            I("dr_pepper", None, "can", ["some cans of dr pepper"]),
            I("cheese_pizza", 2, "extra_large", ["2 xl cheese pizzas"]),
        ],
        method="delivery",
        method_q="delivery",
    ),
    X(
        "syn-t5-0132",
        """
c: 2 large americanos w vanilla and a coffee, pickup for leah, cash
c: nvm the coffee
""",
        "P M",
        items=[I("americano", 2, "large", ["2 large americanos"], [add("vanilla_syrup", "w vanilla")])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t5-0133",
        """
c: a 16 oz americano
c: and a breakfast sandwich no cheese add avocado
c: pickup for luis, cash
""",
        "P P P",
        items=[
            I("americano", 1, "large", ["a 16 oz americano"]),
            I(
                "breakfast_sandwich",
                1,
                None,
                ["a breakfast sandwich"],
                [rm("cheddar", "no cheese"), add("avocado", "add avocado")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t5-0134",
        """
c: Could I get a hot chocolate with oat milk and caramel, no whipped cream?
c: Cash, and could it be ready in about 15 minutes?
""",
        "P P",
        items=[
            I(
                "hot_chocolate",
                1,
                None,
                ["a hot chocolate"],
                [
                    sub("whole_milk", "oat_milk", "with oat milk"),
                    add("caramel_syrup", "caramel"),
                    rm("whipped_cream", "no whipped cream"),
                ],
            ),
        ],
        time=("relative", "in about 15 minutes", None),
        pay="cash",
        pay_q="Cash",
    ),
    X(
        "syn-t5-0135",
        """
c: SIX HOT CHOCOLATES PLEASE!
c: ONE WITHOUT WHIPPED CREAM!
c: AND A BREAKFAST SANDWICH ON A CROISSANT, NO BACON!
c: CASH, CHANGE FOR A 20!
""",
        "P P P P",
        items=[
            I("hot_chocolate", 5, None, ["SIX HOT CHOCOLATES"]),
            I(
                "hot_chocolate",
                1,
                None,
                ["SIX HOT CHOCOLATES", "ONE WITHOUT WHIPPED CREAM"],
                [rm("whipped_cream", "WITHOUT WHIPPED CREAM")],
            ),
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["A BREAKFAST SANDWICH ON A CROISSANT"],
                [rm("bacon", "NO BACON")],
            ),
        ],
        pay="cash",
        pay_q=["CASH", "CHANGE FOR A 20"],
        change=2000,
    ),
    X(
        "syn-t5-0136",
        """
c: hey
c: large coffee w caramel n almond milk
c: and a small vanilla latte
c: pickup for eli
b: Large coffee with caramel and almond milk, and a small vanilla latte, pickup for Eli. Right?
c: yep
c: actually no latte
""",
        "S P P P C M",
        items=[
            I(
                "drip_coffee",
                1,
                "large",
                ["large coffee"],
                [add("caramel_syrup", "w caramel"), add("almond_milk", "almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t5-0137",
        """
c: hey 🍕 can we get some bbq chicken pizzas to 2 delancey pl #13b
""",
        "P",
        items=[I("bbq_chicken_pizza", None, None, ["some bbq chicken pizzas"])],
        method="delivery",
        method_q="to 2 delancey pl #13b",
        addr={"raw": "2 delancey pl #13b", "number": "2", "street": "delancey pl", "unit": "13b"},
    ),
    X(
        "syn-t5-0138",
        """
c: hey 🍔
c: 4 bacon burgers
c: 3 with no cheese
c: and 2 cheeseburgers w avocado 🥑
c: to 242 riverside st
c: thx!!
""",
        "S P P P P S",
        items=[
            I("bacon_burger", 1, None, ["4 bacon burgers"]),
            I("bacon_burger", 3, None, ["4 bacon burgers", "3 with no cheese"], [rm("cheese", "no cheese")]),
            I("cheeseburger", 2, None, ["2 cheeseburgers"], [add("avocado", "w avocado")]),
        ],
        method="delivery",
        method_q="to 242 riverside st",
        addr={"raw": "242 riverside st", "number": "242", "street": "riverside st"},
    ),
    X(
        "syn-t5-0139",
        """
c: Hi there.
c: I'd like to place an order for my family, please.
""",
        "S P",
    ),
    X(
        "syn-t5-0140",
        """
c: 3 medium cheese pizzas
c: 2 orders of breadsticks
c: and 2 dr peppers
c: to 81 brookside pl, card
c: actually only 2 cheese pizzas
""",
        "P P P P M",
        items=[
            I("cheese_pizza", 2, "medium", ["3 medium cheese pizzas", "only 2 cheese pizzas"]),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I("dr_pepper", 2, None, ["2 dr peppers"]),
        ],
        method="delivery",
        method_q="to 81 brookside pl",
        addr={"raw": "81 brookside pl", "number": "81", "street": "brookside pl"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0141",
        """
c: hey
c: is the veggie burger good lol
b: It's one of our most popular!
c: ok one veggie burger and 2 large fries
c: to 4 ivanhoe ln #19, cash
b: One veggie burger and 2 large fries to 4 Ivanhoe Ln #19, cash. Correct?
c: yea
c: wait make the fries regular
""",
        "S Q P P C M",
        items=[
            I("veggie_burger", 1, None, ["one veggie burger"]),
            I("fries", 2, "regular", ["2 large fries", "make the fries regular"]),
        ],
        method="delivery",
        method_q="to 4 ivanhoe ln #19",
        addr={"raw": "4 ivanhoe ln #19", "number": "4", "street": "ivanhoe ln", "unit": "19"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0142",
        """
c: HAWAIIAN PIZZA, NO SAUCE, STUFFED CRUST!
c: AND A CAN OF COKE!
c: THANKS!
""",
        "P P S",
        items=[
            I(
                "hawaiian_pizza",
                1,
                None,
                ["HAWAIIAN PIZZA"],
                [rm("tomato_sauce", "NO SAUCE"), add("crust_stuffed", "STUFFED CRUST")],
            ),
            I("coke", 1, "can", ["A CAN OF COKE"]),
        ],
    ),
    X(
        "syn-t5-0143",
        """
c: FOUR PLAIN CROISSANTS, TWO WITH BUTTER!
c: AND A SMALL OAT MILK LATTE!
c: PICKUP FOR SAM, CASH!
""",
        "P P P",
        items=[
            I("croissant", 2, "plain", ["FOUR PLAIN CROISSANTS"]),
            I(
                "croissant",
                2,
                "plain",
                ["FOUR PLAIN CROISSANTS", "TWO WITH BUTTER"],
                [add("butter", "WITH BUTTER")],
            ),
            I("latte", 1, "small", ["A SMALL OAT MILK LATTE"], [sub("whole_milk", "oat_milk", "OAT MILK")]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Sam",
        name_q="SAM",
    ),
    X(
        "syn-t5-0144",
        """
c: hi! 🍕 some supremes with garlic on thick crust to 9159 sunset dr apt 11a, cash, change for a 50 pls
""",
        "P",
        items=[
            I(
                "supreme_pizza",
                None,
                None,
                ["some supremes"],
                [add("garlic", "with garlic"), add("crust_thick", "thick crust")],
            ),
        ],
        method="delivery",
        method_q="to 9159 sunset dr apt 11a",
        addr={"raw": "9159 sunset dr apt 11a", "number": "9159", "street": "sunset dr", "unit": "11a"},
        pay="cash",
        pay_q=["cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t5-0145",
        """
c: Hi, I'd like four medium hot chocolates with caramel and a large latte with whipped cream and skim milk instead of whole, for pickup as soon as possible under Luis. I'll pay by card.
c: Sorry, make that three hot chocolates.
""",
        "P M",
        items=[
            I(
                "hot_chocolate",
                3,
                "medium",
                ["four medium hot chocolates", "make that three hot chocolates"],
                [add("caramel_syrup", "with caramel")],
            ),
            I(
                "latte",
                1,
                "large",
                ["a large latte"],
                [
                    add("whipped_cream", "with whipped cream"),
                    sub("whole_milk", "skim_milk", "skim milk instead of whole"),
                ],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("asap", "as soon as possible", None),
        pay="card",
        pay_q="pay by card",
        name="Luis",
    ),
    X(
        "syn-t5-0146",
        """
c: hi ☕
c: 3 medium americanos w almond milk pls
c: pickup for grace
b: 3 medium americanos with almond milk, pickup for Grace. Sound right?
c: yes! 😊
c: oh make it 2 americanos sorry
""",
        "S P P C M",
        items=[
            I(
                "americano",
                2,
                "medium",
                ["3 medium americanos", "make it 2 americanos"],
                [add("almond_milk", "w almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t5-0147",
        """
c: hey! 3 12 oz cappuccinos pls ☕☕☕
c: pickup for leah, cash
""",
        "P P",
        items=[I("cappuccino", 3, "medium", ["3 12 oz cappuccinos"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t5-0148",
        """
c: good morning 🌤️
c: a breakfast sandwich and a 12 oz coffee pls
c: pickup for omar
c: in 20 min 🙏
""",
        "S P P P",
        items=[
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
            I("drip_coffee", 1, "medium", ["a 12 oz coffee"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20 min", None),
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t5-0149",
        """
c: yo
c: 2 fries
c: cash
c: change for a 20
c: make the fries large
""",
        "S P P P M",
        items=[I("fries", 2, "large", ["2 fries", "make the fries large"])],
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0150",
        """
c: Could I get a few Hawaiian pizzas? I'll pay cash and need change for a 20.
""",
        "P",
        items=[I("hawaiian_pizza", None, None, ["a few Hawaiian pizzas"])],
        pay="cash",
        pay_q=["pay cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0151",
        """
c: can u make a cheese pizza w no cheese lol
b: Sure, we can do a cheese pizza without cheese!
c: ok some large ones like that
c: delivery
""",
        "Q P P",
        items=[
            I(
                "cheese_pizza",
                None,
                "large",
                ["a cheese pizza w no cheese", "some large ones like that"],
                [rm("cheese", "w no cheese")],
            ),
        ],
        method="delivery",
        method_q="delivery",
    ),
    X(
        "syn-t5-0152",
        """
c: some onion rings n a chocolate shake in 20 min
""",
        "P",
        items=[
            I("onion_rings", None, None, ["some onion rings"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
        time=("relative", "in 20 min", None),
    ),
    X(
        "syn-t5-0153",
        """
c: hey
c: 2 bacon burgers
c: 2 onion rings n one of those
c: 6369 ivanhoe ln unit 8c at 8:30
""",
        "S P P P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("onion_rings", 2, None, ["2 onion rings"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="6369 ivanhoe ln unit 8c",
        time=("clock_time", "at 8:30", "20:30"),
        addr={"raw": "6369 ivanhoe ln unit 8c", "number": "6369", "street": "ivanhoe ln", "unit": "8c"},
    ),
    X(
        "syn-t5-0154",
        """
c: HI!!! ORDERING FOR MY KIDS' SLEEPOVER!
""",
        "P",
    ),
    X(
        "syn-t5-0155",
        """
c: hi
c: onion rings
c: and a 20 oz sprite
c: 922 clement ave asap
c: cash
""",
        "S P P P P",
        items=[
            I("onion_rings", 1, None, ["onion rings"]),
            I("sprite", 1, None, ["a 20 oz sprite"], unmatched_variant="20 oz"),
        ],
        method="delivery",
        method_q="922 clement ave",
        time=("asap", "asap", None),
        addr={"raw": "922 clement ave", "number": "922", "street": "clement ave"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0156",
        """
c: hi ordering for the team this morning
""",
        "P",
    ),
    X(
        "syn-t5-0157",
        """
c: hey there 👋
c: how big is a small?
b: Our small is 10 inches.
c: perfect, a few small cheese pizzas for pickup then 🍕
""",
        "S Q P",
        items=[I("cheese_pizza", None, "small", ["a few small cheese pizzas"])],
        method="pickup",
        method_q="for pickup",
    ),
    X(
        "syn-t5-0158",
        """
c: hi! what muffins do u have today? 🧁
b: Blueberry, chocolate chip and banana nut!
c: yum ok a muffin and a large latte
c: pickup for jordan, cash
""",
        "Q P P",
        items=[I("muffin", 1, None, ["a muffin"]), I("latte", 1, "large", ["a large latte"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t5-0159",
        """
c: hello ☀️ we'd like to order for the nurses' station
""",
        "P",
    ),
    X(
        "syn-t5-0160",
        """
c: hey 👋 3 medium supremes, 1 with ground beef
c: 2 xl bbq chicken pizzas
c: 2 orders of breadsticks 🥖
c: pickup asap for omar
""",
        "P P P P",
        items=[
            I("supreme_pizza", 2, "medium", ["3 medium supremes"]),
            I(
                "supreme_pizza",
                1,
                "medium",
                ["3 medium supremes", "1 with ground beef"],
                [add("beef", "with ground beef")],
            ),
            I("bbq_chicken_pizza", 2, "extra_large", ["2 xl bbq chicken pizzas"]),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Omar",
        name_q="omar",
    ),
]
