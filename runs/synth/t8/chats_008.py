"""t8 syn-t8-0211–0240 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t8-0211",
        """
c: 4 veggie burgers
c: half w mustard
c: 2 fries
c: strawberry shake
c: card
""",
        "P P P P P",
        items=[
            I("veggie_burger", 2, None, ["4 veggie burgers", "half w mustard"]),
            I(
                "veggie_burger",
                2,
                None,
                ["4 veggie burgers", "half w mustard"],
                [add("mustard", "w mustard")],
            ),
            I("fries", 2, None, ["2 fries"]),
            I("milkshake", 1, "strawberry", ["strawberry shake"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0212",
        """
c: Hi, a personal margherita with no fresh mozzarella and pineapple, two iced teas, and the one I always get.
c: Card, please.
""",
        "P P",
        items=[
            I(
                "margherita_pizza",
                1,
                "personal",
                ["a personal margherita with no fresh mozzarella and pineapple"],
                [rm("mozzarella", "no fresh mozzarella"), add("pineapple", "pineapple")],
            ),
            I("iced_tea", 2, None, ["two iced teas"]),
            I(
                None,
                1,
                None,
                ["the one I always get"],
                unmatched="the one I always get",
                flag="item_menu_match",
            ),
        ],
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0213",
        """
c: hey 🍕
c: 2 pepperonis no pepperoni lol, thin crust
c: one of the bigger sizes for both
c: n a can of coke, pickup, card
""",
        "S P P P",
        items=[
            I(
                "pepperoni_pizza",
                2,
                None,
                ["2 pepperonis no pepperoni", "one of the bigger sizes for both"],
                [rm("pepperoni", "no pepperoni"), add("crust_thin", "thin crust")],
                flag="item_variant",
            ),
            I("coke", 1, "can", ["a can of coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0214",
        """
c: Hi, some Sprites delivered at 7:45, cash, I'll have a 20.
""",
        "P",
        items=[I("sprite", None, None, ["some Sprites"])],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 7:45", "19:45"),
        pay="cash",
        pay_q=["cash", "I'll have a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0215",
        """
c: Two everything bagels and a breakfast sandwich, please.
c: Pickup for Ivy, cash. I'll have a 20.
b: Got it, Ivy: 2 everything bagels and 1 breakfast sandwich, pickup, paying cash. Is that right?
c: Yes.
c: Actually, please take off the breakfast sandwich.
""",
        "P P C M",
        items=[I("bagel", 2, "everything", ["Two everything bagels"])],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q=["cash", "I'll have a 20"],
        change=2000,
        name="Ivy",
        name_q="Ivy",
    ),
    X(
        "syn-t8-0216",
        """
c: hi ☀️
c: a cap pls ☕
c: whatever size is bigger than small
c: pickup keisha
""",
        "S P P P",
        items=[
            I("cappuccino", 1, None, ["a cap", "whatever size is bigger than small"], flag="item_variant")
        ],
        method="pickup",
        method_q="pickup",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t8-0217",
        """
c: morning
c: coffee + pastry deal
c: drip n a muffin
c: pickup nico
""",
        "S P P P",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["coffee + pastry deal", "drip n a muffin"],
                combo={"drink": "drip_coffee", "pastry": "muffin"},
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t8-0218",
        """
c: Hi, can I order an iced tea for tomorrow?
c: I'll pick it up at 1. Name is Nico.
""",
        "P P",
        items=[I("iced_tea", 1, None, ["an iced tea"])],
        method="pickup",
        method_q="I'll pick it up",
        time=("clock_time", "at 1", "13:00"),
        day=("tomorrow", "tomorrow"),
        name="Nico",
        name_q="Nico",
    ),
    X(
        "syn-t8-0219",
        """
c: A COFFEE WITH CARAMEL AND A CROISSANT
c: PICKUP FOR JORDAN
c: CASH
c: SKIP THE CROISSANT
""",
        "P P P M",
        items=[I("drip_coffee", 1, None, ["A COFFEE WITH CARAMEL"], [add("caramel_syrup", "WITH CARAMEL")])],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Jordan",
        name_q="JORDAN",
    ),
    X(
        "syn-t8-0220",
        """
c: hi 👋 we have a big meeting monday, need coffee n pastries for 40 ppl, can i talk to someone about it?
""",
        "P/HU",
        time=("ambiguous", "monday"),
        day=("weekday", "mon", "monday"),
    ),
    X(
        "syn-t8-0221",
        """
c: can i order for thurs
b: Yes, you can order up to a week ahead!
c: 2 bec for thurs at 8, card
""",
        "D P",
        items=[I("breakfast_sandwich", 2, None, ["2 bec"])],
        time=("clock_time", "at 8", "08:00"),
        day=("weekday", "thu", (2, "thurs")),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0222",
        """
c: Hello!
c: Six medium margheritas, five of them with no sauce.
c: An extra large pepperoni with feta.
c: And two orders of garlic knots.
""",
        "S P P P",
        items=[
            I("margherita_pizza", 1, "medium", ["Six medium margheritas, five of them with no sauce"]),
            I(
                "margherita_pizza",
                5,
                "medium",
                ["Six medium margheritas, five of them with no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I(
                "pepperoni_pizza",
                1,
                "extra_large",
                ["An extra large pepperoni with feta"],
                [add("feta_cheese", "with feta")],
            ),
            I("garlic_knots", 2, None, ["two orders of garlic knots"]),
        ],
    ),
    X(
        "syn-t8-0223",
        """
c: 2 XL DRIP COFFEES ASAP FOR PICKUP, MARCUS, CASH
""",
        "P",
        items=[I("drip_coffee", 2, None, ["2 XL DRIP COFFEES"], unmatched_variant="XL")],
        method="pickup",
        method_q="FOR PICKUP",
        time=("asap", "ASAP", None),
        pay="cash",
        pay_q="CASH",
        name="Marcus",
        name_q="MARCUS",
    ),
    X(
        "syn-t8-0224",
        """
c: hi
c: order for sunday oct 25
c: a diet coke
c: lol thats it
c: 372 glenwood rd
c: above the bakery
c: at 5
c: cash
""",
        "S P P S P P P P",
        items=[I("diet_coke", 1, None, ["a diet coke"])],
        method="delivery",
        method_q="372 glenwood rd",
        addr={
            "raw": "372 glenwood rd",
            "number": "372",
            "street": "glenwood rd",
            "reference": "above the bakery",
            "q": "372 glenwood rd",
        },
        time=("clock_time", "at 5", "17:00"),
        day=("date", 10, 25, "oct 25"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0225",
        """
c: hey
c: hawaiian w feta
c: the larger size, not sure which one
""",
        "S P P",
        items=[
            I(
                "hawaiian_pizza",
                1,
                None,
                ["hawaiian w feta", "the larger size"],
                [add("feta_cheese", "w feta")],
                flag="item_variant",
            )
        ],
    ),
    X(
        "syn-t8-0226",
        """
c: same as last time
b: Sorry, we can't see past orders here. What would you like?
c: 3 cheeseburgers no pickles, a veggie burger, rings, 4 cokes n 2 sprites, pickup in 20, cash
""",
        "P P",
        items=[
            I("cheeseburger", 3, None, ["3 cheeseburgers no pickles"], [rm("pickle", "no pickles")]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("onion_rings", 1, None, ["rings"]),
            I("coke", 4, None, ["4 cokes"]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0227",
        """
c: IS THE HOT CHOCOLATE SWEET?
b: It's rich and sweet, with whipped cream on top.
c: OK ONE WITH NO WHIP AND VANILLA, AND A LARGE CAPPUCCINO. PICKUP FOR BEN, CASH
b: Got it, Ben: 1 hot chocolate with no whipped cream and vanilla, 1 large cappuccino, pickup, paying cash. Is that right?
c: YEP
""",
        "Q P C",
        items=[
            I(
                "hot_chocolate",
                1,
                None,
                ["ONE WITH NO WHIP AND VANILLA"],
                [rm("whipped_cream", "NO WHIP"), add("vanilla_syrup", "VANILLA")],
            ),
            I("cappuccino", 1, "large", ["A LARGE CAPPUCCINO"]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Ben",
        name_q="BEN",
        decision="confirmed",
        decision_q="YEP",
    ),
    X(
        "syn-t8-0228",
        """
c: Good afternoon!
c: Three bagels, any kind but plain, and a small hot chocolate.
c: Cash.
""",
        "S P P",
        items=[
            I("bagel", 3, None, ["Three bagels, any kind but plain"], flag="item_variant"),
            I("hot_chocolate", 1, "small", ["a small hot chocolate"]),
        ],
        pay="cash",
        pay_q="Cash",
    ),
    X(
        "syn-t8-0229",
        """
c: ordering for monday
c: a croissant n 2 small hot chocs w almond milk n vanilla
c: pickup 7:45, omar
c: card
""",
        "P P P P",
        items=[
            I("croissant", 1, None, ["a croissant"]),
            I(
                "hot_chocolate",
                2,
                "small",
                ["2 small hot chocs w almond milk n vanilla"],
                [sub("whole_milk", "almond_milk", "w almond milk"), add("vanilla_syrup", "vanilla")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "7:45", "07:45"),
        day=("weekday", "mon", "monday"),
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t8-0230",
        """
c: the usual pls 🙏
b: Sorry, we can't see past orders here. What would you like?
c: 2 large margheritas, a large cheese w pineapple, 3 cans of diet coke, 3 sprites, 2 20 oz cokes n a can of iced tea. do u have ranch? 🤔
b: No ranch, sorry!
c: ok np. 6065 easton ct, card
""",
        "P P/Q P",
        items=[
            I("margherita_pizza", 2, "large", ["2 large margheritas"]),
            I("cheese_pizza", 1, "large", ["a large cheese w pineapple"], [add("pineapple", "w pineapple")]),
            I("diet_coke", 3, "can", ["3 cans of diet coke"]),
            I("sprite", 3, None, ["3 sprites"]),
            I("coke", 2, "bottle_20oz", ["2 20 oz cokes"]),
            I("iced_tea", 1, "can", ["a can of iced tea"]),
        ],
        method="delivery",
        method_q="6065 easton ct",
        addr={"raw": "6065 easton ct", "number": "6065", "street": "easton ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0231",
        """
c: a double cheeseburger, 2 lemonades n 3 vanilla shakes 🍔
c: are the shakes big?
b: 16 oz each!
c: nice 😎 pickup for ben, card
c: actually make the cheeseburger a single
""",
        "P Q P M",
        items=[
            I("cheeseburger", 1, "single", ["a double cheeseburger", "make the cheeseburger a single"]),
            I("lemonade", 2, None, ["2 lemonades"]),
            I("milkshake", 3, "vanilla", ["3 vanilla shakes"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t8-0232",
        """
c: a shake 🥤 any flavor u recommend
c: cash, i have a 20
""",
        "P P",
        items=[I("milkshake", 1, None, ["a shake 🥤 any flavor u recommend"], flag="item_variant")],
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0233",
        """
c: Hi, a medium margherita with garlic, four large cheese pizzas with no cheese blend and ground beef, and an order of garlic knots.
c: Is the ground beef seasoned?
b: Yes, lightly seasoned. Anything else?
c: In 30 minutes, cash, I have a 100. Actually, swap the garlic knots for a large meat lovers.
""",
        "P Q M",
        items=[
            I(
                "margherita_pizza",
                1,
                "medium",
                ["a medium margherita with garlic"],
                [add("garlic", "with garlic")],
            ),
            I(
                "cheese_pizza",
                4,
                "large",
                ["four large cheese pizzas with no cheese blend and ground beef"],
                [rm("cheese", "no cheese blend"), add("beef", "ground beef")],
            ),
            I("meat_lovers_pizza", 1, "large", ["a large meat lovers"]),
        ],
        time=("relative", "In 30 minutes", None),
        pay="cash",
        pay_q=["cash", "I have a 100"],
        change=10000,
    ),
    X(
        "syn-t8-0234",
        """
c: hi
c: 5 bec, 4 w no bacon
c: n a chocolate croissant
c: pickup maya, card
""",
        "S P P P",
        items=[
            I("breakfast_sandwich", 1, None, ["5 bec, 4 w no bacon"]),
            I("breakfast_sandwich", 4, None, ["5 bec, 4 w no bacon"], [rm("bacon", "no bacon")]),
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t8-0235",
        """
c: hey we want to do a coffee bar for our office wednesday, like 50 ppl
c: who can i talk to about that
""",
        "P HU",
        time=("ambiguous", "wednesday"),
        day=("weekday", "wed", "wednesday"),
    ),
    X(
        "syn-t8-0236",
        """
c: Hi, a small meat lovers, a Coke and a Sprite. What drink sizes do you have?
b: Cans, 20 oz bottles and 2-liters.
c: A 20 oz Sprite and a can of Coke, then. Pickup, card.
""",
        "P/Q P",
        items=[
            I("meat_lovers_pizza", 1, "small", ["a small meat lovers"]),
            I("coke", 1, "can", ["a Coke", "a can of Coke"]),
            I("sprite", 1, "bottle_20oz", ["a Sprite", "A 20 oz Sprite"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0237",
        """
c: 2 PERSONAL SUPREMES WITH STUFFED CRUST AND ONE OF THOSE
c: 29 PROSPECT TERRACE, BLUE DOOR
""",
        "P P",
        items=[
            I(
                "supreme_pizza",
                2,
                "personal",
                ["2 PERSONAL SUPREMES WITH STUFFED CRUST"],
                [add("crust_stuffed", "STUFFED CRUST")],
            ),
            I(None, 1, None, ["ONE OF THOSE"], unmatched="ONE OF THOSE", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="29 PROSPECT TERRACE",
        addr={
            "raw": "29 PROSPECT TERRACE, BLUE DOOR",
            "number": "29",
            "street": "PROSPECT TERRACE",
            "reference": "BLUE DOOR",
        },
    ),
    X(
        "syn-t8-0238",
        """
c: HELLO
c: A CHEESEBURGER WITH MAYO, DO YOU HAVE PEPSI? AND AN ORDER OF ONION RINGS
b: No Pepsi, sorry. We have Coke, Sprite and lemonade.
c: OK A COKE THEN. PICKUP
""",
        "S P/Q P",
        items=[
            I("cheeseburger", 1, None, ["A CHEESEBURGER WITH MAYO"], [add("mayo", "WITH MAYO")]),
            I("onion_rings", 1, None, ["AN ORDER OF ONION RINGS"]),
            I("coke", 1, None, ["A COKE"]),
        ],
        method="pickup",
        method_q="PICKUP",
    ),
    X(
        "syn-t8-0239",
        """
c: xl bbq chicken w bacon n capers 🍕
c: xl hawaiian w olive oil, thick crust
c: n a 2 liter dr pepper
""",
        "P P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "extra_large",
                ["xl bbq chicken w bacon n capers"],
                [add("bacon", "w bacon"), offmod("capers")],
            ),
            I(
                "hawaiian_pizza",
                1,
                "extra_large",
                ["xl hawaiian w olive oil, thick crust"],
                [add("olive_oil", "w olive oil"), add("crust_thick", "thick crust")],
            ),
            I("dr_pepper", 1, "two_liter", ["a 2 liter dr pepper"]),
        ],
    ),
    X(
        "syn-t8-0240",
        """
c: Good morning!
c: Four banana nut muffins for pickup, please. The name is Tara.
b: Got it, Tara: 4 banana nut muffins for pickup. Is that right?
c: Yes, thank you.
c: Oh, sorry, could I get two plain bagels instead of the muffins?
""",
        "S P C M",
        items=[I("bagel", 2, "plain", ["two plain bagels instead of the muffins"])],
        method="pickup",
        method_q="for pickup",
        name="Tara",
        name_q="Tara",
    ),
]
