"""t6 entries 0141–0150 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t6-0141",
        """
c: hey can i get a medium americano tomorrow at 7:10
c: pickup for rosa
c: card
""",
        "P P P",
        items=[I("americano", 1, "medium", ["a medium americano"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:10", "07:10"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0142",
        """
c: can u guys do orders for later in the week
b: Yes, we take orders up to a week ahead. What day?
c: thurs at 3
c: 2 lemonades n a strawberry shake, pickup, ben, card
""",
        "D P P",
        items=[
            I("lemonade", 2, None, ["2 lemonades"]),
            I("milkshake", 1, "strawberry", ["a strawberry shake"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 3", "15:00"),
        day=("weekday", "thu", "thurs"),
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0143",
        """
c: HEY
c: ONE MILKSHAKE FOR TOMORROW
c: PICKUP AT 4
c: CARD
""",
        "S P P P",
        items=[I("milkshake", 1, None, ["ONE MILKSHAKE"])],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 4", "16:00"),
        day=("tomorrow", "TOMORROW"),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t6-0144",
        """
c: Hello!
c: I'd like 4 regular fries, an order of onion rings and 4 lemonades.
c: Is the lemonade freshly squeezed?
b: Sorry, I can't confirm that here.
c: Alright. Delivery to 847 Mission Way, paying cash.
c: Actually, instead of the 4 fries, could I get a bacon burger?
""",
        "S P Q P M",
        items=[
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("onion_rings", 1, None, ["an order of onion rings"]),
            I("lemonade", 4, None, ["4 lemonades"]),
        ],
        method="delivery",
        method_q="Delivery to 847 Mission Way",
        addr={"raw": "847 Mission Way", "number": "847", "street": "Mission Way"},
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t6-0145",
        """
c: hey
c: can i order ahead for saturday?
b: Yes, we can take that now. What would you like?
c: 2 small pepperonis no cheese, w olive oil, saturday at 6:15
c: deliver to 8063 fulton ct
""",
        "S D P P",
        items=[
            I(
                "pepperoni_pizza",
                2,
                "small",
                ["2 small pepperonis no cheese, w olive oil"],
                [rm("cheese", "no cheese"), add("olive_oil", "w olive oil")],
            )
        ],
        method="delivery",
        method_q="deliver to 8063 fulton ct",
        time=("clock_time", "at 6:15", "18:15"),
        day=("weekday", "sat", "saturday"),
        addr={"raw": "8063 fulton ct", "number": "8063", "street": "fulton ct"},
    ),
    X(
        "syn-t6-0146",
        """
c: do u have cinnamon raisin bagels?
b: Yes, we do!
c: great: 3 breakfast sandwiches, 2 of them w avocado, 4 large hot chocolates w vanilla n a cinnamon raisin bagel. pickup for june, card
""",
        "Q P",
        items=[
            I("breakfast_sandwich", 1, None, ["3 breakfast sandwiches"]),
            I(
                "breakfast_sandwich",
                2,
                None,
                ["3 breakfast sandwiches", "2 of them w avocado"],
                [add("avocado", "w avocado")],
            ),
            I(
                "hot_chocolate",
                4,
                "large",
                ["4 large hot chocolates w vanilla"],
                [add("vanilla_syrup", "w vanilla")],
            ),
            I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t6-0147",
        """
c: hi 👋
c: just a sprite 🥤
c: for monday
c: pickup at 11:30 ⏰
""",
        "S P P P",
        items=[I("sprite", 1, None, ["a sprite"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 11:30", "11:30"),
        day=("weekday", "mon", "monday"),
    ),
    X(
        "syn-t6-0148",
        """
c: Hi, I'd like 4 small supreme pizzas with no cheese.
c: Delivered to 797 Easton Blvd, apt 11B.
c: Paying by card.
c: Sorry, make that 3 supremes, not 4.
""",
        "P P P M",
        items=[
            I(
                "supreme_pizza",
                3,
                "small",
                ["4 small supreme pizzas with no cheese", "make that 3 supremes"],
                [rm("cheese", "with no cheese")],
            )
        ],
        method="delivery",
        method_q="Delivered to 797 Easton Blvd",
        addr={"raw": "797 Easton Blvd, apt 11B", "number": "797", "street": "Easton Blvd", "unit": "apt 11B"},
        pay="card",
        pay_q="Paying by card",
    ),
    X(
        "syn-t6-0149",
        """
c: hey can i get a milkshake delivered to 28 wexford ln on saturday at 3
""",
        "P",
        items=[I("milkshake", 1, None, ["a milkshake"])],
        method="delivery",
        method_q="delivered to 28 wexford ln",
        time=("clock_time", "at 3", "15:00"),
        day=("weekday", "sat", "saturday"),
        addr={"raw": "28 wexford ln", "number": "28", "street": "wexford ln"},
    ),
    X(
        "syn-t6-0150",
        """
c: hey 🍔 bacon burger no pickles w mayo + onion rings for the 20th at 12:30 pls
""",
        "P",
        items=[
            I(
                "bacon_burger",
                1,
                None,
                ["bacon burger no pickles w mayo"],
                [rm("pickle", "no pickles"), add("mayo", "w mayo")],
            ),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", None, 20, "the 20th"),
    ),
]
