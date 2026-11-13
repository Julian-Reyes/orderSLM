"""t7 syn-t7-0211–0240 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t7-0211",
        """
c: small bbq chicken w tomatoes 🍅
c: n something bready, what do u have?
b: Garlic Knots (6 per order) and Breadsticks (4 per order).
c: the breadsticks + a sprite
c: to 9750 vine pl in 30 min 🙏
""",
        "P P P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "small",
                ["small bbq chicken w tomatoes"],
                [add("tomatoes", "w tomatoes")],
            ),
            I("breadsticks", 1, None, ["the breadsticks"]),
            I("sprite", 1, "can", ["a sprite"]),
        ],
        method="delivery",
        method_q="to 9750 vine pl",
        time=("relative", "in 30 min", None),
        addr={"raw": "9750 vine pl", "number": "9750", "street": "vine pl"},
    ),
    X(
        "syn-t7-0212",
        """
c: 4 bacon burgers
c: 3 no pickles
c: rings n fries
c: pickup ben cash
""",
        "P P P P",
        items=[
            I("bacon_burger", 1, None, ["4 bacon burgers"]),
            I("bacon_burger", 3, None, ["4 bacon burgers", "3 no pickles"], [rm("pickle", "no pickles")]),
            I("onion_rings", 1, None, ["rings"]),
            I("fries", 1, "regular", ["fries"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t7-0213",
        """
c: a choc chip muffin, are they baked today? n a medium drip
b: Yes, fresh this morning!
c: nice. pickup for ben, cash, i have a 20
""",
        "P/Q P",
        items=[
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
            I("drip_coffee", 1, "medium", ["a medium drip"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t7-0214",
        """
c: vanilla shake, single cheeseburger w chili on top n a coke
c: pickup, card
""",
        "P P",
        items=[
            I("milkshake", 1, "vanilla", ["vanilla shake"]),
            I(
                "cheeseburger",
                1,
                "single",
                ["single cheeseburger w chili on top"],
                [offmod("w chili on top")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0215",
        """
c: do u have avocado for bagels?
b: Yes, avocado is an add-on for any bagel.
c: 3 sesame bagels then, one w avocado, a small vanilla cap n 2 drips. pickup at 12:15 for ana, cash
""",
        "Q P",
        items=[
            I("bagel", 2, "sesame", ["3 sesame bagels"]),
            I("bagel", 1, "sesame", ["3 sesame bagels", "one w avocado"], [add("avocado", "w avocado")]),
            I("cappuccino", 1, "small", ["a small vanilla cap"], [add("vanilla_syrup", "vanilla")]),
            I("drip_coffee", 2, "medium", ["2 drips"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:15", "12:15"),
        pay="cash",
        pay_q="cash",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0216",
        """
c: is the pepperoni spicy? 🌶️
b: It's a mild pepperoni.
c: ok large pepperoni no sauce, 2 iced teas n a 20 oz coke
c: pickup in 30 for jordan, card 💳
c: oh make the pepperoni thick crust
""",
        "Q P P M",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "large",
                ["large pepperoni no sauce", "make the pepperoni thick crust"],
                [rm("tomato_sauce", "no sauce"), add("crust_thick", "thick crust")],
            ),
            I("iced_tea", 2, "can", ["2 iced teas"]),
            I("coke", 1, "bottle_20oz", ["a 20 oz coke"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 30", None),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t7-0217",
        """
c: do u have hazelnut syrup
b: Yes, we do!
c: great, a medium americano w hazelnut for tomorrow
c: pickup, grace, card
""",
        "Q P P",
        items=[
            I(
                "americano",
                1,
                "medium",
                ["a medium americano w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tomorrow"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0218",
        """
c: HELLO
c: ARE THE SHAKES MADE WITH REAL ICE CREAM?
b: Yes, real ice cream!
c: 2 STRAWBERRY SHAKES, A COKE, ONION RINGS AND THE USUAL TO 3117 SPRUCE DR, SIDE ENTRANCE
""",
        "S Q P",
        items=[
            I("milkshake", 2, "strawberry", ["2 STRAWBERRY SHAKES"]),
            I("coke", 1, None, ["A COKE"]),
            I("onion_rings", 1, None, ["ONION RINGS"]),
            I(None, 1, None, ["THE USUAL"], unmatched="THE USUAL", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="TO 3117 SPRUCE DR",
        addr={
            "raw": "3117 SPRUCE DR, SIDE ENTRANCE",
            "number": "3117",
            "street": "SPRUCE DR",
            "reference": "SIDE ENTRANCE",
        },
    ),
    X(
        "syn-t7-0219",
        """
c: personal veggie
c: medium meat lovers no sauce
c: 2 xl supremes
c: in 40 min, cash
b: Got it: 1 personal Veggie Pizza, 1 medium Meat Lovers Pizza with no sauce and 2 extra large Supreme Pizzas, in 40 minutes, paying cash. Is that right?
c: yes
c: can the veggie be stuffed crust
""",
        "P P P P C M",
        items=[
            I(
                "veggie_pizza",
                1,
                "personal",
                ["personal veggie", "can the veggie be stuffed crust"],
                [add("crust_stuffed", "stuffed crust")],
            ),
            I(
                "meat_lovers_pizza",
                1,
                "medium",
                ["medium meat lovers no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I("supreme_pizza", 2, "extra_large", ["2 xl supremes"]),
        ],
        time=("relative", "in 40 min", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0220",
        """
c: 4 veggie burgers
c: 3 w jalapenos
c: n 2 bacon burgers
c: no ketchup on those
c: pickup
c: in 25
""",
        "P P P P P P",
        items=[
            I("veggie_burger", 1, None, ["4 veggie burgers"]),
            I(
                "veggie_burger",
                3,
                None,
                ["4 veggie burgers", "3 w jalapenos"],
                [add("jalapeno", "w jalapenos")],
            ),
            I(
                "bacon_burger",
                2,
                None,
                ["2 bacon burgers", "no ketchup on those"],
                [rm("ketchup", "no ketchup")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 25", None),
    ),
    X(
        "syn-t7-0221",
        """
c: some small meat lovers on gluten free for 6:30, card 🍕
""",
        "P",
        items=[
            I(
                "meat_lovers_pizza",
                None,
                "small",
                ["some small meat lovers on gluten free"],
                [add("crust_gluten_free", "on gluten free")],
            ),
        ],
        time=("clock_time", "6:30", "18:30"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0222",
        """
c: 4 bacon burgers one no lettuce, a sprite, a large fries n a double cheeseburger w mayo
c: asap to 7 easton terrace
""",
        "P P",
        items=[
            I("bacon_burger", 3, None, ["4 bacon burgers"]),
            I("bacon_burger", 1, None, ["4 bacon burgers", "one no lettuce"], [rm("lettuce", "no lettuce")]),
            I("sprite", 1, None, ["a sprite"]),
            I("fries", 1, "large", ["a large fries"]),
            I("cheeseburger", 1, "double", ["a double cheeseburger w mayo"], [add("mayo", "w mayo")]),
        ],
        method="delivery",
        method_q="to 7 easton terrace",
        time=("asap", "asap", None),
        addr={"raw": "7 easton terrace", "number": "7", "street": "easton terrace"},
    ),
    X(
        "syn-t7-0223",
        """
c: 2 MEDIUM HAWAIIANS AND 2 WATERS TO 309 BIRCH BLVD ACROSS FROM THE PARK, IN 45 MIN, CARD
b: Got it: 2 medium Hawaiian Pizzas and 2 Bottled Waters, delivered to 309 Birch Blvd in 45 minutes, paying by card. Is that right?
c: YES
c: MAKE BOTH HAWAIIANS GLUTEN FREE CRUST PLEASE
""",
        "P C M",
        items=[
            I(
                "hawaiian_pizza",
                2,
                "medium",
                ["2 MEDIUM HAWAIIANS", "MAKE BOTH HAWAIIANS GLUTEN FREE CRUST"],
                [add("crust_gluten_free", "GLUTEN FREE CRUST")],
            ),
            I("water", 2, None, ["2 WATERS"]),
        ],
        method="delivery",
        method_q="TO 309 BIRCH BLVD",
        time=("relative", "IN 45 MIN", None),
        addr={
            "raw": "309 BIRCH BLVD ACROSS FROM THE PARK",
            "number": "309",
            "street": "BIRCH BLVD",
            "reference": "ACROSS FROM THE PARK",
        },
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0224",
        """
c: Hi there.
c: Some croissants, a breakfast sandwich on a bagel and 4 drip coffees with vanilla, please.
c: Cash.
""",
        "S P P",
        items=[
            I("croissant", None, "plain", ["Some croissants"]),
            I("breakfast_sandwich", 1, "bagel", ["a breakfast sandwich on a bagel"]),
            I(
                "drip_coffee",
                4,
                "medium",
                ["4 drip coffees with vanilla"],
                [add("vanilla_syrup", "with vanilla")],
            ),
        ],
        pay="cash",
        pay_q="Cash",
    ),
    X(
        "syn-t7-0225",
        """
c: 2 bottled waters, is the water sparkling or still? n a 20 oz diet coke, pickup, card
""",
        "P/Q",
        items=[
            I("water", 2, None, ["2 bottled waters"]),
            I("diet_coke", 1, "bottle_20oz", ["a 20 oz diet coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0226",
        """
c: can i get 2 bacon burgers n a sprite delivered to 449 clement ave on oct 9 at 7pm
""",
        "P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="delivery",
        method_q="delivered to 449 clement ave",
        time=("clock_time", "at 7pm", "19:00"),
        day=("date", 10, 9, "oct 9"),
        addr={"raw": "449 clement ave", "number": "449", "street": "clement ave"},
    ),
    X(
        "syn-t7-0227",
        """
c: 3 almond croissants for the 5th at 8am
c: pickup for omar
""",
        "P P",
        items=[I("croissant", 3, "almond", ["3 almond croissants"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8am", "08:00"),
        day=("date", None, 5, "the 5th"),
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t7-0228",
        """
c: hi
c: bec no bacon
c: w hot sauce pls
c: 4 choc chip muffins
c: pickup
c: maya
""",
        "S P P P P P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["bec no bacon", "w hot sauce"],
                [rm("bacon", "no bacon"), offmod("w hot sauce")],
            ),
            I("muffin", 4, "chocolate_chip", ["4 choc chip muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0229",
        """
c: 3 ONION RINGS, IS THE SHAKE THICK? AND A CHOCOLATE SHAKE AND 2 COKES
b: Yes, nice and thick!
c: ASAP TO 990 PROSPECT DR APT 9
""",
        "P/Q P",
        items=[
            I("onion_rings", 3, None, ["3 ONION RINGS"]),
            I("milkshake", 1, "chocolate", ["A CHOCOLATE SHAKE"]),
            I("coke", 2, None, ["2 COKES"]),
        ],
        method="delivery",
        method_q="TO 990 PROSPECT DR",
        time=("asap", "ASAP", None),
        addr={"raw": "990 PROSPECT DR APT 9", "number": "990", "street": "PROSPECT DR", "unit": "APT 9"},
    ),
    X(
        "syn-t7-0230",
        """
c: does the hawaiian have bbq sauce?
b: No, it has tomato sauce, cheese, ham and pineapple.
c: ok a small hawaiian, a water n a sprite to 43 vine ave, side entrance. cash
c: actually add bbq sauce to the hawaiian
""",
        "Q P M",
        items=[
            I(
                "hawaiian_pizza",
                1,
                "small",
                ["a small hawaiian", "add bbq sauce to the hawaiian"],
                [add("bbq_sauce", "add bbq sauce")],
            ),
            I("water", 1, None, ["a water"]),
            I("sprite", 1, "can", ["a sprite"]),
        ],
        method="delivery",
        method_q="to 43 vine ave",
        addr={
            "raw": "43 vine ave, side entrance",
            "number": "43",
            "street": "vine ave",
            "reference": "side entrance",
        },
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0231",
        """
c: I NEED THE
c: HJKL
""",
        "U U",
    ),
    X(
        "syn-t7-0232",
        """
c: do u have curly fries
b: Sorry, just regular fries and onion rings.
c: ok 2 rings n a cola then, asap to 40 lakeview terrace unit 2c
""",
        "Q P",
        items=[
            I("onion_rings", 2, None, ["2 rings"]),
            I("coke", 1, None, ["a cola"]),
        ],
        method="delivery",
        method_q="to 40 lakeview terrace",
        time=("asap", "asap", None),
        addr={
            "raw": "40 lakeview terrace unit 2c",
            "number": "40",
            "street": "lakeview terrace",
            "unit": "unit 2c",
        },
    ),
    X(
        "syn-t7-0233",
        """
c: A lemonade and a double cheeseburger, please.
c: Delivered to 3516 Chestnut Terrace.
c: At 7:30.
c: Card.
""",
        "P P P P",
        items=[
            I("lemonade", 1, None, ["A lemonade"]),
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
        ],
        method="delivery",
        method_q="Delivered to 3516 Chestnut Terrace",
        time=("clock_time", "At 7:30", "19:30"),
        addr={"raw": "3516 Chestnut Terrace", "number": "3516", "street": "Chestnut Terrace"},
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t7-0234",
        """
c: can u do a hal
c: ?
""",
        "U U",
    ),
    X(
        "syn-t7-0235",
        """
c: 5 large americanos ☕
c: 4 w oat milk
c: n a bec 🥓
""",
        "P P P",
        items=[
            I("americano", 1, "large", ["5 large americanos"]),
            I(
                "americano",
                4,
                "large",
                ["5 large americanos", "4 w oat milk"],
                [add("oat_milk", "w oat milk")],
            ),
            I("breakfast_sandwich", 1, "english_muffin", ["a bec"]),
        ],
    ),
    X(
        "syn-t7-0236",
        """
c: 🍕🍕 can i get a mediu
""",
        "U",
    ),
    X(
        "syn-t7-0237",
        """
c: hey 👋
c: veggie burger at 7:45
c: cash
""",
        "S P P",
        items=[I("veggie_burger", 1, None, ["veggie burger"])],
        time=("clock_time", "at 7:45", "19:45"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0238",
        """
c: hey
c: personal hawaiian on thick crust n 2 cans of coke for tomorrow, delivery
c: cash, paying w a 20
""",
        "S P P",
        items=[
            I(
                "hawaiian_pizza",
                1,
                "personal",
                ["personal hawaiian on thick crust"],
                [add("crust_thick", "on thick crust")],
            ),
            I("coke", 2, "can", ["2 cans of coke"]),
        ],
        method="delivery",
        method_q="delivery",
        time=("ambiguous", "for tomorrow"),
        day=("tomorrow", "tomorrow"),
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0239",
        """
c: 2 shakes
c: n one of those
c: card
c: in 20
""",
        "P P P P",
        items=[
            I("milkshake", 2, None, ["2 shakes"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0240",
        """
c: 🍔 can i ge
""",
        "U",
    ),
]
