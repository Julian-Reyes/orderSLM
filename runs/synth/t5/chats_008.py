"""t5 entries 0191–0220 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0191",
        """
c: GOOD AFTERNOON!
c: ONE 16 OZ LATTE PLEASE!
c: PICKUP FOR BEN, CARD!
""",
        "S P P",
        items=[I("latte", 1, "large", ["ONE 16 OZ LATTE"])],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
        name="Ben",
        name_q="BEN",
    ),
    X(
        "syn-t5-0192",
        """
c: yo
c: bacon burger
c: and the usual
c: asap
""",
        "S P P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        time=("asap", "asap", None),
    ),
    X(
        "syn-t5-0193",
        """
c: Could I have a chocolate croissant and one of those?
c: I'll pay cash.
c: Ready at 11, please.
""",
        "P P P",
        items=[
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        time=("clock_time", "at 11", "11:00"),
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t5-0194",
        """
c: coffee w oat milk
c: 2 small lattes
c: breakfast sandwich
c: pickup for grace
c: cash
""",
        "P P P P P",
        items=[
            I("drip_coffee", 1, None, ["coffee"], [add("oat_milk", "w oat milk")]),
            I("latte", 2, "small", ["2 small lattes"]),
            I("breakfast_sandwich", 1, None, ["breakfast sandwich"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t5-0195",
        """
c: 6 bacon burgers
c: 5 w no bacon lol
c: lemonade n sprite
c: pickup for maya
c: card
""",
        "P P P P P",
        items=[
            I("bacon_burger", 1, None, ["6 bacon burgers"]),
            I("bacon_burger", 5, None, ["6 bacon burgers", "5 w no bacon"], [rm("bacon", "no bacon")]),
            I("lemonade", 1, None, ["lemonade"]),
            I("sprite", 1, None, ["sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t5-0196",
        """
c: hey 🍕 4 small cheese pizzas
c: a small meat lovers on thick crust + a large pepperoni
c: to 656 dover blvd
c: oh and make the cheese ones stuffed crust 😋
""",
        "P P P M",
        items=[
            I(
                "cheese_pizza",
                4,
                "small",
                ["4 small cheese pizzas", "make the cheese ones stuffed crust"],
                [add("crust_stuffed", "stuffed crust")],
            ),
            I(
                "meat_lovers_pizza",
                1,
                "small",
                ["a small meat lovers"],
                [add("crust_thick", "on thick crust")],
            ),
            I("pepperoni_pizza", 1, "large", ["a large pepperoni"]),
        ],
        method="delivery",
        method_q="to 656 dover blvd",
        addr={"raw": "656 dover blvd", "number": "656", "street": "dover blvd"},
    ),
    X(
        "syn-t5-0197",
        """
c: hi 🥐 can i get some plain croissants?
c: pickup for sam
""",
        "P P",
        items=[I("croissant", None, "plain", ["some plain croissants"])],
        method="pickup",
        method_q="pickup",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t5-0198",
        """
c: hey
c: can i get some 20 oz iced teas
c: to 6766 brookside way #14a
""",
        "S P P",
        items=[I("iced_tea", None, "bottle_20oz", ["some 20 oz iced teas"])],
        method="delivery",
        method_q="to 6766 brookside way #14a",
        addr={"raw": "6766 brookside way #14a", "number": "6766", "street": "brookside way", "unit": "14a"},
    ),
    X(
        "syn-t5-0199",
        """
c: Hi, can you add basil to a supreme?
b: Sure, basil can go on any pizza.
c: Great, a few large supremes with basil and a Diet Coke, for delivery at 9:30. I'll pay cash and need change for a 50.
""",
        "Q P",
        items=[
            I("supreme_pizza", None, "large", ["a few large supremes"], [add("basil", "with basil")]),
            I("diet_coke", 1, None, ["a Diet Coke"]),
        ],
        method="delivery",
        method_q="for delivery",
        time=("clock_time", "at 9:30", "21:30"),
        pay="cash",
        pay_q=["pay cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t5-0200",
        """
c: hi! can u swap the bacon for chicken on a meat lovers? 🍕
b: We can leave off the bacon and add grilled chicken!
c: awesome, 2 meat lovers like that + 2 sprites
c: pickup, cash 💵
""",
        "Q P P",
        items=[
            I(
                "meat_lovers_pizza",
                2,
                None,
                ["a meat lovers", "2 meat lovers like that"],
                [sub("bacon", "grilled_chicken", "swap the bacon for chicken")],
            ),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0201",
        """
c: hey
c: wanna order for me n my buddies
""",
        "S P",
    ),
    X(
        "syn-t5-0202",
        """
c: Hi, two cheeseburgers, a strawberry milkshake and a 2 liter Sprite delivered to 27 Vine Dr, please.
c: As soon as you can.
""",
        "P P",
        items=[
            I("cheeseburger", 2, None, ["two cheeseburgers"]),
            I("milkshake", 1, "strawberry", ["a strawberry milkshake"]),
            I("sprite", 1, None, ["a 2 liter Sprite"], unmatched_variant="2 liter"),
        ],
        method="delivery",
        method_q="delivered to 27 Vine Dr",
        time=("asap", "As soon as you can", None),
        addr={"raw": "27 Vine Dr", "number": "27", "street": "Vine Dr"},
    ),
    X(
        "syn-t5-0203",
        """
c: hi! just a muffin for pickup, name's ana 🧁
""",
        "P",
        items=[I("muffin", 1, None, ["a muffin"])],
        method="pickup",
        method_q="for pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t5-0204",
        """
c: hey
c: do u deliver drinks only
b: Yes, there's a small order minimum for delivery.
c: hmm ok 2 waters and a diet coke
c: to 28 harbor st #11a
c: card
c: actually just 1 water
""",
        "S D P P P M",
        items=[I("water", 1, None, ["2 waters", "just 1 water"]), I("diet_coke", 1, None, ["a diet coke"])],
        method="delivery",
        method_q="to 28 harbor st #11a",
        addr={"raw": "28 harbor st #11a", "number": "28", "street": "harbor st", "unit": "11a"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0205",
        """
c: hey
c: 2 plain croissants w butter n 3 small coffees w caramel, pickup at 8:15 for jordan, card
b: 2 plain croissants with butter and 3 small coffees with caramel, pickup at 8:15 for Jordan, card. Right?
c: yep
c: actually just 1 croissant
""",
        "S P C M",
        items=[
            I(
                "croissant",
                1,
                "plain",
                ["2 plain croissants", "just 1 croissant"],
                [add("butter", "w butter")],
            ),
            I("drip_coffee", 3, "small", ["3 small coffees"], [add("caramel_syrup", "w caramel")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8:15", "08:15"),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t5-0206",
        """
c: heyyy 🌙
c: midnight snack order for the apartment 😂
""",
        "S P",
    ),
    X(
        "syn-t5-0207",
        """
c: chocolate croissant
c: 4 hot chocolates
c: no whip
c: skim
c: card
""",
        "P P P P P",
        items=[
            I("croissant", 1, "chocolate", ["chocolate croissant"]),
            I(
                "hot_chocolate",
                4,
                None,
                ["4 hot chocolates", "no whip", "skim"],
                [rm("whipped_cream", "no whip"), sub("whole_milk", "skim_milk", "skim")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0208",
        """
c: Do you have blueberry muffins today?
b: We do!
c: Great, one blueberry muffin and two large americanos, please.
c: Could you make the americanos with whole milk?
""",
        "Q P M",
        items=[
            I("muffin", 1, "blueberry", ["one blueberry muffin"]),
            I(
                "americano",
                2,
                "large",
                ["two large americanos", "make the americanos with whole milk"],
                [add("whole_milk", "with whole milk")],
            ),
        ],
    ),
    X(
        "syn-t5-0209",
        """
c: 2 veggie burgers
c: 1 no tomato
c: fries, pickup for rosa, card
""",
        "P P P",
        items=[
            I("veggie_burger", 1, None, ["2 veggie burgers"]),
            I("veggie_burger", 1, None, ["2 veggie burgers", "1 no tomato"], [rm("tomato", "no tomato")]),
            I("fries", 1, None, ["fries"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t5-0210",
        """
c: Hello, is the chocolate croissant fresh today?
b: Baked this morning!
c: Lovely. One chocolate croissant, please.
c: And a breakfast sandwich with avocado.
c: Plus a medium cappuccino with oat milk.
c: I'll pick it up. The name is Luis.
""",
        "Q P P P P",
        items=[
            I("croissant", 1, "chocolate", ["One chocolate croissant"]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"], [add("avocado", "with avocado")]),
            I(
                "cappuccino",
                1,
                "medium",
                ["a medium cappuccino"],
                [sub("whole_milk", "oat_milk", "with oat milk")],
            ),
        ],
        method="pickup",
        method_q="I'll pick it up",
        name="Luis",
    ),
    X(
        "syn-t5-0211",
        """
c: Hi, a supreme pizza on thick crust and two orders of garlic knots, please.
c: I'll pay by card.
c: Thanks.
""",
        "P P S",
        items=[
            I("supreme_pizza", 1, None, ["a supreme pizza"], [add("crust_thick", "on thick crust")]),
            I("garlic_knots", 2, None, ["two orders of garlic knots"]),
        ],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0212",
        """
c: Could I get a few extra large margherita pizzas delivered?
c: I'll pay cash.
""",
        "P P",
        items=[I("margherita_pizza", None, "extra_large", ["a few extra large margherita pizzas"])],
        method="delivery",
        method_q="delivered",
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t5-0213",
        """
c: Good evening!
c: Is the margherita made with fresh basil?
b: Yes, fresh basil on every one.
c: Okay, three extra large margheritas without basil, two large supremes, and three Diet Cokes.
c: Please deliver to 3897 Elm Ln. I'll pay by card.
b: Three extra large margheritas without basil, two large supremes and three Diet Cokes to 3897 Elm Ln, paying by card. Is that correct?
c: Yes.
c: Actually, just one supreme, please.
""",
        "S Q P P C M",
        items=[
            I(
                "margherita_pizza",
                3,
                "extra_large",
                ["three extra large margheritas"],
                [rm("basil", "without basil")],
            ),
            I("supreme_pizza", 1, "large", ["two large supremes", "just one supreme"]),
            I("diet_coke", 3, None, ["three Diet Cokes"]),
        ],
        method="delivery",
        method_q="deliver to 3897 Elm Ln",
        addr={"raw": "3897 Elm Ln", "number": "3897", "street": "Elm Ln"},
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0214",
        """
c: is the gluten free crust any good
b: People love it!
c: ok 2 large veggies no green peppers on gluten free crust
c: and that thing from before, to 6834 willow creek blvd
""",
        "Q P P",
        items=[
            I(
                "veggie_pizza",
                2,
                "large",
                ["2 large veggies"],
                [rm("green_peppers", "no green peppers"), add("crust_gluten_free", "on gluten free crust")],
            ),
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
        method_q="to 6834 willow creek blvd",
        addr={"raw": "6834 willow creek blvd", "number": "6834", "street": "willow creek blvd"},
    ),
    X(
        "syn-t5-0215",
        """
c: meat lovers
c: 3 easton ln
c: cash
""",
        "P P P",
        items=[I("meat_lovers_pizza", 1, None, ["meat lovers"])],
        method="delivery",
        method_q="3 easton ln",
        addr={"raw": "3 easton ln", "number": "3", "street": "easton ln"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0216",
        """
c: small americano w oat milk
c: pickup asap
c: priya
""",
        "P P P",
        items=[I("americano", 1, "small", ["small americano"], [add("oat_milk", "w oat milk")])],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t5-0217",
        """
c: do the breadsticks come w sauce
b: Yes, with a side of marinara!
c: ok some breadsticks to 524 sunset way asap
""",
        "Q P",
        items=[I("breadsticks", None, None, ["some breadsticks"])],
        method="delivery",
        method_q="to 524 sunset way",
        time=("asap", "asap", None),
        addr={"raw": "524 sunset way", "number": "524", "street": "sunset way"},
    ),
    X(
        "syn-t5-0218",
        """
c: hi! 4 bagels please 🥯
c: thanks!
""",
        "P S",
        items=[I("bagel", 4, None, ["4 bagels"])],
    ),
    X(
        "syn-t5-0219",
        """
c: 2 cokes a sprite and the usual, cash
""",
        "P",
        items=[
            I("coke", 2, None, ["2 cokes"]),
            I("sprite", 1, None, ["a sprite"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0220",
        """
c: xl bbq chicken w olive oil
c: order of garlic knots
c: 2 personal hawaiians
c: 2 cans of diet coke, card
c: nvm the diet cokes
""",
        "P P P P M",
        items=[
            I("bbq_chicken_pizza", 1, "extra_large", ["xl bbq chicken"], [add("olive_oil", "w olive oil")]),
            I("garlic_knots", 1, None, ["order of garlic knots"]),
            I("hawaiian_pizza", 2, "personal", ["2 personal hawaiians"]),
        ],
        pay="card",
        pay_q="card",
    ),
]
