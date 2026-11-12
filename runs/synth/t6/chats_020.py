"""t6 entries 0191–0203 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t6-0191",
        """
c: hump day lol, a cinnamon raisin bagel for pickup, luis, card
""",
        "P",
        items=[I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin bagel"])],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t6-0192",
        """
c: medium cap w vanilla
c: 3 small lattes w caramel
c: a cinnamon raisin bagel
c: 3 large coffees
c: 2 breakfast sandwiches no bacon
c: pickup, june
""",
        "P P P P P P",
        items=[
            I("cappuccino", 1, "medium", ["medium cap w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("latte", 3, "small", ["3 small lattes w caramel"], [add("caramel_syrup", "w caramel")]),
            I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin bagel"]),
            I("drip_coffee", 3, "large", ["3 large coffees"]),
            I("breakfast_sandwich", 2, None, ["2 breakfast sandwiches no bacon"], [rm("bacon", "no bacon")]),
        ],
        method="pickup",
        method_q="pickup",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t6-0193",
        """
c: hi
c: medium americano w hazelnut
c: for 2pm
c: oh wait make it monday at 2 instead
""",
        "S P P M",
        items=[
            I(
                "americano",
                1,
                "medium",
                ["medium americano w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            )
        ],
        time=("clock_time", "at 2", "14:00"),
        day=("weekday", "mon", "monday"),
    ),
    X(
        "syn-t6-0194",
        """
c: is hazelnut syrup extra?
b: Yes, syrups are an add-on.
c: ok 4 large cappuccinos, 3 of them w hazelnut
c: n a large americano + 2 hot chocolates, card
""",
        "Q P P",
        items=[
            I("cappuccino", 1, "large", ["4 large cappuccinos"]),
            I(
                "cappuccino",
                3,
                "large",
                ["4 large cappuccinos", "3 of them w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("americano", 1, "large", ["a large americano"]),
            I("hot_chocolate", 2, None, ["2 hot chocolates"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0195",
        """
c: 3 personal margheritas for tmrw at 12:30
c: card
""",
        "P P",
        items=[I("margherita_pizza", 3, "personal", ["3 personal margheritas"])],
        time=("clock_time", "at 12:30", "12:30"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0196",
        """
c: morning!
c: a latte w almond milk n 2 hot chocs w caramel n oat milk for tues at 8, pickup for priya, cash w a 20
""",
        "S P",
        items=[
            I(
                "latte",
                1,
                None,
                ["a latte w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocs w caramel n oat milk"],
                [add("caramel_syrup", "w caramel"), sub("whole_milk", "oat_milk", "oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "08:00"),
        day=("weekday", "tue", "tues"),
        pay="cash",
        pay_q=["cash", "w a 20"],
        change=2000,
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t6-0197",
        """
c: 4 blueberry muffins
c: 2 small americanos
c: w honey in them
c: pickup for sam
c: card
""",
        "P P P P P",
        items=[
            I("muffin", 4, "blueberry", ["4 blueberry muffins"]),
            I(
                "americano",
                2,
                "small",
                ["2 small americanos", "w honey in them"],
                [offmod("w honey in them")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t6-0198",
        """
c: Happy almost-Friday! Two bacon burgers for pickup, please, and I'll pay cash.
""",
        "P",
        items=[I("bacon_burger", 2, None, ["Two bacon burgers"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t6-0199",
        """
c: can i order for sat
b: Yes, we take orders up to a week ahead!
c: ok
c: a sprite + a lemonade
c: sat at 4
c: card
""",
        "D S P P P",
        items=[
            I("sprite", 1, None, ["a sprite"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        time=("clock_time", "at 4", "16:00"),
        day=("weekday", "sat", "sat"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0200",
        """
c: hey
c: does the meat lovers have bacon?
b: Yes: pepperoni, sausage, ham, bacon and beef.
c: ok a large meat lovers w bbq sauce at 7
c: card
c: actually swap the pizza for a diet coke
""",
        "S Q P P M",
        items=[I("diet_coke", 1, None, ["swap the pizza for a diet coke"])],
        time=("clock_time", "at 7", "19:00"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0201",
        """
c: Hi, I'll have the same as last time, please.
b: Sorry, I can't see past orders here. What would you like?
c: Oh, sorry. A breakfast sandwich on an English muffin, a small americano with hazelnut, a sesame bagel and a hot chocolate. Pickup for June, card.
""",
        "P P",
        items=[
            I("breakfast_sandwich", 1, "english_muffin", ["A breakfast sandwich on an English muffin"]),
            I(
                "americano",
                1,
                "small",
                ["a small americano with hazelnut"],
                [add("hazelnut_syrup", "with hazelnut")],
            ),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="June",
    ),
    X(
        "syn-t6-0202",
        """
c: hey
c: is the veggie one plant based?
b: Sorry, I can't confirm that here.
c: ok a veggie w cheese then
c: deliver to 86 orchard st, card
""",
        "S Q P P",
        items=[I("veggie_burger", 1, None, ["a veggie w cheese"], [add("cheese", "w cheese")])],
        method="delivery",
        method_q="deliver to 86 orchard st",
        addr={"raw": "86 orchard st", "number": "86", "street": "orchard st"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0203",
        """
c: hi
c: a 20 oz diet coke for pickup tmrw at 3:15
c: priya
""",
        "S P P",
        items=[I("diet_coke", 1, "bottle_20oz", ["a 20 oz diet coke"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 3:15", "15:15"),
        day=("tomorrow", "tmrw"),
        name="Priya",
        name_q="priya",
    ),
]
