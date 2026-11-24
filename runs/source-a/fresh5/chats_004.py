"""fresh5 a-fresh5-085–110 (chats + gold by hand; see build.py)."""

from build import F, I, offmod, rm

ENTRIES = [
    F(
        "a-fresh5-085",
        """
c: yo
c: one of the big burgers
c: n a coke
""",
        "S P P",
        start="Thu 13:00",
        items=[
            I(None, 1, None, ["one of the big burgers"], unmatched="the big burgers", flag="item_menu_match"),
            I("coke", 1, None, ["a coke"]),
        ],
        annotation="'the big burgers' could be the double cheeseburger or the bacon burger: unclear item, asked.",
    ),
    F(
        "a-fresh5-086",
        """
c: Hi, a medium latte and a blueberry muffin for pickup.
c: The name is Cy.
c: Card, please.
c: Actually, I've changed my mind, please cancel the order.
""",
        "P P P X",
        start="Fri 09:50",
        items=[
            I("latte", 1, "medium", ["a medium latte"]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="Card",
        name="Cy",
        name_q="Cy",
        decision="cancelled",
        decision_q="cancel the order",
    ),
    F(
        "a-fresh5-087",
        """
c: large pepperoni
c: a small margherita
c: n breadsticks
c: pickup, cash
c: no breadsticks actually
""",
        "P P P P M",
        start="Sat 17:10",
        items=[
            I("pepperoni_pizza", 1, "large", ["large pepperoni"]),
            I("margherita_pizza", 1, "small", ["a small margherita"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-088",
        """
c: hhhhgggfffbbb
""",
        "U",
        start="Sun 16:30",
    ),
    F(
        "a-fresh5-089",
        """
c: xl pepperoni
c: medium veggie no onions
c: 2 cans of coke
c: 330 elm st apt 7
c: card
""",
        "P P P P P",
        start="Mon 19:30",
        items=[
            I("pepperoni_pizza", 1, "extra_large", ["xl pepperoni"]),
            I("veggie_pizza", 1, "medium", ["medium veggie no onions"], [rm("onions", "no onions")]),
            I("coke", 2, "can", ["2 cans of coke"]),
        ],
        method="delivery",
        method_q="330 elm st apt 7",
        addr={"raw": "330 elm st apt 7", "number": "330", "street": "elm st", "unit": "apt 7"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-090",
        """
c: hi 😊 2 bagels, 1 sesame 1 plain, n a med drip for pickup at 11
c: name is mo, card 💳
c: oops wrong day, can it be for thursday at 11? 🙏
c: thx!
""",
        "P P M S",
        start="Tue 08:00",
        items=[
            I("bagel", 1, "sesame", ["2 bagels, 1 sesame 1 plain"]),
            I("bagel", 1, "plain", ["2 bagels, 1 sesame 1 plain"]),
            I("drip_coffee", 1, "medium", ["a med drip"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 11", "11:00"),
        day=("weekday", "thu", "thursday"),
        pay="card",
        pay_q="card",
        name="Mo",
        name_q="mo",
        annotation="Moved from today to Thursday at 11 before any confirmation: MODIFY_ORDER.",
    ),
    F(
        "a-fresh5-091",
        """
c: LARGE SUPREME
c: PICKUP
c: CASH
""",
        "P P P",
        start="Wed 18:00",
        items=[I("supreme_pizza", 1, "large", ["LARGE SUPREME"])],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh5-092",
        """
c: hey
c: can i get a few medium cheese pizzas
""",
        "S P",
        start="Thu 19:20",
        items=[I("cheese_pizza", None, "medium", ["a few medium cheese pizzas"])],
    ),
    F(
        "a-fresh5-093",
        """
c: Hi, my son has a severe tree nut allergy.
c: Can I speak to someone about how your pastries are made?
c: I'd rather talk to a person about it.
""",
        "HU HU HU",
        start="Fri 08:30",
        order=False,
    ),
    F(
        "a-fresh5-094",
        """
c: HELLO
c: 2 OF YOUR BIGGEST BURGERS AND 2 LARGE FRIES TO 81 PROSPECT ST
""",
        "S P",
        start="Sat 18:40",
        items=[
            I(
                None,
                2,
                None,
                ["2 OF YOUR BIGGEST BURGERS"],
                unmatched="YOUR BIGGEST BURGERS",
                flag="item_menu_match",
            ),
            I("fries", 2, "large", ["2 LARGE FRIES"]),
        ],
        method="delivery",
        method_q="TO 81 PROSPECT ST",
        addr={"raw": "81 PROSPECT ST", "number": "81", "street": "PROSPECT ST"},
        annotation="The double cheeseburger and the bacon burger are both the biggest: unclear item, asked.",
    ),
    F(
        "a-fresh5-095",
        """
c: HI
c: WE WANT TO ORDER FOR SATURDAY
c: 3 LARGE PEPPERONI
c: AND 2 ORDERS OF GARLIC KNOTS
""",
        "S P P P",
        start="Wed 15:30",
        items=[
            I("pepperoni_pizza", 3, "large", ["3 LARGE PEPPERONI"]),
            I("garlic_knots", 2, None, ["2 ORDERS OF GARLIC KNOTS"]),
        ],
        time=("ambiguous", "FOR SATURDAY"),
        day=("weekday", "sat", "SATURDAY"),
    ),
    F(
        "a-fresh5-096",
        """
c: 3 VEGGIE BURGERS AND 3 SPRITES TO 12 BIRCH ST, CARD
c: SORRY MAKE THAT 4 VEGGIE BURGERS
""",
        "P M",
        start="Thu 12:15",
        items=[
            I("veggie_burger", 4, None, ["3 VEGGIE BURGERS", "MAKE THAT 4 VEGGIE BURGERS"]),
            I("sprite", 3, None, ["3 SPRITES"]),
        ],
        method="delivery",
        method_q="TO 12 BIRCH ST",
        addr={"raw": "12 BIRCH ST", "number": "12", "street": "BIRCH ST"},
        pay="card",
        pay_q="CARD",
    ),
    F(
        "a-fresh5-097",
        """
c: can i preorder for friday morning?
b: Yes, you can order up to a week ahead!
c: ok
c: 6 croissants, 3 plain 3 chocolate
c: at 7:30
c: card
""",
        "D S P P P",
        start="Mon 10:00",
        items=[
            I("croissant", 3, "plain", ["6 croissants, 3 plain 3 chocolate"]),
            I("croissant", 3, "chocolate", ["6 croissants, 3 plain 3 chocolate"]),
        ],
        time=("clock_time", "at 7:30", "07:30"),
        day=("weekday", "fri", "friday"),
        pay="card",
        pay_q="card",
        annotation="The day is only in the question about ordering ahead; the order that follows is for it.",
    ),
    F(
        "a-fresh5-098",
        """
c: Hi, what's the most popular thing on your menu?
""",
        "Q",
        start="Tue 07:40",
    ),
    F(
        "a-fresh5-099",
        """
c: Hi, do your breadsticks come with marinara?
b: Yes, every order comes with marinara.
c: Great, some breadsticks and a large cheese pizza delivered to 40 Glenwood Ave, please.
""",
        "Q P",
        start="Wed 18:50",
        items=[
            I("breadsticks", None, None, ["some breadsticks"]),
            I("cheese_pizza", 1, "large", ["a large cheese pizza"]),
        ],
        method="delivery",
        method_q="delivered to 40 Glenwood Ave",
        addr={"raw": "40 Glenwood Ave", "number": "40", "street": "Glenwood Ave"},
    ),
    F(
        "a-fresh5-100",
        """
c: Thank you, dinner was delicious tonight. The fries were perfect.
""",
        "S",
        start="Thu 21:00",
    ),
    F(
        "a-fresh5-101",
        """
c: hi 😕 i ordered an almond croissant but got a plain one
""",
        "PR",
        start="Fri 10:10",
        order=False,
    ),
    F(
        "a-fresh5-102",
        """
c: bacon burger w chili 🌶️
c: n a lemonade
c: to 77 sunset blvd, cash 💵
""",
        "P P P",
        start="Sat 19:50",
        items=[
            I("bacon_burger", 1, None, ["bacon burger w chili"], [offmod("w chili")]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="to 77 sunset blvd",
        addr={"raw": "77 sunset blvd", "number": "77", "street": "sunset blvd"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-103",
        """
c: lg cap n a choc croissant
c: pickup for flo, card
""",
        "P P",
        start="Sun 08:30",
        items=[
            I("cappuccino", 1, "large", ["lg cap"]),
            I("croissant", 1, "chocolate", ["a choc croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Flo",
        name_q="flo",
    ),
    F(
        "a-fresh5-104",
        """
c: Hi, a cheeseburger and something fizzy to drink, for pickup.
b: We have Coke and Sprite. Which would you like?
c: Sprite, please. Paying cash.
""",
        "P P",
        start="Mon 13:10",
        items=[
            I("cheeseburger", 1, None, ["a cheeseburger"]),
            I("sprite", 1, None, ["Sprite, please"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="Paying cash",
        annotation="'something fizzy' is settled by the next message: the vague line is dropped.",
    ),
    F(
        "a-fresh5-105",
        """
c: hey
c: large bbq chicken
c: n a can of iced tea
c: pickup
c: at 8
c: card
""",
        "S P P P P P",
        start="Tue 15:00",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["large bbq chicken"]),
            I("iced_tea", 1, "can", ["a can of iced tea"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "20:00"),
        pay="card",
        pay_q="card",
        annotation="'at 8' at 15:00, open 12-23: 20:00.",
    ),
    F(
        "a-fresh5-106",
        """
c: 3 cheeseburgers
c: 2 shakes
b: Sure! Which flavors for the milkshakes?
c: 1 vanilla 1 strawberry
c: 3 fries n 3 lemonades
c: pickup
""",
        "P P P P P",
        start="Wed 12:30",
        items=[
            I("cheeseburger", 3, None, ["3 cheeseburgers"]),
            I("milkshake", 1, "vanilla", ["2 shakes", "1 vanilla 1 strawberry"]),
            I("milkshake", 1, "strawberry", ["2 shakes", "1 vanilla 1 strawberry"]),
            I("fries", 3, None, ["3 fries"]),
            I("lemonade", 3, None, ["3 lemonades"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    F(
        "a-fresh5-107",
        """
c: hi
c: 2 medium margheritas
c: pickup
c: 6:45
c: name ty
c: cash
""",
        "S P P P P P",
        start="Thu 14:20",
        items=[I("margherita_pizza", 2, "medium", ["2 medium margheritas"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "6:45", "18:45"),
        pay="cash",
        pay_q="cash",
        name="Ty",
        name_q="ty",
        annotation="'6:45' at 14:20, open 12-23: 18:45.",
    ),
    F(
        "a-fresh5-108",
        """
c: hey big order
c: 2 xl pepperoni, a large veggie, a medium meat lovers, 3 orders of knots n 2 two liter sprites
c: pickup
c: at 7
c: card
c: name is rio
""",
        "P P P P P P",
        start="Fri 16:40",
        items=[
            I("pepperoni_pizza", 2, "extra_large", ["2 xl pepperoni"]),
            I("veggie_pizza", 1, "large", ["a large veggie"]),
            I("meat_lovers_pizza", 1, "medium", ["a medium meat lovers"]),
            I("garlic_knots", 3, None, ["3 orders of knots"]),
            I("sprite", 2, "two_liter", ["2 two liter sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "19:00"),
        pay="card",
        pay_q="card",
        name="Rio",
        name_q="rio",
    ),
    F(
        "a-fresh5-109",
        """
c: 2 med lattes for pickup, name is al
b: Got it, Al: 2 medium lattes for pickup. How would you like to pay?
c: oh i already paid on ur website
c: got the confirmation email
""",
        "P PC PC",
        start="Sat 09:00",
        items=[I("latte", 2, "medium", ["2 med lattes"])],
        method="pickup",
        method_q="for pickup",
        pay_q="i already paid on ur website",
        paid=True,
        name="Al",
        name_q="al",
        annotation="A website is a channel, not a method: payment unknown, customer_claims_paid (unverified).",
    ),
    F(
        "a-fresh5-110",
        """
c: Hi there!
c: Could I order two bacon burgers and an order of onion rings for Friday at 6, delivered to 14 Willow Ln?
""",
        "S P",
        start="Sun 15:00",
        items=[
            I("bacon_burger", 2, None, ["two bacon burgers"]),
            I("onion_rings", 1, None, ["an order of onion rings"]),
        ],
        method="delivery",
        method_q="delivered to 14 Willow Ln",
        addr={"raw": "14 Willow Ln", "number": "14", "street": "Willow Ln"},
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "fri", "Friday"),
    ),
]
