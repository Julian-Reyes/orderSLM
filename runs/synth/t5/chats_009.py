"""t5 entries 0221–0250 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0221",
        """
c: yo
c: 6 double cheeseburgers
c: 3 no onions
c: chocolate shake
c: 6613 bayview ln
c: cash
c: in 30
c: thx
""",
        "S P P P P P P S",
        items=[
            I("cheeseburger", 3, "double", ["6 double cheeseburgers"]),
            I(
                "cheeseburger",
                3,
                "double",
                ["6 double cheeseburgers", "3 no onions"],
                [rm("onion", "no onions")],
            ),
            I("milkshake", 1, "chocolate", ["chocolate shake"]),
        ],
        method="delivery",
        method_q="6613 bayview ln",
        time=("relative", "in 30", None),
        addr={"raw": "6613 bayview ln", "number": "6613", "street": "bayview ln"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0222",
        """
c: hiii 👋
c: just a can of coke for pickup, cash 🥤
b: One can of Coke for pickup, paying cash. Right?
c: yep!
c: oh can u make it a 20 oz bottle instead
""",
        "S P C M",
        items=[I("coke", 1, "bottle_20oz", ["a can of coke", "make it a 20 oz bottle"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0223",
        """
c: can of sprite, 2 xl meat lovers no beef, garlic knots n one of those
c: delivery, cash, change for a 20
""",
        "P P",
        items=[
            I("sprite", 1, "can", ["can of sprite"]),
            I("meat_lovers_pizza", 2, "extra_large", ["2 xl meat lovers"], [rm("beef", "no beef")]),
            I("garlic_knots", 1, None, ["garlic knots"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="delivery",
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
    ),
    X(
        "syn-t5-0224",
        """
c: 3 breakfast sandwiches on croissants n 3 everything bagels
c: + 2 medium hot chocolates w hazelnut, oat milk pls
c: pickup for omar, card
""",
        "P P P",
        items=[
            I("breakfast_sandwich", 3, "croissant", ["3 breakfast sandwiches on croissants"]),
            I("bagel", 3, "everything", ["3 everything bagels"]),
            I(
                "hot_chocolate",
                2,
                "medium",
                ["2 medium hot chocolates"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "oat_milk", "oat milk pls")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t5-0225",
        """
c: hey
c: gonna place an order for the fam tonight
""",
        "S P",
    ),
    X(
        "syn-t5-0226",
        """
c: hi
c: wanna put in an order for my coworkers
""",
        "S P",
    ),
    X(
        "syn-t5-0227",
        """
c: veggie pizza
c: personal supreme no sausage
c: 623 mission ave
c: cash
""",
        "P P P P",
        items=[
            I("veggie_pizza", 1, None, ["veggie pizza"]),
            I("supreme_pizza", 1, "personal", ["personal supreme"], [rm("sausage", "no sausage")]),
        ],
        method="delivery",
        method_q="623 mission ave",
        addr={"raw": "623 mission ave", "number": "623", "street": "mission ave"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0228",
        """
c: Hi there!
c: Two medium hot chocolates with oat milk and no whipped cream, please.
c: For pickup in 20 minutes, under Keisha. I'll pay by card.
""",
        "S P P",
        items=[
            I(
                "hot_chocolate",
                2,
                "medium",
                ["Two medium hot chocolates"],
                [sub("whole_milk", "oat_milk", "with oat milk"), rm("whipped_cream", "no whipped cream")],
            ),
        ],
        method="pickup",
        method_q="For pickup",
        time=("relative", "in 20 minutes", None),
        pay="card",
        pay_q="pay by card",
        name="Keisha",
    ),
    X(
        "syn-t5-0229",
        """
c: a muffin, a small latte n the one i always get, pickup asap for tara, cash
""",
        "P",
        items=[
            I("muffin", 1, None, ["a muffin"]),
            I("latte", 1, "small", ["a small latte"]),
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
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t5-0230",
        """
c: do u have hazelnut syrup
b: Yes we do!
c: ok a few large lattes w hazelnut and a small cappuccino, ready in 20
""",
        "Q P",
        items=[
            I("latte", None, "large", ["a few large lattes"], [add("hazelnut_syrup", "w hazelnut")]),
            I("cappuccino", 1, "small", ["a small cappuccino"]),
        ],
        time=("relative", "in 20", None),
    ),
    X(
        "syn-t5-0231",
        """
c: hi
c: small americano
c: w whole milk
c: pickup at 9
c: dev
c: card
c: make it a large actually
""",
        "S P P P P P M",
        items=[
            I(
                "americano",
                1,
                "large",
                ["small americano", "make it a large"],
                [add("whole_milk", "w whole milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t5-0232",
        """
c: hey
c: xl meat lovers to 6806 hawthorne ct apt 14a
b: One extra large meat lovers to 6806 Hawthorne Ct, apt 14A. Correct?
c: yup
c: oh make it thick crust
""",
        "S P C M",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                "extra_large",
                ["xl meat lovers", "make it thick crust"],
                [add("crust_thick", "thick crust")],
            ),
        ],
        method="delivery",
        method_q="to 6806 hawthorne ct apt 14a",
        addr={"raw": "6806 hawthorne ct apt 14a", "number": "6806", "street": "hawthorne ct", "unit": "14a"},
    ),
    X(
        "syn-t5-0233",
        """
c: cheeseburger
c: n a 32 oz coke
c: 1509 juniper pl
""",
        "P P P",
        items=[
            I("cheeseburger", 1, None, ["cheeseburger"]),
            I("coke", 1, None, ["a 32 oz coke"], unmatched_variant="32 oz"),
        ],
        method="delivery",
        method_q="1509 juniper pl",
        addr={"raw": "1509 juniper pl", "number": "1509", "street": "juniper pl"},
    ),
    X(
        "syn-t5-0234",
        """
c: Hello!
c: A coffee and a medium cappuccino, please.
c: For pickup in 20 minutes. My name is Maya.
c: I'll pay by card.
b: A coffee and a medium cappuccino for pickup in 20 minutes under Maya, paying by card. Is that right?
c: Yes, thank you.
c: Oh, could you make the coffee with skim milk?
""",
        "S P P P C M",
        items=[
            I(
                "drip_coffee",
                1,
                None,
                ["A coffee", "make the coffee with skim milk"],
                [add("skim_milk", "with skim milk")],
            ),
            I("cappuccino", 1, "medium", ["a medium cappuccino"]),
        ],
        method="pickup",
        method_q="For pickup",
        time=("relative", "in 20 minutes", None),
        pay="card",
        pay_q="pay by card",
        name="Maya",
    ),
    X(
        "syn-t5-0235",
        """
c: hey
c: 2 choc chip muffins
c: 2 medium coffees
c: pickup
c: priya
c: cash
c: change for a 20
c: actually no coffees
""",
        "S P P P P P P M",
        items=[I("muffin", 2, "chocolate_chip", ["2 choc chip muffins"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t5-0236",
        """
c: hi 😊 2 choc chip muffins and a plain bagel
c: pickup for ben, cash
c: wait just 1 muffin 🙈
""",
        "P P M",
        items=[
            I("muffin", 1, "chocolate_chip", ["2 choc chip muffins", "just 1 muffin"]),
            I("bagel", 1, "plain", ["a plain bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t5-0237",
        """
c: hey
c: some shakes
c: cash
c: in 20
c: ty
""",
        "S P P P S",
        items=[I("milkshake", None, None, ["some shakes"])],
        time=("relative", "in 20", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0238",
        """
c: Do you have almond milk?
b: Yes, we do.
c: Then two medium lattes with almond milk and the usual, please, in about 20 minutes. I'll pay by card.
""",
        "Q P",
        items=[
            I(
                "latte",
                2,
                "medium",
                ["two medium lattes"],
                [sub("whole_milk", "almond_milk", "with almond milk")],
            ),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        time=("relative", "in about 20 minutes", None),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0239",
        """
c: hi! 2 hot chocolates w hazelnut, a coffee, a small vanilla latte w almond milk and 2 large cappuccinos ☕
c: pickup for tara, card
c: oh no cappuccinos actually!
""",
        "P P M",
        items=[
            I("hot_chocolate", 2, None, ["2 hot chocolates"], [add("hazelnut_syrup", "w hazelnut")]),
            I("drip_coffee", 1, None, ["a coffee"]),
            I(
                "latte",
                1,
                "small",
                ["a small vanilla latte"],
                [add("vanilla_syrup", "vanilla"), sub("whole_milk", "almond_milk", "w almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t5-0240",
        """
c: TWO PERSONAL MEAT LOVERS, NO BACON!
c: THREE SMALL HAWAIIANS WITH RED ONIONS!
c: CASH!
c: ACTUALLY ONLY ONE MEAT LOVERS!
""",
        "P P P M",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                "personal",
                ["TWO PERSONAL MEAT LOVERS", "ONLY ONE MEAT LOVERS"],
                [rm("bacon", "NO BACON")],
            ),
            I(
                "hawaiian_pizza",
                3,
                "small",
                ["THREE SMALL HAWAIIANS"],
                [add("red_onions", "WITH RED ONIONS")],
            ),
        ],
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t5-0241",
        """
c: hey
c: a few bacon burgers but no bacon on em, cash
""",
        "S P",
        items=[I("bacon_burger", None, None, ["a few bacon burgers"], [rm("bacon", "no bacon")])],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0242",
        """
c: hi
c: 4 blueberry muffins
c: almond croissant
c: n a large latte
c: oat
c: ready in 20
c: thx
""",
        "S P P P P P S",
        items=[
            I("muffin", 4, "blueberry", ["4 blueberry muffins"]),
            I("croissant", 1, "almond", ["almond croissant"]),
            I("latte", 1, "large", ["a large latte", "oat"], [sub("whole_milk", "oat_milk", "oat")]),
        ],
        time=("relative", "in 20", None),
    ),
    X(
        "syn-t5-0243",
        """
c: hey ☕ can i get some medium coffees with hazelnut?
c: thank you!!
""",
        "P S",
        items=[
            I(
                "drip_coffee",
                None,
                "medium",
                ["some medium coffees"],
                [add("hazelnut_syrup", "with hazelnut")],
            )
        ],
    ),
    X(
        "syn-t5-0244",
        """
c: Good evening, I'd like to place a pizza order for my family.
""",
        "P",
    ),
    X(
        "syn-t5-0245",
        """
c: Hi, could I get a latte?
c: I'll pick it up and pay cash.
c: My name is Grace.
""",
        "P P P",
        items=[I("latte", 1, None, ["a latte"])],
        method="pickup",
        method_q="I'll pick it up",
        pay="cash",
        pay_q="pay cash",
        name="Grace",
    ),
    X(
        "syn-t5-0246",
        """
c: hey
c: 3 blueberry muffins
c: r they warm
b: We can warm them up for you!
c: nah its ok
c: and a medium americano
c: almond pls
c: pickup
c: tara
c: card
""",
        "S P Q S P P P P P",
        items=[
            I("muffin", 3, "blueberry", ["3 blueberry muffins"]),
            I("americano", 1, "medium", ["a medium americano"], [add("almond_milk", "almond pls")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t5-0247",
        """
c: 2 milkshakes
c: and that thing from before
c: 31 prospect rd unit 3
""",
        "P P P",
        items=[
            I("milkshake", 2, None, ["2 milkshakes"]),
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
        method_q="31 prospect rd unit 3",
        addr={"raw": "31 prospect rd unit 3", "number": "31", "street": "prospect rd", "unit": "3"},
    ),
    X(
        "syn-t5-0248",
        """
c: some 2 liter diet cokes
c: cash
c: thx
""",
        "P P S",
        items=[I("diet_coke", None, "two_liter", ["some 2 liter diet cokes"])],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0249",
        """
c: hey
c: 4 milkshakes n same as last time
c: 757 quincy blvd #13c asap
c: card
""",
        "S P P P",
        items=[
            I("milkshake", 4, None, ["4 milkshakes"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="757 quincy blvd #13c",
        time=("asap", "asap", None),
        addr={"raw": "757 quincy blvd #13c", "number": "757", "street": "quincy blvd", "unit": "13c"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0250",
        """
c: 2 cappuccinos
c: 16 oz
c: pickup for sam, cash
""",
        "P P P",
        items=[I("cappuccino", 2, "large", ["2 cappuccinos", "16 oz"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Sam",
        name_q="sam",
    ),
]
