"""fresh4 a-fresh4-001–028 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm, sub

ENTRIES = [
    F(
        "a-fresh4-001",
        """
c: hey ordering for a bday party
c: 2 lg lattes
c: 3 choc chip muffins
c: 4 plain croissants
c: n a med hot choc
c: name is priya
""",
        "P P P P P P",
        start="Sat 09:30",
        items=[
            I("latte", 2, "large", ["2 lg lattes"]),
            I("muffin", 3, "chocolate_chip", ["3 choc chip muffins"]),
            I("croissant", 4, "plain", ["4 plain croissants"]),
            I("hot_chocolate", 1, "medium", ["a med hot choc"]),
        ],
        name="Priya",
        name_q="priya",
        annotation="Announcing the order with no items yet is PLACE_ORDER (2026-11-03 rule).",
    ),
    F(
        "a-fresh4-002",
        """
c: 2 bacon burgers n lg fries
c: deliver to 88 maple ave
c: card
c: wait actually can u make it for tmrw at 6:30 instead
c: thx
""",
        "P P P M S",
        start="Mon 17:10",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("fries", 1, "large", ["lg fries"]),
        ],
        method="delivery",
        method_q="deliver to 88 maple ave",
        time=("clock_time", "at 6:30", "18:30"),
        day=("tomorrow", "tmrw"),
        addr={"raw": "88 maple ave", "number": "88", "street": "maple ave"},
        pay="card",
        pay_q="card",
        annotation="Moved from now to tomorrow at 6:30 (pm: open 11-22) before any confirmation: MODIFY_ORDER, "
        "requested_time.day tomorrow.",
    ),
    F(
        "a-fresh4-003",
        """
c: do u guys do pickup or only delivry
""",
        "D",
        start="Tue 13:00",
    ),
    F(
        "a-fresh4-004",
        """
c: random q
c: is a tomato a fruit or veg?? settling a bet
""",
        "S O",
        start="Wed 10:15",
    ),
    F(
        "a-fresh4-005",
        """
c: hiii 🍕
c: do u deliver to the north side? 🚗
b: We deliver within 5 miles of the shop. What's the address?
c: 🫠
""",
        "S D U",
        start="Fri 19:40",
    ),
    F(
        "a-fresh4-006",
        """
c: HELLO
c: FIRST TIME ORDERING HERE. CAN I GET 2 CHEESEBURGERS, A BACON BURGER, A VEGGIE BURGER, 3 LARGE FRIES AND 2 CHOCOLATE SHAKES FOR PICKUP
c: THANK YOU
""",
        "S P S",
        start="Sat 13:20",
        items=[
            I("cheeseburger", 2, "single", ["2 CHEESEBURGERS"]),
            I("bacon_burger", 1, None, ["A BACON BURGER"]),
            I("veggie_burger", 1, None, ["A VEGGIE BURGER"]),
            I("fries", 3, "large", ["3 LARGE FRIES"]),
            I("milkshake", 2, "chocolate", ["2 CHOCOLATE SHAKES"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
    ),
    F(
        "a-fresh4-007",
        """
c: GOOD MORNING
c: A LARGE LATTE AND A BLUEBERRY MUFFIN
c: PICKUP FOR DOUG
c: PAYING CARD
c: ACTUALLY CAN YOU MAKE THE LATTE WITH OAT MILK
""",
        "S P P P M",
        start="Tue 07:45",
        items=[
            I(
                "latte",
                1,
                "large",
                ["A LARGE LATTE", "MAKE THE LATTE WITH OAT MILK"],
                [sub("whole_milk", "oat_milk", "WITH OAT MILK")],
            ),
            I("muffin", 1, "blueberry", ["A BLUEBERRY MUFFIN"]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="PAYING CARD",
        name="Doug",
        name_q="DOUG",
    ),
    F(
        "a-fresh4-008",
        """
c: Hi there.
c: I work nights, so I'd like to order for tomorrow: a large pepperoni and an order of garlic knots.
c: Pickup at 5:30 pm, please.
c: I'll pay with card when I get there.
""",
        "S P P P",
        start="Wed 22:10",
        items=[
            I("pepperoni_pizza", 1, "large", ["a large pepperoni"]),
            I("garlic_knots", 1, None, ["an order of garlic knots"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 5:30 pm", "17:30"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="I'll pay with card",
    ),
    F(
        "a-fresh4-009",
        """
c: veggie burger no mayo, im vegan
c: n a large fries
c: pickup at 7
c: card
""",
        "P P P P",
        start="Thu 16:30",
        items=[
            I("veggie_burger", 1, None, ["veggie burger no mayo"], [rm("mayo", "no mayo")]),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "19:00"),
        pay="card",
        pay_q="card",
        annotation="'at 7' at 16:30, open 11-22: 19:00.",
    ),
    F(
        "a-fresh4-010",
        """
c: hii
c: can i order ahead for friday morning?
b: Yes, we take orders up to a week ahead. What would you like?
c: ok 2 med cappucinos n 2 almond croissants for fri at 8:15
""",
        "S D P",
        start="Mon 09:20",
        items=[
            I("cappuccino", 2, "medium", ["2 med cappucinos"]),
            I("croissant", 2, "almond", ["2 almond croissants"]),
        ],
        time=("clock_time", "at 8:15", "08:15"),
        day=("weekday", "fri", "fri"),
        annotation="Asking whether they can order ahead is a DELIVERY_QUESTION (2026-11-12 rule).",
    ),
    F(
        "a-fresh4-011",
        """
c: some onion rings n a cheesburger for pickup, do they come w a dip?
""",
        "P/Q",
        start="Sun 14:00",
        items=[
            I("onion_rings", None, None, ["some onion rings"]),
            I("cheeseburger", 1, "single", ["a cheesburger"]),
        ],
        method="pickup",
        method_q="for pickup",
    ),
    F(
        "a-fresh4-012",
        """
c: a few personal margheritas to 230 elm st pls, r they vegetarian? my kids dont eat meat
""",
        "P/Q",
        start="Thu 18:00",
        items=[I("margherita_pizza", None, "personal", ["a few personal margheritas"])],
        method="delivery",
        method_q="to 230 elm st",
        addr={"raw": "230 elm st", "number": "230", "street": "elm st"},
    ),
    F(
        "a-fresh4-013",
        """
c: yo
c: order for satrday
c: 3 double cbs n 3 fries
c: deliver to 15 campus dr dorm b at 9pm
c: cash
""",
        "S P P P P",
        start="Wed 21:15",
        items=[
            I("cheeseburger", 3, "double", ["3 double cbs"]),
            I("fries", 3, "regular", ["3 fries"]),
        ],
        method="delivery",
        method_q="deliver to 15 campus dr",
        time=("clock_time", "at 9pm", "21:00"),
        day=("weekday", "sat", "satrday"),
        addr={"raw": "15 campus dr dorm b", "number": "15", "street": "campus dr", "unit": "dorm b"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-014",
        """
c: Hello, may I have a medium supreme and a medium cheese for pickup? Is the supreme very spicy?
b: It isn't spicy: pepperoni, sausage, peppers, onions, olives and mushrooms.
c: Lovely, thank you. Please make the cheese pizza a large insted.
""",
        "P/Q M",
        start="Tue 12:40",
        items=[
            I("supreme_pizza", 1, "medium", ["a medium supreme"]),
            I("cheese_pizza", 1, "large", ["a medium cheese", "make the cheese pizza a large"]),
        ],
        method="pickup",
        method_q="for pickup",
    ),
    F(
        "a-fresh4-015",
        """
c: 3 med lattes, 1 w almond milk
c: pickup, name kenji
""",
        "P P",
        start="Thu 08:00",
        items=[
            I("latte", 2, "medium", ["3 med lattes"]),
            I(
                "latte",
                1,
                "medium",
                ["3 med lattes", "1 w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Kenji",
        name_q="kenji",
    ),
    F(
        "a-fresh4-016",
        """
c: Good evening.
c: I would like 4 large cheese pizzas, two of them with mushrooms please.
c: For pickup.
c: Thank you kindly.
""",
        "S P P S",
        start="Fri 18:15",
        items=[
            I("cheese_pizza", 2, "large", ["4 large cheese pizzas"]),
            I(
                "cheese_pizza",
                2,
                "large",
                ["4 large cheese pizzas", "two of them with mushrooms"],
                [add("mushrooms", "with mushrooms")],
            ),
        ],
        method="pickup",
        method_q="For pickup",
    ),
    F(
        "a-fresh4-017",
        """
c: HI CAN I GET A MEDIUM DRIP COFFEE
c: AND WHAT MUFFINS DO YOU HAVE
b: Blueberry, chocolate chip and banana nut!
c: I'LL TAKE THAT ONE THEN
c: PICKUP FOR RAY
c: MAKE THE COFFEE A LARGE
""",
        "P Q P P M",
        start="Mon 08:30",
        items=[
            I("drip_coffee", 1, "large", ["A MEDIUM DRIP COFFEE", "MAKE THE COFFEE A LARGE"]),
            I("muffin", 1, None, ["THAT ONE"], flag="item_variant"),
        ],
        method="pickup",
        method_q="PICKUP",
        name="Ray",
        name_q="RAY",
        annotation="'THAT ONE' after three muffin flavors: a muffin, flavor ambiguous (as dev 049).",
    ),
    F(
        "a-fresh4-018",
        """
c: lg americano n a sesame bagel w cream cheese
c: pickup at 2:15
c: name is aimee
c: card
""",
        "P P P P",
        start="Wed 11:30",
        items=[
            I("americano", 1, "large", ["lg americano"]),
            I(
                "bagel",
                1,
                "sesame",
                ["a sesame bagel w cream cheese"],
                [add("cream_cheese", "w cream cheese")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 2:15", "14:15"),
        pay="card",
        pay_q="card",
        name="Aimee",
        name_q="aimee",
        annotation="'at 2:15' at 11:30, open 7-15: only 14:15 is open.",
    ),
    F(
        "a-fresh4-019",
        """
c: Hi, a bacon burger, a regular fries and a lemonade please.
c: Delivered to 72 Linden St.
c: Card.
""",
        "P P P",
        start="Thu 20:30",
        items=[
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("fries", 1, "regular", ["a regular fries"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="Delivered to 72 Linden St",
        addr={"raw": "72 Linden St", "number": "72", "street": "Linden St"},
        pay="card",
        pay_q="Card",
    ),
    F(
        "a-fresh4-020",
        """
c: hi im visiting, whats the most popular burger?
b: The Bacon Burger is a favorite!
c: ok 2 of those n 2 cokes
c: to the bayside hotel, 500 harbor blvd
c: actualy make it 3 bacon burgers
""",
        "Q P P M",
        start="Sat 12:15",
        items=[
            I("bacon_burger", 3, None, ["2 of those", "make it 3 bacon burgers"]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        method="delivery",
        method_q="to the bayside hotel",
        addr={"raw": "the bayside hotel, 500 harbor blvd", "number": "500", "street": "harbor blvd"},
    ),
    F(
        "a-fresh4-021",
        """
c: is the veggie pizza dairy free
b: It comes with cheese, but we can leave it off.
c: ok large veggie no cheese
c: deliver to 9 oak ct
c: card
c: n add vegan cheese pls
""",
        "Q P P P P",
        start="Tue 19:00",
        items=[
            I(
                "veggie_pizza",
                1,
                "large",
                ["large veggie no cheese", "add vegan cheese"],
                [rm("cheese", "no cheese"), offmod("vegan cheese")],
            ),
        ],
        method="delivery",
        method_q="deliver to 9 oak ct",
        addr={"raw": "9 oak ct", "number": "9", "street": "oak ct"},
        pay="card",
        pay_q="card",
        annotation="Vegan cheese isn't on the menu: a not_on_menu add, asked (as fresh 080). Adding a detail "
        "replaces nothing: PLACE_ORDER.",
    ),
    F(
        "a-fresh4-022",
        """
c: hey
c: for tmrw
c: 2 lg drips
c: 1 w oat milk
c: n 3 blueberry muffins
c: pickup
c: name sol
""",
        "S P P P P P P",
        start="Sun 10:00",
        items=[
            I("drip_coffee", 1, "large", ["2 lg drips"]),
            I("drip_coffee", 1, "large", ["2 lg drips", "1 w oat milk"], [add("oat_milk", "w oat milk")]),
            I("muffin", 3, "blueberry", ["3 blueberry muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tmrw"),
        day=("tomorrow", "tmrw"),
        name="Sol",
        name_q="sol",
    ),
    F(
        "a-fresh4-023",
        """
c: HELLO
c: I NEED 3 LARGE PEPPERONI AND 2 GARLIC KNOTS FOR NOVEMBER 28 AT 6PM
c: DELIVER TO 1400 RIVER RD
""",
        "S P P",
        start="Tue 17:00",
        items=[
            I("pepperoni_pizza", 3, "large", ["3 LARGE PEPPERONI"]),
            I("garlic_knots", 2, None, ["2 GARLIC KNOTS"]),
        ],
        method="delivery",
        method_q="DELIVER TO 1400 RIVER RD",
        time=("clock_time", "AT 6PM", "18:00"),
        day=("date", 11, 28, "NOVEMBER 28"),
        addr={"raw": "1400 RIVER RD", "number": "1400", "street": "RIVER RD"},
    ),
    F(
        "a-fresh4-024",
        """
c: Hello, does the cheeseburger come with pickles?
b: Yes, pickles, lettuce, tomato, onion and ketchup.
c: Great, two cheeseburgers without pickles and an order of onion rings.
c: Please deliver to 31 Beacon St. I'll pay cash.
""",
        "Q P P",
        start="Mon 13:10",
        items=[
            I(
                "cheeseburger",
                2,
                "single",
                ["two cheeseburgers without pickles"],
                [rm("pickle", "without pickles")],
            ),
            I("onion_rings", 1, None, ["an order of onion rings"]),
        ],
        method="delivery",
        method_q="deliver to 31 Beacon St",
        addr={"raw": "31 Beacon St", "number": "31", "street": "Beacon St"},
        pay="cash",
        pay_q="I'll pay cash",
    ),
    F(
        "a-fresh4-025",
        """
c: Hello, for tomorrow at 11:30: 3 medium lattes, 2 breakfast sandwiches on croissants and a chocolate croissant, please. Name is Farah.
""",
        "P",
        start="Wed 12:20",
        items=[
            I("latte", 3, "medium", ["3 medium lattes"]),
            I("breakfast_sandwich", 2, "croissant", ["2 breakfast sandwiches on croissants"]),
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
        ],
        time=("clock_time", "at 11:30", "11:30"),
        day=("tomorrow", "tomorrow"),
        name="Farah",
    ),
    F(
        "a-fresh4-026",
        """
c: need food for the team, 2 lg meat lovers
c: n 2 lg cheese, some sodas too
b: Which sodas, and how many? We have Coke, Diet Coke, Sprite, Dr Pepper and iced tea.
c: 3 cokes n a diet coke, 2 liters
c: + breadsticks
""",
        "P P P P",
        start="Thu 12:30",
        items=[
            I("meat_lovers_pizza", 2, "large", ["2 lg meat lovers"]),
            I("cheese_pizza", 2, "large", ["2 lg cheese"]),
            I("coke", 3, "two_liter", ["3 cokes", "2 liters"]),
            I("diet_coke", 1, "two_liter", ["a diet coke", "2 liters"]),
            I("breadsticks", 1, None, ["breadsticks"]),
        ],
        annotation="'some sodas' is settled by the next message: the vague line is dropped.",
    ),
    F(
        "a-fresh4-027",
        """
c: 2 cheeseburgers n 2 lg fries
c: deliver to 640 grove st
c: card
c: n 2 cokes
c: actually swap the cokes for lemonades
""",
        "P P P P M",
        start="Fri 18:45",
        items=[
            I("cheeseburger", 2, "single", ["2 cheeseburgers"]),
            I("fries", 2, "large", ["2 lg fries"]),
            I("lemonade", 2, None, ["2 cokes", "swap the cokes for lemonades"]),
        ],
        method="delivery",
        method_q="deliver to 640 grove st",
        addr={"raw": "640 grove st", "number": "640", "street": "grove st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh4-028",
        """
c: Good afternoon 😊
c: Could I please have a veggie burger and a vanilla milkshake? I'll pay by card.
b: Of course! 1 Veggie Burger and 1 vanilla Milkshake, paying by card. Is that right?
c: Yes, that's right, thank you 🙏
c: Oh, and could you add an order of onion rings as well?
c: Much appreciated 😊
""",
        "S P C M S",
        start="Sat 14:40",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("milkshake", 1, "vanilla", ["a vanilla milkshake"]),
            I("onion_rings", 1, None, ["an order of onion rings"]),
        ],
        pay="card",
        pay_q="I'll pay by card",
        annotation="A new item after the yes changes the placed order (MODIFY_ORDER, time_sensitive); the "
        "decision is back to pending.",
    ),
]
