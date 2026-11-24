"""fresh5 a-fresh5-057–084 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm, sub

ENTRIES = [
    F(
        "a-fresh5-057",
        """
c: hi
c: large cheese w olives
c: medium pepperoni
c: pickup
c: card
c: name is eve
c: oh can u do mushrooms instead of olives on the cheese
""",
        "S P P P P P M",
        start="Thu 17:50",
        items=[
            I(
                "cheese_pizza",
                1,
                "large",
                ["large cheese w olives", "mushrooms instead of olives on the cheese"],
                [add("mushrooms", "mushrooms instead of olives")],
            ),
            I("pepperoni_pizza", 1, "medium", ["medium pepperoni"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Eve",
        name_q="eve",
    ),
    F(
        "a-fresh5-058",
        """
c: 2 bacon burgers to 66 maple ct, around 7 or 8, do u have sweet potato fries?
b: Sorry, just regular fries and onion rings.
c: ok just the burgers then, card
""",
        "P/Q P",
        start="Fri 16:30",
        items=[I("bacon_burger", 2, None, ["2 bacon burgers"])],
        method="delivery",
        method_q="to 66 maple ct",
        addr={"raw": "66 maple ct", "number": "66", "street": "maple ct"},
        time=("ambiguous", "around 7 or 8"),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-059",
        """
c: hi ☕ 3 lattes, 2 bagels n a bec 🥯 whats in the bec?
b: Egg, cheddar and bacon! What size for the lattes, and which bagels?
c: 3 medium lattes, 1 plain 1 everything bagel, pickup for kit 😊
""",
        "P/Q P",
        start="Sat 09:10",
        items=[
            I("latte", 3, "medium", ["3 lattes", "3 medium lattes"]),
            I("bagel", 1, "plain", ["2 bagels", "1 plain 1 everything bagel"]),
            I("bagel", 1, "everything", ["2 bagels", "1 plain 1 everything bagel"]),
            I("breakfast_sandwich", 1, None, ["a bec"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Kit",
        name_q="kit",
    ),
    F(
        "a-fresh5-060",
        """
c: hi, just checking on my order from about 40 min ago for 12 pine st, no rush, thanks!
""",
        "ST",
        start="Sun 19:45",
        order=False,
    ),
    F(
        "a-fresh5-061",
        """
c: Hello, the the ordr fro
c: sorry wfh
""",
        "U U",
        start="Mon 12:30",
    ),
    F(
        "a-fresh5-062",
        """
c: 2 med caps n a sesame bagel
c: for 2:30
c: card
""",
        "P P P",
        start="Tue 09:40",
        items=[
            I("cappuccino", 2, "medium", ["2 med caps"]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
        ],
        time=("clock_time", "for 2:30", "14:30"),
        pay="card",
        pay_q="card",
        annotation="'for 2:30' at 09:40, open 7-15: only 14:30 fits.",
    ),
    F(
        "a-fresh5-063",
        """
c: hey
c: ordering for wednesday
c: is the bbq chicken spicy
b: Not spicy, it's sweet and smoky!
c: ok a large one
c: n a 2 liter dr pepper
c: at 6
""",
        "S P Q P P P",
        start="Mon 13:30",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["the bbq chicken", "a large one"]),
            I("dr_pepper", 1, "two_liter", ["a 2 liter dr pepper"]),
        ],
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "wed", "wednesday"),
        annotation="'a large one' right after asking about the BBQ chicken is that pizza.",
    ),
    F(
        "a-fresh5-064",
        """
c: Hi, a small hot chocolate and a plain croissant for pickup.
c: Name is Dot, card.
b: Got it, Dot: 1 small hot chocolate and 1 plain croissant, pickup, paying by card. Is that right?
c: ok sounds good
""",
        "P P C",
        start="Wed 13:00",
        items=[
            I("hot_chocolate", 1, "small", ["a small hot chocolate"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
        name="Dot",
        name_q="Dot",
        decision="confirmed",
        decision_q="ok sounds good",
    ),
    F(
        "a-fresh5-065",
        """
c: 2 cheeseburgers n a lemonade to 19 grant ave, card 💳 oh n can u put a fried egg on one 🍳
""",
        "P",
        start="Thu 18:10",
        items=[
            I("cheeseburger", 1, None, ["2 cheeseburgers"]),
            I(
                "cheeseburger",
                1,
                None,
                ["2 cheeseburgers", "put a fried egg on one"],
                [offmod("a fried egg")],
            ),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="to 19 grant ave",
        addr={"raw": "19 grant ave", "number": "19", "street": "grant ave"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-066",
        """
c: hey
c: medium veggie
c: 6 garlic knots
c: n pad thai
c: pickup
c: card
""",
        "S P P P P P",
        start="Fri 18:00",
        items=[
            I("veggie_pizza", 1, "medium", ["medium veggie"]),
            I("garlic_knots", 1, None, ["6 garlic knots"]),
            I(None, 1, None, ["pad thai"], unmatched="pad thai"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        annotation="Garlic knots come 6 to an order: '6 garlic knots' is 1 order.",
    ),
    F(
        "a-fresh5-067",
        """
c: 3 veggie burgers 🍔 1 w no onions
c: to 501 alder st, cash 💵
""",
        "P P",
        start="Sat 13:20",
        items=[
            I("veggie_burger", 2, None, ["3 veggie burgers 🍔 1 w no onions"]),
            I("veggie_burger", 1, None, ["3 veggie burgers 🍔 1 w no onions"], [rm("onion", "no onions")]),
        ],
        method="delivery",
        method_q="to 501 alder st",
        addr={"raw": "501 alder st", "number": "501", "street": "alder st"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-068",
        """
c: Hi, which country invented pizza, Italy or Greece?
""",
        "O",
        start="Sun 14:00",
    ),
    F(
        "a-fresh5-069",
        """
c: 2 cheeseburgers w bacon
c: a coke
c: n a sprite
c: card
c: asap
c: actually avocado instead of bacon on them
""",
        "P P P P P M",
        start="Mon 12:20",
        items=[
            I(
                "cheeseburger",
                2,
                None,
                ["2 cheeseburgers w bacon", "avocado instead of bacon on them"],
                [add("avocado", "avocado instead of bacon")],
            ),
            I("coke", 1, None, ["a coke"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-070",
        """
c: breakfast deal w a large latte n a choc chip muffin
c: pickup for sol, cash
""",
        "P P",
        start="Tue 08:15",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["breakfast deal w a large latte n a choc chip muffin"],
                combo={"drink": ("latte", "large"), "pastry": ("muffin", "chocolate_chip")},
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Sol",
        name_q="sol",
    ),
    F(
        "a-fresh5-071",
        """
c: hey can i get 2 bec on bagels for tmrw
c: is the bacon crispy?
b: Yes, nice and crispy!
c: great, at 8:15
c: card
""",
        "P Q P P",
        start="Wed 12:00",
        items=[I("breakfast_sandwich", 2, "bagel", ["2 bec on bagels"])],
        time=("clock_time", "at 8:15", "08:15"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-072",
        """
c: hi
c: do u take orders for sunday
b: Yes, up to a week ahead!
c: cool
c: 4 cheeseburgers n 4 fries for sunday at 12:30
c: cash
""",
        "S D S P P",
        start="Thu 19:00",
        items=[
            I("cheeseburger", 4, None, ["4 cheeseburgers"]),
            I("fries", 4, None, ["4 fries"]),
        ],
        time=("clock_time", "at 12:30", "12:30"),
        day=("weekday", "sun", "sunday"),
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-073",
        """
c: Hello!
c: Could I get four medium cheese pizzas, two of them with sausage, delivered to 25 Quincy St? Paying cash.
""",
        "S P",
        start="Fri 19:10",
        items=[
            I("cheese_pizza", 2, "medium", ["four medium cheese pizzas, two of them with sausage"]),
            I(
                "cheese_pizza",
                2,
                "medium",
                ["four medium cheese pizzas, two of them with sausage"],
                [add("sausage", "with sausage")],
            ),
        ],
        method="delivery",
        method_q="delivered to 25 Quincy St",
        addr={"raw": "25 Quincy St", "number": "25", "street": "Quincy St"},
        pay="cash",
        pay_q="Paying cash",
    ),
    F(
        "a-fresh5-074",
        """
c: hi 🍕
c: can i ge
c: t a lar
""",
        "S U U",
        start="Sat 20:30",
    ),
    F(
        "a-fresh5-075",
        """
c: Hi, I was charged twice for my order last night.
c: Could you refund the extra charge, please?
""",
        "R R",
        start="Sun 12:40",
        order=False,
        annotation="A double charge is a billing problem, not a complaint about the food: REFUND_REQUEST.",
    ),
    F(
        "a-fresh5-076",
        """
c: Hi, same as last time for pickup, please, and two Cokes.
c: Actually make it three Cokes.
""",
        "P M",
        start="Mon 17:30",
        items=[
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
            I("coke", 3, None, ["two Cokes", "make it three Cokes"]),
        ],
        method="pickup",
        method_q="for pickup",
    ),
    F(
        "a-fresh5-077",
        """
c: Do you have almond milk?
b: Yes, we have almond and oat milk.
c: Great. Three large lattes, two of them with almond milk.
c: For pickup, the name is Liv. Paying by card.
""",
        "Q P P",
        start="Tue 10:50",
        items=[
            I("latte", 1, "large", ["Three large lattes, two of them with almond milk"]),
            I(
                "latte",
                2,
                "large",
                ["Three large lattes, two of them with almond milk"],
                [sub("whole_milk", "almond_milk", "with almond milk")],
            ),
        ],
        method="pickup",
        method_q="For pickup",
        pay="card",
        pay_q="Paying by card",
        name="Liv",
        name_q="Liv",
    ),
    F(
        "a-fresh5-078",
        """
c: lg drip w cinnamon
c: n a blueberry muffin
c: asap
c: cash
""",
        "P P P P",
        start="Wed 07:30",
        items=[
            I("drip_coffee", 1, "large", ["lg drip w cinnamon"], [offmod("w cinnamon")]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
        ],
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-079",
        """
c: 2 almond croissants
c: a med americano
c: n a hot choc
c: nvm no hot choc
""",
        "P P P M",
        start="Thu 11:10",
        items=[
            I("croissant", 2, "almond", ["2 almond croissants"]),
            I("americano", 1, "medium", ["a med americano"]),
        ],
    ),
    F(
        "a-fresh5-080",
        """
c: hey
c: ordered delivery to 9 oak st like 45 min ago
c: any eta?
""",
        "S ST ST",
        start="Fri 20:20",
        order=False,
    ),
    F(
        "a-fresh5-081",
        """
c: j
c: ]
""",
        "U U",
        start="Sat 16:00",
    ),
    F(
        "a-fresh5-082",
        """
c: A LARGE CAPPUCCINO WITH HAZELNUT
c: AND AN EVERYTHING BAGEL WITH BUTTER
c: PICKUP FOR ABE
""",
        "P P P",
        start="Sun 09:20",
        items=[
            I(
                "cappuccino",
                1,
                "large",
                ["A LARGE CAPPUCCINO WITH HAZELNUT"],
                [add("hazelnut_syrup", "WITH HAZELNUT")],
            ),
            I("bagel", 1, "everything", ["AN EVERYTHING BAGEL WITH BUTTER"], [add("butter", "WITH BUTTER")]),
        ],
        method="pickup",
        method_q="PICKUP",
        name="Abe",
        name_q="ABE",
    ),
    F(
        "a-fresh5-083",
        """
c: Hello!
c: I'd like to place an order for December 5th.
c: Two veggie burgers and two lemonades.
c: I'll pick them up at 1:30.
c: Paying cash.
""",
        "S P P P P",
        start="Tue 14:00",
        items=[
            I("veggie_burger", 2, None, ["Two veggie burgers"]),
            I("lemonade", 2, None, ["two lemonades"]),
        ],
        method="pickup",
        method_q="I'll pick them up",
        time=("clock_time", "at 1:30", "13:30"),
        day=("date", 12, 5, "December 5th"),
        pay="cash",
        pay_q="Paying cash",
    ),
    F(
        "a-fresh5-084",
        """
c: hi 👋 can i pay online?
c: or only card at the door? 💳
""",
        "PQ PQ",
        start="Wed 18:30",
    ),
]
