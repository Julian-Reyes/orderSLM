"""t5 entries 0161–0190 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0161",
        """
c: hey 👋
c: 2 milkshakes pls, card, at 7:30 🥤
""",
        "S P",
        items=[I("milkshake", 2, None, ["2 milkshakes"])],
        time=("clock_time", "at 7:30", "19:30"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0162",
        """
c: 4 large cappuccinos 2 w caramel n a banana nut muffin
c: pickup asap for leah, cash
""",
        "P P",
        items=[
            I("cappuccino", 2, "large", ["4 large cappuccinos"]),
            I(
                "cappuccino",
                2,
                "large",
                ["4 large cappuccinos", "2 w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t5-0163",
        """
c: Hi, I'd like a few veggie pizzas with bacon, an extra large supreme with jalapeños, and three Cokes.
c: Pickup as soon as possible, for Leah.
c: I'll pay cash.
""",
        "P P P",
        items=[
            I("veggie_pizza", None, None, ["a few veggie pizzas"], [add("bacon", "with bacon")]),
            I(
                "supreme_pizza",
                1,
                "extra_large",
                ["an extra large supreme"],
                [add("jalapenos", "with jalapeños")],
            ),
            I("coke", 3, None, ["three Cokes"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("asap", "as soon as possible", None),
        pay="cash",
        pay_q="pay cash",
        name="Leah",
    ),
    X(
        "syn-t5-0164",
        """
c: 2 breakfast sandwiches on english muffins
c: w avocado
c: 2 cinnamon raisin bagels
c: medium latte w almond
c: card
c: asap
""",
        "P P P P P P",
        items=[
            I(
                "breakfast_sandwich",
                2,
                "english_muffin",
                ["2 breakfast sandwiches on english muffins", "w avocado"],
                [add("avocado", "w avocado")],
            ),
            I("bagel", 2, "cinnamon_raisin", ["2 cinnamon raisin bagels"]),
            I("latte", 1, "medium", ["medium latte"], [sub("whole_milk", "almond_milk", "w almond")]),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0165",
        """
c: hey
c: whats in the house coffee
b: It's a medium roast drip, black unless you add milk!
c: ok one coffee
c: w vanilla
c: and whole milk
c: card asap
""",
        "S Q P P P P",
        items=[
            I(
                "drip_coffee",
                1,
                None,
                ["one coffee"],
                [add("vanilla_syrup", "w vanilla"), add("whole_milk", "whole milk")],
            ),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0166",
        """
c: Good evening, I'd like to place an order for my coworkers.
""",
        "P",
    ),
    X(
        "syn-t5-0167",
        """
c: do u have strawberry shakes
b: We do!
c: ok one strawberry shake
c: and a cheeseburger no lettuce
c: pickup for keisha, cash
c: actually forget the shake
""",
        "Q P P P M",
        items=[I("cheeseburger", 1, None, ["a cheeseburger"], [rm("lettuce", "no lettuce")])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t5-0168",
        """
c: hi
c: 3 sesame bagels
c: do u toast them
b: We can toast them for you!
c: ok cool
c: and a large americano
c: w oat milk
c: pickup
c: tom
c: card
""",
        "S P Q S P P P P P",
        items=[
            I("bagel", 3, "sesame", ["3 sesame bagels"]),
            I("americano", 1, "large", ["a large americano"], [add("oat_milk", "w oat milk")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t5-0169",
        """
c: 3 bbq chicken pizzas thick crust, pickup in 30 for rosa, card
""",
        "P",
        items=[
            I("bbq_chicken_pizza", 3, None, ["3 bbq chicken pizzas"], [add("crust_thick", "thick crust")])
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 30", None),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t5-0170",
        """
c: Hi, could I get three large cappuccinos, two small coffees, and a chocolate croissant?
c: I'll pay by card.
b: Three large cappuccinos, two small coffees and a chocolate croissant, paying by card. Is that right?
c: Yes, that's right.
c: Actually, please leave out the croissant.
""",
        "P P C M",
        items=[
            I("cappuccino", 3, "large", ["three large cappuccinos"]),
            I("drip_coffee", 2, "small", ["two small coffees"]),
        ],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0171",
        """
c: croissant
c: hot chocolate w skim
c: card
""",
        "P P P",
        items=[
            I("croissant", 1, None, ["croissant"]),
            I("hot_chocolate", 1, None, ["hot chocolate"], [sub("whole_milk", "skim_milk", "w skim")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0172",
        """
c: heyy
c: a breakfast sandwich on a croissant no cheese
c: and a 16 oz coffee
c: card, at 10:15
""",
        "S P P P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["a breakfast sandwich on a croissant"],
                [rm("cheddar", "no cheese")],
            ),
            I("drip_coffee", 1, "large", ["a 16 oz coffee"]),
        ],
        time=("clock_time", "at 10:15", "10:15"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0173",
        """
c: hey
c: is the veggie pizza vegan
b: It has cheese, but we can leave it off!
c: ok 2 veggie pizzas
c: breadsticks
c: and garlic knots
c: cash
""",
        "S Q P P P P",
        items=[
            I("veggie_pizza", 2, None, ["2 veggie pizzas"]),
            I("breadsticks", 1, None, ["breadsticks"]),
            I("garlic_knots", 1, None, ["garlic knots"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0174",
        """
c: 2 cheeseburgers
c: 1 no pickles
c: n onion rings
c: to 23 wexford ln, cash
""",
        "P P P P",
        items=[
            I("cheeseburger", 1, None, ["2 cheeseburgers"]),
            I("cheeseburger", 1, None, ["2 cheeseburgers", "1 no pickles"], [rm("pickle", "no pickles")]),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        method="delivery",
        method_q="to 23 wexford ln",
        addr={"raw": "23 wexford ln", "number": "23", "street": "wexford ln"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0175",
        """
c: HEY!
c: A CHEESE PIZZA, TWO MEDIUM HAWAIIANS, A 20 OZ ICED TEA AND THE ONE I ALWAYS GET!
c: TO 6242 VINE TERRACE, CARD!
""",
        "S P P",
        items=[
            I("cheese_pizza", 1, None, ["A CHEESE PIZZA"]),
            I("hawaiian_pizza", 2, "medium", ["TWO MEDIUM HAWAIIANS"]),
            I("iced_tea", 1, "bottle_20oz", ["A 20 OZ ICED TEA"]),
            I(
                None,
                1,
                None,
                ["THE ONE I ALWAYS GET"],
                unmatched="THE ONE I ALWAYS GET",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="TO 6242 VINE TERRACE",
        addr={"raw": "6242 VINE TERRACE", "number": "6242", "street": "VINE TERRACE"},
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0176",
        """
c: hey
c: onion rings, a coke and a bacon burger no onions to 5580 oak st
b: Onion rings, a Coke and a bacon burger with no onions to 5580 Oak St. Is that right?
c: ya
c: actually skip the burger
""",
        "S P C M",
        items=[I("onion_rings", 1, None, ["onion rings"]), I("coke", 1, None, ["a coke"])],
        method="delivery",
        method_q="to 5580 oak st",
        addr={"raw": "5580 oak st", "number": "5580", "street": "oak st"},
    ),
    X(
        "syn-t5-0177",
        """
c: some sprites and 3 cheeseburgers
c: delivery
c: card
""",
        "P P P",
        items=[I("sprite", None, None, ["some sprites"]), I("cheeseburger", 3, None, ["3 cheeseburgers"])],
        method="delivery",
        method_q="delivery",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0178",
        """
c: a few medium americanos, a breakfast sandwich n a medium hot chocolate w almond milk
c: asap pls
""",
        "P P",
        items=[
            I("americano", None, "medium", ["a few medium americanos"]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
            I(
                "hot_chocolate",
                1,
                "medium",
                ["a medium hot chocolate"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
        ],
        time=("asap", "asap", None),
    ),
    X(
        "syn-t5-0179",
        """
c: 2 cheeseburgers
c: veggie burger n a 16 oz coke
c: pickup, card
""",
        "P P P",
        items=[
            I("cheeseburger", 2, None, ["2 cheeseburgers"]),
            I("veggie_burger", 1, None, ["veggie burger"]),
            I("coke", 1, None, ["a 16 oz coke"], unmatched_variant="16 oz"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0180",
        """
c: hi! bacon burger w mayo, a single cheeseburger, 2 onion rings and a 12 oz lemonade 🍋
c: pickup at 6, cash 💵
""",
        "P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger"], [add("mayo", "w mayo")]),
            I("cheeseburger", 1, "single", ["a single cheeseburger"]),
            I("onion_rings", 2, None, ["2 onion rings"]),
            I("lemonade", 1, None, ["a 12 oz lemonade"], unmatched_variant="12 oz"),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 6", "18:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0181",
        """
c: Good afternoon.
c: Three plain croissants with butter, please.
c: And a chocolate chip muffin.
c: Also a small latte with almond milk.
c: I'll pay by card.
c: Thank you.
""",
        "S P P P P S",
        items=[
            I("croissant", 3, "plain", ["Three plain croissants"], [add("butter", "with butter")]),
            I("muffin", 1, "chocolate_chip", ["a chocolate chip muffin"]),
            I("latte", 1, "small", ["a small latte"], [sub("whole_milk", "almond_milk", "with almond milk")]),
        ],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0182",
        """
c: Good morning!
c: Two medium lattes, a hot chocolate with vanilla, two chocolate chip muffins, and the usual, please.
c: Ready at 9:45, if possible.
""",
        "S P P",
        items=[
            I("latte", 2, "medium", ["Two medium lattes"]),
            I("hot_chocolate", 1, None, ["a hot chocolate"], [add("vanilla_syrup", "with vanilla")]),
            I("muffin", 2, "chocolate_chip", ["two chocolate chip muffins"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        time=("clock_time", "at 9:45", "09:45"),
    ),
    X(
        "syn-t5-0183",
        """
c: some supreme pizzas
c: 999 vine ct, side entrance
c: card
""",
        "P P P",
        items=[I("supreme_pizza", None, None, ["some supreme pizzas"])],
        method="delivery",
        method_q="999 vine ct",
        addr={
            "raw": "999 vine ct, side entrance",
            "number": "999",
            "street": "vine ct",
            "reference": "side entrance",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0184",
        """
c: Hi, I'd like four personal margherita pizzas, three of them on gluten-free crust, a Coke, and two medium veggie pizzas with no onions and bacon added, for pickup in 30 minutes. I'll pay by card.
""",
        "P",
        items=[
            I("margherita_pizza", 1, "personal", ["four personal margherita pizzas"]),
            I(
                "margherita_pizza",
                3,
                "personal",
                ["four personal margherita pizzas", "three of them on gluten-free crust"],
                [add("crust_gluten_free", "on gluten-free crust")],
            ),
            I("coke", 1, None, ["a Coke"]),
            I(
                "veggie_pizza",
                2,
                "medium",
                ["two medium veggie pizzas"],
                [rm("onions", "no onions"), add("bacon", "bacon added")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in 30 minutes", None),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0185",
        """
c: some chocolate shakes for delivery
c: card
""",
        "P P",
        items=[I("milkshake", None, "chocolate", ["some chocolate shakes"])],
        method="delivery",
        method_q="for delivery",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0186",
        """
c: hi! a choc chip muffin and a small skim cappuccino pls ☕
c: pickup for grace, card
b: A chocolate chip muffin and a small cappuccino with skim milk, pickup for Grace, card. Correct?
c: yes 😊
c: actually just the muffin!
""",
        "P P C M",
        items=[I("muffin", 1, "chocolate_chip", ["a choc chip muffin"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t5-0187",
        """
c: 2 cans of iced tea for pickup, cash
c: actually make them 20 oz bottles
""",
        "P M",
        items=[I("iced_tea", 2, "bottle_20oz", ["2 cans of iced tea", "make them 20 oz bottles"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0188",
        """
c: 6 veggie burgers
c: 2 w mustard
c: double cheeseburger no tomato, cash
""",
        "P P P",
        items=[
            I("veggie_burger", 4, None, ["6 veggie burgers"]),
            I("veggie_burger", 2, None, ["6 veggie burgers", "2 w mustard"], [add("mustard", "w mustard")]),
            I("cheeseburger", 1, "double", ["double cheeseburger"], [rm("tomato", "no tomato")]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0189",
        """
c: 5 large coffees
c: 3 w caramel
c: and a croissant
c: card
c: in 15
""",
        "P P P P P",
        items=[
            I("drip_coffee", 2, "large", ["5 large coffees"]),
            I(
                "drip_coffee",
                3,
                "large",
                ["5 large coffees", "3 w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
            I("croissant", 1, None, ["a croissant"]),
        ],
        time=("relative", "in 15", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0190",
        """
c: Hi, I'd like a small latte for pickup under Leah, paying by card.
c: Could you make that with skim milk instead?
""",
        "P M",
        items=[
            I(
                "latte",
                1,
                "small",
                ["a small latte", "make that with skim milk instead"],
                [sub("whole_milk", "skim_milk", "with skim milk instead")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="paying by card",
        name="Leah",
    ),
]
