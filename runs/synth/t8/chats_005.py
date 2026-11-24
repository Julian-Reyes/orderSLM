"""t8 syn-t8-0121–0150 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t8-0121",
        """
c: bacon burger w mustard
c: a lemonade
c: a shake
c: n that thing from before
c: 97 harbor rd #28a, cash, i have a 50
""",
        "P P P P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger w mustard"], [add("mustard", "w mustard")]),
            I("lemonade", 1, None, ["a lemonade"]),
            I("milkshake", 1, None, ["a shake"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="97 harbor rd #28a",
        addr={"raw": "97 harbor rd #28a", "number": "97", "street": "harbor rd", "unit": "#28a"},
        pay="cash",
        pay_q=["cash", "i have a 50"],
        change=5000,
    ),
    X(
        "syn-t8-0122",
        """
c: 2 plain bagels w egg n same as last time
c: cash
""",
        "P P",
        items=[
            I("bagel", 2, "plain", ["2 plain bagels w egg"], [add("egg", "w egg")]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0123",
        """
c: Hi, two veggie burgers, one with bacon, two cheeseburgers and two Cokes.
c: Pickup for Ben.
c: Card.
""",
        "P P P",
        items=[
            I("veggie_burger", 1, None, ["two veggie burgers, one with bacon"]),
            I("veggie_burger", 1, None, ["two veggie burgers, one with bacon"], [add("bacon", "with bacon")]),
            I("cheeseburger", 2, None, ["two cheeseburgers"]),
            I("coke", 2, None, ["two Cokes"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="Card",
        name="Ben",
        name_q="Ben",
    ),
    X(
        "syn-t8-0124",
        """
c: 3 small bbq chicken 🍗 2 of em no bbq sauce
c: a large margherita no basil
c: n a medium hawaiian no pineapple 🍍
c: 791 union st
""",
        "P P P P",
        items=[
            I("bbq_chicken_pizza", 1, "small", ["3 small bbq chicken 🍗 2 of em no bbq sauce"]),
            I(
                "bbq_chicken_pizza",
                2,
                "small",
                ["3 small bbq chicken 🍗 2 of em no bbq sauce"],
                [rm("bbq_sauce", "no bbq sauce")],
            ),
            I("margherita_pizza", 1, "large", ["a large margherita no basil"], [rm("basil", "no basil")]),
            I(
                "hawaiian_pizza",
                1,
                "medium",
                ["a medium hawaiian no pineapple"],
                [rm("pineapple", "no pineapple")],
            ),
        ],
        method="delivery",
        method_q="791 union st",
        addr={"raw": "791 union st", "number": "791", "street": "union st"},
    ),
    X(
        "syn-t8-0125",
        """
c: heyy
c: the one i always get pls
b: Sorry, we can't see past orders here. What would you like?
c: 2 medium pepperoni but no pepperoni lol, an order of knots, a water n a 2 liter sprite. are the knots vegan?
b: They have butter, so not vegan.
c: ok still want them. pickup, ana
""",
        "S P P/Q P",
        items=[
            I(
                "pepperoni_pizza",
                2,
                "medium",
                ["2 medium pepperoni but no pepperoni"],
                [rm("pepperoni", "no pepperoni")],
            ),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("water", 1, None, ["a water"]),
            I("sprite", 1, "two_liter", ["a 2 liter sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t8-0126",
        """
c: that thing from before x3
b: Sorry, we can't see past orders here. What would you like?
c: 3 chocolate shakes, 3 cokes, a sprite n 2 bacon burgers w mustard. pickup, cash
""",
        "P P",
        items=[
            I("milkshake", 3, "chocolate", ["3 chocolate shakes"]),
            I("coke", 3, None, ["3 cokes"]),
            I("sprite", 1, None, ["a sprite"]),
            I("bacon_burger", 2, None, ["2 bacon burgers w mustard"], [add("mustard", "w mustard")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0127",
        """
c: Hi, I'd like to order for Tuesday: a veggie burger and a bacon burger.
c: Is the veggie patty made in house?
b: Yes, we make it here every morning.
c: Great. Deliver to 148 Willow Creek Dr at 6:30, please. Card.
""",
        "P Q P",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
        ],
        method="delivery",
        method_q="Deliver to 148 Willow Creek Dr",
        addr={"raw": "148 Willow Creek Dr", "number": "148", "street": "Willow Creek Dr"},
        time=("clock_time", "at 6:30", "18:30"),
        day=("weekday", "tue", "Tuesday"),
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0128",
        """
c: bacon burger n a large lemonade asap, card
""",
        "P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger"]),
            I("lemonade", 1, None, ["a large lemonade"], unmatched_variant="large"),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0129",
        """
c: hello
c: 2 large margheritas no olive oil add onions
c: an order of knots
c: n a mini coke
c: pickup, card
""",
        "S P P P P",
        items=[
            I(
                "margherita_pizza",
                2,
                "large",
                ["2 large margheritas no olive oil add onions"],
                [rm("olive_oil", "no olive oil"), add("onions", "add onions")],
            ),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("coke", 1, None, ["a mini coke"], unmatched_variant="mini"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0130",
        """
c: breadsticks n the one i always get
c: 58 ivanhoe terrace #25b
c: asap
""",
        "P P P",
        items=[
            I("breadsticks", 1, None, ["breadsticks"]),
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
        method_q="58 ivanhoe terrace #25b",
        addr={"raw": "58 ivanhoe terrace #25b", "number": "58", "street": "ivanhoe terrace", "unit": "#25b"},
        time=("asap", "asap", None),
    ),
    X(
        "syn-t8-0131",
        """
c: pepperoni no sauce 🍕
c: whats bigger than a medium?
b: Large (14 inch) and extra large (16 inch).
c: one of those 👍
""",
        "P Q P",
        items=[
            I(
                "pepperoni_pizza",
                1,
                None,
                ["pepperoni no sauce", "one of those"],
                [rm("tomato_sauce", "no sauce")],
                flag="item_variant",
            )
        ],
    ),
    X(
        "syn-t8-0132",
        """
c: hiii 🍕
c: 5 xl supremes
c: 3 no green peppers
c: a water 💧
c: n a personal margherita no sauce w onions
c: pickup, cash, paying w a 100 💵
""",
        "S P P P P P",
        items=[
            I("supreme_pizza", 2, "extra_large", ["5 xl supremes", "3 no green peppers"]),
            I(
                "supreme_pizza",
                3,
                "extra_large",
                ["5 xl supremes", "3 no green peppers"],
                [rm("green_peppers", "no green peppers")],
            ),
            I("water", 1, None, ["a water"]),
            I(
                "margherita_pizza",
                1,
                "personal",
                ["a personal margherita no sauce w onions"],
                [rm("tomato_sauce", "no sauce"), add("onions", "w onions")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "paying w a 100"],
        change=10000,
    ),
    X(
        "syn-t8-0133",
        """
c: hey
c: 4 bacon burgers
c: 2 sprites
c: is the bacon crispy
b: Yes, nice and crispy!
c: pickup
c: oh wait 3 bacon burgers not 4
""",
        "S P P Q P M",
        items=[
            I("bacon_burger", 3, None, ["4 bacon burgers", "3 bacon burgers not 4"]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    X(
        "syn-t8-0134",
        """
c: Hello!
c: Two BBQ chicken pizzas, please, delivered to 8393 Alder Ct, unit 9.
b: Sure! What size would you like?
c: What sizes are there?
b: Personal, small, medium, large and extra large.
c: Extra large for both. In 30 minutes, paying cash.
""",
        "S P Q P",
        items=[I("bbq_chicken_pizza", 2, "extra_large", ["Two BBQ chicken pizzas", "Extra large for both"])],
        method="delivery",
        method_q="delivered to 8393 Alder Ct, unit 9",
        addr={"raw": "8393 Alder Ct, unit 9", "number": "8393", "street": "Alder Ct", "unit": "unit 9"},
        time=("relative", "In 30 minutes", None),
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t8-0135",
        """
c: hey
c: number 1
c: no ketchup add bacon
c: does the combo come w a drink
b: Yes! The combo comes with fries or onion rings and a Coke, Sprite or lemonade.
c: rings
c: coke
""",
        "S P P Q P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["number 1", "no ketchup add bacon", "rings", "coke"],
                [rm("ketchup", "no ketchup"), add("bacon", "add bacon")],
                combo={"side": "onion_rings", "drink": "coke"},
            ),
        ],
    ),
    X(
        "syn-t8-0136",
        """
c: 4 small meat lovers w fresh mozz n gluten free crust 🍕
c: + a veggie, one of the bigger sizes
c: pickup for marcus
""",
        "P P P",
        items=[
            I(
                "meat_lovers_pizza",
                4,
                "small",
                ["4 small meat lovers w fresh mozz n gluten free crust"],
                [add("mozzarella", "w fresh mozz"), add("crust_gluten_free", "gluten free crust")],
            ),
            I("veggie_pizza", 1, None, ["a veggie, one of the bigger sizes"], flag="item_variant"),
        ],
        method="pickup",
        method_q="pickup",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t8-0137",
        """
c: can i order now for friday? 🍔
b: Yes, you can order up to a week ahead!
c: 2 cheeseburgers w bacon, a fries n 4 sprites, pickup fri at 1, card 💳
""",
        "D P",
        items=[
            I("cheeseburger", 2, None, ["2 cheeseburgers w bacon"], [add("bacon", "w bacon")]),
            I("fries", 1, None, ["a fries"]),
            I("sprite", 4, None, ["4 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 1", "13:00"),
        day=("weekday", "fri", "fri"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0138",
        """
c: 🍔🍔🍔❓
""",
        "U",
    ),
    X(
        "syn-t8-0139",
        """
c: Hi, a cheeseburger combo with bacon, onion rings and a Sprite, to 10 Delancey Blvd, above the bakery.
c: Card, please.
""",
        "P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["a cheeseburger combo with bacon, onion rings and a Sprite"],
                [add("bacon", "with bacon")],
                combo={"side": "onion_rings", "drink": "sprite"},
            ),
        ],
        method="delivery",
        method_q="to 10 Delancey Blvd",
        addr={
            "raw": "10 Delancey Blvd, above the bakery",
            "number": "10",
            "street": "Delancey Blvd",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0140",
        """
c: HELLO
c: A LARGE MARGHERITA, A XXL PEPPERONI WITH THICK CRUST AND A MEATBALL SUB TO 5870 THORNTON AVE UNIT 13B, CARD
""",
        "S P",
        items=[
            I("margherita_pizza", 1, "large", ["A LARGE MARGHERITA"]),
            I(
                "pepperoni_pizza",
                1,
                None,
                ["A XXL PEPPERONI WITH THICK CRUST"],
                [add("crust_thick", "THICK CRUST")],
                unmatched_variant="XXL",
            ),
            I(None, 1, None, ["A MEATBALL SUB"], unmatched="A MEATBALL SUB"),
        ],
        method="delivery",
        method_q="TO 5870 THORNTON AVE UNIT 13B",
        addr={
            "raw": "5870 THORNTON AVE UNIT 13B",
            "number": "5870",
            "street": "THORNTON AVE",
            "unit": "UNIT 13B",
        },
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t8-0141",
        """
c: 2 bacon burgers n some cokes 🥤
c: in 20 min, card
""",
        "P P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("coke", None, None, ["some cokes"]),
        ],
        time=("relative", "in 20 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0142",
        """
c: hey
c: do u take orders for sunday
b: Yes, we take orders up to a week ahead!
c: ok a medium meat lovers, a small supreme w jalapenos n 2 sprites for sunday at 6
c: card
""",
        "S D P P",
        items=[
            I("meat_lovers_pizza", 1, "medium", ["a medium meat lovers"]),
            I(
                "supreme_pizza",
                1,
                "small",
                ["a small supreme w jalapenos"],
                [add("jalapenos", "w jalapenos")],
            ),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "sun", "sunday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0143",
        """
c: Hello!
c: A medium Americano, please.
c: As soon as possible, for pickup.
c: The name is Grace.
b: Got it, Grace: 1 medium Americano, pickup as soon as possible. Is that right?
c: Yes.
c: Sorry, could I switch that to a medium cappuccino with caramel?
""",
        "S P P P C M",
        items=[
            I(
                "cappuccino",
                1,
                "medium",
                ["a medium cappuccino with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("asap", "As soon as possible", None),
        name="Grace",
        name_q="Grace",
    ),
    X(
        "syn-t8-0144",
        """
c: lemonade
c: 3 rings
c: 2 fries
c: do u have honey mustard
b: Just regular mustard, sorry!
c: ok
c: bacon burger w avocado
c: 2 cokes
""",
        "P P P Q S P P",
        items=[
            I("lemonade", 1, None, ["lemonade"]),
            I("onion_rings", 3, None, ["3 rings"]),
            I("fries", 2, None, ["2 fries"]),
            I("bacon_burger", 1, None, ["bacon burger w avocado"], [add("avocado", "w avocado")]),
            I("coke", 2, None, ["2 cokes"]),
        ],
    ),
    X(
        "syn-t8-0145",
        """
c: med americano, 2 lg almond lattes w whip n 2 lg drips
c: n a plain bagel n a croissant
c: pickup in 20, leah, card
""",
        "P P P",
        items=[
            I("americano", 1, "medium", ["med americano"]),
            I(
                "latte",
                2,
                "large",
                ["2 lg almond lattes w whip"],
                [sub("whole_milk", "almond_milk", "almond"), add("whipped_cream", "w whip")],
            ),
            I("drip_coffee", 2, "large", ["2 lg drips"]),
            I("bagel", 1, "plain", ["a plain bagel"]),
            I("croissant", 1, None, ["a croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t8-0146",
        """
c: Hi, a BBQ chicken pizza without the chicken, a size up from medium, and three Dr Peppers.
c: Card.
""",
        "P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "large",
                ["a BBQ chicken pizza without the chicken, a size up from medium"],
                [rm("grilled_chicken", "without the chicken")],
            ),
            I("dr_pepper", 3, None, ["three Dr Peppers"]),
        ],
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0147",
        """
c: HI THERE
c: 2 BBQ CHICKEN WITH RED SAUCE AND THE ONE I ALWAYS GET
""",
        "S P",
        items=[
            I(
                "bbq_chicken_pizza",
                2,
                None,
                ["2 BBQ CHICKEN WITH RED SAUCE"],
                [add("tomato_sauce", "WITH RED SAUCE")],
            ),
            I(
                None,
                1,
                None,
                ["THE ONE I ALWAYS GET"],
                unmatched="THE ONE I ALWAYS GET",
                flag="item_menu_match",
            ),
        ],
    ),
    X(
        "syn-t8-0148",
        """
c: lg americano w vanilla, is the vanilla sugar free? 🤔 n a medium hot choc no whip, pickup at 1:30 for rosa, card
""",
        "P/Q",
        items=[
            I("americano", 1, "large", ["lg americano w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("hot_chocolate", 1, "medium", ["a medium hot choc no whip"], [rm("whipped_cream", "no whip")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 1:30", "13:30"),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t8-0149",
        """
c: veggie burger no pickles, 2 sprites n a chocolate shake
c: pickup asap, cash
b: Got it: 1 Veggie Burger with no pickles, 2 Sprites and 1 chocolate milkshake, pickup as soon as possible, paying cash. Is that right?
c: ya
c: actually no shake
""",
        "P P C M",
        items=[
            I("veggie_burger", 1, None, ["veggie burger no pickles"], [rm("pickle", "no pickles")]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0150",
        """
c: 4 breakfast deals, all w medium lattes n blueberry muffins
c: pickup tom, card
""",
        "P P",
        items=[
            I(
                "coffee_pastry_combo",
                4,
                None,
                ["4 breakfast deals, all w medium lattes n blueberry muffins"],
                combo={"drink": ("latte", "medium"), "pastry": ("muffin", "blueberry")},
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Tom",
        name_q="tom",
    ),
]
