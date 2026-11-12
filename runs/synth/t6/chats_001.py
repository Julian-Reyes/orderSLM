"""t6 entries 0001–0010 (chats + labels by hand; see build.py)."""

from build import I, X, add

ENTRIES = [
    X(
        "syn-t6-0001",
        """
c: 2 onion rings n a cheeseburger + sprite
c: for tmrw at 6 pls
c: deliver to 25 elm st unit 7, card
""",
        "P P P",
        items=[
            I("onion_rings", 2, None, ["2 onion rings"]),
            I("cheeseburger", 1, None, ["a cheeseburger"]),
            I("sprite", 1, None, ["sprite"]),
        ],
        method="delivery",
        method_q="deliver to 25 elm st",
        time=("clock_time", "at 6", "18:00"),
        day=("tomorrow", "tmrw"),
        addr={"raw": "25 elm st unit 7", "number": "25", "street": "elm st", "unit": "unit 7"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0002",
        """
c: HI CAN I GET A PERSONAL SUPREME ON GLUTEN FREE CRUST, 2 ORDERS OF BREADSTICKS AND A CAN OF DR PEPPER DELIVERED TO 715 MAGNOLIA LN. PAYING CARD
c: DOES THE SUPREME HAVE OLIVES ON IT?
b: Yes, the Supreme has pepperoni, sausage, green peppers, onions, olives and mushrooms.
c: OK THATS FINE. ACTUALLY CAN YOU MAKE IT FOR TOMORROW AT 7 INSTEAD OF TONIGHT
""",
        "P Q M",
        items=[
            I(
                "supreme_pizza",
                1,
                "personal",
                ["A PERSONAL SUPREME ON GLUTEN FREE CRUST"],
                [add("crust_gluten_free", "ON GLUTEN FREE CRUST")],
            ),
            I("breadsticks", 2, None, ["2 ORDERS OF BREADSTICKS"]),
            I("dr_pepper", 1, "can", ["A CAN OF DR PEPPER"]),
        ],
        method="delivery",
        method_q="DELIVERED TO 715 MAGNOLIA LN",
        time=("clock_time", "AT 7", "19:00"),
        day=("tomorrow", "TOMORROW"),
        addr={"raw": "715 MAGNOLIA LN", "number": "715", "street": "MAGNOLIA LN"},
        pay="card",
        pay_q="PAYING CARD",
    ),
    X(
        "syn-t6-0003",
        """
c: Hi, I'd like to place an order for pickup tomorrow.
c: Just one order of onion rings, please.
c: The name is June.
""",
        "P P P",
        items=[I("onion_rings", 1, None, ["one order of onion rings"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "tomorrow"),
        day=("tomorrow", "tomorrow"),
        name="June",
    ),
    X(
        "syn-t6-0004",
        """
c: hey good morning
c: can i get some americanos w hazelnut
c: n a choc chip muffin
c: pickup in 20 min for jordan, card
""",
        "S P P P",
        items=[
            I("americano", None, None, ["some americanos w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20 min", None),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t6-0005",
        """
c: hi can i get a blueberry
b: Sure! Do you mean a blueberry muffin? That's our only blueberry item.
c: ya the muffin
c: n 3 plain croissants
c: pickup for dev, card
""",
        "P P P P",
        items=[
            I("muffin", 1, "blueberry", ["a blueberry", "the muffin"]),
            I("croissant", 3, "plain", ["3 plain croissants"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Dev",
        name_q="dev",
    ),
    X(
        "syn-t6-0006",
        """
c: HI I NEED 4 BREAKFAST SANDWICHES ON CROISSANTS WITH AVOCADO
c: AND 2 CROISSANTS AND A LARGE CAPPUCCINO WITH HAZELNUT
c: DO YOU HAVE DECAF?
b: Sorry, we don't have decaf on the menu.
c: OK NO PROBLEM. PICKUP IN 30 MIN, NAME IS MARCUS
b: Got it, Marcus! Will you pay by card or cash?
c: ACTUALLY TAKE OFF THE BREAKFAST SANDWICHES, JUST THE CROISSANTS AND THE CAPPUCCINO
""",
        "P P Q P M",
        items=[
            I("croissant", 2, None, ["2 CROISSANTS"]),
            I(
                "cappuccino",
                1,
                "large",
                ["A LARGE CAPPUCCINO WITH HAZELNUT"],
                [add("hazelnut_syrup", "WITH HAZELNUT")],
            ),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("relative", "IN 30 MIN", None),
        name="Marcus",
        name_q="MARCUS",
    ),
    X(
        "syn-t6-0007",
        """
c: hi can i get a croissant for fri at 8
c: paying cash
c: thx!
""",
        "P P S",
        items=[I("croissant", 1, None, ["a croissant"])],
        time=("clock_time", "at 8", "08:00"),
        day=("weekday", "fri", "fri"),
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t6-0008",
        """
c: heyy 🍟 3 orders of fries
c: + a sprite 🥤
c: its for sunday, pickup at 1 pls 🙏
c: name jordan, paying card 💳
""",
        "P P P P",
        items=[
            I("fries", 3, None, ["3 orders of fries"]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 1", "13:00"),
        day=("weekday", "sun", "sunday"),
        pay="card",
        pay_q="paying card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t6-0009",
        """
c: GOOD MORNING!
c: CAN I GET A SMALL HOT CHOCOLATE, 2 DRIP COFFEES AND 2 CHOCOLATE CHIP MUFFINS FOR PICKUP TOMORROW MORNING. NAME IS ELI, PAYING CARD
""",
        "S P",
        items=[
            I("hot_chocolate", 1, "small", ["A SMALL HOT CHOCOLATE"]),
            I("drip_coffee", 2, None, ["2 DRIP COFFEES"]),
            I("muffin", 2, "chocolate_chip", ["2 CHOCOLATE CHIP MUFFINS"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        time=("ambiguous", "TOMORROW MORNING"),
        day=("tomorrow", "TOMORROW"),
        pay="card",
        pay_q="PAYING CARD",
        name="Eli",
        name_q="ELI",
    ),
    X(
        "syn-t6-0010",
        """
c: Hi, could I get a Sprite and the usual for pickup in 20 minutes? Name's Marcus.
""",
        "P",
        items=[
            I("sprite", 1, None, ["a Sprite"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in 20 minutes", None),
        name="Marcus",
    ),
]
