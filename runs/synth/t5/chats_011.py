"""t5 entries 0276–0300 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0276",
        """
c: hey 🍔 single cheeseburger no tomato, fries, a bacon burger no onions w avocado + 2 sprites, cash, at 9
c: oh no sprites pls
""",
        "P M",
        items=[
            I("cheeseburger", 1, "single", ["single cheeseburger"], [rm("tomato", "no tomato")]),
            I("fries", 1, None, ["fries"]),
            I(
                "bacon_burger",
                1,
                None,
                ["a bacon burger"],
                [rm("onion", "no onions"), add("avocado", "w avocado")],
            ),
        ],
        time=("clock_time", "at 9", "21:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0277",
        """
c: GOOD MORNING!
c: TWO BREAKFAST SANDWICHES AND A LARGE LATTE WITH OAT MILK, PICKUP ASAP FOR ANA!
""",
        "S P",
        items=[
            I("breakfast_sandwich", 2, None, ["TWO BREAKFAST SANDWICHES"]),
            I("latte", 1, "large", ["A LARGE LATTE"], [sub("whole_milk", "oat_milk", "WITH OAT MILK")]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("asap", "ASAP", None),
        name="Ana",
        name_q="ANA",
    ),
    X(
        "syn-t5-0278",
        """
c: Could I get a veggie burger and a 20 oz lemonade for pickup as soon as possible?
""",
        "P",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("lemonade", 1, None, ["a 20 oz lemonade"], unmatched_variant="20 oz"),
        ],
        method="pickup",
        method_q="for pickup",
        time=("asap", "as soon as possible", None),
    ),
    X(
        "syn-t5-0279",
        """
c: 4 cheeseburgers
c: 3 no lettuce
c: n a bacon burger no pickles
c: 135 alder ct apt 3b at 8:45, cash
""",
        "P P P P",
        items=[
            I("cheeseburger", 1, None, ["4 cheeseburgers"]),
            I("cheeseburger", 3, None, ["4 cheeseburgers", "3 no lettuce"], [rm("lettuce", "no lettuce")]),
            I("bacon_burger", 1, None, ["a bacon burger"], [rm("pickle", "no pickles")]),
        ],
        method="delivery",
        method_q="135 alder ct apt 3b",
        time=("clock_time", "at 8:45", "20:45"),
        addr={"raw": "135 alder ct apt 3b", "number": "135", "street": "alder ct", "unit": "3b"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0280",
        """
c: hey ordering for the soccer team after practice
""",
        "P",
    ),
    X(
        "syn-t5-0281",
        """
c: ONE LARGE LATTE WITH ALMOND MILK!
c: AND A LARGE COFFEE, BLACK!
c: PICKUP FOR JORDAN, CASH!
""",
        "P P P",
        items=[
            I(
                "latte",
                1,
                "large",
                ["ONE LARGE LATTE"],
                [sub("whole_milk", "almond_milk", "WITH ALMOND MILK")],
            ),
            I("drip_coffee", 1, "large", ["A LARGE COFFEE"]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Jordan",
        name_q="JORDAN",
    ),
    X(
        "syn-t5-0282",
        """
c: 3 sesame bagels
c: + one of those
c: card
""",
        "P P P",
        items=[
            I("bagel", 3, "sesame", ["3 sesame bagels"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0283",
        """
c: a bagel w avocado and a breakfast sandwich pls
""",
        "P",
        items=[
            I("bagel", 1, None, ["a bagel"], [add("avocado", "w avocado")]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
        ],
    ),
    X(
        "syn-t5-0284",
        """
c: hey
c: a breakfast sandwich n 2 large caramel lattes w skim
""",
        "S P",
        items=[
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
            I(
                "latte",
                2,
                "large",
                ["2 large caramel lattes"],
                [add("caramel_syrup", "caramel"), sub("whole_milk", "skim_milk", "w skim")],
            ),
        ],
    ),
    X(
        "syn-t5-0285",
        """
c: hey
c: 4 cokes
c: 2573 quincy st
c: asap
c: cash
b: 4 Cokes to 2573 Quincy St, ASAP, cash. Right?
c: ye
c: make it 3 cokes
""",
        "S P P P P C M",
        items=[I("coke", 3, None, ["4 cokes", "make it 3 cokes"])],
        method="delivery",
        method_q="2573 quincy st",
        time=("asap", "asap", None),
        addr={"raw": "2573 quincy st", "number": "2573", "street": "quincy st"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0286",
        """
c: hey
c: 4 personal supremes
c: 3 no green peppers
c: a water
c: 2 liter dr pepper
c: 20 oz diet coke
c: pickup, card
""",
        "S P P P P P P",
        items=[
            I("supreme_pizza", 1, "personal", ["4 personal supremes"]),
            I(
                "supreme_pizza",
                3,
                "personal",
                ["4 personal supremes", "3 no green peppers"],
                [rm("green_peppers", "no green peppers")],
            ),
            I("water", 1, None, ["a water"]),
            I("dr_pepper", 1, "two_liter", ["2 liter dr pepper"]),
            I("diet_coke", 1, "bottle_20oz", ["20 oz diet coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0287",
        """
c: 3 veggie burgers
c: 2 no lettuce
c: 2 large fries
c: pickup for june
""",
        "P P P P",
        items=[
            I("veggie_burger", 1, None, ["3 veggie burgers"]),
            I("veggie_burger", 2, None, ["3 veggie burgers", "2 no lettuce"], [rm("lettuce", "no lettuce")]),
            I("fries", 2, "large", ["2 large fries"]),
        ],
        method="pickup",
        method_q="pickup",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t5-0288",
        """
c: hi 👋
c: 3 lemonades, a bacon burger no ketchup, a vanilla shake and 3 double cheeseburgers to 45 fairmont terrace, card 💳
c: hmm actually no cheeseburgers
""",
        "S P M",
        items=[
            I("lemonade", 3, None, ["3 lemonades"]),
            I("bacon_burger", 1, None, ["a bacon burger"], [rm("ketchup", "no ketchup")]),
            I("milkshake", 1, "vanilla", ["a vanilla shake"]),
        ],
        method="delivery",
        method_q="to 45 fairmont terrace",
        addr={"raw": "45 fairmont terrace", "number": "45", "street": "fairmont terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0289",
        """
c: hey
c: 2 milkshakes n 3 bacon burgers no bacon
c: and the one i always get
c: 24 hawthorne rd, blue door
""",
        "S P P P",
        items=[
            I("milkshake", 2, None, ["2 milkshakes"]),
            I("bacon_burger", 3, None, ["3 bacon burgers"], [rm("bacon", "no bacon")]),
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
        method_q="24 hawthorne rd",
        addr={
            "raw": "24 hawthorne rd, blue door",
            "number": "24",
            "street": "hawthorne rd",
            "reference": "blue door",
        },
    ),
    X(
        "syn-t5-0290",
        """
c: Hi, I'd like a bacon burger, a Sprite, and the one I always get.
c: I'll pay by card.
c: Thanks!
""",
        "P P S",
        items=[
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("sprite", 1, None, ["a Sprite"]),
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
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0291",
        """
c: some milkshakes pls
c: card
""",
        "P P",
        items=[I("milkshake", None, None, ["some milkshakes"])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0292",
        """
c: hey
c: 2 onion rings n 2 large fries
c: card
c: actually no fries
""",
        "S P P M",
        items=[I("onion_rings", 2, None, ["2 onion rings"])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0293",
        """
c: hey
c: 2 meat lovers no cheese on gluten free crust n a small pepperoni
c: to 531 ridgecrest st, card, in 40 min
""",
        "S P P",
        items=[
            I(
                "meat_lovers_pizza",
                2,
                None,
                ["2 meat lovers"],
                [rm("cheese", "no cheese"), add("crust_gluten_free", "on gluten free crust")],
            ),
            I("pepperoni_pizza", 1, "small", ["a small pepperoni"]),
        ],
        method="delivery",
        method_q="to 531 ridgecrest st",
        time=("relative", "in 40 min", None),
        addr={"raw": "531 ridgecrest st", "number": "531", "street": "ridgecrest st"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0294",
        """
c: HELLO!
c: TWO BANANA NUT MUFFINS, TWO CROISSANTS, A SESAME BAGEL WITH TOMATO AND A BREAKFAST SANDWICH WITH NO EGG!
c: PICKUP AT 9:15 FOR OMAR!
c: ACTUALLY FORGET THE SANDWICH!
""",
        "S P P M",
        items=[
            I("muffin", 2, "banana_nut", ["TWO BANANA NUT MUFFINS"]),
            I("croissant", 2, None, ["TWO CROISSANTS"]),
            I("bagel", 1, "sesame", ["A SESAME BAGEL"], [add("tomato", "WITH TOMATO")]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 9:15", "09:15"),
        name="Omar",
        name_q="OMAR",
    ),
    X(
        "syn-t5-0295",
        """
c: hi! 3 plain bagels, 1 w tomato 🥯 + a croissant + a small oat milk cappuccino ☕
c: pickup for june, card
""",
        "P P",
        items=[
            I("bagel", 2, "plain", ["3 plain bagels"]),
            I("bagel", 1, "plain", ["3 plain bagels", "1 w tomato"], [add("tomato", "w tomato")]),
            I("croissant", 1, None, ["a croissant"]),
            I(
                "cappuccino",
                1,
                "small",
                ["a small oat milk cappuccino"],
                [sub("whole_milk", "oat_milk", "oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t5-0296",
        """
c: hey ☕ a cappuccino, 3 blueberry muffins and a medium hot chocolate, card, ready in 20 pls 🙏
""",
        "P",
        items=[
            I("cappuccino", 1, None, ["a cappuccino"]),
            I("muffin", 3, "blueberry", ["3 blueberry muffins"]),
            I("hot_chocolate", 1, "medium", ["a medium hot chocolate"]),
        ],
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0297",
        """
c: 14 inch cheese pizza no sauce
c: 2 small supremes w ham
c: cash
c: at 7:30
""",
        "P P P P",
        items=[
            I("cheese_pizza", 1, "large", ["14 inch cheese pizza"], [rm("tomato_sauce", "no sauce")]),
            I("supreme_pizza", 2, "small", ["2 small supremes"], [add("ham", "w ham")]),
        ],
        time=("clock_time", "at 7:30", "19:30"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0298",
        """
c: single cheeseburger
c: 16 oz sprite
c: pickup asap
c: rosa
c: cash
""",
        "P P P P P",
        items=[
            I("cheeseburger", 1, "single", ["single cheeseburger"]),
            I("sprite", 1, None, ["16 oz sprite"], unmatched_variant="16 oz"),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t5-0299",
        """
c: 4 croissants 3 w butter
c: 4 choc chip muffins n a hot chocolate
c: pickup in 20 for tara, card
""",
        "P P P",
        items=[
            I("croissant", 1, None, ["4 croissants"]),
            I("croissant", 3, None, ["4 croissants", "3 w butter"], [add("butter", "w butter")]),
            I("muffin", 4, "chocolate_chip", ["4 choc chip muffins"]),
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Tara",
        name_q="tara",
    ),
    X(
        "syn-t5-0300",
        """
c: hey
c: need to order for a work meeting
""",
        "S P",
    ),
]
