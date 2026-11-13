"""t7 syn-t7-0011–0030 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t7-0011",
        """
c: hey can i get 4 cheeseburgers, 3 of em no ketchup
c: n a coke
c: deliver to 26 clement blvd
""",
        "P P P",
        items=[
            I("cheeseburger", 1, "single", ["4 cheeseburgers"]),
            I(
                "cheeseburger",
                3,
                "single",
                ["4 cheeseburgers", "3 of em no ketchup"],
                [rm("ketchup", "no ketchup")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="deliver to 26 clement blvd",
        addr={"raw": "26 clement blvd", "number": "26", "street": "clement blvd"},
    ),
    X(
        "syn-t7-0012",
        """
c: Good morning!
c: A small cappuccino and a large latte for pickup, please. Name is Tara, paying by card.
b: Got it, Tara: 1 small Cappuccino and 1 large Latte, pickup, paying by card. Is that right?
c: Yes, thank you.
c: Oh, could you add vanilla syrup to the cappuccino?
""",
        "S P C M",
        items=[
            I(
                "cappuccino",
                1,
                "small",
                ["A small cappuccino", "add vanilla syrup to the cappuccino"],
                [add("vanilla_syrup", "add vanilla syrup")],
            ),
            I("latte", 1, "large", ["a large latte"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="paying by card",
        name="Tara",
    ),
    X(
        "syn-t7-0013",
        """
c: hey 😊 could i get a lar
""",
        "U",
    ),
    X(
        "syn-t7-0014",
        """
c: vanilla shake
c: double cb no onions
c: lg fries n a lemonade
c: pickup at 5, dev
c: actually no lemonade
""",
        "P P P P M",
        items=[
            I("milkshake", 1, "vanilla", ["vanilla shake"]),
            I("cheeseburger", 1, "double", ["double cb no onions"], [rm("onion", "no onions")]),
            I("fries", 1, "large", ["lg fries"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 5", "17:00"),
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t7-0015",
        """
c: 2 everything bagels, one w avocado
c: n a small drip w almond milk, card
""",
        "P P",
        items=[
            I("bagel", 1, "everything", ["2 everything bagels"]),
            I(
                "bagel",
                1,
                "everything",
                ["2 everything bagels", "one w avocado"],
                [add("avocado", "w avocado")],
            ),
            I(
                "drip_coffee",
                1,
                "small",
                ["a small drip w almond milk"],
                [add("almond_milk", "w almond milk")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0016",
        """
c: hiii 🍔
c: the usual pls 🙏
b: Hi! We can't see past orders here, sorry. What would you like?
c: oh right 😅 veggie burger no tomato add jalapeños, a cheeseburger no onions, fries n a coke
c: asap to 366 dover way, cash, paying w a 50 💵
""",
        "S P P P",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["veggie burger no tomato add jalapeños"],
                [rm("tomato", "no tomato"), add("jalapeno", "add jalapeños")],
            ),
            I("cheeseburger", 1, "single", ["a cheeseburger no onions"], [rm("onion", "no onions")]),
            I("fries", 1, "regular", ["fries"]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="to 366 dover way",
        time=("asap", "asap", None),
        addr={"raw": "366 dover way", "number": "366", "street": "dover way"},
        pay="cash",
        pay_q=["cash", "paying w a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0017",
        """
c: 2 sesame bagels w butter
c: 2 lg caps
c: do u guys have oat milk
b: Yes, oat milk is 70¢ extra.
c: ok a lg oat latte n a plain croissant
c: pickup 7:45 for tom
""",
        "P P Q P P",
        items=[
            I("bagel", 2, "sesame", ["2 sesame bagels w butter"], [add("butter", "w butter")]),
            I("cappuccino", 2, "large", ["2 lg caps"]),
            I("latte", 1, "large", ["a lg oat latte"], [sub("whole_milk", "oat_milk", "oat")]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "7:45", "07:45"),
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0018",
        """
c: hey 🍕
c: 3 medium cheese pizzas pls, 2 of them with no sauce
c: + garlic knots
c: deliver to 910 glenwood blvd 🏠 card
""",
        "S P P P",
        items=[
            I("cheese_pizza", 1, "medium", ["3 medium cheese pizzas"]),
            I(
                "cheese_pizza",
                2,
                "medium",
                ["3 medium cheese pizzas", "2 of them with no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I("garlic_knots", 1, None, ["garlic knots"]),
        ],
        method="delivery",
        method_q="deliver to 910 glenwood blvd",
        addr={"raw": "910 glenwood blvd", "number": "910", "street": "glenwood blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0019",
        """
c: hey
c: 3 bacon burgers one no tomato, a veggie burger, a cheeseburger w mustard n 2 onion rings. pickup asap, card
""",
        "S P",
        items=[
            I("bacon_burger", 2, None, ["3 bacon burgers"]),
            I("bacon_burger", 1, None, ["3 bacon burgers", "one no tomato"], [rm("tomato", "no tomato")]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("cheeseburger", 1, "single", ["a cheeseburger w mustard"], [add("mustard", "w mustard")]),
            I("onion_rings", 2, None, ["2 onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0020",
        """
c: HI CAN I GET SOMETHING TO SNACK ON AND A LARGE PEPPERONI
b: For sides we have Garlic Knots (6 per order) and Breadsticks (4 per order). Which would you like?
c: BREADSTICKS PLEASE. ASAP TO 399 EASTON WAY, CARD
""",
        "P P",
        items=[
            I("pepperoni_pizza", 1, "large", ["A LARGE PEPPERONI"]),
            I("breadsticks", 1, None, ["BREADSTICKS"]),
        ],
        method="delivery",
        method_q="TO 399 EASTON WAY",
        time=("asap", "ASAP", None),
        addr={"raw": "399 EASTON WAY", "number": "399", "street": "EASTON WAY"},
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0021",
        """
c: hi 👋 medium cheese w ham n the usual, pickup for eli 🍕
""",
        "P",
        items=[
            I("cheese_pizza", 1, "medium", ["medium cheese w ham"], [add("ham", "w ham")]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t7-0022",
        """
c: veggie burger w jalapenos n coleslaw on it
c: thx
""",
        "P S",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["veggie burger w jalapenos n coleslaw on it"],
                [add("jalapeno", "w jalapenos"), offmod("coleslaw")],
            ),
        ],
    ),
    X(
        "syn-t7-0023",
        """
c: hey there 😊
c: a 20oz diet coke n 2 orders of breadsticks
c: a medium margherita, 3 sprites 20 oz too 🥤
c: a large supreme + an xl meat lovers no ham on thick crust. deliver to 98 orchard terrace, card 💳
""",
        "S P P P",
        items=[
            I("diet_coke", 1, "bottle_20oz", ["a 20oz diet coke"]),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I("margherita_pizza", 1, "medium", ["a medium margherita"]),
            I("sprite", 3, "bottle_20oz", ["3 sprites 20 oz"]),
            I("supreme_pizza", 1, "large", ["a large supreme"]),
            I(
                "meat_lovers_pizza",
                1,
                "extra_large",
                ["an xl meat lovers no ham on thick crust"],
                [rm("ham", "no ham"), add("crust_thick", "on thick crust")],
            ),
        ],
        method="delivery",
        method_q="deliver to 98 orchard terrace",
        addr={"raw": "98 orchard terrace", "number": "98", "street": "orchard terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0024",
        """
c: Hi, could I get 3 large cheese pizzas, 2 of them with olives, and a Coke? I'll pay cash.
""",
        "P",
        items=[
            I("cheese_pizza", 1, "large", ["3 large cheese pizzas"]),
            I(
                "cheese_pizza",
                2,
                "large",
                ["3 large cheese pizzas", "2 of them with olives"],
                [add("olives", "with olives")],
            ),
            I("coke", 1, "can", ["a Coke"]),
        ],
        pay="cash",
        pay_q="I'll pay cash",
    ),
    X(
        "syn-t7-0025",
        """
c: hi
c: 4 med hot chocs
c: 2 no whip
c: everything bagel w cream cheese
c: pickup june
c: card
""",
        "S P P P P P",
        items=[
            I("hot_chocolate", 2, "medium", ["4 med hot chocs"]),
            I(
                "hot_chocolate",
                2,
                "medium",
                ["4 med hot chocs", "2 no whip"],
                [rm("whipped_cream", "no whip")],
            ),
            I(
                "bagel",
                1,
                "everything",
                ["everything bagel w cream cheese"],
                [add("cream_cheese", "w cream cheese")],
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
        "syn-t7-0026",
        """
c: lg hot choc w oat milk n 2 banana nut muffins, card
b: Got it: 1 large Hot Chocolate with oat milk and 2 banana nut Muffins, paying by card. Is that right?
c: yep
c: actually skip the muffins
""",
        "P C M",
        items=[
            I(
                "hot_chocolate",
                1,
                "large",
                ["lg hot choc w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0027",
        """
c: 2 hot chocs no whip w skim
c: 4 bec
c: lg drip
c: pickup 12:45 leah, card
c: just 1 hot choc actually
""",
        "P P P P M",
        items=[
            I(
                "hot_chocolate",
                1,
                "medium",
                ["2 hot chocs no whip w skim", "just 1 hot choc"],
                [rm("whipped_cream", "no whip"), sub("whole_milk", "skim_milk", "w skim")],
            ),
            I("breakfast_sandwich", 4, "english_muffin", ["4 bec"]),
            I("drip_coffee", 1, "large", ["lg drip"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "12:45", "12:45"),
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t7-0028",
        """
c: 2 xl veggies n bread sticks 🍕
c: + a doctor pepper
c: pickup at 10:45, cash 💵
""",
        "P P P",
        items=[
            I("veggie_pizza", 2, "extra_large", ["2 xl veggies"]),
            I("breadsticks", 1, None, ["bread sticks"]),
            I("dr_pepper", 1, "can", ["a doctor pepper"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10:45", "22:45"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0029",
        """
c: 5 xl hawaiians, 1 w stuffed crust
c: 2 diet cokes n a medium veggie
c: pickup
""",
        "P P P",
        items=[
            I("hawaiian_pizza", 4, "extra_large", ["5 xl hawaiians"]),
            I(
                "hawaiian_pizza",
                1,
                "extra_large",
                ["5 xl hawaiians", "1 w stuffed crust"],
                [add("crust_stuffed", "w stuffed crust")],
            ),
            I("diet_coke", 2, "can", ["2 diet cokes"]),
            I("veggie_pizza", 1, "medium", ["a medium veggie"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t7-0030",
        """
c: Hi!
c: One medium margherita for pickup in 20 minutes, please. Cash, I have a 20.
c: Could you make it thin crust?
""",
        "S P P",
        items=[
            I(
                "margherita_pizza",
                1,
                "medium",
                ["One medium margherita", "make it thin crust"],
                [add("crust_thin", "make it thin crust")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in 20 minutes", None),
        pay="cash",
        pay_q=["Cash", "I have a 20"],
        change=2000,
    ),
]
