"""t5 entries 0013–0040 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0013",
        """
c: HEY THERE!!
c: CAN I GET A CHEESE PIZZA, A COKE AND A CAN OF DIET COKE! PAYING WITH CARD!
""",
        "S P",
        items=[
            I("cheese_pizza", 1, None, ["A CHEESE PIZZA"]),
            I("coke", 1, None, ["A COKE"]),
            I("diet_coke", 1, "can", ["A CAN OF DIET COKE"]),
        ],
        pay="card",
        pay_q="PAYING WITH CARD",
    ),
    X(
        "syn-t5-0014",
        """
c: Hi, I'd like four small lattes, two of them with hazelnut syrup.
c: Also two hot chocolates with vanilla.
c: And one coffee, please.
c: I'll pick it up and pay cash. The name is Ana.
""",
        "P P P P",
        items=[
            I("latte", 2, "small", ["four small lattes"]),
            I(
                "latte",
                2,
                "small",
                ["four small lattes", "two of them with hazelnut syrup"],
                [add("hazelnut_syrup", "with hazelnut syrup")],
            ),
            I("hot_chocolate", 2, None, ["two hot chocolates"], [add("vanilla_syrup", "with vanilla")]),
            I("drip_coffee", 1, None, ["one coffee"]),
        ],
        method="pickup",
        method_q="pick it up",
        pay="cash",
        pay_q="pay cash",
        name="Ana",
    ),
    X(
        "syn-t5-0015",
        """
c: hey
c: hawaiian
c: medium ones
c: like a few of them
c: for the game tonight
""",
        "S P P P P",
        items=[I("hawaiian_pizza", None, "medium", ["hawaiian", "medium ones", "a few of them"])],
    ),
    X(
        "syn-t5-0016",
        """
c: Hi, could I get three supreme pizzas?
c: We'd like them in about 45 minutes.
c: Thank you!
""",
        "P P S",
        items=[I("supreme_pizza", 3, None, ["three supreme pizzas"])],
        time=("relative", "in about 45 minutes", None),
    ),
    X(
        "syn-t5-0017",
        """
c: morning ☀️ can i get 5 coffees, 2 of them with caramel 😋
c: plus a breakfast sandwich 🥪
c: picking up, name's jordan 🙌
""",
        "P P P",
        items=[
            I("drip_coffee", 3, None, ["5 coffees"]),
            I(
                "drip_coffee",
                2,
                None,
                ["5 coffees", "2 of them with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
        ],
        method="pickup",
        method_q="picking up",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t5-0018",
        """
c: yo whats good, need to order food for the fam
""",
        "P",
    ),
    X(
        "syn-t5-0019",
        """
c: Hi, I'd like three bacon burgers, one of them without bacon, and a large fries.
c: I'll pick it up.
c: Paying by card.
""",
        "P P P",
        items=[
            I("bacon_burger", 2, None, ["three bacon burgers"]),
            I(
                "bacon_burger",
                1,
                None,
                ["three bacon burgers", "one of them without bacon"],
                [rm("bacon", "without bacon")],
            ),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="pickup",
        method_q="I'll pick it up",
        pay="card",
        pay_q="Paying by card",
    ),
    X(
        "syn-t5-0020",
        """
c: hi there 😊
c: could we get some waters delivered to 240 chestnut way 💧
""",
        "S P",
        items=[I("water", None, None, ["some waters"])],
        method="delivery",
        method_q="delivered to 240 chestnut way",
        addr={"raw": "240 chestnut way", "number": "240", "street": "chestnut way"},
    ),
    X(
        "syn-t5-0021",
        """
c: can i get 2 almond croissants
c: do u have oat milk
b: We do! Oat, almond, skim or whole.
c: ok and a medium latte w oat milk
c: cash
""",
        "P Q P P",
        items=[
            I("croissant", 2, "almond", ["2 almond croissants"]),
            I("latte", 1, "medium", ["a medium latte"], [sub("whole_milk", "oat_milk", "w oat milk")]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0022",
        """
c: heyy
c: gonna put in an order for the crew tonight
""",
        "S P",
    ),
    X(
        "syn-t5-0023",
        """
c: hey hey 👋
c: 3 double cheeseburgers, 2 of em with mayo 🍔 + a veggie burger w avo + a bacon burger w mayo + a coke. pickup, cash 💵
""",
        "S P",
        items=[
            I("cheeseburger", 1, "double", ["3 double cheeseburgers"]),
            I(
                "cheeseburger",
                2,
                "double",
                ["3 double cheeseburgers", "2 of em with mayo"],
                [add("mayo", "with mayo")],
            ),
            I("veggie_burger", 1, None, ["a veggie burger"], [add("avocado", "w avo")]),
            I("bacon_burger", 1, None, ["a bacon burger"], [add("mayo", "w mayo")]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0024",
        """
c: Hello, could I get some muffins and two large coffees with vanilla?
c: It's for pickup, under Ana.
c: Thanks so much!
""",
        "P P S",
        items=[
            I("muffin", None, None, ["some muffins"]),
            I("drip_coffee", 2, "large", ["two large coffees"], [add("vanilla_syrup", "with vanilla")]),
        ],
        method="pickup",
        method_q="for pickup",
        name="Ana",
    ),
    X(
        "syn-t5-0025",
        """
c: hii
c: can i get a few cinnamon raisin bagels w butter, 2 blueberry muffins and a croissant w butter too, paying cash
""",
        "S P",
        items=[
            I(
                "bagel",
                None,
                "cinnamon_raisin",
                ["a few cinnamon raisin bagels"],
                [add("butter", "w butter")],
            ),
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
            I("croissant", 1, None, ["a croissant"], [add("butter", "w butter")]),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t5-0026",
        """
c: hey
c: a muffin and a coffee w skim milk pls, pickup for ben, card
""",
        "S P",
        items=[
            I("muffin", 1, None, ["a muffin"]),
            I("drip_coffee", 1, None, ["a coffee"], [add("skim_milk", "w skim milk")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t5-0027",
        """
c: hi!! 😄 wanna place an order for the family tonight
""",
        "P",
    ),
    X(
        "syn-t5-0028",
        """
c: hey!!
c: ordering for the office party
""",
        "S P",
    ),
    X(
        "syn-t5-0029",
        """
c: hi! can i get a breakfast sandwich on a croissant w avocado 🥑, a cinnamon raisin bagel and a banana nut muffin 🧁
c: pickup asap, card, name's luis
b: A breakfast sandwich on a croissant with avocado, a cinnamon raisin bagel and a banana nut muffin, for pickup ASAP under Luis, paying by card. Correct?
c: yes 👍
c: actually no muffin pls, just the other two
""",
        "P P C M",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["a breakfast sandwich on a croissant"],
                [add("avocado", "w avocado")],
            ),
            I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t5-0030",
        """
c: HEY I NEED SIX BACON BURGERS
c: THREE OF THEM NO CHEESE
c: AND A SPRITE
c: DELIVER TO 97 PROSPECT ST, ACROSS FROM THE PARK
c: CARD
""",
        "P P P P P",
        items=[
            I("bacon_burger", 3, None, ["SIX BACON BURGERS"]),
            I(
                "bacon_burger",
                3,
                None,
                ["SIX BACON BURGERS", "THREE OF THEM NO CHEESE"],
                [rm("cheese", "NO CHEESE")],
            ),
            I("sprite", 1, None, ["A SPRITE"]),
        ],
        method="delivery",
        method_q="DELIVER TO 97 PROSPECT ST",
        addr={
            "raw": "97 PROSPECT ST, ACROSS FROM THE PARK",
            "number": "97",
            "street": "PROSPECT ST",
            "reference": "ACROSS FROM THE PARK",
        },
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0031",
        """
c: hey ☕ 2 cinnamon raisin bagels pls
c: + a small latte w almond milk
c: and 3 coffees w vanilla 😋
c: pickup for dev, cash
""",
        "P P P P",
        items=[
            I("bagel", 2, "cinnamon_raisin", ["2 cinnamon raisin bagels"]),
            I("latte", 1, "small", ["a small latte"], [sub("whole_milk", "almond_milk", "w almond milk")]),
            I("drip_coffee", 3, None, ["3 coffees"], [add("vanilla_syrup", "w vanilla")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t5-0032",
        """
c: hi! 2 croissants w butter and an americano with oat milk 🥐☕ pickup for maya
""",
        "P",
        items=[
            I("croissant", 2, None, ["2 croissants"], [add("butter", "w butter")]),
            I("americano", 1, None, ["an americano"], [add("oat_milk", "with oat milk")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t5-0033",
        """
c: lemme get 5 cheeseburgers 4 no pickles n 2 vanilla shakes
""",
        "P",
        items=[
            I("cheeseburger", 1, None, ["5 cheeseburgers"]),
            I("cheeseburger", 4, None, ["5 cheeseburgers", "4 no pickles"], [rm("pickle", "no pickles")]),
            I("milkshake", 2, "vanilla", ["2 vanilla shakes"]),
        ],
    ),
    X(
        "syn-t5-0034",
        """
c: do u have whipped cream on the hot chocolate
b: Yes, it comes with whipped cream!
c: ok 4 hot chocolates one without whip and a large cappuccino
c: pickup, jordan, cash, change for a 20
""",
        "Q P P",
        items=[
            I("hot_chocolate", 3, None, ["4 hot chocolates"]),
            I(
                "hot_chocolate",
                1,
                None,
                ["4 hot chocolates", "one without whip"],
                [rm("whipped_cream", "without whip")],
            ),
            I("cappuccino", 1, "large", ["a large cappuccino"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "change for a 20"],
        change=2000,
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t5-0035",
        """
c: Could I get a few small supreme pizzas with no sauce, four large cheese pizzas with thick crust, and an order of garlic knots? I'll pay cash.
""",
        "P",
        items=[
            I(
                "supreme_pizza",
                None,
                "small",
                ["a few small supreme pizzas"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I("cheese_pizza", 4, "large", ["four large cheese pizzas"], [add("crust_thick", "thick crust")]),
            I("garlic_knots", 1, None, ["an order of garlic knots"]),
        ],
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t5-0036",
        """
c: hey
c: can i get a large fries and a lemonade
c: deliver to 918 glenwood ct
c: paying cash, need change for a 50
c: oh and make the fries a regular actually
""",
        "S P P P M",
        items=[
            I("fries", 1, "regular", ["a large fries", "make the fries a regular"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="deliver to 918 glenwood ct",
        addr={"raw": "918 glenwood ct", "number": "918", "street": "glenwood ct"},
        pay="cash",
        pay_q=["paying cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t5-0037",
        """
c: hi!! 6 croissants pls, 4 of them w butter 🥐
c: a hot chocolate w vanilla and almond milk instead of whole
c: 4 small lattes w vanilla ☕
c: and a breakfast sandwich no bacon
c: pickup for rosa, cash, change for a 50 🙏
""",
        "P P P P P",
        items=[
            I("croissant", 2, None, ["6 croissants"]),
            I("croissant", 4, None, ["6 croissants", "4 of them w butter"], [add("butter", "w butter")]),
            I(
                "hot_chocolate",
                1,
                None,
                ["a hot chocolate"],
                [
                    add("vanilla_syrup", "w vanilla"),
                    sub("whole_milk", "almond_milk", "almond milk instead of whole"),
                ],
            ),
            I("latte", 4, "small", ["4 small lattes"], [add("vanilla_syrup", "w vanilla")]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"], [rm("bacon", "no bacon")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "change for a 50"],
        change=5000,
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t5-0038",
        """
c: hi 🍕 we're ordering for movie night!
""",
        "P",
    ),
    X(
        "syn-t5-0039",
        """
c: Hi, I'd like a sesame bagel and one of those, please.
c: I'll come by at 8:30 and pay cash.
""",
        "P P",
        items=[
            I("bagel", 1, "sesame", ["a sesame bagel"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="I'll come by",
        time=("clock_time", "at 8:30", "08:30"),
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t5-0040",
        """
c: yo
c: can i get some milkshakes
c: and 2 lemonades n 3 sprites
""",
        "S P P",
        items=[
            I("milkshake", None, None, ["some milkshakes"]),
            I("lemonade", 2, None, ["2 lemonades"]),
            I("sprite", 3, None, ["3 sprites"]),
        ],
    ),
]
