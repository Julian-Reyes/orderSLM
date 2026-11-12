"""t6 entries 0131–0140 (chats + labels by hand; see build.py)."""

from build import I, X, add

ENTRIES = [
    X(
        "syn-t6-0131",
        """
c: Hi, I'd like 3 double cheeseburgers, a chocolate milkshake, a Sprite and a veggie burger with ketchup.
c: Delivery to 6761 Fulton Ct, above the bakery, at 7:15.
c: I'll pay by card.
c: Actually, please remove the veggie burger.
""",
        "P P P M",
        items=[
            I("cheeseburger", 3, "double", ["3 double cheeseburgers"]),
            I("milkshake", 1, "chocolate", ["a chocolate milkshake"]),
            I("sprite", 1, None, ["a Sprite"]),
        ],
        method="delivery",
        method_q="Delivery to 6761 Fulton Ct",
        time=("clock_time", "at 7:15", "19:15"),
        addr={
            "raw": "6761 Fulton Ct, above the bakery",
            "number": "6761",
            "street": "Fulton Ct",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0132",
        """
c: hey
c: personal veggie thin crust
c: + a sprite
c: thats for thursday
""",
        "S P P P",
        items=[
            I(
                "veggie_pizza",
                1,
                "personal",
                ["personal veggie thin crust"],
                [add("crust_thin", "thin crust")],
            ),
            I("sprite", 1, None, ["a sprite"]),
        ],
        time=("ambiguous", "for thursday"),
        day=("weekday", "thu", "thursday"),
    ),
    X(
        "syn-t6-0133",
        """
c: hi 🙂 a choc chip muffin, a medium hot chocolate n one of those 😋 card pls
""",
        "P",
        items=[
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
            I("hot_chocolate", 1, "medium", ["a medium hot chocolate"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0134",
        """
c: hi
c: 2 pepperonis thin crust
c: an iced tea
c: n that thing from before
c: pickup
c: ben, card
""",
        "S P P P P P",
        items=[
            I("pepperoni_pizza", 2, None, ["2 pepperonis thin crust"], [add("crust_thin", "thin crust")]),
            I("iced_tea", 1, None, ["an iced tea"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0135",
        """
c: lg americano w skim milk
c: n 2 coffees
c: card
c: wait no coffees, just the americano
""",
        "P P P M",
        items=[I("americano", 1, "large", ["lg americano w skim milk"], [add("skim_milk", "w skim milk")])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0136",
        """
c: 3 coffee n pastry deals
c: w drip coffee n a croissant each
c: plus 4 small coffees on the side
c: pickup, maya, card
""",
        "P P P P",
        items=[
            I(
                "coffee_pastry_combo",
                3,
                None,
                ["3 coffee n pastry deals", "w drip coffee n a croissant each"],
                combo={"drink": "drip_coffee", "pastry": "croissant"},
            ),
            I("drip_coffee", 4, "small", ["4 small coffees"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t6-0137",
        """
c: hey there
c: 4 cokes for friday at 5:30
""",
        "S P",
        items=[I("coke", 4, None, ["4 cokes"])],
        time=("clock_time", "at 5:30", "17:30"),
        day=("weekday", "fri", "friday"),
    ),
    X(
        "syn-t6-0138",
        """
c: AN ORDER OF BREADSTICKS FOR TOMORROW, PAYING CASH
""",
        "P",
        items=[I("breadsticks", 1, None, ["AN ORDER OF BREADSTICKS"])],
        time=("ambiguous", "FOR TOMORROW"),
        day=("tomorrow", "TOMORROW"),
        pay="cash",
        pay_q="PAYING CASH",
    ),
    X(
        "syn-t6-0139",
        """
c: hey same as last time pls
b: Sorry, I can't see past orders here. What would you like?
c: oh. 2 xl supremes w jalapenos, an xl cheese, 2 iced teas n 2 cans of dr pepper
c: deliver to 20 chestnut ave next to the laundromat in 45 min, card
""",
        "P P P",
        items=[
            I(
                "supreme_pizza",
                2,
                "extra_large",
                ["2 xl supremes w jalapenos"],
                [add("jalapenos", "w jalapenos")],
            ),
            I("cheese_pizza", 1, "extra_large", ["an xl cheese"]),
            I("iced_tea", 2, None, ["2 iced teas"]),
            I("dr_pepper", 2, "can", ["2 cans of dr pepper"]),
        ],
        method="delivery",
        method_q="deliver to 20 chestnut ave",
        time=("relative", "in 45 min", None),
        addr={
            "raw": "20 chestnut ave next to the laundromat",
            "number": "20",
            "street": "chestnut ave",
            "reference": "next to the laundromat",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0140",
        """
c: 2 liter sprite
c: pickup asap
c: rosa, card
b: Got it, Rosa: 1 Sprite 2-liter for pickup as soon as possible, paying by card. Is that right?
c: ya
c: actually swap the sprite for a medium pepperoni w ham
""",
        "P P P C M",
        items=[I("pepperoni_pizza", 1, "medium", ["a medium pepperoni w ham"], [add("ham", "w ham")])],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
]
