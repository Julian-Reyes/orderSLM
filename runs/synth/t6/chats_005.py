"""t6 entries 0041–0050 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0041",
        """
c: hey hey
c: wanna order for tmrw
c: 1 onion rings
c: a cheeseburger w mayo
c: 2 bacon burgers no pickles
c: pickup, card
""",
        "S P P P P P",
        items=[
            I("onion_rings", 1, None, ["1 onion rings"]),
            I("cheeseburger", 1, None, ["a cheeseburger w mayo"], [add("mayo", "w mayo")]),
            I("bacon_burger", 2, None, ["2 bacon burgers no pickles"], [rm("pickle", "no pickles")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for tmrw"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0042",
        """
c: DO YOU HAVE ALMOND CROISSANTS TODAY?
b: Yes, we do!
c: GREAT, SOME ALMOND CROISSANTS AND 2 SMALL CAPPUCCINOS. CARD
""",
        "Q P",
        items=[
            I("croissant", None, "almond", ["SOME ALMOND CROISSANTS"]),
            I("cappuccino", 2, "small", ["2 SMALL CAPPUCCINOS"]),
        ],
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0043",
        """
c: Hello there!
c: Can I get a personal supreme without onions but with spinach, plus a can of Dr Pepper and a 20 oz Coke?
c: Pickup in 25 minutes, name Eli, cash.
""",
        "S P P",
        items=[
            I(
                "supreme_pizza",
                1,
                "personal",
                ["a personal supreme without onions but with spinach"],
                [rm("onions", "without onions"), add("spinach", "with spinach")],
            ),
            I("dr_pepper", 1, "can", ["a can of Dr Pepper"]),
            I("coke", 1, "bottle_20oz", ["a 20 oz Coke"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("relative", "in 25 minutes", None),
        pay="cash",
        pay_q="cash",
        name="Eli",
    ),
    X(
        "syn-t6-0044",
        """
c: hi can i get a breakfast sandwich on a bagel n 3 coffees w almond milk for pickup at 1
c: name eli, card
c: actually can u make it tomorrow morning at 8 instead, sorry
""",
        "P P M",
        items=[
            I("breakfast_sandwich", 1, "bagel", ["a breakfast sandwich on a bagel"]),
            I("drip_coffee", 3, None, ["3 coffees w almond milk"], [add("almond_milk", "w almond milk")]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8", "08:00"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t6-0045",
        """
c: morning
c: lg latte w caramel
c: a coffee w vanilla
c: n a large cappuccino
c: oh n one of those too
c: pickup at 10:15, jordan
""",
        "S P P P P P",
        items=[
            I("latte", 1, "large", ["lg latte w caramel"], [add("caramel_syrup", "w caramel")]),
            I("drip_coffee", 1, None, ["a coffee w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("cappuccino", 1, "large", ["a large cappuccino"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10:15", "10:15"),
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t6-0046",
        """
c: hi 👋 do u take orders for tomorrow?
b: Yes! We take orders up to a week ahead.
c: awesome 🙌 2 bacon burgers, 2 fries n a coke for tomorrow at 7pm, deliver to 89 hollis blvd, card 💳
""",
        "D P",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("fries", 2, None, ["2 fries"]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="deliver to 89 hollis blvd",
        time=("clock_time", "at 7pm", "19:00"),
        day=("tomorrow", "tomorrow"),
        addr={"raw": "89 hollis blvd", "number": "89", "street": "hollis blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0047",
        """
c: HI, I NEED TO ORDER FOR NOVEMBER 2ND
c: 3 BREAKFAST SANDWICHES, NO BACON ON ANY OF THEM
c: AT 9 AM PLEASE
""",
        "P P P",
        items=[I("breakfast_sandwich", 3, None, ["3 BREAKFAST SANDWICHES"], [rm("bacon", "NO BACON")])],
        time=("clock_time", "AT 9 AM", "09:00"),
        day=("date", 11, 2, "NOVEMBER 2ND"),
    ),
    X(
        "syn-t6-0048",
        """
c: 3 XL BBQ CHICKEN WITH ANCHOVIES, 2 DR PEPPERS AND 2 PERSONAL MARGHERITAS ON GLUTEN FREE CRUST
c: AND THE ONE I ALWAYS GET. DELIVER TO 968 MISSION CT #13A
""",
        "P P",
        items=[
            I(
                "bbq_chicken_pizza",
                3,
                "extra_large",
                ["3 XL BBQ CHICKEN WITH ANCHOVIES"],
                [add("anchovies", "WITH ANCHOVIES")],
            ),
            I("dr_pepper", 2, None, ["2 DR PEPPERS"]),
            I(
                "margherita_pizza",
                2,
                "personal",
                ["2 PERSONAL MARGHERITAS ON GLUTEN FREE CRUST"],
                [add("crust_gluten_free", "ON GLUTEN FREE CRUST")],
            ),
            I(
                None,
                1,
                None,
                ["THE ONE I ALWAYS GET"],
                unmatched="THE ONE I ALWAYS GET",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="DELIVER TO 968 MISSION CT #13A",
        addr={"raw": "968 MISSION CT #13A", "number": "968", "street": "MISSION CT", "unit": "#13A"},
    ),
    X(
        "syn-t6-0049",
        """
c: hi
c: 1 hot chocolate
c: 1 breakfast sandwich w avocado
c: 3 medium americanos w caramel
c: do u have oat milk
b: Yes, we have oat milk and almond milk.
c: ok 2 medium lattes w oat milk then
c: card
""",
        "S P P P Q P P",
        items=[
            I("hot_chocolate", 1, None, ["1 hot chocolate"]),
            I(
                "breakfast_sandwich",
                1,
                None,
                ["1 breakfast sandwich w avocado"],
                [add("avocado", "w avocado")],
            ),
            I(
                "americano",
                3,
                "medium",
                ["3 medium americanos w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
            I(
                "latte",
                2,
                "medium",
                ["2 medium lattes w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0050",
        """
c: Hi there.
c: Do you sell 2 liter bottles of Sprite?
b: Yes, Sprite comes in a can, a 20 oz bottle or a 2-liter.
c: Great. I'd like 3 two liter Sprites for a party on Sunday.
c: I'll pick them up at 3 and pay by card.
""",
        "S Q P P",
        items=[I("sprite", 3, "two_liter", ["3 two liter Sprites"])],
        method="pickup",
        method_q="pick them up",
        time=("clock_time", "at 3", "15:00"),
        day=("weekday", "sun", "Sunday"),
        pay="card",
        pay_q="pay by card",
    ),
]
