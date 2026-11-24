"""t8 syn-t8-0001–0030 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t8-0001",
        """
c: hey
c: bacon burger w jalapenos n a shake
c: 2 rings
c: n one of those
c: pickup, card
""",
        "S P P P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger w jalapenos"], [add("jalapeno", "w jalapenos")]),
            I("milkshake", 1, None, ["a shake"]),
            I("onion_rings", 2, None, ["2 rings"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0002",
        """
c: hi there
c: lg hawaiian n some garlic knots
c: deliver to 2005 ivanhoe ave
""",
        "S P P",
        items=[
            I("hawaiian_pizza", 1, "large", ["lg hawaiian"]),
            I("garlic_knots", None, None, ["some garlic knots"]),
        ],
        method="delivery",
        method_q="deliver to 2005 ivanhoe ave",
        addr={"raw": "2005 ivanhoe ave", "number": "2005", "street": "ivanhoe ave"},
    ),
    X(
        "syn-t8-0003",
        """
c: hey 👋 2 double cheeseburgers 🍔🍔, a jumbo fries 🍟 n a lemonade 🍋 to 364 magnolia dr in 30 min pls
""",
        "P",
        items=[
            I("cheeseburger", 2, "double", ["2 double cheeseburgers"]),
            I("fries", 1, None, ["a jumbo fries"], unmatched_variant="jumbo"),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="to 364 magnolia dr",
        addr={"raw": "364 magnolia dr", "number": "364", "street": "magnolia dr"},
        time=("relative", "in 30 min", None),
    ),
    X(
        "syn-t8-0004",
        """
c: 2 medium meat lovers no pepperoni, thin crust
c: n an order of breadsticks + a 20 oz dr pepper
c: asap, card
c: actually make the meat lovers gluten free crust instead of thin
""",
        "P P P M",
        items=[
            I(
                "meat_lovers_pizza",
                2,
                "medium",
                [
                    "2 medium meat lovers no pepperoni, thin crust",
                    "make the meat lovers gluten free crust instead of thin",
                ],
                [
                    rm("pepperoni", "no pepperoni"),
                    add("crust_gluten_free", "gluten free crust instead of thin"),
                ],
            ),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
            I("dr_pepper", 1, "bottle_20oz", ["a 20 oz dr pepper"]),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0005",
        """
c: hi
c: xl veggie
c: 2 orders breadsticks
c: 4 waters
c: n 2 two liter dr peppers
c: pickup
c: name maya
""",
        "S P P P P P P",
        items=[
            I("veggie_pizza", 1, "extra_large", ["xl veggie"]),
            I("breadsticks", 2, None, ["2 orders breadsticks"]),
            I("water", 4, None, ["4 waters"]),
            I("dr_pepper", 2, "two_liter", ["2 two liter dr peppers"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t8-0006",
        """
c: supreme
c: one of the bigger sizes
c: w parm n thick crust
c: + a 20oz iced tea
c: 35 grant st, cash, have a 50
""",
        "P P P P P",
        items=[
            I(
                "supreme_pizza",
                1,
                None,
                ["supreme", "one of the bigger sizes", "w parm n thick crust"],
                [add("parmesan", "w parm"), add("crust_thick", "thick crust")],
                flag="item_variant",
            ),
            I("iced_tea", 1, "bottle_20oz", ["a 20oz iced tea"]),
        ],
        method="delivery",
        method_q="35 grant st",
        addr={"raw": "35 grant st", "number": "35", "street": "grant st"},
        pay="cash",
        pay_q=["cash", "have a 50"],
        change=5000,
    ),
    X(
        "syn-t8-0007",
        """
c: hey!!
c: 3 medium cheese thin crust
c: 2 large margheritas
c: 3 large pepperoni
c: does the margherita have fresh basil?
b: Yes, fresh basil and mozzarella!
c: nice. a 20 oz dr pepper n an iced tea too
c: pickup for grace
""",
        "S P P P Q P P",
        items=[
            I("cheese_pizza", 3, "medium", ["3 medium cheese thin crust"], [add("crust_thin", "thin crust")]),
            I("margherita_pizza", 2, "large", ["2 large margheritas"]),
            I("pepperoni_pizza", 3, "large", ["3 large pepperoni"]),
            I("dr_pepper", 1, "bottle_20oz", ["a 20 oz dr pepper"]),
            I("iced_tea", 1, None, ["an iced tea"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t8-0008",
        """
c: Hi, could I get 2 cans of iced tea, and is the iced tea sweetened? Also a medium pepperoni, please.
b: It's lightly sweetened.
c: Great. Pickup for Luis, paying by card.
""",
        "P/Q P",
        items=[
            I("iced_tea", 2, "can", ["2 cans of iced tea"]),
            I("pepperoni_pizza", 1, "medium", ["a medium pepperoni"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="paying by card",
        name="Luis",
        name_q="Luis",
    ),
    X(
        "syn-t8-0009",
        """
c: can i get 3 shakes, 2 bacon burgers w mustard, 4 rings n 2 of the big burgers to 335 hawthorne ln unit 15
""",
        "P",
        items=[
            I("milkshake", 3, None, ["3 shakes"]),
            I("bacon_burger", 2, None, ["2 bacon burgers w mustard"], [add("mustard", "w mustard")]),
            I("onion_rings", 4, None, ["4 rings"]),
            I(None, 2, None, ["2 of the big burgers"], unmatched="the big burgers", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="to 335 hawthorne ln unit 15",
        addr={"raw": "335 hawthorne ln unit 15", "number": "335", "street": "hawthorne ln", "unit": "15"},
    ),
    X(
        "syn-t8-0010",
        """
c: hi 😊 a cheeseburger combo no cheese pls + 3 sprites
c: what sides come w the combo?
b: Fries or onion rings, and a drink: Coke, Sprite or lemonade.
c: rings n a coke 🥤 paying cash 💵
""",
        "P Q P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["a cheeseburger combo no cheese", "rings n a coke"],
                [rm("cheese", "no cheese")],
                combo={"side": "onion_rings", "drink": "coke"},
            ),
            I("sprite", 3, None, ["3 sprites"]),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t8-0011",
        """
c: Hello, I'd like a breakfast sandwich on an English muffin with avocado, a hot chocolate with coconut milk and hazelnut, and an almond croissant. Pickup for Eli, cash, I have a 20.
""",
        "P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["a breakfast sandwich on an English muffin with avocado"],
                [add("avocado", "with avocado")],
            ),
            I(
                "hot_chocolate",
                1,
                None,
                ["a hot chocolate with coconut milk and hazelnut"],
                [offmod("coconut milk"), add("hazelnut_syrup", "hazelnut")],
            ),
            I("croissant", 1, "almond", ["an almond croissant"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q=["cash", "I have a 20"],
        change=2000,
        name="Eli",
        name_q="Eli",
    ),
    X(
        "syn-t8-0012",
        """
c: 2 strawberry shakes for pickup at 6:30, cash, paying w a 20
b: Got it: 2 strawberry milkshakes, pickup at 6:30 PM, paying cash. Is that right?
c: yep
c: actually make them both vanilla
""",
        "P C M",
        items=[I("milkshake", 2, "vanilla", ["2 strawberry shakes", "make them both vanilla"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6:30", "18:30"),
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0013",
        """
c: 2 personal meat lovers w onions n 3 orders of knots
c: n a party size cheese pizza
c: n a cannoli
c: to 58 thornton way above the bakery, card, in 40 min
""",
        "P P P P",
        items=[
            I(
                "meat_lovers_pizza",
                2,
                "personal",
                ["2 personal meat lovers w onions"],
                [add("onions", "w onions")],
            ),
            I("garlic_knots", 3, None, ["3 orders of knots"]),
            I("cheese_pizza", 1, None, ["a party size cheese pizza"], unmatched_variant="party size"),
            I(None, 1, None, ["a cannoli"], unmatched="a cannoli"),
        ],
        method="delivery",
        method_q="to 58 thornton way",
        addr={
            "raw": "58 thornton way above the bakery",
            "number": "58",
            "street": "thornton way",
            "reference": "above the bakery",
        },
        time=("relative", "in 40 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0014",
        """
c: coffee n pastry deal pls
b: Sure! Which drink (drip coffee, latte or americano) and which pastry (croissant or muffin)?
c: a medium latte n a plain croissant. also a small hot choc n 2 sm caps w oat milk, at 9:15, cash
""",
        "P P",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["coffee n pastry deal", "a medium latte n a plain croissant"],
                combo={"drink": ("latte", "medium"), "pastry": ("croissant", "plain")},
            ),
            I("hot_chocolate", 1, "small", ["a small hot choc"]),
            I(
                "cappuccino",
                2,
                "small",
                ["2 sm caps w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
        ],
        time=("clock_time", "at 9:15", "09:15"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0015",
        """
c: hiii ☕ a large latte w almond milk, an americano n my usual 😅
c: cash 💵
""",
        "P P",
        items=[
            I(
                "latte",
                1,
                "large",
                ["a large latte w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
            I("americano", 1, None, ["an americano"]),
            I(None, 1, None, ["my usual"], unmatched="my usual", flag="item_menu_match"),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0016",
        """
c: fries n 3 cokes to 3527 lakeview ln at 7:15, card
b: Got it: 1 fries and 3 Cokes, delivered to 3527 Lakeview Ln at 7:15 PM, paying by card. Is that right?
c: ya
""",
        "P C",
        items=[
            I("fries", 1, None, ["fries"]),
            I("coke", 3, None, ["3 cokes"]),
        ],
        method="delivery",
        method_q="to 3527 lakeview ln",
        addr={"raw": "3527 lakeview ln", "number": "3527", "street": "lakeview ln"},
        time=("clock_time", "at 7:15", "19:15"),
        pay="card",
        pay_q="card",
        decision="confirmed",
        decision_q="ya",
    ),
    X(
        "syn-t8-0017",
        """
c: hey ☀️ an almond croissant n a chai latte pls 🥐
c: pickup for tom
""",
        "P P",
        items=[
            I("croissant", 1, "almond", ["an almond croissant"]),
            I(None, 1, None, ["a chai latte"], unmatched="a chai latte"),
        ],
        method="pickup",
        method_q="pickup",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t8-0018",
        """
c: Good morning!
c: Could I get a muffin and one of those, as soon as possible? Pickup for Luis.
""",
        "S P",
        items=[
            I("muffin", 1, None, ["a muffin"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="Pickup",
        time=("asap", "as soon as possible", None),
        name="Luis",
        name_q="Luis",
    ),
    X(
        "syn-t8-0019",
        """
c: hi
c: need food for like 30 ppl tmrw for a work thing
c: can i talk to someone about a big order like that
""",
        "S P HU",
        time=("ambiguous", "tmrw"),
        day=("tomorrow", "tmrw"),
    ),
    X(
        "syn-t8-0020",
        """
c: yo
c: 6 bacon burgers, 2 of em w mayo
c: 3 veggie
c: 2 rings
c: n a cheeseburger single
c: 1882 alder st, cash
""",
        "S P P P P P",
        items=[
            I("bacon_burger", 4, None, ["6 bacon burgers, 2 of em w mayo"]),
            I("bacon_burger", 2, None, ["6 bacon burgers, 2 of em w mayo"], [add("mayo", "w mayo")]),
            I("veggie_burger", 3, None, ["3 veggie"]),
            I("onion_rings", 2, None, ["2 rings"]),
            I("cheeseburger", 1, "single", ["a cheeseburger single"]),
        ],
        method="delivery",
        method_q="1882 alder st",
        addr={"raw": "1882 alder st", "number": "1882", "street": "alder st"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0021",
        """
c: HI THERE
c: ORDERING FOR FRIDAY, 3 VEGGIE BURGERS WITH CHEESE AND AN ORDER OF ONION RINGS
c: WE'LL COME GET IT AT 12:30
c: CASH
""",
        "S P P P",
        items=[
            I("veggie_burger", 3, None, ["3 VEGGIE BURGERS WITH CHEESE"], [add("cheese", "WITH CHEESE")]),
            I("onion_rings", 1, None, ["AN ORDER OF ONION RINGS"]),
        ],
        method="pickup",
        method_q="WE'LL COME GET IT",
        time=("clock_time", "AT 12:30", "12:30"),
        day=("weekday", "fri", "FRIDAY"),
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t8-0022",
        """
c: HELLO!!
c: 2 MEDIUM FRIES AND A SIDE SALAD TO 55 BROOKSIDE ST APT 6C, CARD, ASAP
""",
        "S P",
        items=[
            I("fries", 2, None, ["2 MEDIUM FRIES"], unmatched_variant="MEDIUM"),
            I(None, 1, None, ["A SIDE SALAD"], unmatched="A SIDE SALAD"),
        ],
        method="delivery",
        method_q="TO 55 BROOKSIDE ST APT 6C",
        addr={"raw": "55 BROOKSIDE ST APT 6C", "number": "55", "street": "BROOKSIDE ST", "unit": "APT 6C"},
        time=("asap", "ASAP", None),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t8-0023",
        """
c: Hi!
c: I'd like a cheese pizza with no sauce, one of the larger sizes, and a 20 oz Diet Coke.
c: For pickup.
c: Card is fine.
""",
        "S P P P",
        items=[
            I(
                "cheese_pizza",
                1,
                None,
                ["a cheese pizza with no sauce, one of the larger sizes"],
                [rm("tomato_sauce", "no sauce")],
                flag="item_variant",
            ),
            I("diet_coke", 1, "bottle_20oz", ["a 20 oz Diet Coke"]),
        ],
        method="pickup",
        method_q="For pickup",
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0024",
        """
c: Hello, three lattes please, a bigger size than small, and a banana nut muffin.
c: As soon as you can, for Maya. I'll pay cash.
""",
        "P P",
        items=[
            I("latte", 3, None, ["three lattes please, a bigger size than small"], flag="item_variant"),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
        time=("asap", "As soon as you can", None),
        pay="cash",
        pay_q="I'll pay cash",
        name="Maya",
        name_q="Maya",
    ),
    X(
        "syn-t8-0025",
        """
c: hey ordering for tmrw
c: personal hawaiian n a coke
c: pickup at 7 for grace
""",
        "P P P",
        items=[
            I("hawaiian_pizza", 1, "personal", ["personal hawaiian"]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "19:00"),
        day=("tomorrow", "tmrw"),
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t8-0026",
        """
c: hawaiian thin crust, one of the big ones, pickup, card
""",
        "P",
        items=[
            I(
                "hawaiian_pizza",
                1,
                None,
                ["hawaiian thin crust, one of the big ones"],
                [add("crust_thin", "thin crust")],
                flag="item_variant",
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0027",
        """
c: hm
c: the
""",
        "U U",
    ),
    X(
        "syn-t8-0028",
        """
c: hey 🍔 is the avocado fresh?
b: Yes, sliced fresh every morning!
c: 👍
c: a bacon burger w avocado then, cash 💵, pickup
b: Got it: 1 Bacon Burger with avocado, pickup, paying cash. Is that right?
c: 👍
""",
        "Q S P C",
        items=[I("bacon_burger", 1, None, ["a bacon burger w avocado"], [add("avocado", "w avocado")])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        decision="confirmed",
        decision_q="👍",
    ),
    X(
        "syn-t8-0029",
        """
c: CINNAMON RAISIN BAGEL AND A LARGE OAT LATTE
c: PICKUP FOR ROSA
c: CASH, I HAVE A 20
c: ACTUALLY ALMOND MILK INSTEAD OF OAT
""",
        "P P P M",
        items=[
            I("bagel", 1, "cinnamon_raisin", ["CINNAMON RAISIN BAGEL"]),
            I(
                "latte",
                1,
                "large",
                ["A LARGE OAT LATTE", "ALMOND MILK INSTEAD OF OAT"],
                [sub("whole_milk", "almond_milk", "ALMOND MILK INSTEAD OF OAT")],
            ),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q=["CASH", "I HAVE A 20"],
        change=2000,
        name="Rosa",
        name_q="ROSA",
    ),
    X(
        "syn-t8-0030",
        """
c: big order 🙌 2 strawberry shakes, a veggie burger w cheese, a bacon burger, a sprite n 4 cheeseburgers 🍔
c: 986 ivanhoe ln, card 💳
""",
        "P P",
        items=[
            I("milkshake", 2, "strawberry", ["2 strawberry shakes"]),
            I("veggie_burger", 1, None, ["a veggie burger w cheese"], [add("cheese", "w cheese")]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("sprite", 1, None, ["a sprite"]),
            I("cheeseburger", 4, None, ["4 cheeseburgers"]),
        ],
        method="delivery",
        method_q="986 ivanhoe ln",
        addr={"raw": "986 ivanhoe ln", "number": "986", "street": "ivanhoe ln"},
        pay="card",
        pay_q="card",
    ),
]
