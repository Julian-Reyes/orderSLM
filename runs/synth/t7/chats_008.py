"""t7 syn-t7-0181–0210 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t7-0181",
        """
c: Hello!
c: Could I get a cappuccino with almond milk, one of the bigger sizes, and 2 croissants?
c: Pickup for Ana.
""",
        "S P P",
        items=[
            I(
                "cappuccino",
                1,
                None,
                ["a cappuccino with almond milk, one of the bigger sizes"],
                [sub("whole_milk", "almond_milk", "with almond milk")],
                flag="item_variant",
            ),
            I("croissant", 2, "plain", ["2 croissants"]),
        ],
        method="pickup",
        method_q="Pickup",
        name="Ana",
    ),
    X(
        "syn-t7-0182",
        """
c: 2 single cheeseburgers w mustard, is the mustard yellow or dijon? n a large fries
b: It's classic yellow mustard.
c: ok cool, deliver to 805 ivanhoe pl apt 11a
""",
        "P/Q P",
        items=[
            I(
                "cheeseburger",
                2,
                "single",
                ["2 single cheeseburgers w mustard"],
                [add("mustard", "w mustard")],
            ),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="delivery",
        method_q="deliver to 805 ivanhoe pl",
        addr={"raw": "805 ivanhoe pl apt 11a", "number": "805", "street": "ivanhoe pl", "unit": "apt 11a"},
    ),
    X(
        "syn-t7-0183",
        """
c: A PERSONAL SUPREME WITH ANCHOVIES ON GLUTEN FREE, A DR PEPPER AND SAME AS LAST TIME
c: TO 2 BIRCH RD UNIT 15B IN 30 MIN
""",
        "P P",
        items=[
            I(
                "supreme_pizza",
                1,
                "personal",
                ["A PERSONAL SUPREME WITH ANCHOVIES ON GLUTEN FREE"],
                [add("anchovies", "WITH ANCHOVIES"), add("crust_gluten_free", "ON GLUTEN FREE")],
            ),
            I("dr_pepper", 1, "can", ["A DR PEPPER"]),
            I(
                None,
                1,
                None,
                ["SAME AS LAST TIME"],
                unmatched="SAME AS LAST TIME",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="TO 2 BIRCH RD",
        time=("relative", "IN 30 MIN", None),
        addr={"raw": "2 BIRCH RD UNIT 15B", "number": "2", "street": "BIRCH RD", "unit": "UNIT 15B"},
    ),
    X(
        "syn-t7-0184",
        """
c: lg hot choc no whip
c: 2 drips w skim
c: bec w tomato n same as last time
c: pickup in 15, eli
""",
        "P P P P",
        items=[
            I("hot_chocolate", 1, "large", ["lg hot choc no whip"], [rm("whipped_cream", "no whip")]),
            I("drip_coffee", 2, "medium", ["2 drips w skim"], [add("skim_milk", "w skim")]),
            I("breakfast_sandwich", 1, "english_muffin", ["bec w tomato"], [add("tomato", "w tomato")]),
            I(
                None,
                1,
                None,
                ["same as last time"],
                unmatched="same as last time",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 15", None),
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t7-0185",
        """
c: hi! 2 blueberry muffins n which pastry is the most popular?
b: The chocolate croissant and the banana nut muffin are tied!
c: ok one of those too, card
""",
        "P/Q P",
        items=[
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0186",
        """
c: hi ☀️
c: 2 small hot chocs, 1 no whip
c: is the sesame bagel good w tomato? 🍅
b: It's a great combo!
c: ok one of those 😄
c: pickup in 20, nico, card
""",
        "S P Q P P",
        items=[
            I("hot_chocolate", 1, "small", ["2 small hot chocs"]),
            I(
                "hot_chocolate",
                1,
                "small",
                ["2 small hot chocs", "1 no whip"],
                [rm("whipped_cream", "no whip")],
            ),
            I(
                "bagel",
                1,
                "sesame",
                ["the sesame bagel good w tomato", "one of those"],
                [add("tomato", "w tomato")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t7-0187",
        """
c: veggie burger w sriracha, fries n a sprite
c: pickup at 6:30 for tara
c: card
""",
        "P P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger w sriracha"], [offmod("w sriracha")]),
            I("fries", 1, "regular", ["fries"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 6:30", "18:30"),
        pay="card",
        pay_q="card",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t7-0188",
        """
c: medium hawaiian
c: no cheese
c: pickup
c: cash
c: make it gluten free crust
""",
        "P P P P P",
        items=[
            I(
                "hawaiian_pizza",
                1,
                "medium",
                ["medium hawaiian", "no cheese", "make it gluten free crust"],
                [rm("cheese", "no cheese"), add("crust_gluten_free", "gluten free crust")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0189",
        """
c: Just a milkshake for pickup, card please.
""",
        "P",
        items=[I("milkshake", 1, None, ["a milkshake"])],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0190",
        """
c: a shake pls
c: chocolate or strawberry, whichever u think
c: card
""",
        "P P P",
        items=[
            I(
                "milkshake",
                1,
                None,
                ["a shake", "chocolate or strawberry, whichever u think"],
                flag="item_variant",
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0191",
        """
c: a milkshake n 2 sprites
c: card
""",
        "P P",
        items=[
            I("milkshake", 1, None, ["a milkshake"]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0192",
        """
c: 2 drips w whole milk
c: 4 banana nut muffins
c: n 2 hot chocs w vanilla
c: pickup for ivy
b: Got it, Ivy: 2 medium Drip Coffees with whole milk, 4 banana nut Muffins and 2 medium Hot Chocolates with vanilla syrup, pickup. Is that right?
c: yep
c: actually no hot chocs
""",
        "P P P P C M",
        items=[
            I("drip_coffee", 2, "medium", ["2 drips w whole milk"], [add("whole_milk", "w whole milk")]),
            I("muffin", 4, "banana_nut", ["4 banana nut muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t7-0193",
        """
c: GOOD MORNING
c: 3 DRIP COFFEES, 2 WITH CARAMEL
c: A CHOCOLATE CHIP MUFFIN AND 3 EVERYTHING BAGELS WITH TOMATO
c: PICKUP FOR BEN, CASH
""",
        "S P P P",
        items=[
            I("drip_coffee", 1, "medium", ["3 DRIP COFFEES"]),
            I(
                "drip_coffee",
                2,
                "medium",
                ["3 DRIP COFFEES", "2 WITH CARAMEL"],
                [add("caramel_syrup", "WITH CARAMEL")],
            ),
            I("muffin", 1, "chocolate_chip", ["A CHOCOLATE CHIP MUFFIN"]),
            I("bagel", 3, "everything", ["3 EVERYTHING BAGELS WITH TOMATO"], [add("tomato", "WITH TOMATO")]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Ben",
        name_q="BEN",
    ),
    X(
        "syn-t7-0194",
        """
c: 4 large cappuccinos ☕
c: pickup for luis, card
c: wait swap the cappuccinos for a bec no egg 🙏
""",
        "P P M",
        items=[I("breakfast_sandwich", 1, "english_muffin", ["a bec no egg"], [rm("egg", "no egg")])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t7-0195",
        """
c: 5 personal cheese pizzas, 1 on stuffed crust
c: n a personal veggie
c: asap to 488 fulton ln, cash
""",
        "P P P",
        items=[
            I("cheese_pizza", 4, "personal", ["5 personal cheese pizzas"]),
            I(
                "cheese_pizza",
                1,
                "personal",
                ["5 personal cheese pizzas", "1 on stuffed crust"],
                [add("crust_stuffed", "on stuffed crust")],
            ),
            I("veggie_pizza", 1, "personal", ["a personal veggie"]),
        ],
        method="delivery",
        method_q="to 488 fulton ln",
        time=("asap", "asap", None),
        addr={"raw": "488 fulton ln", "number": "488", "street": "fulton ln"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0196",
        """
c: 2 muffins n a hot choc w hazelnut n oat milk, pickup for ana, cash w a 20
""",
        "P",
        items=[
            I("muffin", 2, None, ["2 muffins"]),
            I(
                "hot_chocolate",
                1,
                "medium",
                ["a hot choc w hazelnut n oat milk"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "oat_milk", "oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "w a 20"],
        change=2000,
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0197",
        """
c: 2 caramel coffees n 3 everything
b: Two drip coffees with caramel and 3 everything bagels?
c: yes. pickup at 11:45 for luis, cash
""",
        "P P",
        items=[
            I("drip_coffee", 2, "medium", ["2 caramel coffees"], [add("caramel_syrup", "caramel")]),
            I("bagel", 3, "everything", ["3 everything"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 11:45", "11:45"),
        pay="cash",
        pay_q="cash",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t7-0198",
        """
c: 2 plain bagels
c: w avocado
c: medium latte
c: vanilla
c: almond milk
c: pickup
c: at 12:30
c: ana
""",
        "P P P P P P P P",
        items=[
            I("bagel", 2, "plain", ["2 plain bagels", "w avocado"], [add("avocado", "w avocado")]),
            I(
                "latte",
                1,
                "medium",
                ["medium latte", "vanilla", "almond milk"],
                [add("vanilla_syrup", "vanilla"), sub("whole_milk", "almond_milk", "almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:30", "12:30"),
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0199",
        """
c: Good morning! I'd like to order for Monday at 8:30: 2 breakfast sandwiches on bagels with tomato, 2 hot chocolates with vanilla and a sesame bagel. Pickup for Luis, cash.
""",
        "P",
        items=[
            I(
                "breakfast_sandwich",
                2,
                "bagel",
                ["2 breakfast sandwiches on bagels with tomato"],
                [add("tomato", "with tomato")],
            ),
            I(
                "hot_chocolate",
                2,
                "medium",
                ["2 hot chocolates with vanilla"],
                [add("vanilla_syrup", "with vanilla")],
            ),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 8:30", "08:30"),
        day=("weekday", "mon", "Monday"),
        pay="cash",
        pay_q="cash",
        name="Luis",
    ),
    X(
        "syn-t7-0200",
        """
c: personal cheese no sauce w pineapple on gluten free + an xl meat lovers on gluten free, pickup, cash
b: Got it: 1 personal Cheese Pizza with no sauce and pineapple on gluten-free crust and 1 extra large Meat Lovers Pizza on gluten-free crust, pickup, paying cash. Is that right?
c: yes
c: actually drop the meat lovers
""",
        "P C M",
        items=[
            I(
                "cheese_pizza",
                1,
                "personal",
                ["personal cheese no sauce w pineapple on gluten free"],
                [
                    rm("tomato_sauce", "no sauce"),
                    add("pineapple", "w pineapple"),
                    add("crust_gluten_free", "on gluten free"),
                ],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0201",
        """
c: veggie burger n a choc shake for pickup 🍔
c: cash, paying w a 20
c: nvm no shake
""",
        "P P M",
        items=[I("veggie_burger", 1, None, ["veggie burger"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0202",
        """
c: do u have vegan cheese? 🧀
b: Sorry, not right now.
c: ok a small cheese then n the one i always get
c: to 25 union ct 🏠
""",
        "Q P P",
        items=[
            I("cheese_pizza", 1, "small", ["a small cheese"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="to 25 union ct",
        addr={"raw": "25 union ct", "number": "25", "street": "union ct"},
    ),
    X(
        "syn-t7-0203",
        """
c: Hi, 2 medium veggie pizzas, a personal pepperoni with no sauce and green peppers, and 3 large meat lovers.
c: Delivered to 69 Harbor Ln, unit 11C. Cash.
b: Got it: 2 medium Veggie Pizzas, 1 personal Pepperoni Pizza with no sauce and green peppers, and 3 large Meat Lovers Pizzas, delivered to 69 Harbor Ln, unit 11C, paying cash. Is that right?
c: Yes.
c: Sorry, please take off the meat lovers.
""",
        "P P C M",
        items=[
            I("veggie_pizza", 2, "medium", ["2 medium veggie pizzas"]),
            I(
                "pepperoni_pizza",
                1,
                "personal",
                ["a personal pepperoni with no sauce and green peppers"],
                [rm("tomato_sauce", "no sauce"), add("green_peppers", "green peppers")],
            ),
        ],
        method="delivery",
        method_q="Delivered to 69 Harbor Ln",
        addr={"raw": "69 Harbor Ln, unit 11C", "number": "69", "street": "Harbor Ln", "unit": "unit 11C"},
        pay="cash",
        pay_q="Cash",
    ),
    X(
        "syn-t7-0204",
        """
c: 6 bacon burgers, half no onions 🍔
c: 2 cokes n a veggie burger no lettuce
c: 7726 ridgecrest rd, blue door, delivery, card
""",
        "P P P",
        items=[
            I("bacon_burger", 3, None, ["6 bacon burgers"]),
            I("bacon_burger", 3, None, ["6 bacon burgers", "half no onions"], [rm("onion", "no onions")]),
            I("coke", 2, None, ["2 cokes"]),
            I("veggie_burger", 1, None, ["a veggie burger no lettuce"], [rm("lettuce", "no lettuce")]),
        ],
        method="delivery",
        method_q="delivery",
        addr={
            "raw": "7726 ridgecrest rd, blue door",
            "number": "7726",
            "street": "ridgecrest rd",
            "reference": "blue door",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0205",
        """
c: hi
c: is the hazelnut syrup nut free?
b: It's flavored syrup, but we can't promise it's free of nut traces.
c: ok 2 drips w hazelnut
c: pickup in 20, luis, card
c: n make them w whole milk pls
""",
        "S Q P P P",
        items=[
            I(
                "drip_coffee",
                2,
                "medium",
                ["2 drips w hazelnut", "make them w whole milk"],
                [add("hazelnut_syrup", "w hazelnut"), add("whole_milk", "w whole milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t7-0206",
        """
c: almond croissant w butter, 2 med americanos w almond milk, a bec on a croissant no bacon n one of those
c: pickup asap for grace
""",
        "P P",
        items=[
            I("croissant", 1, "almond", ["almond croissant w butter"], [add("butter", "w butter")]),
            I(
                "americano",
                2,
                "medium",
                ["2 med americanos w almond milk"],
                [add("almond_milk", "w almond milk")],
            ),
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["a bec on a croissant no bacon"],
                [rm("bacon", "no bacon")],
            ),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0207",
        """
c: bec on a croissant w lavender syrup
c: asap pickup keisha, card
""",
        "P P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["bec on a croissant w lavender syrup"],
                [offmod("w lavender syrup")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t7-0208",
        """
c: HI
c: 4 EVERYTHING BAGELS, 3 WITH CREAM CHEESE
c: A HOT CHOCOLATE WITH OAT MILK
c: AND A MEDIUM VANILLA CAPPUCCINO
c: PICKUP FOR KEISHA, CARD
""",
        "S P P P P",
        items=[
            I("bagel", 1, "everything", ["4 EVERYTHING BAGELS"]),
            I(
                "bagel",
                3,
                "everything",
                ["4 EVERYTHING BAGELS", "3 WITH CREAM CHEESE"],
                [add("cream_cheese", "WITH CREAM CHEESE")],
            ),
            I(
                "hot_chocolate",
                1,
                "medium",
                ["A HOT CHOCOLATE WITH OAT MILK"],
                [sub("whole_milk", "oat_milk", "WITH OAT MILK")],
            ),
            I("cappuccino", 1, "medium", ["A MEDIUM VANILLA CAPPUCCINO"], [add("vanilla_syrup", "VANILLA")]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
        name="Keisha",
        name_q="KEISHA",
    ),
    X(
        "syn-t7-0209",
        """
c: can i get a 2 liter of diet n a large pepperoni to 9484 thornton ln
""",
        "P",
        items=[
            I("diet_coke", 1, "two_liter", ["a 2 liter of diet"]),
            I("pepperoni_pizza", 1, "large", ["a large pepperoni"]),
        ],
        method="delivery",
        method_q="to 9484 thornton ln",
        addr={"raw": "9484 thornton ln", "number": "9484", "street": "thornton ln"},
    ),
    X(
        "syn-t7-0210",
        """
c: 2 xl cheese w mushrooms on gluten free, are the mushrooms fresh? n 2 diet cokes
b: Yes, fresh mushrooms every day!
c: great, asap
c: cash
c: have a 50
""",
        "P/Q P P P",
        items=[
            I(
                "cheese_pizza",
                2,
                "extra_large",
                ["2 xl cheese w mushrooms on gluten free"],
                [add("mushrooms", "w mushrooms"), add("crust_gluten_free", "on gluten free")],
            ),
            I("diet_coke", 2, "can", ["2 diet cokes"]),
        ],
        time=("asap", "asap", None),
        pay="cash",
        pay_q=["cash", "have a 50"],
        change=5000,
    ),
]
