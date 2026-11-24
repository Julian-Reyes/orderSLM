"""t8 syn-t8-0151–0180 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t8-0151",
        """
c: the one i always get
b: Sorry, we can't see past orders here. What would you like?
c: 4 cheeseburgers w jalapenos
c: 2 bacon burgers
c: a lemonade, 4 sprites n a chocolate shake
c: pickup at 7, cash
""",
        "P P P P P",
        items=[
            I("cheeseburger", 4, None, ["4 cheeseburgers w jalapenos"], [add("jalapeno", "w jalapenos")]),
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("lemonade", 1, None, ["a lemonade"]),
            I("sprite", 4, None, ["4 sprites"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "19:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0152",
        """
c: hi we need like 15 pizzas for a party saturday
c: is there a manager i can talk to about a big order
c: thx
""",
        "P HU S",
        time=("ambiguous", "saturday"),
        day=("weekday", "sat", "saturday"),
    ),
    X(
        "syn-t8-0153",
        """
c: Hello.
c: I'd like to place an order for Thursday.
c: Two hot chocolates with skim milk.
c: Do they come with whipped cream?
b: Yes, unless you'd like them without.
c: With is fine.
c: I'll come at 11, paying cash with a 20.
""",
        "S P P Q S P",
        items=[
            I(
                "hot_chocolate",
                2,
                None,
                ["Two hot chocolates with skim milk"],
                [sub("whole_milk", "skim_milk", "with skim milk")],
            ),
        ],
        method="pickup",
        method_q="I'll come",
        time=("clock_time", "at 11", "11:00"),
        day=("weekday", "thu", "Thursday"),
        pay="cash",
        pay_q=["paying cash", "with a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0154",
        """
c: veggie burger
c: rings
c: coke
c: pickup
c: sam
c: card
c: oh make it 4 veggie burgers
""",
        "P P P P P P M",
        items=[
            I("veggie_burger", 4, None, ["veggie burger", "make it 4 veggie burgers"]),
            I("onion_rings", 1, None, ["rings"]),
            I("coke", 1, None, ["coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t8-0155",
        """
c: Hi, a personal BBQ chicken with no chicken and a cheese pizza in one of your larger sizes. Card.
""",
        "P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "personal",
                ["a personal BBQ chicken with no chicken"],
                [rm("grilled_chicken", "no chicken")],
            ),
            I("cheese_pizza", 1, None, ["a cheese pizza in one of your larger sizes"], flag="item_variant"),
        ],
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0156",
        """
c: hey
c: 2 margheritas
c: to 672 union blvd apt 21b
b: Sure! What size for the margheritas?
c: what size feeds 2
b: A medium (12 inch) is good for two.
c: medium then, card
""",
        "S P P Q P",
        items=[I("margherita_pizza", 2, "medium", ["2 margheritas", "medium then"])],
        method="delivery",
        method_q="to 672 union blvd apt 21b",
        addr={"raw": "672 union blvd apt 21b", "number": "672", "street": "union blvd", "unit": "apt 21b"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0157",
        """
c: Good evening!
c: Three Cokes, two veggie burgers with ketchup and two bacon burgers with mayo.
c: And the same as last time for my son.
c: Delivered to 16 Cedar Hill Pl.
""",
        "S P P P",
        items=[
            I("coke", 3, None, ["Three Cokes"]),
            I(
                "veggie_burger",
                2,
                None,
                ["two veggie burgers with ketchup"],
                [add("ketchup", "with ketchup")],
            ),
            I("bacon_burger", 2, None, ["two bacon burgers with mayo"], [add("mayo", "with mayo")]),
            I(
                None,
                1,
                None,
                ["the same as last time"],
                unmatched="the same as last time",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="Delivered to 16 Cedar Hill Pl",
        addr={"raw": "16 Cedar Hill Pl", "number": "16", "street": "Cedar Hill Pl"},
    ),
    X(
        "syn-t8-0158",
        """
c: morning ☀️
c: a few americanos, an everything bagel w cream cheese n a bec on a croissant w avo, asap, pickup for ana
""",
        "S P",
        items=[
            I("americano", None, None, ["a few americanos"]),
            I(
                "bagel",
                1,
                "everything",
                ["an everything bagel w cream cheese"],
                [add("cream_cheese", "w cream cheese")],
            ),
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["a bec on a croissant w avo"],
                [add("avocado", "w avo")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t8-0159",
        """
c: 3 bacon burgers no lettuce
c: large fries
c: a shake
c: idk the flavor, not vanilla
c: 9578 dover terrace #8c at 7, cash
""",
        "P P P P P",
        items=[
            I("bacon_burger", 3, None, ["3 bacon burgers no lettuce"], [rm("lettuce", "no lettuce")]),
            I("fries", 1, "large", ["large fries"]),
            I("milkshake", 1, None, ["a shake", "not vanilla"], flag="item_variant"),
        ],
        method="delivery",
        method_q="9578 dover terrace #8c",
        addr={"raw": "9578 dover terrace #8c", "number": "9578", "street": "dover terrace", "unit": "#8c"},
        time=("clock_time", "at 7", "19:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0160",
        """
c: 3 veggie burgers
c: one w bacon
c: a lemonade
c: n a sprite
c: card
""",
        "P P P P P",
        items=[
            I("veggie_burger", 2, None, ["3 veggie burgers", "one w bacon"]),
            I("veggie_burger", 1, None, ["3 veggie burgers", "one w bacon"], [add("bacon", "w bacon")]),
            I("lemonade", 1, None, ["a lemonade"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0161",
        """
c: 2 cheeseburgers, 1 no onion
c: a coke n 3 fries
c: 275 sycamore ln
c: card
""",
        "P P P P",
        items=[
            I("cheeseburger", 1, None, ["2 cheeseburgers, 1 no onion"]),
            I("cheeseburger", 1, None, ["2 cheeseburgers, 1 no onion"], [rm("onion", "no onion")]),
            I("coke", 1, None, ["a coke"]),
            I("fries", 3, None, ["3 fries"]),
        ],
        method="delivery",
        method_q="275 sycamore ln",
        addr={"raw": "275 sycamore ln", "number": "275", "street": "sycamore ln"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0162",
        """
c: party time 🎉 4 large supremes, 2 large bbq chicken w basil n a small margherita no basil
c: 3 orders of breadsticks 🥖
c: a can of iced tea n 2 two liter cokes 🥤
c: to 689 easton ct apt 28 asap
""",
        "P P P P",
        items=[
            I("supreme_pizza", 4, "large", ["4 large supremes"]),
            I("bbq_chicken_pizza", 2, "large", ["2 large bbq chicken w basil"], [add("basil", "w basil")]),
            I("margherita_pizza", 1, "small", ["a small margherita no basil"], [rm("basil", "no basil")]),
            I("breadsticks", 3, None, ["3 orders of breadsticks"]),
            I("iced_tea", 1, "can", ["a can of iced tea"]),
            I("coke", 2, "two_liter", ["2 two liter cokes"]),
        ],
        method="delivery",
        method_q="to 689 easton ct apt 28",
        addr={"raw": "689 easton ct apt 28", "number": "689", "street": "easton ct", "unit": "apt 28"},
        time=("asap", "asap", None),
    ),
    X(
        "syn-t8-0163",
        """
c: CAN I GET ONE OF THOSE
b: Sure! Which item would you like?
c: A BACON BURGER NO LETTUCE, A DOUBLE CHEESEBURGER NO LETTUCE, ONION RINGS, FRIES AND A COKE
""",
        "P P",
        items=[
            I("bacon_burger", 1, None, ["A BACON BURGER NO LETTUCE"], [rm("lettuce", "NO LETTUCE")]),
            I(
                "cheeseburger",
                1,
                "double",
                ["A DOUBLE CHEESEBURGER NO LETTUCE"],
                [rm("lettuce", "NO LETTUCE")],
            ),
            I("onion_rings", 1, None, ["ONION RINGS"]),
            I("fries", 1, None, ["FRIES"]),
            I("coke", 1, None, ["A COKE"]),
        ],
    ),
    X(
        "syn-t8-0164",
        """
c: hi
c: one of those pls
b: Sorry, which one would you like?
c: a large bbq chicken, an xl pepperoni n 2 xl veggies no sauce
c: an order of knots, a 20 oz iced tea n a 2 liter coke
c: pickup, cash, i have a 100
""",
        "S P P P P",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["a large bbq chicken"]),
            I("pepperoni_pizza", 1, "extra_large", ["an xl pepperoni"]),
            I("veggie_pizza", 2, "extra_large", ["2 xl veggies no sauce"], [rm("tomato_sauce", "no sauce")]),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("iced_tea", 1, "bottle_20oz", ["a 20 oz iced tea"]),
            I("coke", 1, "two_liter", ["a 2 liter coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "i have a 100"],
        change=10000,
    ),
    X(
        "syn-t8-0165",
        """
c: Hi, three large Hawaiians, one with spinach, and an order of breadsticks to 5692 Wexford Pl, apt 26.
c: Paying by card.
""",
        "P P",
        items=[
            I("hawaiian_pizza", 2, "large", ["three large Hawaiians, one with spinach"]),
            I(
                "hawaiian_pizza",
                1,
                "large",
                ["three large Hawaiians, one with spinach"],
                [add("spinach", "with spinach")],
            ),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
        ],
        method="delivery",
        method_q="to 5692 Wexford Pl, apt 26",
        addr={"raw": "5692 Wexford Pl, apt 26", "number": "5692", "street": "Wexford Pl", "unit": "apt 26"},
        pay="card",
        pay_q="Paying by card",
    ),
    X(
        "syn-t8-0166",
        """
c: ordering for tmrw 🙌 2 personal hawaiians w pepperoni n a coke 🍕
c: pickup for omar
c: at 6, card 💳
""",
        "P P P",
        items=[
            I(
                "hawaiian_pizza",
                2,
                "personal",
                ["2 personal hawaiians w pepperoni"],
                [add("pepperoni", "w pepperoni")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 6", "18:00"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t8-0167",
        """
c: HEY!
c: 2 VANILLA SHAKES FOR PICKUP, KEISHA, CASH
b: Got it, Keisha: 2 vanilla milkshakes, pickup, paying cash. Is that right?
c: YES
c: ACTUALLY SWAP THE SHAKES FOR A CHEESEBURGER
""",
        "S P C M",
        items=[I("cheeseburger", 1, None, ["A CHEESEBURGER"])],
        method="pickup",
        method_q="FOR PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Keisha",
        name_q="KEISHA",
    ),
    X(
        "syn-t8-0168",
        """
c: A MEAT LOVERS WITH BLACK OLIVES AND A 20 OZ DIET COKE
c: WHAT SIZES DO YOU HAVE
b: Personal, small, medium, large and extra large.
c: ONE OF THOSE. 9354 SUNSET CT, ASAP, CARD
""",
        "P Q P",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                None,
                ["A MEAT LOVERS WITH BLACK OLIVES", "ONE OF THOSE"],
                [add("olives", "WITH BLACK OLIVES")],
                flag="item_variant",
            ),
            I("diet_coke", 1, "bottle_20oz", ["A 20 OZ DIET COKE"]),
        ],
        method="delivery",
        method_q="9354 SUNSET CT",
        addr={"raw": "9354 SUNSET CT", "number": "9354", "street": "SUNSET CT"},
        time=("asap", "ASAP", None),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t8-0169",
        """
c: a coke
c: 58 sunset way
c: card
c: wait
c: no coke
c: 4 single cheeseburgers no ketchup instead
""",
        "P P P U M M",
        items=[
            I(
                "cheeseburger",
                4,
                "single",
                ["4 single cheeseburgers no ketchup"],
                [rm("ketchup", "no ketchup")],
            ),
        ],
        method="delivery",
        method_q="58 sunset way",
        addr={"raw": "58 sunset way", "number": "58", "street": "sunset way"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0170",
        """
c: 🍕?
c: lol
""",
        "U S",
    ),
    X(
        "syn-t8-0171",
        """
c: hey!
c: can i put in an order for tuesday
c: just an order of breadsticks
c: lol
c: pickup at 5:30
c: marcus
c: card
""",
        "S P P S P P P",
        items=[I("breadsticks", 1, None, ["an order of breadsticks"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 5:30", "17:30"),
        day=("weekday", "tue", "tuesday"),
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t8-0172",
        """
c: LARGE BBQ CHICKEN, NO BBQ SAUCE, ADD BASIL, FOR PICKUP IN 25
b: Sure! Which crust: regular, thin, thick, stuffed or gluten-free?
c: THICK
""",
        "P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "large",
                ["LARGE BBQ CHICKEN, NO BBQ SAUCE, ADD BASIL", "THICK"],
                [rm("bbq_sauce", "NO BBQ SAUCE"), add("basil", "ADD BASIL"), add("crust_thick", "THICK")],
            ),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        time=("relative", "IN 25", None),
    ),
    X(
        "syn-t8-0173",
        """
c: 3 veggie burgers w grilled mushrooms
c: to 2422 easton pl above the bakery in 20, card
""",
        "P P",
        items=[
            I(
                "veggie_burger",
                3,
                None,
                ["3 veggie burgers w grilled mushrooms"],
                [offmod("w grilled mushrooms")],
            )
        ],
        method="delivery",
        method_q="to 2422 easton pl",
        addr={
            "raw": "2422 easton pl above the bakery",
            "number": "2422",
            "street": "easton pl",
            "reference": "above the bakery",
        },
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0174",
        """
c: 2 lg hot chocs
c: 1 no whip
c: n a croissant
c: pickup
c: ivy
c: cash
c: have a 20
""",
        "P P P P P P P",
        items=[
            I("hot_chocolate", 1, "large", ["2 lg hot chocs", "1 no whip"]),
            I("hot_chocolate", 1, "large", ["2 lg hot chocs", "1 no whip"], [rm("whipped_cream", "no whip")]),
            I("croissant", 1, None, ["a croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "have a 20"],
        change=2000,
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t8-0175",
        """
c: 4 hawaiians
c: the larger ones
c: not personal or small
""",
        "P P P",
        items=[I("hawaiian_pizza", 4, None, ["4 hawaiians", "the larger ones"], flag="item_variant")],
    ),
    X(
        "syn-t8-0176",
        """
c: 2 sesame bagels 🥯 pickup for ben
c: card 💳
b: Got it, Ben: 2 sesame bagels, pickup, paying by card. Is that right?
c: 👍
c: oh wait just 1 bagel
""",
        "P P C M",
        items=[I("bagel", 1, "sesame", ["2 sesame bagels", "just 1 bagel"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t8-0177",
        """
c: hey can i get one of those office coffee things
b: Do you mean coffees for a group? Which drinks would you like?
c: oh ya: 4 small lattes, 2 lg caps w hazelnut, a small americano n 2 med drips w vanilla
c: pickup, leah
""",
        "P P P",
        items=[
            I("latte", 4, "small", ["4 small lattes"]),
            I("cappuccino", 2, "large", ["2 lg caps w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("americano", 1, "small", ["a small americano"]),
            I("drip_coffee", 2, "medium", ["2 med drips w vanilla"], [add("vanilla_syrup", "w vanilla")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t8-0178",
        """
c: 2 bec no egg n a breakfast burrito 🌯 pickup in 15 for dev
""",
        "P",
        items=[
            I("breakfast_sandwich", 2, None, ["2 bec no egg"], [rm("egg", "no egg")]),
            I(None, 1, None, ["a breakfast burrito"], unmatched="a breakfast burrito"),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 15", None),
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t8-0179",
        """
c: hi!
c: 3 med caps
c: n one of those
c: pickup maya
""",
        "S P P P",
        items=[
            I("cappuccino", 3, "medium", ["3 med caps"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t8-0180",
        """
c: 2 shakes 🥤 diff flavors, surprise me
c: 72 thornton ave asap, cash
""",
        "P P",
        items=[I("milkshake", 2, None, ["2 shakes 🥤 diff flavors"], flag="item_variant")],
        method="delivery",
        method_q="72 thornton ave",
        addr={"raw": "72 thornton ave", "number": "72", "street": "thornton ave"},
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
]
