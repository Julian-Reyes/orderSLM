"""fresh3 a-fresh3-001–020 (chats + gold by hand; see build.py)."""

from build import F, I, add, note, offmod

ENTRIES = [
    F(
        "a-fresh3-001",
        """
c: yo
c: 2 med pepperoni
c: n a med hawaiian
c: pickup in 25
c: wait make the hawaiian a large
c: card
""",
        "S P P P M P",
        start="Tue 17:40",
        items=[
            I("pepperoni_pizza", 2, "medium", ["2 med pepperoni"]),
            I("hawaiian_pizza", 1, "large", ["a med hawaiian", "make the hawaiian a large"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 25", None),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-002",
        """
c: hey do u guys take orders for tmrw
b: Yes, we take orders up to a week ahead. What would you like?
c: ok bet. 2 bacon burgers n a large fries
c: for tmrw at 7pm, deliver to 410 kensington ave apt 2
c: paying card
""",
        "D P P P",
        start="Wed 21:30",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="delivery",
        method_q="deliver to 410 kensington ave",
        time=("clock_time", "at 7pm", "19:00"),
        day=("tomorrow", "tmrw"),
        addr={
            "raw": "410 kensington ave apt 2",
            "number": "410",
            "street": "kensington ave",
            "unit": "apt 2",
        },
        pay="card",
        pay_q="paying card",
        annotation="Asking whether they take orders for tomorrow is a DELIVERY_QUESTION (2026-11-12 rule); the order "
        "for tomorrow at 7 pm: requested_time.day tomorrow.",
    ),
    F(
        "a-fresh3-003",
        """
c: Good morning! Do your croissants come warm?
b: We can warm them up for you if you'd like.
c: Yes please. For a little party: 2 large lattes, a medium hot chocolate, 3 chocolate croissants warmed, 2 blueberry muffins and an everything bagel with cream cheese. Pickup under Nadia, card.
""",
        "Q P",
        start="Sat 09:10",
        items=[
            I("latte", 2, "large", ["2 large lattes"]),
            I("hot_chocolate", 1, "medium", ["a medium hot chocolate"]),
            I("croissant", 3, "chocolate", ["3 chocolate croissants warmed"], [note("warmed")]),
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
            I(
                "bagel",
                1,
                "everything",
                ["an everything bagel with cream cheese"],
                [add("cream_cheese", "with cream cheese")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Nadia",
    ),
    F(
        "a-fresh3-004",
        """
c: Hi, I'd like a veggie burger with grilled mushrooms added, a regular fries and a Sprite for pickup, paying cash.
""",
        "P",
        start="Mon 12:15",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["a veggie burger with grilled mushrooms added"],
                [offmod("with grilled mushrooms added")],
            ),
            I("fries", 1, "regular", ["a regular fries"]),
            I("sprite", 1, None, ["a Sprite"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="paying cash",
    ),
    F(
        "a-fresh3-005",
        """
c: lg drip w oat milk + a plain bagel w butter
c: pickup now, theo, card
""",
        "P P",
        start="Tue 08:05",
        items=[
            I("drip_coffee", 1, "large", ["lg drip w oat milk"], [add("oat_milk", "w oat milk")]),
            I("bagel", 1, "plain", ["a plain bagel w butter"], [add("butter", "w butter")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "now", None),
        pay="card",
        pay_q="card",
        name="Theo",
        name_q="theo",
    ),
    F(
        "a-fresh3-006",
        """
c: hey 🍕 2 large cheese pizzas to 77 hawthorne st for the office, i already paid online, got the screenshot 📸
""",
        "P/PC",
        start="Thu 12:40",
        items=[I("cheese_pizza", 2, "large", ["2 large cheese pizzas"])],
        method="delivery",
        method_q="to 77 hawthorne st",
        addr={"raw": "77 hawthorne st", "number": "77", "street": "hawthorne st"},
        pay_q="i already paid",
        paid=True,
        annotation="A claim in the order message: PLACE_ORDER + PAYMENT_CLAIM; 'online' and a screenshot are not a "
        "method (unknown), unverified, not asked again.",
    ),
    F(
        "a-fresh3-007",
        """
c: k
""",
        "U",
        start="Fri 15:05",
    ),
    F(
        "a-fresh3-008",
        """
c: hey quick q
c: is the bacon burger ok for someone who cant ea
""",
        "S U",
        start="Sun 17:30",
        annotation="Cut off mid-word: what can't be eaten is unknown, so UNKNOWN (like fresh 001).",
    ),
    F(
        "a-fresh3-009",
        """
c: Hello, I'd like to order for my family: 2 cheeseburgers, a bacon burger, a veggie burger and 2 milkshakes.
b: Sure! Which flavors for the milkshakes: vanilla, chocolate or strawberry?
c: One chocolate and one strawberry, plus 2 large fries. Delivered to 1520 Willow Creek Rd, please. I'll pay by card.
""",
        "P P",
        start="Fri 18:10",
        items=[
            I("cheeseburger", 2, None, ["2 cheeseburgers"]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("milkshake", 1, "chocolate", ["2 milkshakes", "One chocolate"]),
            I("milkshake", 1, "strawberry", ["2 milkshakes", "one strawberry"]),
            I("fries", 2, "large", ["2 large fries"]),
        ],
        method="delivery",
        method_q="Delivered to 1520 Willow Creek Rd",
        addr={"raw": "1520 Willow Creek Rd", "number": "1520", "street": "Willow Creek Rd"},
        pay="card",
        pay_q="pay by card",
    ),
    F(
        "a-fresh3-010",
        """
c: hey
c: 4 small lattes
c: 2 w vanilla
c: pickup for ari, cash
""",
        "S P P P",
        start="Wed 07:50",
        items=[
            I("latte", 2, "small", ["4 small lattes"]),
            I("latte", 2, "small", ["4 small lattes", "2 w vanilla"], [add("vanilla_syrup", "w vanilla")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ari",
        name_q="ari",
    ),
    F(
        "a-fresh3-011",
        """
c: Hello, a drip coffee and a cappuccino for pickup, please. Name is Walt, card.
c: Oh, and make both of those large.
""",
        "P M",
        start="Thu 10:30",
        items=[
            I("drip_coffee", 1, "large", ["a drip coffee", "make both of those large"]),
            I("cappuccino", 1, "large", ["a cappuccino", "make both of those large"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
        name="Walt",
    ),
    F(
        "a-fresh3-012",
        """
c: hey need some food for the game
c: 2 lg meat lovers
c: an order of knots n 2 liter coke
c: paying cash
""",
        "P P P P",
        start="Sun 15:20",
        items=[
            I("meat_lovers_pizza", 2, "large", ["2 lg meat lovers"]),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("coke", 1, "two_liter", ["2 liter coke"]),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    F(
        "a-fresh3-013",
        """
c: hi can i get 3 medium lattes n a choc chip muffin
c: pickup at 8:45, name is bea
c: card
b: Got it, Bea: 3 medium lattes and 1 chocolate chip muffin, pickup at 8:45, paying by card. Is that right?
c: yes!
c: oh add a sesame bagel too
""",
        "P P P C M",
        start="Mon 08:15",
        items=[
            I("latte", 3, "medium", ["3 medium lattes"]),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8:45", "08:45"),
        pay="card",
        pay_q="card",
        name="Bea",
        name_q="bea",
    ),
    F(
        "a-fresh3-014",
        """
c: hiya
c: can i get a jumbo pepperoni n a small cheese delivered to 39 grant st
""",
        "S P",
        start="Tue 18:25",
        items=[
            I("pepperoni_pizza", 1, None, ["a jumbo pepperoni"], unmatched_variant="jumbo"),
            I("cheese_pizza", 1, "small", ["a small cheese"]),
        ],
        method="delivery",
        method_q="delivered to 39 grant st",
        addr={"raw": "39 grant st", "number": "39", "street": "grant st"},
    ),
    F(
        "a-fresh3-015",
        """
c: Just wanted to say your burgers were amazing last night. Thanks!
""",
        "S",
        start="Sat 13:00",
    ),
    F(
        "a-fresh3-016",
        """
c: HEY
c: 2 LARGE PEPPERONI
c: 1 LARGE VEGGIE
c: 2 ORDERS OF BREADSTICKS
c: AND SOME SODAS
b: Which sodas would you like, and how many? We have Coke, Diet Coke, Sprite, Dr Pepper and iced tea.
c: 2 COKES AND A SPRITE, CANS. PICKUP
""",
        "S P P P P P",
        start="Fri 22:05",
        items=[
            I("pepperoni_pizza", 2, "large", ["2 LARGE PEPPERONI"]),
            I("veggie_pizza", 1, "large", ["1 LARGE VEGGIE"]),
            I("breadsticks", 2, None, ["2 ORDERS OF BREADSTICKS"]),
            I("coke", 2, "can", ["2 COKES", "CANS"]),
            I("sprite", 1, "can", ["A SPRITE", "CANS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        annotation="'SOME SODAS' is settled by the next message: the vague line is dropped.",
    ),
    F(
        "a-fresh3-017",
        """
c: whats vegetarian on ur menu
""",
        "Q",
        start="Wed 21:40",
    ),
    F(
        "a-fresh3-018",
        """
c: hey ☕ how much is delivery to the office park? 🚗
""",
        "D",
        start="Thu 09:00",
    ),
    F(
        "a-fresh3-019",
        """
c: hi im visiting next week
c: can i get 2 large americanos n 2 almond croissants for monday
c: at 8:15
c: paying card
""",
        "S P P P",
        start="Thu 10:20",
        items=[
            I("americano", 2, "large", ["2 large americanos"]),
            I("croissant", 2, "almond", ["2 almond croissants"]),
        ],
        time=("clock_time", "at 8:15", "08:15"),
        day=("weekday", "mon", "monday"),
        pay="card",
        pay_q="paying card",
    ),
    F(
        "a-fresh3-020",
        """
c: Hi, a medium margherita and a medium supreme delivered to 2210 Fairmont Ave, paying cash.
b: Got it: 1 medium Margherita Pizza and 1 medium Supreme Pizza, delivered to 2210 Fairmont Ave, paying cash. Is that right?
c: Yes, that's right.
c: Actually, could the supreme be a large?
""",
        "P C M",
        start="Sat 19:10",
        items=[
            I("margherita_pizza", 1, "medium", ["a medium margherita"]),
            I("supreme_pizza", 1, "large", ["a medium supreme", "the supreme be a large"]),
        ],
        method="delivery",
        method_q="delivered to 2210 Fairmont Ave",
        addr={"raw": "2210 Fairmont Ave", "number": "2210", "street": "Fairmont Ave"},
        pay="cash",
        pay_q="paying cash",
    ),
]
