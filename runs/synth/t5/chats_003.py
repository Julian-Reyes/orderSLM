"""t5 entries 0041–0070 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0041",
        """
c: hey 👋 can i get a 32 oz lemonade 🍋
c: asap pls!
c: thank u
""",
        "P P S",
        items=[I("lemonade", 1, None, ["a 32 oz lemonade"], unmatched_variant="32 oz")],
        time=("asap", "asap", None),
    ),
    X(
        "syn-t5-0042",
        """
c: good morning 🌞
c: 6 sesame bagels, 2 w butter pls 🥯 + a coffee w hazelnut + a breakfast sandwich, no bacon but add avocado 🥑
c: pickup for sam, paying cash
""",
        "S P P",
        items=[
            I("bagel", 4, "sesame", ["6 sesame bagels"]),
            I("bagel", 2, "sesame", ["6 sesame bagels", "2 w butter"], [add("butter", "w butter")]),
            I("drip_coffee", 1, None, ["a coffee"], [add("hazelnut_syrup", "w hazelnut")]),
            I(
                "breakfast_sandwich",
                1,
                None,
                ["a breakfast sandwich"],
                [rm("bacon", "no bacon"), add("avocado", "add avocado")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="paying cash",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t5-0043",
        """
c: hiya 🥐 a croissant w butter and 2 hot chocolates with oat milk pls
c: pickup for eli ☺️
""",
        "P P",
        items=[
            I("croissant", 1, None, ["a croissant"], [add("butter", "w butter")]),
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocolates"],
                [sub("whole_milk", "oat_milk", "with oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t5-0044",
        """
c: heyyy ☕
c: 1 choc chip muffin and 2 medium lattes, almond pls
c: pickup, jordan, card 💳
""",
        "S P P",
        items=[
            I("muffin", 1, "chocolate_chip", ["1 choc chip muffin"]),
            I("latte", 2, "medium", ["2 medium lattes"], [sub("whole_milk", "almond_milk", "almond pls")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t5-0045",
        """
c: 4 breakfast sandwiches on croissant no cheese and an 8 oz americano w oat milk, pickup asap for keisha, card
""",
        "P",
        items=[
            I(
                "breakfast_sandwich",
                4,
                "croissant",
                ["4 breakfast sandwiches on croissant"],
                [rm("cheddar", "no cheese")],
            ),
            I("americano", 1, "small", ["an 8 oz americano"], [add("oat_milk", "w oat milk")]),
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
        "syn-t5-0046",
        """
c: GOOD MORNING! I'D LIKE TO PLACE AN ORDER FOR MY BOOK CLUB!
""",
        "P",
    ),
    X(
        "syn-t5-0047",
        """
c: Hi there.
c: I'd like two bacon burgers.
c: One of them with mayo, please.
c: Also two chocolate milkshakes.
c: Please deliver to 40 Dover St.
c: I'll pay cash.
""",
        "S P P P P P",
        items=[
            I("bacon_burger", 1, None, ["two bacon burgers"]),
            I(
                "bacon_burger",
                1,
                None,
                ["two bacon burgers", "One of them with mayo"],
                [add("mayo", "with mayo")],
            ),
            I("milkshake", 2, "chocolate", ["two chocolate milkshakes"]),
        ],
        method="delivery",
        method_q="deliver to 40 Dover St",
        addr={"raw": "40 Dover St", "number": "40", "street": "Dover St"},
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t5-0048",
        """
c: hey
c: chocolate shake
c: fries
c: lemonade
c: pickup
c: wait make the shake strawberry
""",
        "S P P P P M",
        items=[
            I("milkshake", 1, "strawberry", ["chocolate shake", "make the shake strawberry"]),
            I("fries", 1, None, ["fries"]),
            I("lemonade", 1, None, ["lemonade"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t5-0049",
        """
c: can i get a medium margherita thin crust, a medium pepperoni no cheese w stuffed crust, 2 orders of garlic knots n a sprite. pickup for ana, card
c: nvm on the sprite
""",
        "P M",
        items=[
            I("margherita_pizza", 1, "medium", ["a medium margherita"], [add("crust_thin", "thin crust")]),
            I(
                "pepperoni_pizza",
                1,
                "medium",
                ["a medium pepperoni"],
                [rm("cheese", "no cheese"), add("crust_stuffed", "w stuffed crust")],
            ),
            I("garlic_knots", 2, None, ["2 orders of garlic knots"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t5-0050",
        """
c: yo
c: order of breadsticks
c: and same as last time
c: in like 30 min
c: thx
""",
        "S P P P S",
        items=[
            I("breadsticks", 1, None, ["order of breadsticks"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        time=("relative", "in like 30 min", None),
    ),
    X(
        "syn-t5-0051",
        """
c: Hello, I'd like three bacon burgers, two of them without pickles.
c: Three orders of onion rings as well.
c: And a veggie burger with jalapeños.
c: I'll pay cash, and I'll need change for a 20.
""",
        "P P P P",
        items=[
            I("bacon_burger", 1, None, ["three bacon burgers"]),
            I(
                "bacon_burger",
                2,
                None,
                ["three bacon burgers", "two of them without pickles"],
                [rm("pickle", "without pickles")],
            ),
            I("onion_rings", 3, None, ["Three orders of onion rings"]),
            I("veggie_burger", 1, None, ["a veggie burger"], [add("jalapeno", "with jalapeños")]),
        ],
        pay="cash",
        pay_q=["pay cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0052",
        """
c: DO YOU GUYS HAVE ANCHOVIES?
b: We do!
c: OK SOME BREADSTICKS AND FOUR LARGE HAWAIIANS, NO SAUCE, ADD ANCHOVIES! DELIVERY, CARD!
""",
        "Q P",
        items=[
            I("breadsticks", None, None, ["SOME BREADSTICKS"]),
            I(
                "hawaiian_pizza",
                4,
                "large",
                ["FOUR LARGE HAWAIIANS"],
                [rm("tomato_sauce", "NO SAUCE"), add("anchovies", "ADD ANCHOVIES")],
            ),
        ],
        method="delivery",
        method_q="DELIVERY",
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0053",
        """
c: hey can i put in an order for my roommates
""",
        "P",
    ),
    X(
        "syn-t5-0054",
        """
c: Hi, is the lemonade fresh?
b: It's made in-house every morning!
c: Great, then one lemonade and four orders of fries, please.
c: Pickup, cash, name is June.
c: Actually, please remove the fries.
""",
        "Q P P M",
        items=[I("lemonade", 1, None, ["one lemonade"])],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q="cash",
        name="June",
    ),
    X(
        "syn-t5-0055",
        """
c: can i get a diet coke, a small cheese no sauce w mushrooms stuffed crust, 3 small meat lovers no sausage stuffed crust, and the usual. cash
""",
        "P",
        items=[
            I("diet_coke", 1, None, ["a diet coke"]),
            I(
                "cheese_pizza",
                1,
                "small",
                ["a small cheese"],
                [
                    rm("tomato_sauce", "no sauce"),
                    add("mushrooms", "w mushrooms"),
                    add("crust_stuffed", "stuffed crust"),
                ],
            ),
            I(
                "meat_lovers_pizza",
                3,
                "small",
                ["3 small meat lovers"],
                [rm("sausage", "no sausage"), add("crust_stuffed", "stuffed crust")],
            ),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0056",
        """
c: DOES THE SUPREME COME WITH OLIVES?
b: Yes, black olives are on the Supreme.
c: COOL, TWO SUPREMES WITH OLIVE OIL ON TOP! PICKUP, CARD!
""",
        "Q P",
        items=[I("supreme_pizza", 2, None, ["TWO SUPREMES"], [add("olive_oil", "WITH OLIVE OIL")])],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0057",
        """
c: veggie pizza w ham
c: and the one i always get
c: 72 chestnut terrace
c: cash, change for a 20
c: in 40 min
""",
        "P P P P P",
        items=[
            I("veggie_pizza", 1, None, ["veggie pizza"], [add("ham", "w ham")]),
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
        method_q="72 chestnut terrace",
        time=("relative", "in 40 min", None),
        addr={"raw": "72 chestnut terrace", "number": "72", "street": "chestnut terrace"},
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0058",
        """
c: 5 bacon burgers
c: 1 no tomato
c: and fries
c: pickup at 6:30, leah
c: cash
""",
        "P P P P P",
        items=[
            I("bacon_burger", 4, None, ["5 bacon burgers"]),
            I("bacon_burger", 1, None, ["5 bacon burgers", "1 no tomato"], [rm("tomato", "no tomato")]),
            I("fries", 1, None, ["fries"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "6:30", "18:30"),
        pay="cash",
        pay_q="cash",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t5-0059",
        """
c: 2 supremes for pickup
c: ready in 25?
""",
        "P P",
        items=[I("supreme_pizza", 2, None, ["2 supremes"])],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in 25", None),
    ),
    X(
        "syn-t5-0060",
        """
c: HELLO! SIX MEDIUM AMERICANOS PLEASE!
c: FOUR OF THEM WITH HAZELNUT!
c: AND TWO BLUEBERRY MUFFINS!
c: PICKUP AT 9 FOR PRIYA!
c: CARD!
""",
        "P P P P P",
        items=[
            I("americano", 2, "medium", ["SIX MEDIUM AMERICANOS"]),
            I(
                "americano",
                4,
                "medium",
                ["SIX MEDIUM AMERICANOS", "FOUR OF THEM WITH HAZELNUT"],
                [add("hazelnut_syrup", "WITH HAZELNUT")],
            ),
            I("muffin", 2, "blueberry", ["TWO BLUEBERRY MUFFINS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 9", "09:00"),
        pay="card",
        pay_q="CARD",
        name="Priya",
        name_q="PRIYA",
    ),
    X(
        "syn-t5-0061",
        """
c: hey can i get 2 large hot chocolates w almond milk n a sesame bagel
c: pickup for keisha, card
b: 2 large hot chocolates with almond milk and a sesame bagel, pickup for Keisha, card. Sound good?
c: yep
c: actually skip the bagel
""",
        "P P C M",
        items=[
            I(
                "hot_chocolate",
                2,
                "large",
                ["2 large hot chocolates"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t5-0062",
        """
c: 3 almond croissants
c: 1 w butter
c: 2 large lattes
c: banana nut muffin
c: 2 breakfast sandwiches on english muffin
c: asap, card
""",
        "P P P P P P",
        items=[
            I("croissant", 2, "almond", ["3 almond croissants"]),
            I("croissant", 1, "almond", ["3 almond croissants", "1 w butter"], [add("butter", "w butter")]),
            I("latte", 2, "large", ["2 large lattes"]),
            I("muffin", 1, "banana_nut", ["banana nut muffin"]),
            I("breakfast_sandwich", 2, "english_muffin", ["2 breakfast sandwiches on english muffin"]),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0063",
        """
c: hii
c: ordering lunch for the team
""",
        "S P",
    ),
    X(
        "syn-t5-0064",
        """
c: HEY!
c: THREE VEGGIE BURGERS
c: TWO OF THEM NO MAYO
c: IS THE VEGGIE BURGER VEGAN?
b: The patty is plant-based, but it comes with mayo.
c: OK COOL. TWO SPRITES TOO
c: AND A CHEESEBURGER NO LETTUCE ADD BACON
c: AND A COKE
""",
        "S P P Q P P P",
        items=[
            I("veggie_burger", 1, None, ["THREE VEGGIE BURGERS"]),
            I(
                "veggie_burger",
                2,
                None,
                ["THREE VEGGIE BURGERS", "TWO OF THEM NO MAYO"],
                [rm("mayo", "NO MAYO")],
            ),
            I("sprite", 2, None, ["TWO SPRITES"]),
            I(
                "cheeseburger",
                1,
                None,
                ["A CHEESEBURGER"],
                [rm("lettuce", "NO LETTUCE"), add("bacon", "ADD BACON")],
            ),
            I("coke", 1, None, ["A COKE"]),
        ],
    ),
    X(
        "syn-t5-0065",
        """
c: Hi, could I get two veggie burgers with mustard and a strawberry milkshake, delivered to 971 Riverside Rd? I'll pay by card.
b: Two veggie burgers with mustard and a strawberry milkshake, delivered to 971 Riverside Rd, paying by card. Is that right?
c: Yes, that's right.
c: Sorry, could you take off the milkshake?
""",
        "P C M",
        items=[I("veggie_burger", 2, None, ["two veggie burgers"], [add("mustard", "with mustard")])],
        method="delivery",
        method_q="delivered to 971 Riverside Rd",
        addr={"raw": "971 Riverside Rd", "number": "971", "street": "Riverside Rd"},
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0066",
        """
c: 2 liter dr pepper
c: to 72 juniper pl #9b
c: by 12:45
c: card
""",
        "P P P P",
        items=[I("dr_pepper", 1, "two_liter", ["2 liter dr pepper"])],
        method="delivery",
        method_q="to 72 juniper pl #9b",
        time=("clock_time", "by 12:45", "12:45"),
        addr={"raw": "72 juniper pl #9b", "number": "72", "street": "juniper pl", "unit": "9b"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0067",
        """
c: good morning! ☕ want to order for our team meeting
""",
        "P",
    ),
    X(
        "syn-t5-0068",
        """
c: Hello!
c: Five cheeseburgers, four of them with bacon, two veggie burgers and fries, delivered as soon as possible to 412 Glenwood Rd. Card, please.
""",
        "S P",
        items=[
            I("cheeseburger", 1, None, ["Five cheeseburgers"]),
            I(
                "cheeseburger",
                4,
                None,
                ["Five cheeseburgers", "four of them with bacon"],
                [add("bacon", "with bacon")],
            ),
            I("veggie_burger", 2, None, ["two veggie burgers"]),
            I("fries", 1, None, ["fries"]),
        ],
        method="delivery",
        method_q="delivered",
        time=("asap", "as soon as possible", None),
        addr={"raw": "412 Glenwood Rd", "number": "412", "street": "Glenwood Rd"},
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t5-0069",
        """
c: hi
c: what sizes is the drip
b: Small 8 oz, medium 12 oz, large 16 oz.
c: ok an 8 oz
c: drip
c: pickup at 10
c: grace
""",
        "S Q P P P P",
        items=[I("drip_coffee", 1, "small", ["an 8 oz", "drip"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10", "10:00"),
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t5-0070",
        """
c: HELLO!!
c: TWO VEGGIE BURGERS AND TWO LEMONADES! PICKUP! CARD!
b: Two veggie burgers and two lemonades for pickup, paying by card. Is that right?
c: YES!
c: NO LEMONADES ACTUALLY!
""",
        "S P C M",
        items=[I("veggie_burger", 2, None, ["TWO VEGGIE BURGERS"])],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
    ),
]
