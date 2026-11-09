"""t5 entries 0071–0100 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0071",
        """
c: hi! 2 medium americanos and a hot chocolate pls ☕
c: pickup for june, card
b: 2 medium americanos and a hot chocolate, pickup for June, paying by card. All good?
c: yes!! 😊
c: oh actually no hot chocolate
""",
        "P P C M",
        items=[I("americano", 2, "medium", ["2 medium americanos"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t5-0072",
        """
c: ARE YOU GUYS STILL DELIVERING?
b: Yes, until 10!
c: OK TWO SINGLE CHEESEBURGERS TO 69 CLEMENT ST
c: IN LIKE 30 MIN
c: ACTUALLY JUST ONE CHEESEBURGER
""",
        "D P P M",
        items=[I("cheeseburger", 1, "single", ["TWO SINGLE CHEESEBURGERS", "JUST ONE CHEESEBURGER"])],
        method="delivery",
        method_q="TO 69 CLEMENT ST",
        time=("relative", "IN LIKE 30 MIN", None),
        addr={"raw": "69 CLEMENT ST", "number": "69", "street": "CLEMENT ST"},
    ),
    X(
        "syn-t5-0073",
        """
c: hey! 6 medium lattes, 2 with vanilla ☕ + 2 small hot chocolates w hazelnut & almond milk + 3 sesame bagels w egg 🥯
c: pickup for ben, card pls
""",
        "P P",
        items=[
            I("latte", 4, "medium", ["6 medium lattes"]),
            I(
                "latte",
                2,
                "medium",
                ["6 medium lattes", "2 with vanilla"],
                [add("vanilla_syrup", "with vanilla")],
            ),
            I(
                "hot_chocolate",
                2,
                "small",
                ["2 small hot chocolates"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "almond_milk", "almond milk")],
            ),
            I("bagel", 3, "sesame", ["3 sesame bagels"], [add("egg", "w egg")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t5-0074",
        """
c: Good evening!
c: I'd like two strawberry milkshakes, please.
c: And a large order of fries.
c: I'll pick it up and pay by card.
b: Two strawberry milkshakes and a large fries for pickup, paying by card. Is that correct?
c: Yes, that's correct.
c: Actually, I'll skip the fries.
""",
        "S P P P C M",
        items=[I("milkshake", 2, "strawberry", ["two strawberry milkshakes"])],
        method="pickup",
        method_q="pick it up",
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0075",
        """
c: hey 😋 can we get a few bacon burgers w avocado 🥑
c: in about 20 min
""",
        "P P",
        items=[I("bacon_burger", None, None, ["a few bacon burgers"], [add("avocado", "w avocado")])],
        time=("relative", "in about 20 min", None),
    ),
    X(
        "syn-t5-0076",
        """
c: Hi, can I get some Sprites, three Dr Peppers, and two extra large Hawaiian pizzas on gluten-free crust?
c: Ready in about half an hour, please.
""",
        "P P",
        items=[
            I("sprite", None, None, ["some Sprites"]),
            I("dr_pepper", 3, None, ["three Dr Peppers"]),
            I(
                "hawaiian_pizza",
                2,
                "extra_large",
                ["two extra large Hawaiian pizzas"],
                [add("crust_gluten_free", "gluten-free crust")],
            ),
        ],
        time=("relative", "in about half an hour", None),
    ),
    X(
        "syn-t5-0077",
        """
c: hey
c: can i get a coke
c: and that thing from before
c: thx
""",
        "S P P S",
        items=[
            I("coke", 1, None, ["a coke"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
    ),
    X(
        "syn-t5-0078",
        """
c: yo
c: 2 bacon burgers
c: 1 no ketchup
c: a veggie burger
c: 3 cheeseburgers
c: w avocado
c: asap
c: ty
""",
        "S P P P P P P S",
        items=[
            I("bacon_burger", 1, None, ["2 bacon burgers"]),
            I("bacon_burger", 1, None, ["2 bacon burgers", "1 no ketchup"], [rm("ketchup", "no ketchup")]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("cheeseburger", 3, None, ["3 cheeseburgers", "w avocado"], [add("avocado", "w avocado")]),
        ],
        time=("asap", "asap", None),
    ),
    X(
        "syn-t5-0079",
        """
c: hi 🍕 one 10 inch pepperoni pizza but no pepperoni lol, to 66 orchard ct
c: card, in 30 min pls 🙏
""",
        "P P",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "small",
                ["one 10 inch pepperoni pizza"],
                [rm("pepperoni", "no pepperoni")],
            )
        ],
        method="delivery",
        method_q="to 66 orchard ct",
        time=("relative", "in 30 min", None),
        addr={"raw": "66 orchard ct", "number": "66", "street": "orchard ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0080",
        """
c: Hi, I'd like a bottle of water and a personal margherita with mushrooms, paying by card, ready in 20 minutes.
c: Actually, could you make the margherita gluten-free crust?
""",
        "P M",
        items=[
            I("water", 1, None, ["a bottle of water"]),
            I(
                "margherita_pizza",
                1,
                "personal",
                ["a personal margherita", "make the margherita gluten-free crust"],
                [add("mushrooms", "with mushrooms"), add("crust_gluten_free", "gluten-free crust")],
            ),
        ],
        time=("relative", "in 20 minutes", None),
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t5-0081",
        """
c: hey there 👋
c: 2 cokes, a veggie burger w bacon, a sprite and 3 chocolate shakes 🥤 pickup!
c: hmm actually forget the shakes
""",
        "S P M",
        items=[
            I("coke", 2, None, ["2 cokes"]),
            I("veggie_burger", 1, None, ["a veggie burger"], [add("bacon", "w bacon")]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t5-0082",
        """
c: morning
c: can i get a few medium americanos w caramel n skim milk, and 3 croissants w butter
c: pickup for tom
""",
        "S P P",
        items=[
            I(
                "americano",
                None,
                "medium",
                ["a few medium americanos"],
                [add("caramel_syrup", "w caramel"), add("skim_milk", "skim milk")],
            ),
            I("croissant", 3, None, ["3 croissants"], [add("butter", "w butter")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t5-0083",
        """
c: hiii 🌙
c: late night order for the dorm incoming 😅
""",
        "S P",
    ),
    X(
        "syn-t5-0084",
        """
c: can i get some sprites
c: and a bacon burger no bacon lol
c: card
""",
        "P P P",
        items=[
            I("sprite", None, None, ["some sprites"]),
            I("bacon_burger", 1, None, ["a bacon burger"], [rm("bacon", "no bacon")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0085",
        """
c: Hi, could I get a supreme pizza with no olives on gluten-free crust, and the same as last time? Pickup, paying by card.
""",
        "P",
        items=[
            I(
                "supreme_pizza",
                1,
                None,
                ["a supreme pizza"],
                [rm("olives", "no olives"), add("crust_gluten_free", "gluten-free crust")],
            ),
            I(
                None,
                1,
                None,
                ["the same as last time"],
                unmatched="the same as last time",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t5-0086",
        """
c: bagel w cream cheese
c: breakfast sandwich w avocado
c: and the one i always get, pickup for ben, cash, change for a 20
""",
        "P P P",
        items=[
            I("bagel", 1, None, ["bagel"], [add("cream_cheese", "w cream cheese")]),
            I("breakfast_sandwich", 1, None, ["breakfast sandwich"], [add("avocado", "w avocado")]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t5-0087",
        """
c: hey 🍕 a supreme and a personal hawaiian with pepperoni pls
c: paying cash 💵
c: ready in 20?
""",
        "P P P",
        items=[
            I("supreme_pizza", 1, None, ["a supreme"]),
            I("hawaiian_pizza", 1, "personal", ["a personal hawaiian"], [add("pepperoni", "with pepperoni")]),
        ],
        time=("relative", "in 20", None),
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t5-0088",
        """
c: HI! TWO BREAKFAST SANDWICHES ON CROISSANTS WITH AVOCADO, A SMALL LATTE AND TWO BANANA NUT MUFFINS!
c: PICKUP IN 20 MINUTES FOR IVY, CARD!
c: ACTUALLY PUT THE SANDWICHES ON BAGELS!
""",
        "P P M",
        items=[
            I(
                "breakfast_sandwich",
                2,
                "bagel",
                ["TWO BREAKFAST SANDWICHES ON CROISSANTS", "PUT THE SANDWICHES ON BAGELS"],
                [add("avocado", "WITH AVOCADO")],
            ),
            I("latte", 1, "small", ["A SMALL LATTE"]),
            I("muffin", 2, "banana_nut", ["TWO BANANA NUT MUFFINS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("relative", "IN 20 MINUTES", None),
        pay="card",
        pay_q="CARD",
        name="Ivy",
        name_q="IVY",
    ),
    X(
        "syn-t5-0089",
        """
c: small cappuccino w hazelnut, 2 breakfast sandwiches on bagels w tomato and one of those
c: card
""",
        "P P",
        items=[
            I("cappuccino", 1, "small", ["small cappuccino"], [add("hazelnut_syrup", "w hazelnut")]),
            I(
                "breakfast_sandwich",
                2,
                "bagel",
                ["2 breakfast sandwiches on bagels"],
                [add("tomato", "w tomato")],
            ),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0090",
        """
c: do the onion rings come w sauce
b: They come plain, but we can add ketchup on the side.
c: ok onion rings and one of those to 9359 hawthorne blvd unit 24a
""",
        "Q P",
        items=[
            I("onion_rings", 1, None, ["onion rings"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="to 9359 hawthorne blvd unit 24a",
        addr={
            "raw": "9359 hawthorne blvd unit 24a",
            "number": "9359",
            "street": "hawthorne blvd",
            "unit": "24a",
        },
    ),
    X(
        "syn-t5-0091",
        """
c: 2 waters and an xl meat lovers no beef
c: to 7253 bayview terrace unit 4c
c: cash, at 7 pls
c: oh make the meat lovers gluten free crust
""",
        "P P P M",
        items=[
            I("water", 2, None, ["2 waters"]),
            I(
                "meat_lovers_pizza",
                1,
                "extra_large",
                ["an xl meat lovers", "make the meat lovers gluten free crust"],
                [rm("beef", "no beef"), add("crust_gluten_free", "gluten free crust")],
            ),
        ],
        method="delivery",
        method_q="to 7253 bayview terrace unit 4c",
        time=("clock_time", "at 7", "19:00"),
        addr={
            "raw": "7253 bayview terrace unit 4c",
            "number": "7253",
            "street": "bayview terrace",
            "unit": "4c",
        },
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0092",
        """
c: HEY!
c: MEDIUM SUPREME WITH JALAPENOS AND A SMALL BBQ CHICKEN WITH NO CHICKEN!
c: PLUS A CAN OF ICED TEA AND TWO CANS OF SPRITE!
c: PICKUP, CASH, MARCUS!
b: Medium supreme with jalapeños, small BBQ chicken with no chicken, a can of iced tea and two cans of Sprite, pickup for Marcus, cash. Right?
c: YES!
c: WAIT, NO SPRITES!
""",
        "S P P P C M",
        items=[
            I("supreme_pizza", 1, "medium", ["MEDIUM SUPREME"], [add("jalapenos", "WITH JALAPENOS")]),
            I(
                "bbq_chicken_pizza",
                1,
                "small",
                ["A SMALL BBQ CHICKEN"],
                [rm("grilled_chicken", "NO CHICKEN")],
            ),
            I("iced_tea", 1, "can", ["A CAN OF ICED TEA"]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Marcus",
        name_q="MARCUS",
    ),
    X(
        "syn-t5-0093",
        """
c: Hello!
c: Could I get some vanilla milkshakes and a veggie burger without tomato?
""",
        "S P",
        items=[
            I("milkshake", None, "vanilla", ["some vanilla milkshakes"]),
            I("veggie_burger", 1, None, ["a veggie burger"], [rm("tomato", "without tomato")]),
        ],
    ),
    X(
        "syn-t5-0094",
        """
c: hi
c: do u have skim
b: Yes, we have skim milk!
c: ok small hot chocolate
c: w hazelnut
c: skim pls
c: cash
c: change for a 20
""",
        "S Q P P P P P",
        items=[
            I(
                "hot_chocolate",
                1,
                "small",
                ["small hot chocolate"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "skim_milk", "skim pls")],
            ),
        ],
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0095",
        """
c: Hi, could I get a few pepperoni pizzas with no sauce and ground beef added?
c: Pickup under Luis, paying by card.
""",
        "P P",
        items=[
            I(
                "pepperoni_pizza",
                None,
                None,
                ["a few pepperoni pizzas"],
                [rm("tomato_sauce", "no sauce"), add("beef", "ground beef added")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="paying by card",
        name="Luis",
    ),
    X(
        "syn-t5-0096",
        """
c: FOUR HOT CHOCOLATES, ONE WITH NO WHIP!
c: A SMALL AMERICANO WITH CARAMEL!
c: AND A BREAKFAST SANDWICH ON A CROISSANT!
""",
        "P P P",
        items=[
            I("hot_chocolate", 3, None, ["FOUR HOT CHOCOLATES"]),
            I(
                "hot_chocolate",
                1,
                None,
                ["FOUR HOT CHOCOLATES", "ONE WITH NO WHIP"],
                [rm("whipped_cream", "NO WHIP")],
            ),
            I("americano", 1, "small", ["A SMALL AMERICANO"], [add("caramel_syrup", "WITH CARAMEL")]),
            I("breakfast_sandwich", 1, "croissant", ["A BREAKFAST SANDWICH ON A CROISSANT"]),
        ],
    ),
    X(
        "syn-t5-0097",
        """
c: 4 personal supremes to 1938 alder ln, card
b: 4 personal supremes delivered to 1938 Alder Ln, card. Correct?
c: ya
c: actually make it 3
""",
        "P C M",
        items=[I("supreme_pizza", 3, "personal", ["4 personal supremes", "make it 3"])],
        method="delivery",
        method_q="to 1938 alder ln",
        addr={"raw": "1938 alder ln", "number": "1938", "street": "alder ln"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0098",
        """
c: hey we wanna order breakfast for the office
""",
        "P",
    ),
    X(
        "syn-t5-0099",
        """
c: 4 small hot chocolates
c: 2 no whip
c: medium americano
c: card
""",
        "P P P P",
        items=[
            I("hot_chocolate", 2, "small", ["4 small hot chocolates"]),
            I(
                "hot_chocolate",
                2,
                "small",
                ["4 small hot chocolates", "2 no whip"],
                [rm("whipped_cream", "no whip")],
            ),
            I("americano", 1, "medium", ["medium americano"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0100",
        """
c: some large coffees
c: 3 plain bagels
c: breakfast sandwich on english muffin no bacon add avo
c: at 11:30
""",
        "P P P P",
        items=[
            I("drip_coffee", None, "large", ["some large coffees"]),
            I("bagel", 3, "plain", ["3 plain bagels"]),
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["breakfast sandwich on english muffin"],
                [rm("bacon", "no bacon"), add("avocado", "add avo")],
            ),
        ],
        time=("clock_time", "at 11:30", "11:30"),
    ),
]
