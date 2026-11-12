"""t6 entries 0071–0080 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t6-0071",
        """
c: hii ☕ can i get a small cappuccino w vanilla n almond milk
c: for tomorrow at 10
c: pickup, name nico 😊
""",
        "P P P",
        items=[
            I(
                "cappuccino",
                1,
                "small",
                ["a small cappuccino w vanilla n almond milk"],
                [add("vanilla_syrup", "w vanilla"), sub("whole_milk", "almond_milk", "almond milk")],
            )
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10", "10:00"),
        day=("tomorrow", "tomorrow"),
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t6-0072",
        """
c: hi
c: 3 large supremes no olives for wed at 6:30
c: card
""",
        "S P P",
        items=[I("supreme_pizza", 3, "large", ["3 large supremes no olives"], [rm("olives", "no olives")])],
        time=("clock_time", "at 6:30", "18:30"),
        day=("weekday", "wed", "wed"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0073",
        """
c: HI A SESAME BAGEL WITH TOMATO PLEASE
c: FOR PICKUP NEXT FRIDAY AT 9
c: NAME NICO, CARD
""",
        "P P P",
        items=[I("bagel", 1, "sesame", ["A SESAME BAGEL WITH TOMATO"], [add("tomato", "WITH TOMATO")])],
        method="pickup",
        method_q="FOR PICKUP",
        time=("clock_time", "AT 9", "09:00"),
        day=("weekday", "fri", "NEXT FRIDAY"),
        pay="card",
        pay_q="CARD",
        name="Nico",
        name_q="NICO",
    ),
    X(
        "syn-t6-0074",
        """
c: yo
c: 2 bacon burgers no onions
c: delivery, card
c: oh wait not now, can u do sunday at 1 instead
""",
        "S P P M",
        items=[I("bacon_burger", 2, None, ["2 bacon burgers no onions"], [rm("onion", "no onions")])],
        method="delivery",
        method_q="delivery",
        time=("clock_time", "at 1", "13:00"),
        day=("weekday", "sun", "sunday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0075",
        """
c: hi
c: ordering for tmrw
c: small hot chocolate
c: 2 small americanos
c: pickup
c: ben
c: cash
""",
        "S P P P P P P",
        items=[
            I("hot_chocolate", 1, "small", ["small hot chocolate"]),
            I("americano", 2, "small", ["2 small americanos"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tmrw"),
        day=("tomorrow", "tmrw"),
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0076",
        """
c: Hi, I'd like 2 personal BBQ chicken pizzas with no cheese but add capers, a bottled water and a Coke for pickup. I'll pay by card.
""",
        "P",
        items=[
            I(
                "bbq_chicken_pizza",
                2,
                "personal",
                ["2 personal BBQ chicken pizzas with no cheese but add capers"],
                [rm("cheese", "no cheese"), offmod("add capers")],
            ),
            I("water", 1, None, ["a bottled water"]),
            I("coke", 1, None, ["a Coke"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0077",
        """
c: Happy Tuesday! It's a busy one at the office.
c: Could I get 2 chocolate chip muffins?
c: Also 4 large americanos with caramel.
c: And 3 medium lattes, please.
""",
        "S P P P",
        items=[
            I("muffin", 2, "chocolate_chip", ["2 chocolate chip muffins"]),
            I(
                "americano",
                4,
                "large",
                ["4 large americanos with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
            I("latte", 3, "medium", ["3 medium lattes"]),
        ],
    ),
    X(
        "syn-t6-0078",
        """
c: hey 🍔 2 veggie burgers w cheese
c: n a regular fries + a bacon burger
c: deliver to 18 larkin blvd 🏠
b: Got it! Will you pay by card or cash?
c: actually drop the bacon burger 🙅
""",
        "P P P M",
        items=[
            I("veggie_burger", 2, None, ["2 veggie burgers w cheese"], [add("cheese", "w cheese")]),
            I("fries", 1, "regular", ["a regular fries"]),
        ],
        method="delivery",
        method_q="deliver to 18 larkin blvd",
        addr={"raw": "18 larkin blvd", "number": "18", "street": "larkin blvd"},
    ),
    X(
        "syn-t6-0079",
        """
c: hey 👋 2 breakfast sandwiches + 2 everything bagels
c: its for sunday morning 🌞
c: card 💳
""",
        "P P P",
        items=[
            I("breakfast_sandwich", 2, None, ["2 breakfast sandwiches"]),
            I("bagel", 2, "everything", ["2 everything bagels"]),
        ],
        time=("ambiguous", "sunday morning"),
        day=("weekday", "sun", "sunday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0080",
        """
c: Hello!
c: A chocolate milkshake, a veggie burger and 4 orders of onion rings for delivery, please.
c: Actually, could we push it to Friday at 6? Plans changed.
""",
        "S P M",
        items=[
            I("milkshake", 1, "chocolate", ["A chocolate milkshake"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("onion_rings", 4, None, ["4 orders of onion rings"]),
        ],
        method="delivery",
        method_q="for delivery",
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "fri", "Friday"),
    ),
]
