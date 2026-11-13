"""t7 syn-t7-0061–0090 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t7-0061",
        """
c: bacon burger no cheese w mustard + a veggie burger no tomato 🍔
c: to 3609 delancey ct, cash 💵
c: nvm skip the veggie one
""",
        "P P M",
        items=[
            I(
                "bacon_burger",
                1,
                None,
                ["bacon burger no cheese w mustard"],
                [rm("cheese", "no cheese"), add("mustard", "w mustard")],
            ),
        ],
        method="delivery",
        method_q="to 3609 delancey ct",
        addr={"raw": "3609 delancey ct", "number": "3609", "street": "delancey ct"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0062",
        """
c: hey
c: is the big meat spicy
b: No, the Meat Lovers isn't spicy: pepperoni, sausage, ham, bacon and beef.
c: ok a large big meat
c: n a dr pepper
c: 59 ivanhoe st above the bakery, delivery, card
""",
        "S Q P P P",
        items=[
            I("meat_lovers_pizza", 1, "large", ["a large big meat"]),
            I("dr_pepper", 1, "can", ["a dr pepper"]),
        ],
        method="delivery",
        method_q="delivery",
        addr={
            "raw": "59 ivanhoe st above the bakery",
            "number": "59",
            "street": "ivanhoe st",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0063",
        """
c: for tomorrow pls: 2 muffins n a bec on a bagel w tomato
c: pickup, rosa, card
""",
        "P P",
        items=[
            I("muffin", 2, None, ["2 muffins"]),
            I("breakfast_sandwich", 1, "bagel", ["a bec on a bagel w tomato"], [add("tomato", "w tomato")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tomorrow"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t7-0064",
        """
c: 2 hot chocs
c: one no whip
c: n a croissant w butter
c: cash
""",
        "P P P P",
        items=[
            I("hot_chocolate", 1, "medium", ["2 hot chocs"]),
            I("hot_chocolate", 1, "medium", ["2 hot chocs", "one no whip"], [rm("whipped_cream", "no whip")]),
            I("croissant", 1, "plain", ["a croissant w butter"], [add("butter", "w butter")]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0065",
        """
c: 4 personal hawaiians n 4 dr peppers 🍍 cash, paying w a 50
""",
        "P",
        items=[
            I("hawaiian_pizza", 4, "personal", ["4 personal hawaiians"]),
            I("dr_pepper", 4, "can", ["4 dr peppers"]),
        ],
        pay="cash",
        pay_q=["cash", "paying w a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0066",
        """
c: Hello!
c: A large pepperoni and 2 Diet Cokes, please.
c: Paying by card.
c: Actually, just one Diet Coke.
""",
        "S P P M",
        items=[
            I("pepperoni_pizza", 1, "large", ["A large pepperoni"]),
            I("diet_coke", 1, "can", ["2 Diet Cokes", "just one Diet Coke"]),
        ],
        pay="card",
        pay_q="Paying by card",
    ),
    X(
        "syn-t7-0067",
        """
c: a few banana nut muffins
c: cash
c: got a 20
c: ty
""",
        "P P P S",
        items=[I("muffin", None, "banana_nut", ["a few banana nut muffins"])],
        pay="cash",
        pay_q=["cash", "got a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0068",
        """
c: hi!
c: do u have gluten free bagels?
b: Sorry, not right now. We have plain, everything, sesame and cinnamon raisin.
c: ok a plain bagel w avocado for thursday at 9
c: pickup, jordan, card
""",
        "S Q P P",
        items=[I("bagel", 1, "plain", ["a plain bagel w avocado"], [add("avocado", "w avocado")])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        day=("weekday", "thu", "thursday"),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t7-0069",
        """
c: xl margherita w bbq sauce
c: large veggie
c: 2 orders of breadsticks
c: a 20oz dr pepper n 3 waters
c: deliver to 1963 thornton ln at 6:30, cash
""",
        "P P P P P",
        items=[
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["xl margherita w bbq sauce"],
                [add("bbq_sauce", "w bbq sauce")],
            ),
            I("veggie_pizza", 1, "large", ["large veggie"]),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I("dr_pepper", 1, "bottle_20oz", ["a 20oz dr pepper"]),
            I("water", 3, None, ["3 waters"]),
        ],
        method="delivery",
        method_q="deliver to 1963 thornton ln",
        time=("clock_time", "at 6:30", "18:30"),
        addr={"raw": "1963 thornton ln", "number": "1963", "street": "thornton ln"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0070",
        """
c: Hi, a small latte for pickup. Name is Leah, I'll pay cash with a 20.
b: Got it, Leah: 1 small Latte, pickup, paying cash. Is that right?
c: Yes.
c: Could you add caramel syrup to it?
""",
        "P C M",
        items=[
            I(
                "latte",
                1,
                "small",
                ["a small latte", "add caramel syrup to it"],
                [add("caramel_syrup", "add caramel syrup")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q=["I'll pay cash", "with a 20"],
        change=2000,
        name="Leah",
    ),
    X(
        "syn-t7-0071",
        """
c: is the thick crust really thick? 🍕
b: It's about an inch, soft and chewy!
c: perfect, small meat lovers no sausage w olives on thick crust + the one i always get, asap, card
""",
        "Q P",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                "small",
                ["small meat lovers no sausage w olives on thick crust"],
                [
                    rm("sausage", "no sausage"),
                    add("olives", "w olives"),
                    add("crust_thick", "on thick crust"),
                ],
            ),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0072",
        """
c: cheeseburger
c: n a bacon burger, does it come w cheese? n a vanilla shake
b: Yes, the Bacon Burger comes with cheese.
c: cool
c: pickup grace
c: cash, have a 20
""",
        "P P/Q S P P",
        items=[
            I("cheeseburger", 1, "single", ["cheeseburger"]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("milkshake", 1, "vanilla", ["a vanilla shake"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "have a 20"],
        change=2000,
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0073",
        """
c: 2 medium hawaiians
c: are the banana peppers hot?
b: They're mild and tangy.
c: ok
c: + breadsticks
c: 499 cedar hill ct delivery at 10:30, card
c: add banana peppers to both hawaiians
""",
        "P Q S P P M",
        items=[
            I(
                "hawaiian_pizza",
                2,
                "medium",
                ["2 medium hawaiians", "add banana peppers to both hawaiians"],
                [add("banana_peppers", "add banana peppers")],
            ),
            I("breadsticks", 1, None, ["breadsticks"]),
        ],
        method="delivery",
        method_q="delivery",
        time=("clock_time", "at 10:30", "22:30"),
        addr={"raw": "499 cedar hill ct", "number": "499", "street": "cedar hill ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0074",
        """
c: LARGE AMERICANO WITH ALMOND MILK, 2 MEDIUM CAPPUCCINOS WITH CARAMEL
c: DO YOU HAVE SKIM?
b: Yes, we have skim milk.
c: 2 SMALL VANILLA LATTES WITH SKIM AND 2 CROISSANTS
b: Got it: 1 large Americano with almond milk, 2 medium Cappuccinos with caramel, 2 small vanilla Lattes with skim milk and 2 plain Croissants. Is that right?
c: YES
c: ACTUALLY NO CROISSANTS
""",
        "P Q P C M",
        items=[
            I(
                "americano",
                1,
                "large",
                ["LARGE AMERICANO WITH ALMOND MILK"],
                [add("almond_milk", "WITH ALMOND MILK")],
            ),
            I(
                "cappuccino",
                2,
                "medium",
                ["2 MEDIUM CAPPUCCINOS WITH CARAMEL"],
                [add("caramel_syrup", "WITH CARAMEL")],
            ),
            I(
                "latte",
                2,
                "small",
                ["2 SMALL VANILLA LATTES WITH SKIM"],
                [add("vanilla_syrup", "VANILLA"), sub("whole_milk", "skim_milk", "WITH SKIM")],
            ),
        ],
    ),
    X(
        "syn-t7-0075",
        """
c: small hawaiian on gluten free
c: pickup
c: maya
c: card
c: actually swap that for a large supreme
""",
        "P P P P M",
        items=[I("supreme_pizza", 1, "large", ["a large supreme"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0076",
        """
c: Hi, a margherita with anchovies, 2 orders of breadsticks and same as last time, delivered to 3 Dover Ct. Card.
""",
        "P",
        items=[
            I(
                "margherita_pizza",
                1,
                None,
                ["a margherita with anchovies"],
                [add("anchovies", "with anchovies")],
            ),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I(
                None,
                1,
                None,
                ["same as last time"],
                unmatched="same as last time",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="delivered to 3 Dover Ct",
        addr={"raw": "3 Dover Ct", "number": "3", "street": "Dover Ct"},
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t7-0077",
        """
c: SMALL CAPPUCCINO WITH HAZELNUT AND A SMALL HOT CHOCOLATE WITH SKIM
c: A BACON EGG AND CHEESE AND 2 PLAIN BAGELS
c: ASAP PLEASE
""",
        "P P P",
        items=[
            I(
                "cappuccino",
                1,
                "small",
                ["SMALL CAPPUCCINO WITH HAZELNUT"],
                [add("hazelnut_syrup", "WITH HAZELNUT")],
            ),
            I(
                "hot_chocolate",
                1,
                "small",
                ["A SMALL HOT CHOCOLATE WITH SKIM"],
                [sub("whole_milk", "skim_milk", "WITH SKIM")],
            ),
            I("breakfast_sandwich", 1, "english_muffin", ["A BACON EGG AND CHEESE"]),
            I("bagel", 2, "plain", ["2 PLAIN BAGELS"]),
        ],
        time=("asap", "ASAP", None),
    ),
    X(
        "syn-t7-0078",
        """
c: medium americano w vanilla, card
b: Got it: 1 medium Americano with vanilla syrup, paying by card. Is that right?
c: yes
c: oh can u make it w oat milk
""",
        "P C M",
        items=[
            I(
                "americano",
                1,
                "medium",
                ["medium americano w vanilla", "make it w oat milk"],
                [add("vanilla_syrup", "w vanilla"), add("oat_milk", "w oat milk")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0079",
        """
c: medium americano
c: w hazelnut
c: pickup at 12:30
c: tom
c: cash
""",
        "P P P P P",
        items=[
            I(
                "americano",
                1,
                "medium",
                ["medium americano", "w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:30", "12:30"),
        pay="cash",
        pay_q="cash",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0080",
        """
c: hey can i get a
c: ,,mmn
""",
        "U U",
    ),
    X(
        "syn-t7-0081",
        """
c: sprite n a cheeseburger
c: pickup at 7:30 for grace
c: card
""",
        "P P P",
        items=[
            I("sprite", 1, None, ["sprite"]),
            I("cheeseburger", 1, "single", ["a cheeseburger"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:30", "19:30"),
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0082",
        """
c: some muffins
c: n a medium latte
c: card
c: in 20 min
c: thx
""",
        "P P P P S",
        items=[
            I("muffin", None, None, ["some muffins"]),
            I("latte", 1, "medium", ["a medium latte"]),
        ],
        time=("relative", "in 20 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0083",
        """
c: 2 bagels n a bec
c: pickup in 20 for jordan
c: card
""",
        "P P P",
        items=[
            I("bagel", 2, None, ["2 bagels"]),
            I("breakfast_sandwich", 1, "english_muffin", ["a bec"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t7-0084",
        """
c: 2 cheezburgers w mayo
c: n smth cold to drink
b: We have Coke, Sprite, lemonade and milkshakes. Which would you like?
c: lemonade
c: at 2:30, cash, i have a 20
""",
        "P P P P",
        items=[
            I("cheeseburger", 2, "single", ["2 cheezburgers w mayo"], [add("mayo", "w mayo")]),
            I("lemonade", 1, None, ["lemonade"]),
        ],
        time=("clock_time", "at 2:30", "14:30"),
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0085",
        """
c: cheeseburger no onions n 2 cokes asap 🍔 card
c: wait swap the burger for onion rings 🧅
""",
        "P M",
        items=[
            I("onion_rings", 1, None, ["onion rings"]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0086",
        """
c: 6 everything bagels, 4 w butter, a drip n 3 banana nut muffins ☕
c: pickup for ana 😊
""",
        "P P",
        items=[
            I("bagel", 2, "everything", ["6 everything bagels"]),
            I("bagel", 4, "everything", ["6 everything bagels", "4 w butter"], [add("butter", "w butter")]),
            I("drip_coffee", 1, "medium", ["a drip"]),
            I("muffin", 3, "banana_nut", ["3 banana nut muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0087",
        """
c: Hi!
c: Can I place an order for Monday? A large pepperoni and 3 large Hawaiians delivered to 24 Birch Pl, paying by card.
""",
        "S P",
        items=[
            I("pepperoni_pizza", 1, "large", ["A large pepperoni"]),
            I("hawaiian_pizza", 3, "large", ["3 large Hawaiians"]),
        ],
        method="delivery",
        method_q="delivered to 24 Birch Pl",
        time=("ambiguous", "for Monday"),
        day=("weekday", "mon", "Monday"),
        addr={"raw": "24 Birch Pl", "number": "24", "street": "Birch Pl"},
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t7-0088",
        """
c: hey
c: 5 cheeseburgers
c: singles
c: 2 no onions
c: does the bacon burger have cheese
b: Yes, it comes with cheese.
c: ok 1 bacon burger too
c: cash
c: thats it
""",
        "S P P P Q P P S",
        items=[
            I("cheeseburger", 3, "single", ["5 cheeseburgers", "singles"]),
            I(
                "cheeseburger",
                2,
                "single",
                ["5 cheeseburgers", "singles", "2 no onions"],
                [rm("onion", "no onions")],
            ),
            I("bacon_burger", 1, None, ["1 bacon burger"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0089",
        """
c: Hi, 2 bacon burgers, 2 veggie burgers with bacon, and same as last time for my brother. Delivery please.
""",
        "P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("veggie_burger", 2, None, ["2 veggie burgers with bacon"], [add("bacon", "with bacon")]),
            I(
                None,
                1,
                None,
                ["same as last time"],
                unmatched="same as last time",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="Delivery",
    ),
    X(
        "syn-t7-0090",
        """
c: 4 large bbq chicken, one w no cheese
c: 2 personal cheese on thick crust n a personal pepperoni
c: to 41 dover way, card
""",
        "P P P",
        items=[
            I("bbq_chicken_pizza", 3, "large", ["4 large bbq chicken"]),
            I(
                "bbq_chicken_pizza",
                1,
                "large",
                ["4 large bbq chicken", "one w no cheese"],
                [rm("cheese", "no cheese")],
            ),
            I(
                "cheese_pizza",
                2,
                "personal",
                ["2 personal cheese on thick crust"],
                [add("crust_thick", "on thick crust")],
            ),
            I("pepperoni_pizza", 1, "personal", ["a personal pepperoni"]),
        ],
        method="delivery",
        method_q="to 41 dover way",
        addr={"raw": "41 dover way", "number": "41", "street": "dover way"},
        pay="card",
        pay_q="card",
    ),
]
