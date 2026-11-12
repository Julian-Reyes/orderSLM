"""fresh3 a-fresh3-081–110 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, sub

ENTRIES = [
    F(
        "a-fresh3-081",
        """
c: 2 LARGE CHEESE, A MEDIUM PEPPERONI AND AN ORDER OF KNOTS FOR PICKUP, CASH
c: ACTUALLY NO KNOTS
""",
        "P M",
        start="Mon 19:00",
        items=[
            I("cheese_pizza", 2, "large", ["2 LARGE CHEESE"]),
            I("pepperoni_pizza", 1, "medium", ["A MEDIUM PEPPERONI"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh3-082",
        """
c: HI, DO YOU MAKE BREAKFAST SANDWICHES ON BAGELS?
b: Yes, the breakfast sandwich comes on an English muffin, a croissant or a bagel.
c: GREAT, 3 ON BAGELS AND 3 MEDIUM COFFEES FOR SATURDAY
""",
        "Q P",
        start="Thu 13:00",
        items=[
            I("breakfast_sandwich", 3, "bagel", ["3 ON BAGELS"]),
            I("drip_coffee", 3, "medium", ["3 MEDIUM COFFEES"]),
        ],
        time=("ambiguous", "FOR SATURDAY"),
        day=("weekday", "sat", "SATURDAY"),
    ),
    F(
        "a-fresh3-083",
        """
c: WE JUST GOT OUR ORDER
c: THERE'S MUSTARD ON MY SON'S CHEESEBURGER
c: HE'S ALLERGIC TO MUSTARD, I SAID NO MUSTARD
c: HE DIDN'T EAT IT. WHAT DO WE DO?
""",
        "PR PR PR!n PR!n",
        start="Fri 19:40",
        annotation="As fresh2 053: an allergen on a received order is a food-safety problem once the allergy is said, "
        "needs_staff_now even though it wasn't eaten.",
    ),
    F(
        "a-fresh3-084",
        """
c: hi 👋 is the meat lovers really big? lol
b: It has pepperoni, sausage, ham, bacon and beef, so it's a hearty one!
c: haha ok a medium meat lovers + a can of sprite for pickup, card 💳
c: wait swap the meat lovers for a medium veggie 🥦
""",
        "Q P M",
        start="Wed 18:15",
        items=[
            I("veggie_pizza", 1, "medium", ["swap the meat lovers for a medium veggie"]),
            I("sprite", 1, "can", ["a can of sprite"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-085",
        """
c: is the knots order 6 pieces? 🧄
b: Yes, 6 garlic knots per order.
c: ok 2 orders + a large pepperoni to 23 juniper ct, cash 💵
b: Got it: 2 orders of Garlic Knots and 1 large Pepperoni Pizza, delivered to 23 Juniper Ct, paying cash. Is that right?
c: 👍
""",
        "Q P C",
        start="Sat 20:30",
        items=[
            I("garlic_knots", 2, None, ["2 orders"]),
            I("pepperoni_pizza", 1, "large", ["a large pepperoni"]),
        ],
        method="delivery",
        method_q="to 23 juniper ct",
        addr={"raw": "23 juniper ct", "number": "23", "street": "juniper ct"},
        pay="cash",
        pay_q="cash",
        decision="confirmed",
        decision_q="👍",
    ),
    F(
        "a-fresh3-086",
        """
c: 2 CHEESEBURGERS AND 2 LARGE FRIES
c: TO 990 ELM ST
c: CARD
""",
        "P P P",
        start="Tue 20:00",
        items=[
            I("cheeseburger", 2, None, ["2 CHEESEBURGERS"]),
            I("fries", 2, "large", ["2 LARGE FRIES"]),
        ],
        method="delivery",
        method_q="TO 990 ELM ST",
        addr={"raw": "990 ELM ST", "number": "990", "street": "ELM ST"},
        pay="card",
        pay_q="CARD",
    ),
    F(
        "a-fresh3-087",
        """
c: hi 🌙 can i get the coffee n pastry deal
c: w a drip coffee but large pls ☕
c: n an almond croissant 🥐
c: pickup for sam
""",
        "P P P P",
        start="Mon 07:05",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["the coffee n pastry deal", "w a drip coffee but large", "an almond croissant"],
                combo={"drink": ("drip_coffee", "large"), "pastry": ("croissant", "almond")},
            )
        ],
        method="pickup",
        method_q="pickup",
        name="Sam",
        name_q="sam",
    ),
    F(
        "a-fresh3-088",
        """
c: hello
c: 3 large cheese pizzas please
c: one of them on thin crust
c: delivered to 412 dover st, card
""",
        "S P P P",
        start="Sun 17:10",
        items=[
            I("cheese_pizza", 2, "large", ["3 large cheese pizzas"]),
            I(
                "cheese_pizza",
                1,
                "large",
                ["3 large cheese pizzas", "one of them on thin crust"],
                [add("crust_thin", "on thin crust")],
            ),
        ],
        method="delivery",
        method_q="delivered to 412 dover st",
        addr={"raw": "412 dover st", "number": "412", "street": "dover st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-089",
        """
c: hi ☕ a medium latte w hazelnut n a choc chip muffin for pickup, name ines
c: i already paid thru the app 🙏
""",
        "P PC",
        start="Wed 08:45",
        items=[
            I("latte", 1, "medium", ["a medium latte w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay_q="i already paid",
        paid=True,
        name="Ines",
        name_q="ines",
    ),
    F(
        "a-fresh3-090",
        """
c: hi 👋 we're arriving thursday nov 19, could we get 2 bacon burgers n 2 cokes delivered to the harbor inn, 400 front st, room 210, at 8pm that day? 🏨
""",
        "P",
        start="Mon 15:00",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        method="delivery",
        method_q="delivered to the harbor inn",
        time=("clock_time", "at 8pm", "20:00"),
        day=("date", 11, 19, "nov 19"),
        addr={
            "raw": "the harbor inn, 400 front st, room 210",
            "number": "400",
            "street": "front st",
            "unit": "room 210",
            "reference": "the harbor inn",
        },
        annotation="The weekday and the date name the same day; the date is labeled (kind date).",
    ),
    F(
        "a-fresh3-091",
        """
c: Hi, I'd like a medium margherita for pickup.
c: And something cheesy to snack on while we wait.
b: For sides we have Garlic Knots (6 per order) and Breadsticks (4 per order). Which would you like?
c: The breadsticks, one order. I'll pay cash.
""",
        "P P P",
        start="Fri 17:00",
        items=[
            I("margherita_pizza", 1, "medium", ["a medium margherita"]),
            I("breadsticks", 1, None, ["The breadsticks, one order"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="pay cash",
    ),
    F(
        "a-fresh3-092",
        """
c: hey can i get a cheeseburger, a large fries n a burrito
c: deliver to 72 vine st, card
""",
        "P P",
        start="Thu 12:30",
        items=[
            I("cheeseburger", 1, None, ["a cheeseburger"]),
            I("fries", 1, "large", ["a large fries"]),
            I(None, 1, None, ["a burrito"], unmatched="a burrito"),
        ],
        method="delivery",
        method_q="deliver to 72 vine st",
        addr={"raw": "72 vine st", "number": "72", "street": "vine st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-093",
        """
c: a small latte with oat milk please
c: pickup for ruth, cash
c: oh, almond milk instead of oat, sorry
""",
        "P P M",
        start="Tue 10:20",
        items=[
            I(
                "latte",
                1,
                "small",
                ["a small latte with oat milk", "almond milk instead of oat"],
                [sub("whole_milk", "almond_milk", "almond milk instead of oat")],
            )
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ruth",
        name_q="ruth",
    ),
    F(
        "a-fresh3-094",
        """
c: Do you have hazelnut syrup?
b: We do!
c: Then a medium latte with hazelnut for pickup on Monday at 7:40, under Paul. Card.
""",
        "Q P",
        start="Thu 09:30",
        items=[
            I(
                "latte",
                1,
                "medium",
                ["a medium latte with hazelnut"],
                [add("hazelnut_syrup", "with hazelnut")],
            )
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 7:40", "07:40"),
        day=("weekday", "mon", "Monday"),
        pay="card",
        pay_q="Card",
        name="Paul",
    ),
    F(
        "a-fresh3-095",
        """
c: hey can i get a large half pepperoni half hawaiian
c: n a 2 liter sprite
c: paying cash
""",
        "P P P",
        start="Wed 22:15",
        items=[
            I(
                None,
                1,
                "large",
                ["a large half pepperoni half hawaiian"],
                halves=[("pepperoni_pizza", []), ("hawaiian_pizza", [])],
            ),
            I("sprite", 1, "two_liter", ["a 2 liter sprite"]),
        ],
        pay="cash",
        pay_q="paying cash",
    ),
    F(
        "a-fresh3-096",
        """
c: yo
c: a few cheeseburgers
c: n 2 cokes
c: pickup
""",
        "S P P P",
        start="Sat 14:20",
        items=[
            I("cheeseburger", None, None, ["a few cheeseburgers"]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    F(
        "a-fresh3-097",
        """
c: 2 bacon burgers n a chocolate shake
c: n a regular fries
c: nah skip the fries
""",
        "P P M",
        start="Mon 17:50",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
    ),
    F(
        "a-fresh3-098",
        """
c: hi 🌙 an everything bagel w lox n cream cheese, plus a large americano, paying card
""",
        "P",
        start="Tue 07:10",
        items=[
            I(
                "bagel",
                1,
                "everything",
                ["an everything bagel w lox n cream cheese"],
                [offmod("w lox"), add("cream_cheese", "cream cheese")],
            ),
            I("americano", 1, "large", ["a large americano"]),
        ],
        pay="card",
        pay_q="paying card",
    ),
    F(
        "a-fresh3-099",
        """
c: hey
c: just picked up my order n its a pepperoni, i ordered a veggie
c: can i get my money back
""",
        "S PR R",
        start="Fri 21:30",
    ),
    F(
        "a-fresh3-100",
        """
c: can i preorder for sunday? 🍕
b: Yes! What would you like?
c: 2 lg bbq chicken sunday at 5 to 221 spruce ave, card 💳
""",
        "D P",
        start="Thu 20:00",
        items=[I("bbq_chicken_pizza", 2, "large", ["2 lg bbq chicken"])],
        method="delivery",
        method_q="to 221 spruce ave",
        time=("clock_time", "at 5", "17:00"),
        day=("weekday", "sun", "sunday"),
        addr={"raw": "221 spruce ave", "number": "221", "street": "spruce ave"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-101",
        """
c: HI, FIRST TIME ORDERING
c: CAN I GET A CHEESEBURGER COMBO WITH FRIES AND A COKE
c: AND A STRAWBERRY SHAKE
c: DELIVER TO 45 HOLLIS ST, I'LL PAY CASH
""",
        "S P P P",
        start="Wed 18:30",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["A CHEESEBURGER COMBO WITH FRIES AND A COKE"],
                combo={"side": "fries", "drink": "coke"},
            ),
            I("milkshake", 1, "strawberry", ["A STRAWBERRY SHAKE"]),
        ],
        method="delivery",
        method_q="DELIVER TO 45 HOLLIS ST",
        addr={"raw": "45 HOLLIS ST", "number": "45", "street": "HOLLIS ST"},
        pay="cash",
        pay_q="PAY CASH",
    ),
    F(
        "a-fresh3-102",
        """
c: hey ☕ a large americano n a croissant, do u take apple pay?
b: We take card or cash.
c: ok card then 🙂 pickup for zoe
""",
        "P/PQ P",
        start="Thu 14:00",
        items=[
            I("americano", 1, "large", ["a large americano"]),
            I("croissant", 1, None, ["a croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Zoe",
        name_q="zoe",
    ),
    F(
        "a-fresh3-103",
        """
c: hi
c: is the almond croissant sweet
b: A little sweet, it's filled with almond cream.
c: ok 4 almond croissants
c: n 4 medium lattes
""",
        "S Q P P",
        start="Mon 11:50",
        items=[
            I("croissant", 4, "almond", ["4 almond croissants"]),
            I("latte", 4, "medium", ["4 medium lattes"]),
        ],
    ),
    F(
        "a-fresh3-104",
        """
c: hello
c: i would like to order for wednesday please
c: one large veggie pizza
c: and one order of breadsticks
c: i will pick it up at 5:30, thank you
""",
        "S P P P P",
        start="Sun 14:00",
        items=[
            I("veggie_pizza", 1, "large", ["one large veggie pizza"]),
            I("breadsticks", 1, None, ["one order of breadsticks"]),
        ],
        method="pickup",
        method_q="pick it up",
        time=("clock_time", "at 5:30", "17:30"),
        day=("weekday", "wed", "wednesday"),
    ),
    F(
        "a-fresh3-105",
        """
c: random q
c: who was the first president
c: of the us lol
""",
        "S O O",
        start="Tue 16:30",
    ),
    F(
        "a-fresh3-106",
        """
c: what sizes do your lattes come in
b: Small 8 oz, medium 12 oz or large 16 oz.
c: one of the bigger ones then please, for pickup, name is ed
""",
        "Q P",
        start="Fri 10:00",
        items=[I("latte", 1, None, ["one of the bigger ones"], flag="item_variant")],
        method="pickup",
        method_q="for pickup",
        name="Ed",
        name_q="ed",
        annotation="'one of the bigger ones' fits medium or large: the size is stated unclearly, asked.",
    ),
    F(
        "a-fresh3-107",
        """
c: Hi, are you hiring? I'd like to apply for a cashier job.
""",
        "O",
        start="Wed 15:00",
    ),
    F(
        "a-fresh3-108",
        """
c: Hi, a single cheeseburger and a lemonade delivered to 61 Easton Rd.
c: Paying by card.
c: Actually, make the cheeseburger a double.
""",
        "P P M",
        start="Thu 21:15",
        items=[
            I("cheeseburger", 1, "double", ["a single cheeseburger", "make the cheeseburger a double"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="delivered to 61 Easton Rd",
        addr={"raw": "61 Easton Rd", "number": "61", "street": "Easton Rd"},
        pay="card",
        pay_q="Paying by card",
        annotation="Corner Patty has no milk or crust; the patty size plays that part.",
    ),
    F(
        "a-fresh3-109",
        """
c: hi 👋 for tomorrow at 11:45: 5 breakfast sandwiches n 5 medium coffees for pickup, name is lucia, card 💳
""",
        "P",
        start="Tue 11:00",
        items=[
            I("breakfast_sandwich", 5, None, ["5 breakfast sandwiches"]),
            I("drip_coffee", 5, "medium", ["5 medium coffees"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 11:45", "11:45"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Lucia",
        name_q="lucia",
    ),
    F(
        "a-fresh3-110",
        """
c: hey 👋 is this the sushi place on main st? 🍣
""",
        "O",
        start="Sat 18:00",
    ),
]
