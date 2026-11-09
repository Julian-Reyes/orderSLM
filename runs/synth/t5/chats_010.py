"""t5 entries 0251–0275 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0251",
        """
c: heyy
c: some croissants, a large americano w oat milk n an everything bagel, card
""",
        "S P",
        items=[
            I("croissant", None, None, ["some croissants"]),
            I("americano", 1, "large", ["a large americano"], [add("oat_milk", "w oat milk")]),
            I("bagel", 1, "everything", ["an everything bagel"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0252",
        """
c: yo ordering for the squad
""",
        "P",
    ),
    X(
        "syn-t5-0253",
        """
c: Can I get tomatoes on a meat lovers?
b: Yes, tomatoes can go on any pizza.
c: Then a few medium meat lovers with tomatoes on stuffed crust, and a personal BBQ chicken with no cheese.
c: Pickup as soon as possible, for Omar.
""",
        "Q P P",
        items=[
            I(
                "meat_lovers_pizza",
                None,
                "medium",
                ["a few medium meat lovers"],
                [add("tomatoes", "with tomatoes"), add("crust_stuffed", "on stuffed crust")],
            ),
            I("bbq_chicken_pizza", 1, "personal", ["a personal BBQ chicken"], [rm("cheese", "no cheese")]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("asap", "as soon as possible", None),
        name="Omar",
    ),
    X(
        "syn-t5-0254",
        """
c: bacon burger no cheese n 3 lemonades to 92 elm terrace in 30, card
b: A bacon burger with no cheese and 3 lemonades to 92 Elm Terrace in 30 minutes, card. Correct?
c: yep
c: actually no lemonades
""",
        "P C M",
        items=[I("bacon_burger", 1, None, ["bacon burger"], [rm("cheese", "no cheese")])],
        method="delivery",
        method_q="to 92 elm terrace",
        time=("relative", "in 30", None),
        addr={"raw": "92 elm terrace", "number": "92", "street": "elm terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0255",
        """
c: 2 breakfast sandwiches on bagels
c: no bacon, add avocado
c: and a medium latte w skim
c: card
""",
        "P P P P",
        items=[
            I(
                "breakfast_sandwich",
                2,
                "bagel",
                ["2 breakfast sandwiches on bagels"],
                [rm("bacon", "no bacon"), add("avocado", "add avocado")],
            ),
            I("latte", 1, "medium", ["a medium latte"], [sub("whole_milk", "skim_milk", "w skim")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0256",
        """
c: some lemonades
c: fries
c: 2 onion rings
c: 478 oak ave
""",
        "P P P P",
        items=[
            I("lemonade", None, None, ["some lemonades"]),
            I("fries", 1, None, ["fries"]),
            I("onion_rings", 2, None, ["2 onion rings"]),
        ],
        method="delivery",
        method_q="478 oak ave",
        addr={"raw": "478 oak ave", "number": "478", "street": "oak ave"},
    ),
    X(
        "syn-t5-0257",
        """
c: hi there ☀️
c: some vanilla lattes, 2 hot chocolates and a breakfast sandwich on an english muffin pls
c: pickup for tara, cash 💵
""",
        "S P P",
        items=[
            I("latte", None, None, ["some vanilla lattes"], [add("vanilla_syrup", "vanilla")]),
            I("hot_chocolate", 2, None, ["2 hot chocolates"]),
            I("breakfast_sandwich", 1, "english_muffin", ["a breakfast sandwich on an english muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t5-0258",
        """
c: A FEW PERSONAL BBQ CHICKEN PIZZAS WITH NO BBQ SAUCE! CASH!
""",
        "P",
        items=[
            I(
                "bbq_chicken_pizza",
                None,
                "personal",
                ["A FEW PERSONAL BBQ CHICKEN PIZZAS"],
                [rm("bbq_sauce", "NO BBQ SAUCE")],
            ),
        ],
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t5-0259",
        """
c: 2 veggie burgers 1 w mustard, a double cheeseburger w avocado and a bacon burger no onions to 21 clement ave
""",
        "P",
        items=[
            I("veggie_burger", 1, None, ["2 veggie burgers"]),
            I("veggie_burger", 1, None, ["2 veggie burgers", "1 w mustard"], [add("mustard", "w mustard")]),
            I("cheeseburger", 1, "double", ["a double cheeseburger"], [add("avocado", "w avocado")]),
            I("bacon_burger", 1, None, ["a bacon burger"], [rm("onion", "no onions")]),
        ],
        method="delivery",
        method_q="to 21 clement ave",
        addr={"raw": "21 clement ave", "number": "21", "street": "clement ave"},
    ),
    X(
        "syn-t5-0260",
        """
c: hey 😊
c: one milkshake please 🥤
c: pickup for leah
c: cash!
""",
        "S P P P",
        items=[I("milkshake", 1, None, ["one milkshake"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t5-0261",
        """
c: Can you add bacon to the veggie burger?
b: Yes, bacon can be added.
c: Okay, two veggie burgers, one of them with bacon, and a cheeseburger, ready in 20 minutes. I'll pay by card.
""",
        "Q P",
        items=[
            I("veggie_burger", 1, None, ["two veggie burgers"]),
            I(
                "veggie_burger",
                1,
                None,
                ["two veggie burgers", "one of them with bacon"],
                [add("bacon", "with bacon")],
            ),
            I("cheeseburger", 1, None, ["a cheeseburger"]),
        ],
        time=("relative", "in 20 minutes", None),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0262",
        """
c: hi
c: small lattes
c: a few
c: card
""",
        "S P P P",
        items=[I("latte", None, "small", ["small lattes", "a few"])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0263",
        """
c: hi! breakfast sandwich on an english muffin + 4 croissants 🥐
c: and same as last time
c: card pls
""",
        "P P P",
        items=[
            I("breakfast_sandwich", 1, "english_muffin", ["breakfast sandwich on an english muffin"]),
            I("croissant", 4, None, ["4 croissants"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0264",
        """
c: do u have mustard
b: Yes, we can add mustard to any burger.
c: nah nvm
c: 2 cheeseburgers 1 no ketchup
c: sprite n vanilla shake
c: 72 clement dr, cash
""",
        "Q S P P P",
        items=[
            I("cheeseburger", 1, None, ["2 cheeseburgers"]),
            I("cheeseburger", 1, None, ["2 cheeseburgers", "1 no ketchup"], [rm("ketchup", "no ketchup")]),
            I("sprite", 1, None, ["sprite"]),
            I("milkshake", 1, "vanilla", ["vanilla shake"]),
        ],
        method="delivery",
        method_q="72 clement dr",
        addr={"raw": "72 clement dr", "number": "72", "street": "clement dr"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0265",
        """
c: THREE BANANA NUT MUFFINS AND TWO EVERYTHING BAGELS WITH TOMATO!
c: THREE MEDIUM LATTES TOO!
c: PICKUP AT 10:30 FOR IVY, CARD!
c: MAKE THE LATTES WITH SKIM MILK INSTEAD!
""",
        "P P P M",
        items=[
            I("muffin", 3, "banana_nut", ["THREE BANANA NUT MUFFINS"]),
            I("bagel", 2, "everything", ["TWO EVERYTHING BAGELS"], [add("tomato", "WITH TOMATO")]),
            I(
                "latte",
                3,
                "medium",
                ["THREE MEDIUM LATTES", "MAKE THE LATTES WITH SKIM MILK INSTEAD"],
                [sub("whole_milk", "skim_milk", "WITH SKIM MILK INSTEAD")],
            ),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 10:30", "10:30"),
        pay="card",
        pay_q="CARD",
        name="Ivy",
        name_q="IVY",
    ),
    X(
        "syn-t5-0266",
        """
c: Hi, could I get a bagel, a small americano with hazelnut, and two chocolate chip muffins as soon as possible? I'll pay by card.
""",
        "P",
        items=[
            I("bagel", 1, None, ["a bagel"]),
            I("americano", 1, "small", ["a small americano"], [add("hazelnut_syrup", "with hazelnut")]),
            I("muffin", 2, "chocolate_chip", ["two chocolate chip muffins"]),
        ],
        time=("asap", "as soon as possible", None),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0267",
        """
c: bacon burger
c: 2 cokes
c: pickup
c: card
c: no cokes actually
""",
        "P P P P M",
        items=[I("bacon_burger", 1, None, ["bacon burger"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0268",
        """
c: A PLAIN CROISSANT, TWO HOT CHOCOLATES WITH NO WHIP, AND A SMALL CARAMEL CAPPUCCINO WITH ALMOND MILK!
c: PICKUP ASAP FOR TOM!
""",
        "P P",
        items=[
            I("croissant", 1, "plain", ["A PLAIN CROISSANT"]),
            I("hot_chocolate", 2, None, ["TWO HOT CHOCOLATES"], [rm("whipped_cream", "NO WHIP")]),
            I(
                "cappuccino",
                1,
                "small",
                ["A SMALL CARAMEL CAPPUCCINO"],
                [add("caramel_syrup", "CARAMEL"), sub("whole_milk", "almond_milk", "WITH ALMOND MILK")],
            ),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("asap", "ASAP", None),
        name="Tom",
        name_q="TOM",
    ),
    X(
        "syn-t5-0269",
        """
c: hi 🍋 a lemonade and onion rings for pickup, card
b: A lemonade and onion rings for pickup, paying by card. Right?
c: yes!
c: actually skip the onion rings 😅
""",
        "P C M",
        items=[I("lemonade", 1, None, ["a lemonade"])],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0270",
        """
c: Hello.
c: I'd like to order dinner for my roommates.
""",
        "S P",
    ),
    X(
        "syn-t5-0271",
        """
c: hey 🍕 2 cheese pizzas and one of those to 4 larkin blvd
c: card 💳
""",
        "P P",
        items=[
            I("cheese_pizza", 2, None, ["2 cheese pizzas"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="to 4 larkin blvd",
        addr={"raw": "4 larkin blvd", "number": "4", "street": "larkin blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0272",
        """
c: hey
c: food order for the house
""",
        "S P",
    ),
    X(
        "syn-t5-0273",
        """
c: Good evening.
c: Could I get a cheese pizza without cheese, just sauce?
c: For pickup, paying cash.
""",
        "S P P",
        items=[I("cheese_pizza", 1, None, ["a cheese pizza"], [rm("cheese", "without cheese")])],
        method="pickup",
        method_q="For pickup",
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t5-0274",
        """
c: some large lattes
c: n a coffee
c: cash
""",
        "P P P",
        items=[I("latte", None, "large", ["some large lattes"]), I("drip_coffee", 1, None, ["a coffee"])],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0275",
        """
c: Hi there.
c: We'd like to place an order for our study group.
""",
        "S P",
    ),
]
