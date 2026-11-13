"""fresh4 a-fresh4-029–056 (chats + gold by hand; see build.py)."""

from build import F, I, add, rm, sub

ENTRIES = [
    F(
        "a-fresh4-029",
        """
c: Hi, quick question unrelated to pizza.
c: Who won the World Series last year?
""",
        "S O",
        start="Sun 15:00",
    ),
    F(
        "a-fresh4-030",
        """
c: hi, i placed an order about 20 min ago for pickup under marta
c: just wondering if its ready yet?
c: no rush, thank u!
""",
        "ST ST S",
        start="Thu 09:10",
        order=False,
    ),
    F(
        "a-fresh4-031",
        """
c: hi 👋 can i pay cash when i pick up?
c: n do u give change for a 50? 💵
""",
        "PQ PQ",
        start="Mon 15:30",
    ),
    F(
        "a-fresh4-032",
        """
c: Good afternoon
c: A large Hawaiian please
c: and a medium margherita
c: for pickup
c: at 6:45
c: I'll pay cash
""",
        "S P P P P P",
        start="Tue 15:20",
        items=[
            I("hawaiian_pizza", 1, "large", ["A large Hawaiian"]),
            I("margherita_pizza", 1, "medium", ["a medium margherita"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6:45", "18:45"),
        pay="cash",
        pay_q="I'll pay cash",
        annotation="'at 6:45' at 15:20, open 12-23: 18:45.",
    ),
    F(
        "a-fresh4-033",
        """
c: Hello, I'm in town next week.
c: Do your burgers come with fries?
b: Fries are a separate side, or you can get the Cheeseburger Combo.
c: I see. Could I order 2 cheeseburger combos with fries and cokes for Nov 27 at 12:30?
c: Delievered to the Grand Plaza hotel, 210 Main St, room 418.
c: Paying by card.
""",
        "S Q P P P",
        start="Mon 14:00",
        items=[
            I(
                "cheeseburger_combo",
                2,
                None,
                ["2 cheeseburger combos with fries and cokes"],
                combo={"side": "fries", "drink": "coke"},
            ),
        ],
        method="delivery",
        method_q="Delievered to the Grand Plaza hotel",
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", 11, 27, "Nov 27"),
        addr={
            "raw": "the Grand Plaza hotel, 210 Main St, room 418",
            "number": "210",
            "street": "Main St",
            "unit": "room 418",
        },
        pay="card",
        pay_q="Paying by card",
    ),
    F(
        "a-fresh4-034",
        """
c: med oat latte
c: n a plain bagel w avocado
c: name is jo
c: cash
b: Got it, Jo: 1 medium Latte with oat milk and 1 plain Bagel with avocado, paying cash. Is that right?
c: yep
c: wait card actually
""",
        "P P P P C M",
        start="Fri 08:20",
        items=[
            I("latte", 1, "medium", ["med oat latte"], [sub("whole_milk", "oat_milk", "oat")]),
            I("bagel", 1, "plain", ["a plain bagel w avocado"], [add("avocado", "w avocado")]),
        ],
        pay="card",
        pay_q="card",
        name="Jo",
        name_q="jo",
    ),
    F(
        "a-fresh4-035",
        """
c: Hi, two large pepperoni pizzas and some pop for the office.
b: Which drinks would you like? We have Coke, Diet Coke, Sprite, Dr Pepper and iced tea.
c: Four cans of Sprite, please.
c: Deliver to 600 Commerce St, suite 300. Card.
""",
        "P P P",
        start="Wed 12:10",
        items=[
            I("pepperoni_pizza", 2, "large", ["two large pepperoni pizzas"]),
            I("sprite", 4, "can", ["Four cans of Sprite"]),
        ],
        method="delivery",
        method_q="Deliver to 600 Commerce St",
        addr={
            "raw": "600 Commerce St, suite 300",
            "number": "600",
            "street": "Commerce St",
            "unit": "suite 300",
        },
        pay="card",
        pay_q="Card",
        annotation="'some pop' is settled by the next message: the vague line is dropped.",
    ),
    F(
        "a-fresh4-036",
        """
c: hi, 2 bec on bagels n 2 med drips
c: n a breakfast burrito
c: do u have salsa?
c: pickup for dana
""",
        "P P Q P",
        start="Tue 11:00",
        items=[
            I("breakfast_sandwich", 2, "bagel", ["2 bec on bagels"]),
            I("drip_coffee", 2, "medium", ["2 med drips"]),
            I(None, 1, None, ["a breakfast burrito"], unmatched="a breakfast burrito"),
        ],
        method="pickup",
        method_q="pickup",
        name="Dana",
        name_q="dana",
        annotation="No burritos on the menu: an off-menu line (item_menu_match/off_menu), asked.",
    ),
    F(
        "a-fresh4-037",
        """
c: LARGE VEGGIE ON GLUTEN FREE CRUST AND A SPRITE
c: DELIVER TO 77 PINE ST
c: CASH
c: ACTUALY CAN WE DO IT TOMORROW AT 7 INSTEAD
""",
        "P P P M",
        start="Thu 18:30",
        items=[
            I(
                "veggie_pizza",
                1,
                "large",
                ["LARGE VEGGIE ON GLUTEN FREE CRUST"],
                [add("crust_gluten_free", "ON GLUTEN FREE CRUST")],
            ),
            I("sprite", 1, "can", ["A SPRITE"]),
        ],
        method="delivery",
        method_q="DELIVER TO 77 PINE ST",
        time=("clock_time", "AT 7", "19:00"),
        day=("tomorrow", "TOMORROW"),
        addr={"raw": "77 PINE ST", "number": "77", "street": "PINE ST"},
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh4-038",
        """
c: hjgg kkl;
""",
        "U",
        start="Mon 10:00",
    ),
    F(
        "a-fresh4-039",
        """
c: 47
""",
        "U",
        start="Wed 16:00",
    ),
    F(
        "a-fresh4-040",
        """
c: hey
c: can i get my money back for this mornings order? it was the wrong drink
""",
        "S R",
        start="Sat 11:20",
        order=False,
    ),
    F(
        "a-fresh4-041",
        """
c: a med latte n a blueberry muffin, name ines
c: actually swap the muffin for a choc croissant
""",
        "P M",
        start="Tue 14:00",
        items=[
            I("latte", 1, "medium", ["a med latte"]),
            I("croissant", 1, "chocolate", ["a choc croissant"]),
        ],
        name="Ines",
        name_q="ines",
    ),
    F(
        "a-fresh4-042",
        """
c: Hi, can I get 2 medium supremes for Thursday at 7 pm, deliverd to 45 Lake Dr?
c: I'll pay cash.
""",
        "P P",
        start="Mon 16:00",
        items=[I("supreme_pizza", 2, "medium", ["2 medium supremes"])],
        method="delivery",
        method_q="deliverd to 45 Lake Dr",
        time=("clock_time", "at 7 pm", "19:00"),
        day=("weekday", "thu", "Thursday"),
        addr={"raw": "45 Lake Dr", "number": "45", "street": "Lake Dr"},
        pay="cash",
        pay_q="I'll pay cash",
    ),
    F(
        "a-fresh4-043",
        """
c: hi
c: lg pepperoni
c: n a small cheese for the kid
c: no sauce on the kids one
c: garlic knots
c: 2 liter sprite
c: cash
c: thats all
""",
        "S P P P P P P S",
        start="Fri 17:40",
        items=[
            I("pepperoni_pizza", 1, "large", ["lg pepperoni"]),
            I(
                "cheese_pizza",
                1,
                "small",
                ["a small cheese for the kid", "no sauce on the kids one"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I("garlic_knots", 1, None, ["garlic knots"]),
            I("sprite", 1, "two_liter", ["2 liter sprite"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-044",
        """
c: hey is this the taco place on 5th
c: think i left my wallet there last nite
""",
        "O O",
        start="Sun 20:00",
    ),
    F(
        "a-fresh4-045",
        """
c: medium pepperoni
c: n a veggie
c: pickup
c: card
c: name is luca
c: make both of them large
""",
        "P P P P P M",
        start="Wed 18:10",
        items=[
            I("pepperoni_pizza", 1, "large", ["medium pepperoni", "make both of them large"]),
            I("veggie_pizza", 1, "large", ["a veggie", "make both of them large"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Luca",
        name_q="luca",
    ),
    F(
        "a-fresh4-046",
        """
c: Hi, this is my first time ordering.
c: Could I get a double cheeseburger and a chocolate shake for Saturday?
c: Delivery to 19 Elm Ct please.
c: I'll pay by card.
""",
        "S P P P",
        start="Tue 15:00",
        items=[
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
        method="delivery",
        method_q="Delivery to 19 Elm Ct",
        time=("ambiguous", "for Saturday"),
        day=("weekday", "sat", "Saturday"),
        addr={"raw": "19 Elm Ct", "number": "19", "street": "Elm Ct"},
        pay="card",
        pay_q="I'll pay by card",
    ),
    F(
        "a-fresh4-047",
        """
c: ☕️ hi
c: j
""",
        "S U",
        start="Thu 13:00",
    ),
    F(
        "a-fresh4-048",
        """
c: cb combo w rings n a sprite
c: + a choc shake
c: to 33 ash st
c: cash
""",
        "P P P P",
        start="Sat 19:30",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["cb combo w rings n a sprite"],
                combo={"side": "onion_rings", "drink": "sprite"},
            ),
            I("milkshake", 1, "chocolate", ["a choc shake"]),
        ],
        method="delivery",
        method_q="to 33 ash st",
        addr={"raw": "33 ash st", "number": "33", "street": "ash st"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-049",
        """
c: 3 lg pepperoni n 2 lg cheese to 88 park pl, card. is the cheese just mozz?
b: It's our house cheese blend. Got it: 3 large Pepperoni and 2 large Cheese Pizzas, delivered to 88 Park Pl, paying by card. Is that right?
c: ya
c: actualy drop 1 of the cheese
""",
        "P/Q C M",
        start="Sat 18:00",
        items=[
            I("pepperoni_pizza", 3, "large", ["3 lg pepperoni"]),
            I("cheese_pizza", 1, "large", ["2 lg cheese", "drop 1 of the cheese"]),
        ],
        method="delivery",
        method_q="to 88 park pl",
        addr={"raw": "88 park pl", "number": "88", "street": "park pl"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh4-050",
        """
c: Good morning.
c: I'd like a large cappuccino and an almond croissant for pickup, please.
c: My name is Harold, and I'll pay cash.
b: Thank you, Harold: 1 large Cappuccino and 1 almond Croissant, pickup, paying cash. Is that right?
c: Yes, that's correct.
c: On second thought, I'll pay by card instead.
""",
        "S P P C M",
        start="Wed 08:40",
        items=[
            I("cappuccino", 1, "large", ["a large cappuccino"]),
            I("croissant", 1, "almond", ["an almond croissant"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="I'll pay by card",
        name="Harold",
    ),
    F(
        "a-fresh4-051",
        """
c: 2 bacon burgers n a lemonade to 14 hill rd, cash 🍔 is the lemonade fresh?
b: It's our house lemonade! Got it: 2 Bacon Burgers and 1 Lemonade, delivered to 14 Hill Rd, paying cash. Is that right?
c: 👍
""",
        "P/Q C",
        start="Thu 19:15",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="to 14 hill rd",
        addr={"raw": "14 hill rd", "number": "14", "street": "hill rd"},
        pay="cash",
        pay_q="cash",
        decision="confirmed",
        decision_q="👍",
    ),
    F(
        "a-fresh4-052",
        """
c: 5 cheeseburgers, 2 with no onions 🍔 paying card
""",
        "P",
        start="Mon 12:30",
        items=[
            I("cheeseburger", 3, "single", ["5 cheeseburgers"]),
            I(
                "cheeseburger",
                2,
                "single",
                ["5 cheeseburgers", "2 with no onions"],
                [rm("onion", "no onions")],
            ),
        ],
        pay="card",
        pay_q="paying card",
    ),
    F(
        "a-fresh4-053",
        """
c: hey 👋
c: large bbq chicken n a 2 liter coke 🍕
""",
        "S P",
        start="Fri 13:30",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["large bbq chicken"]),
            I("coke", 1, "two_liter", ["a 2 liter coke"]),
        ],
    ),
    F(
        "a-fresh4-054",
        """
c: 2 MEDIUM LATTES
c: A PLAIN BAGEL WITH BUTTER
c: AND A CHOCOLATE CHIP MUFFIN
c: PICKUP FOR LIN
c: SKIP THE MUFFIN ACTUALLY
""",
        "P P P P M",
        start="Sun 09:15",
        items=[
            I("latte", 2, "medium", ["2 MEDIUM LATTES"]),
            I("bagel", 1, "plain", ["A PLAIN BAGEL WITH BUTTER"], [add("butter", "WITH BUTTER")]),
        ],
        method="pickup",
        method_q="PICKUP",
        name="Lin",
        name_q="LIN",
    ),
    F(
        "a-fresh4-055",
        """
c: 3 medium cheese pizzas, 1 w spinach, all on gluten free crust pls im celiac
c: to 410 birch ave
""",
        "P P",
        start="Tue 18:20",
        items=[
            I(
                "cheese_pizza",
                2,
                "medium",
                ["3 medium cheese pizzas", "all on gluten free crust"],
                [add("crust_gluten_free", "on gluten free crust")],
            ),
            I(
                "cheese_pizza",
                1,
                "medium",
                ["3 medium cheese pizzas", "1 w spinach", "all on gluten free crust"],
                [add("spinach", "w spinach"), add("crust_gluten_free", "on gluten free crust")],
            ),
        ],
        method="delivery",
        method_q="to 410 birch ave",
        addr={"raw": "410 birch ave", "number": "410", "street": "birch ave"},
        annotation="The gluten-free crust is for all 3 (as fresh2 014): both lines get it.",
    ),
    F(
        "a-fresh4-056",
        """
c: Good morning!
c: Do you take orders for another day? I'd like to order for Saturday.
b: Yes, we take orders up to a week ahead. What would you like?
c: Wonderful. Two large lattes and four blueberry muffins for Saturday at 9:30, please. Name is Edith.
""",
        "S D P",
        start="Mon 10:45",
        items=[
            I("latte", 2, "large", ["Two large lattes"]),
            I("muffin", 4, "blueberry", ["four blueberry muffins"]),
        ],
        time=("clock_time", "at 9:30", "09:30"),
        day=("weekday", "sat", "Saturday"),
        name="Edith",
        annotation="Asking whether they take orders for another day is a DELIVERY_QUESTION (2026-11-12 rule).",
    ),
]
