"""t6 entries 0021–0030 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0021",
        """
c: hi 😊 a hot chocolate w vanilla n a croissant w butter pls
c: pickup at 10:30, name ivy, card 💳
b: Got it, Ivy: 1 hot chocolate with vanilla syrup and 1 croissant with butter, pickup at 10:30, paying by card. Is that right?
c: yes 👍
c: oh actually no hot chocolate, just the croissant 🥐
""",
        "P P C M",
        items=[I("croissant", 1, None, ["a croissant w butter"], [add("butter", "w butter")])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10:30", "10:30"),
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t6-0022",
        """
c: Good afternoon!
c: Could I order a large americano for Tuesday at 8:15?
""",
        "S P",
        items=[I("americano", 1, "large", ["a large americano"])],
        time=("clock_time", "at 8:15", "08:15"),
        day=("weekday", "tue", "Tuesday"),
    ),
    X(
        "syn-t6-0023",
        """
c: hey can i get 4 cheese pizzas n an xl margherita w thick crust, paying cash
""",
        "P",
        items=[
            I("cheese_pizza", 4, None, ["4 cheese pizzas"]),
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["an xl margherita w thick crust"],
                [add("crust_thick", "w thick crust")],
            ),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t6-0024",
        """
c: HEY CAN I GET A CHEESEBURGER COMBO WITH BACON, ONION RINGS AND A LEMONADE
c: PLUS A SPRITE ON THE SIDE AND 2 BACON BURGERS WITH AVOCADO
c: IS THE AVOCADO EXTRA?
b: Yes, avocado is an add-on.
c: OK FINE. PICKUP AT 12:45, CARD
""",
        "P P Q P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["A CHEESEBURGER COMBO WITH BACON, ONION RINGS AND A LEMONADE"],
                [add("bacon", "WITH BACON")],
                combo={"side": "onion_rings", "drink": "lemonade"},
            ),
            I("sprite", 1, None, ["A SPRITE"]),
            I("bacon_burger", 2, None, ["2 BACON BURGERS WITH AVOCADO"], [add("avocado", "WITH AVOCADO")]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 12:45", "12:45"),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0025",
        """
c: hey morning
c: 4 small lattes, 1 of them w whipped cream
c: n a croissant + a breakfast sandwich no bacon
c: card
""",
        "S P P P",
        items=[
            I("latte", 3, "small", ["4 small lattes"]),
            I(
                "latte",
                1,
                "small",
                ["4 small lattes", "1 of them w whipped cream"],
                [add("whipped_cream", "w whipped cream")],
            ),
            I("croissant", 1, None, ["a croissant"]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich no bacon"], [rm("bacon", "no bacon")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0026",
        """
c: hiii 👋
c: can i get 2 dr peppers 🥤
c: for pickup
c: in like 30 min ⏰
c: actually swap the dr peppers for a large pepperoni 🍕
""",
        "S P P P M",
        items=[I("pepperoni_pizza", 1, "large", ["swap the dr peppers for a large pepperoni"])],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in like 30 min", None),
    ),
    X(
        "syn-t6-0027",
        """
c: Hi, I'd like to order 3 small Hawaiian pizzas for October 17th at 6:30.
c: Delivered to 398 Mission Rd, please.
""",
        "P P",
        items=[I("hawaiian_pizza", 3, "small", ["3 small Hawaiian pizzas"])],
        method="delivery",
        method_q="Delivered to 398 Mission Rd",
        time=("clock_time", "at 6:30", "18:30"),
        day=("date", 10, 17, "October 17th"),
        addr={"raw": "398 Mission Rd", "number": "398", "street": "Mission Rd"},
    ),
    X(
        "syn-t6-0028",
        """
c: morning!
c: 4 cinnamon raisin bagels w tomato
c: 2 small americanos
c: n a hot choc no whip
c: pickup at 9 for dev
c: card
c: wait can we do tomorrow at 9 instead
""",
        "S P P P P P M",
        items=[
            I(
                "bagel",
                4,
                "cinnamon_raisin",
                ["4 cinnamon raisin bagels w tomato"],
                [add("tomato", "w tomato")],
            ),
            I("americano", 2, "small", ["2 small americanos"]),
            I("hot_chocolate", 1, None, ["a hot choc no whip"], [rm("whipped_cream", "no whip")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0029",
        """
c: hey
c: 1 veggie pizza
c: 1 personal margherita no mozzarella thick crust
c: n a coke
c: deliver to 388 spruce ln
""",
        "S P P P P",
        items=[
            I("veggie_pizza", 1, None, ["1 veggie pizza"]),
            I(
                "margherita_pizza",
                1,
                "personal",
                ["1 personal margherita no mozzarella thick crust"],
                [rm("mozzarella", "no mozzarella"), add("crust_thick", "thick crust")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="deliver to 388 spruce ln",
        addr={"raw": "388 spruce ln", "number": "388", "street": "spruce ln"},
    ),
    X(
        "syn-t6-0030",
        """
c: Hi, can I get a can of Dr Pepper and an iced tea for pickup at 5?
c: I'll pay cash.
c: Sorry, change of plans: make that Friday at 5 instead of today.
""",
        "P P M",
        items=[
            I("dr_pepper", 1, "can", ["a can of Dr Pepper"]),
            I("iced_tea", 1, None, ["an iced tea"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 5", "17:00"),
        day=("weekday", "fri", "Friday"),
        pay="cash",
        pay_q="pay cash",
    ),
]
