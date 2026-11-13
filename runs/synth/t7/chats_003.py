"""t7 syn-t7-0031–0060 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t7-0031",
        """
c: HI 2 BACON EGG AND CHEESE ON ENGLISH MUFFINS, NO CHEESE. PICKUP FOR ELI, CARD
b: Got it, Eli: 2 Breakfast Sandwiches on English muffins, no cheese, pickup, paying by card. Is that right?
c: YES
c: SORRY JUST 1 SANDWICH
""",
        "P C M",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["2 BACON EGG AND CHEESE ON ENGLISH MUFFINS, NO CHEESE", "JUST 1 SANDWICH"],
                [rm("cheddar", "NO CHEESE")],
            ),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
        name="Eli",
        name_q="ELI",
    ),
    X(
        "syn-t7-0032",
        """
c: medium bbq chicken, is the bbq sauce sweet or smoky? also a medium pepperoni
b: It's a sweet and smoky BBQ sauce!
c: cool sounds good
""",
        "P/Q S",
        items=[
            I("bbq_chicken_pizza", 1, "medium", ["medium bbq chicken"]),
            I("pepperoni_pizza", 1, "medium", ["a medium pepperoni"]),
        ],
    ),
    X(
        "syn-t7-0033",
        """
c: hey
c: lg americano
c: do u have banana muffins
b: Yes, banana nut!
c: 2 of those
c: pickup
c: at 12:45
c: omar
c: cash
""",
        "S P Q P P P P P",
        items=[
            I("americano", 1, "large", ["lg americano"]),
            I("muffin", 2, "banana_nut", ["banana muffins", "2 of those"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:45", "12:45"),
        pay="cash",
        pay_q="cash",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t7-0034",
        """
c: hey 👋
c: 3 regular fries, are ur burgers fresh or frozen? n 3 cheeseburgers 🍔 to 500 oak ave
b: Our patties are made fresh every day!
c: awesome 😋
""",
        "S P/Q S",
        items=[
            I("fries", 3, "regular", ["3 regular fries"]),
            I("cheeseburger", 3, "single", ["3 cheeseburgers"]),
        ],
        method="delivery",
        method_q="to 500 oak ave",
        addr={"raw": "500 oak ave", "number": "500", "street": "oak ave"},
    ),
    X(
        "syn-t7-0035",
        """
c: lemme get a large plain pie
c: and a big meat, medium
""",
        "P P",
        items=[
            I("cheese_pizza", 1, "large", ["a large plain pie"]),
            I("meat_lovers_pizza", 1, "medium", ["a big meat, medium"]),
        ],
    ),
    X(
        "syn-t7-0036",
        """
c: Hi, could I get two dou
""",
        "U",
    ),
    X(
        "syn-t7-0037",
        """
c: hey big order for the office
c: 2 bacon burgers no onions n a veggie burger no lettuce
c: 4 large fries, 3 onion rings
c: 3 lemonades
c: deliver to 51 hollis ave apt 14
c: card
""",
        "P P P P P P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers no onions"], [rm("onion", "no onions")]),
            I("veggie_burger", 1, None, ["a veggie burger no lettuce"], [rm("lettuce", "no lettuce")]),
            I("fries", 4, "large", ["4 large fries"]),
            I("onion_rings", 3, None, ["3 onion rings"]),
            I("lemonade", 3, None, ["3 lemonades"]),
        ],
        method="delivery",
        method_q="deliver to 51 hollis ave",
        addr={"raw": "51 hollis ave apt 14", "number": "51", "street": "hollis ave", "unit": "apt 14"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0038",
        """
c: hey
c: 4 xl pepperonis to 1840 chestnut terrace in 45 min, card
c: actually swap the pizzas for 2 orders of garlic knots
""",
        "S P M",
        items=[I("garlic_knots", 2, None, ["2 orders of garlic knots"])],
        method="delivery",
        method_q="to 1840 chestnut terrace",
        time=("relative", "in 45 min", None),
        addr={"raw": "1840 chestnut terrace", "number": "1840", "street": "chestnut terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0039",
        """
c: yo
c: the one i always get
b: Hi! We can't see past orders here, sorry. What would you like?
c: 2 double cbs 2 veggie burgers
c: 2 fries n a sprite
c: deliver to 44 sunset ave, card
""",
        "S P P P P",
        items=[
            I("cheeseburger", 2, "double", ["2 double cbs"]),
            I("veggie_burger", 2, None, ["2 veggie burgers"]),
            I("fries", 2, "regular", ["2 fries"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="delivery",
        method_q="deliver to 44 sunset ave",
        addr={"raw": "44 sunset ave", "number": "44", "street": "sunset ave"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0040",
        """
c: HELLO
c: 6 MEDIUM PEPPERONI, 5 OF THEM WITH EXTRA CHEESE. ALSO 3 MEDIUM BBQ CHICKEN WITH MUSHROOMS ON STUFFED CRUST. DELIVER TO 6848 GLENWOOD RD IN AN HOUR, CASH
""",
        "S P",
        items=[
            I("pepperoni_pizza", 1, "medium", ["6 MEDIUM PEPPERONI"]),
            I(
                "pepperoni_pizza",
                5,
                "medium",
                ["6 MEDIUM PEPPERONI", "5 OF THEM WITH EXTRA CHEESE"],
                [add("cheese", "WITH EXTRA CHEESE", amount="extra")],
            ),
            I(
                "bbq_chicken_pizza",
                3,
                "medium",
                ["3 MEDIUM BBQ CHICKEN WITH MUSHROOMS ON STUFFED CRUST"],
                [add("mushrooms", "WITH MUSHROOMS"), add("crust_stuffed", "ON STUFFED CRUST")],
            ),
        ],
        method="delivery",
        method_q="DELIVER TO 6848 GLENWOOD RD",
        time=("relative", "IN AN HOUR", None),
        addr={"raw": "6848 GLENWOOD RD", "number": "6848", "street": "GLENWOOD RD"},
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t7-0041",
        """
c: Hi, I'd like 3 chocolate chip muffins and 2 large lattes. Is the caramel syrup house-made? If not that's fine, I'll still take a large cappuccino with caramel.
b: It's not made in house, but it's a favorite!
c: Great. Pickup under June.
""",
        "P/Q P",
        items=[
            I("muffin", 3, "chocolate_chip", ["3 chocolate chip muffins"]),
            I("latte", 2, "large", ["2 large lattes"]),
            I(
                "cappuccino",
                1,
                "large",
                ["a large cappuccino with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        name="June",
    ),
    X(
        "syn-t7-0042",
        """
c: hey
c: can i get some small supremes w anchovies on thin crust n an iced tea, pickup
""",
        "S P",
        items=[
            I(
                "supreme_pizza",
                None,
                "small",
                ["some small supremes w anchovies on thin crust"],
                [add("anchovies", "w anchovies"), add("crust_thin", "on thin crust")],
            ),
            I("iced_tea", 1, "can", ["an iced tea"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t7-0043",
        """
c: hiya
c: 6 large lattes
c: is the hazelnut sweet?
b: It's a classic sweet hazelnut syrup.
c: ok 4 of the lattes w hazelnut then
c: + 3 medium americanos, cash
""",
        "S P Q P P",
        items=[
            I("latte", 2, "large", ["6 large lattes"]),
            I(
                "latte",
                4,
                "large",
                ["6 large lattes", "4 of the lattes w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("americano", 3, "medium", ["3 medium americanos"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0044",
        """
c: 2 cheeseburgers one no ketchup, do the rings come w sauce? + a large fries
b: Onion rings come plain, but we have ketchup and mustard.
c: ok add rings too. pickup 9:30 for ana, card
""",
        "P/Q P",
        items=[
            I("cheeseburger", 1, "single", ["2 cheeseburgers"]),
            I(
                "cheeseburger",
                1,
                "single",
                ["2 cheeseburgers", "one no ketchup"],
                [rm("ketchup", "no ketchup")],
            ),
            I("fries", 1, "large", ["a large fries"]),
            I("onion_rings", 1, None, ["add rings"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "9:30", "21:30"),
        pay="card",
        pay_q="card",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0045",
        """
c: hi ☕ 5 medium lattes, 2 of them w whipped cream
c: do u have hazelnut? 🌰
b: Yes, hazelnut syrup!
c: yay 4 large hot chocs w hazelnut + a bec 🥓 pickup leah, card
""",
        "P Q P",
        items=[
            I("latte", 3, "medium", ["5 medium lattes"]),
            I(
                "latte",
                2,
                "medium",
                ["5 medium lattes", "2 of them w whipped cream"],
                [add("whipped_cream", "w whipped cream")],
            ),
            I(
                "hot_chocolate",
                4,
                "large",
                ["4 large hot chocs w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("breakfast_sandwich", 1, "english_muffin", ["a bec"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t7-0046",
        """
c: veggie pizza w sausage, a 20 oz iced tea n garlic knots
c: card
""",
        "P P",
        items=[
            I("veggie_pizza", 1, None, ["veggie pizza w sausage"], [add("sausage", "w sausage")]),
            I("iced_tea", 1, "bottle_20oz", ["a 20 oz iced tea"]),
            I("garlic_knots", 1, None, ["garlic knots"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0047",
        """
c: 5 cheeseburgers
c: 3 no lettuce
c: large fries
c: coke n onion rings
c: pickup
""",
        "P P P P P",
        items=[
            I("cheeseburger", 2, "single", ["5 cheeseburgers"]),
            I(
                "cheeseburger",
                3,
                "single",
                ["5 cheeseburgers", "3 no lettuce"],
                [rm("lettuce", "no lettuce")],
            ),
            I("fries", 1, "large", ["large fries"]),
            I("coke", 1, None, ["coke"]),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t7-0048",
        """
c: LARGE HAWAIIAN WITH SHRIMP AND A SPRITE TO 624 BROOKSIDE AVE
""",
        "P",
        items=[
            I("hawaiian_pizza", 1, "large", ["LARGE HAWAIIAN WITH SHRIMP"], [offmod("WITH SHRIMP")]),
            I("sprite", 1, "can", ["A SPRITE"]),
        ],
        method="delivery",
        method_q="TO 624 BROOKSIDE AVE",
        addr={"raw": "624 BROOKSIDE AVE", "number": "624", "street": "BROOKSIDE AVE"},
    ),
    X(
        "syn-t7-0049",
        """
c: hey 🍕 2 large veggies
c: n which of ur sides is the best?
b: Garlic Knots and Breadsticks are both favorites!
c: ok one of those 😊 card
""",
        "P Q P",
        items=[
            I("veggie_pizza", 2, "large", ["2 large veggies"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0050",
        """
c: sprite
c: n a double cheeseburger
c: deliver to 69 glenwood ave apt 6a
c: at 9
c: cash, i have a 20
c: thx
""",
        "P P P P P S",
        items=[
            I("sprite", 1, None, ["sprite"]),
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
        ],
        method="delivery",
        method_q="deliver to 69 glenwood ave",
        time=("clock_time", "at 9", "21:00"),
        addr={"raw": "69 glenwood ave apt 6a", "number": "69", "street": "glenwood ave", "unit": "apt 6a"},
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0051",
        """
c: Hi there.
c: Same as last time, please.
b: Sorry, we can't see past orders here. What would you like?
c: Of course. An extra large margherita, 2 medium BBQ chicken pizzas, a Coke and 2 iced teas. Pickup at 10:30 for Dev, cash.
""",
        "S P P",
        items=[
            I("margherita_pizza", 1, "extra_large", ["An extra large margherita"]),
            I("bbq_chicken_pizza", 2, "medium", ["2 medium BBQ chicken pizzas"]),
            I("coke", 1, "can", ["a Coke"]),
            I("iced_tea", 2, "can", ["2 iced teas"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 10:30", "22:30"),
        pay="cash",
        pay_q="cash",
        name="Dev",
    ),
    X(
        "syn-t7-0052",
        """
c: the usual pls ☕ for grace, pickup
b: Hi Grace! We can't see past orders here, sorry. What's your usual?
c: oh 😅 an everything bagel, a large americano w vanilla, a medium cap n a blueberry muffin
""",
        "P P",
        items=[
            I("bagel", 1, "everything", ["an everything bagel"]),
            I("americano", 1, "large", ["a large americano w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("cappuccino", 1, "medium", ["a medium cap"]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0053",
        """
c: choc shake
c: single cheeseburger w chili
c: to 19 grant blvd #8a
c: in 30 min
c: card
""",
        "P P P P P",
        items=[
            I("milkshake", 1, "chocolate", ["choc shake"]),
            I("cheeseburger", 1, "single", ["single cheeseburger w chili"], [offmod("w chili")]),
        ],
        method="delivery",
        method_q="to 19 grant blvd",
        time=("relative", "in 30 min", None),
        addr={"raw": "19 grant blvd #8a", "number": "19", "street": "grant blvd", "unit": "#8a"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0054",
        """
c: HI
c: CAN I GET A BIG BOTTLE OF DIET
b: Our biggest is the Diet Coke 2-liter. Would you like that?
c: YES THE 2 LITER. AND A MEDIUM PEPPERONI. CARD
""",
        "S P P",
        items=[
            I("diet_coke", 1, "two_liter", ["A BIG BOTTLE OF DIET", "THE 2 LITER"]),
            I("pepperoni_pizza", 1, "medium", ["A MEDIUM PEPPERONI"]),
        ],
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0055",
        """
c: vanilla shake n a sprite to 60 dover way apt 28c
c: in 20 min
c: oh scratch the sprite
""",
        "P P M",
        items=[I("milkshake", 1, "vanilla", ["vanilla shake"])],
        method="delivery",
        method_q="to 60 dover way",
        time=("relative", "in 20 min", None),
        addr={"raw": "60 dover way apt 28c", "number": "60", "street": "dover way", "unit": "apt 28c"},
    ),
    X(
        "syn-t7-0056",
        """
c: Hi, can I get 4 bacon egg and cheese sandwiches on croissants?
c: Two of them with avocado.
c: And a large latte.
c: Pickup, name Maya.
""",
        "P P P P",
        items=[
            I("breakfast_sandwich", 2, "croissant", ["4 bacon egg and cheese sandwiches on croissants"]),
            I(
                "breakfast_sandwich",
                2,
                "croissant",
                ["4 bacon egg and cheese sandwiches on croissants", "Two of them with avocado"],
                [add("avocado", "with avocado")],
            ),
            I("latte", 1, "large", ["a large latte"]),
        ],
        method="pickup",
        method_q="Pickup",
        name="Maya",
    ),
    X(
        "syn-t7-0057",
        """
c: 2 cokes n a bacon burger for pickup at 8, tom
c: cash, paying w a 20
""",
        "P P",
        items=[
            I("coke", 2, None, ["2 cokes"]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8", "20:00"),
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0058",
        """
c: do your cappuccinos have a lot of foam?
b: A classic amount, and we can do extra foam if you'd like.
c: ok 2 cappuccinos, pickup for rosa, card
""",
        "Q P",
        items=[I("cappuccino", 2, None, ["2 cappuccinos"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t7-0059",
        """
c: 2 double cbs
c: 1 w avocado
c: 2 cokes
c: in 15
""",
        "P P P P",
        items=[
            I("cheeseburger", 1, "double", ["2 double cbs"]),
            I("cheeseburger", 1, "double", ["2 double cbs", "1 w avocado"], [add("avocado", "w avocado")]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        time=("relative", "in 15", None),
    ),
    X(
        "syn-t7-0060",
        """
c: hi, 2 muffins and that thing from before, pickup for omar
""",
        "P",
        items=[
            I("muffin", 2, None, ["2 muffins"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Omar",
        name_q="omar",
    ),
]
