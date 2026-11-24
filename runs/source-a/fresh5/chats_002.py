"""fresh5 a-fresh5-029–056 (chats + gold by hand; see build.py)."""

from build import F, I, add, sub

ENTRIES = [
    F(
        "a-fresh5-029",
        """
c: can i get a few chocolate croissants n a med cap
c: card
""",
        "P P",
        start="Tue 10:20",
        items=[
            I("croissant", None, "chocolate", ["a few chocolate croissants"]),
            I("cappuccino", 1, "medium", ["a med cap"]),
        ],
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-030",
        """
c: is the bacon burger big?
b: It's a single patty with bacon, cheese and the works.
c: ok a bacon burger n a lemonade, pickup, cash
b: Got it: 1 Bacon Burger and 1 Lemonade, pickup, paying cash. Is that right?
c: ya
c: oh actually ill pay by card
""",
        "Q P C M",
        start="Wed 13:40",
        items=[
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="ill pay by card",
    ),
    F(
        "a-fresh5-031",
        """
c: hey!
c: can i order now for thursday?
b: Yes, you can order up to a week ahead!
c: ok 2 veggie burgers n a lemonade for thurs at 1, card
""",
        "S D P",
        start="Mon 15:20",
        items=[
            I("veggie_burger", 2, None, ["2 veggie burgers"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        time=("clock_time", "at 1", "13:00"),
        day=("weekday", "thu", "thurs"),
        pay="card",
        pay_q="card",
        annotation="Asking whether they can order ahead is DELIVERY_QUESTION (as fresh3 002, 100); then the order "
        "for Thursday at 13:00 (open 11-22).",
    ),
    F(
        "a-fresh5-032",
        """
c: 4 blueberry muffins for friday
c: pickup, name lou
""",
        "P P",
        start="Tue 11:00",
        items=[I("muffin", 4, "blueberry", ["4 blueberry muffins"])],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for friday"),
        day=("weekday", "fri", "friday"),
        name="Lou",
        name_q="lou",
        annotation="A day with no clock time: requested_time ambiguous, day fri; the time is asked.",
    ),
    F(
        "a-fresh5-033",
        """
c: hey
c: for sunday
c: medium hawaiian
c: n a small cheese
c: pickup at 5
c: name is jo
""",
        "S P P P P P",
        start="Wed 14:10",
        items=[
            I("hawaiian_pizza", 1, "medium", ["medium hawaiian"]),
            I("cheese_pizza", 1, "small", ["a small cheese"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 5", "17:00"),
        day=("weekday", "sun", "sunday"),
        name="Jo",
        name_q="jo",
    ),
    F(
        "a-fresh5-034",
        """
c: 3 cheeseburgers
c: 3 cokes
c: pickup at 6
c: card
c: name max
c: wait
c: make it tmrw at 6, not tonight
""",
        "P P P P P U M",
        start="Thu 15:00",
        items=[
            I("cheeseburger", 3, None, ["3 cheeseburgers"]),
            I("coke", 3, None, ["3 cokes"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 6", "18:00"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Max",
        name_q="max",
        annotation="Moved from tonight to tomorrow at 18:00 before any confirmation: MODIFY_ORDER. A lone 'wait' "
        "says nothing yet: UNKNOWN.",
    ),
    F(
        "a-fresh5-035",
        """
c: hey do u
c: jjjjkkk
c: asdfgh
""",
        "U U U",
        start="Fri 20:00",
    ),
    F(
        "a-fresh5-036",
        """
c: 2 medium bbq chicken
c: to 77 elm st
c: cash
b: Got it: 2 medium BBQ Chicken Pizzas, delivered to 77 Elm St, paying cash. Is that right?
c: yep
c: actually card instead
""",
        "P P P C M",
        start="Sat 17:30",
        items=[I("bbq_chicken_pizza", 2, "medium", ["2 medium bbq chicken"])],
        method="delivery",
        method_q="to 77 elm st",
        addr={"raw": "77 elm st", "number": "77", "street": "elm st"},
        pay="card",
        pay_q="card instead",
    ),
    F(
        "a-fresh5-037",
        """
c: veggie burger
c: pickup, cash
b: Got it: 1 Veggie Burger, pickup, paying cash. Is that right?
c: yes
c: n add a sprite
""",
        "P P C M",
        start="Sun 12:30",
        items=[
            I("veggie_burger", 1, None, ["veggie burger"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        annotation="Adding an item after confirming is MODIFY_ORDER; the order needs a new yes.",
    ),
    F(
        "a-fresh5-038",
        """
c: morning!
c: some bagels w cream cheese n a large drip
c: pickup for gus
""",
        "S P P",
        start="Mon 08:10",
        items=[
            I("bagel", None, None, ["some bagels w cream cheese"], [add("cream_cheese", "w cream cheese")]),
            I("drip_coffee", 1, "large", ["a large drip"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Gus",
        name_q="gus",
    ),
    F(
        "a-fresh5-039",
        """
c: 2 lg lattes
c: 3 croissants
b: Which croissants would you like: plain, chocolate or almond?
c: 2 plain 1 almond
c: n 2 everything bagels
c: a small hot choc
c: pickup for rae
""",
        "P P P P P P",
        start="Tue 09:00",
        items=[
            I("latte", 2, "large", ["2 lg lattes"]),
            I("croissant", 2, "plain", ["3 croissants", "2 plain 1 almond"]),
            I("croissant", 1, "almond", ["3 croissants", "2 plain 1 almond"]),
            I("bagel", 2, "everything", ["2 everything bagels"]),
            I("hot_chocolate", 1, "small", ["a small hot choc"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Rae",
        name_q="rae",
    ),
    F(
        "a-fresh5-040",
        """
c: hi!
c: a med latte n a banana nut muffin for dec 4 at 9:30
""",
        "S P",
        start="Mon 11:15",
        items=[
            I("latte", 1, "medium", ["a med latte"]),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
        time=("clock_time", "at 9:30", "09:30"),
        day=("date", 12, 4, "dec 4"),
    ),
    F(
        "a-fresh5-041",
        """
c: Hi, I'd like a large pepperoni pizza.
c: Also a small veggie pizza.
c: And one order of garlic knots.
c: A can of Coke too.
c: For pickup.
c: Paying with card.
""",
        "P P P P P P",
        start="Wed 18:40",
        items=[
            I("pepperoni_pizza", 1, "large", ["a large pepperoni pizza"]),
            I("veggie_pizza", 1, "small", ["a small veggie pizza"]),
            I("garlic_knots", 1, None, ["one order of garlic knots"]),
            I("coke", 1, "can", ["A can of Coke"]),
        ],
        method="pickup",
        method_q="For pickup",
        pay="card",
        pay_q="Paying with card",
    ),
    F(
        "a-fresh5-042",
        """
c: Hi, two cheeseburgers and an order of onion rings for pickup at 5:15.
c: Name is Hal, paying cash.
""",
        "P P",
        start="Thu 14:00",
        items=[
            I("cheeseburger", 2, None, ["two cheeseburgers"]),
            I("onion_rings", 1, None, ["an order of onion rings"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 5:15", "17:15"),
        pay="cash",
        pay_q="paying cash",
        name="Hal",
        name_q="Hal",
        annotation="'at 5:15' at 14:00, open 11-22: 17:15.",
    ),
    F(
        "a-fresh5-043",
        """
c: Good morning.
c: I'd like to order for tomorrow.
c: Two medium cappuccinos and a sesame bagel with butter.
c: Pickup at 8:30, please.
c: The name is Pia.
""",
        "S P P P P",
        start="Fri 10:00",
        items=[
            I("cappuccino", 2, "medium", ["Two medium cappuccinos"]),
            I("bagel", 1, "sesame", ["a sesame bagel with butter"], [add("butter", "with butter")]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 8:30", "08:30"),
        day=("tomorrow", "tomorrow"),
        name="Pia",
        name_q="Pia",
    ),
    F(
        "a-fresh5-044",
        """
c: HEY THERE
c: 3 CHEESEBURGERS, 2 BACON BURGERS, A VEGGIE BURGER, 4 LARGE FRIES AND 6 COKES TO 210 HOLLIS ST, PAYING CARD
""",
        "S P",
        start="Fri 18:20",
        items=[
            I("cheeseburger", 3, None, ["3 CHEESEBURGERS"]),
            I("bacon_burger", 2, None, ["2 BACON BURGERS"]),
            I("veggie_burger", 1, None, ["A VEGGIE BURGER"]),
            I("fries", 4, "large", ["4 LARGE FRIES"]),
            I("coke", 6, None, ["6 COKES"]),
        ],
        method="delivery",
        method_q="TO 210 HOLLIS ST",
        addr={"raw": "210 HOLLIS ST", "number": "210", "street": "HOLLIS ST"},
        pay="card",
        pay_q="PAYING CARD",
    ),
    F(
        "a-fresh5-045",
        """
c: hi 🍕 a large half hawaiian half pepperoni
c: n a 20 oz sprite
c: pickup 🙏
c: card 💳
""",
        "P P P P",
        start="Sat 19:30",
        items=[
            I(
                None,
                1,
                "large",
                ["a large half hawaiian half pepperoni"],
                halves=[("hawaiian_pizza", []), ("pepperoni_pizza", [])],
            ),
            I("sprite", 1, "bottle_20oz", ["a 20 oz sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-046",
        """
c: hey
c: 🌀
""",
        "S U",
        start="Sun 15:40",
    ),
    F(
        "a-fresh5-047",
        """
c: HOW BIG IS A MEDIUM?
b: Our medium is 12 inches, 8 slices.
c: OK 2 MEDIUM SUPREMES FOR PICKUP, CASH
b: Got it: 2 medium Supreme Pizzas, pickup, paying cash. Is that right?
c: YES
c: ACTUALLY MAKE THEM LARGE
""",
        "Q P C M",
        start="Mon 19:00",
        items=[I("supreme_pizza", 2, "large", ["2 MEDIUM SUPREMES", "MAKE THEM LARGE"])],
        method="pickup",
        method_q="FOR PICKUP",
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh5-048",
        """
c: xl cheese n 2 cans of iced tea
c: 18 vine st apt 2
c: card
c: swap the iced teas for 2 cans of dr pepper
""",
        "P P P M",
        start="Tue 20:10",
        items=[
            I("cheese_pizza", 1, "extra_large", ["xl cheese"]),
            I("dr_pepper", 2, "can", ["2 cans of dr pepper"]),
        ],
        method="delivery",
        method_q="18 vine st apt 2",
        addr={"raw": "18 vine st apt 2", "number": "18", "street": "vine st", "unit": "apt 2"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-049",
        """
c: CAN I ORDER AHEAD FOR SATURDAY?
b: Yes, you can order up to a week ahead!
c: GREAT, 2 BACON BURGERS AND 2 LEMONADES TO 15 CEDAR LN SATURDAY AT 7, CASH
""",
        "D P",
        start="Wed 17:00",
        items=[
            I("bacon_burger", 2, None, ["2 BACON BURGERS"]),
            I("lemonade", 2, None, ["2 LEMONADES"]),
        ],
        method="delivery",
        method_q="TO 15 CEDAR LN",
        addr={"raw": "15 CEDAR LN", "number": "15", "street": "CEDAR LN"},
        time=("clock_time", "AT 7", "19:00"),
        day=("weekday", "sat", "SATURDAY"),
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh5-050",
        """
c: is the americano strong?
b: It's two espresso shots, so pretty strong!
c: ok a large americano n a monster energy
c: pickup for ola
c: card
""",
        "Q P P P",
        start="Thu 09:30",
        items=[
            I("americano", 1, "large", ["a large americano"]),
            I(None, 1, None, ["a monster energy"], unmatched="a monster energy"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ola",
        name_q="ola",
    ),
    F(
        "a-fresh5-051",
        """
c: hi 😕 got the wrong drinks this morning, can i get a refund pls?
""",
        "R",
        start="Fri 11:20",
        order=False,
        annotation="As fresh4 040: the money back is the request; the wrong drinks are why.",
    ),
    F(
        "a-fresh5-052",
        """
c: 2 med lattes w oat milk
c: n a choc chip muffin
c: pickup for bea, card
c: oh make the lattes almond milk instead
""",
        "P P P M",
        start="Sat 08:50",
        items=[
            I(
                "latte",
                2,
                "medium",
                ["2 med lattes w oat milk", "make the lattes almond milk instead"],
                [sub("whole_milk", "almond_milk", "almond milk instead")],
            ),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Bea",
        name_q="bea",
    ),
    F(
        "a-fresh5-053",
        """
c: want to order a large margherita for tomorrow
c: pickup
""",
        "P P",
        start="Sun 13:00",
        items=[I("margherita_pizza", 1, "large", ["a large margherita"])],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tomorrow"),
        day=("tomorrow", "tomorrow"),
    ),
    F(
        "a-fresh5-054",
        """
c: 3 med drips, 2 w hazelnut
c: card
""",
        "P P",
        start="Mon 10:40",
        items=[
            I("drip_coffee", 1, "medium", ["3 med drips, 2 w hazelnut"]),
            I(
                "drip_coffee",
                2,
                "medium",
                ["3 med drips, 2 w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-055",
        """
c: Hi, a veggie burger and a coke for pickup.
c: Paying cash.
b: Got it: 1 Veggie Burger and 1 Coke, pickup, paying cash. Is that right?
c: 👍
""",
        "P P C",
        start="Tue 12:10",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="Paying cash",
        decision="confirmed",
        decision_q="👍",
    ),
    F(
        "a-fresh5-056",
        """
c: Hi, one double cheeseburger, a large fries and a chocolate milkshake delivered to 300 Union St, I'll pay by card.
""",
        "P",
        start="Wed 19:20",
        items=[
            I("cheeseburger", 1, "double", ["one double cheeseburger"]),
            I("fries", 1, "large", ["a large fries"]),
            I("milkshake", 1, "chocolate", ["a chocolate milkshake"]),
        ],
        method="delivery",
        method_q="delivered to 300 Union St",
        addr={"raw": "300 Union St", "number": "300", "street": "Union St"},
        pay="card",
        pay_q="I'll pay by card",
    ),
]
