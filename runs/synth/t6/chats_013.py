"""t6 entries 0121–0130 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t6-0121",
        """
c: Hello, I'd like to place an order for October 15th.
c: One blueberry muffin and a breakfast sandwich on a bagel, no cheddar, with tomato.
c: Pickup at 10:30 for Jordan. I'll pay cash.
""",
        "P P P",
        items=[
            I("muffin", 1, "blueberry", ["One blueberry muffin"]),
            I(
                "breakfast_sandwich",
                1,
                "bagel",
                ["a breakfast sandwich on a bagel, no cheddar, with tomato"],
                [rm("cheddar", "no cheddar"), add("tomato", "with tomato")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 10:30", "10:30"),
        day=("date", 10, 15, "October 15th"),
        pay="cash",
        pay_q="pay cash",
        name="Jordan",
    ),
    X(
        "syn-t6-0122",
        """
c: hey 😄
c: 2 milkshakes at 6:30 pls, paying cash w a 20 💵
""",
        "S P",
        items=[I("milkshake", 2, None, ["2 milkshakes"])],
        time=("clock_time", "at 6:30", "18:30"),
        pay="cash",
        pay_q=["paying cash", "w a 20"],
        change=2000,
    ),
    X(
        "syn-t6-0123",
        """
c: hey can i get that thing from before
b: Sorry, I can't see past orders here. What would you like?
c: oh ok. a medium cappuccino w vanilla n 4 hot chocolates w hazelnut
c: also 2 choc chip muffins, a sesame bagel n 4 breakfast sandwiches on croissants, no bacon, add tomato
c: pickup for ivy, card
""",
        "P P P P",
        items=[
            I(
                "cappuccino",
                1,
                "medium",
                ["a medium cappuccino w vanilla"],
                [add("vanilla_syrup", "w vanilla")],
            ),
            I(
                "hot_chocolate",
                4,
                None,
                ["4 hot chocolates w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            ),
            I("muffin", 2, "chocolate_chip", ["2 choc chip muffins"]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
            I(
                "breakfast_sandwich",
                4,
                "croissant",
                ["4 breakfast sandwiches on croissants, no bacon, add tomato"],
                [rm("bacon", "no bacon"), add("tomato", "add tomato")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t6-0124",
        """
c: Hi, for October 14th at 8:15 I'd like an everything bagel with avocado, a chocolate croissant and a medium drip coffee with caramel and oat milk, for pickup under Tom.
""",
        "P",
        items=[
            I(
                "bagel",
                1,
                "everything",
                ["an everything bagel with avocado"],
                [add("avocado", "with avocado")],
            ),
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
            I(
                "drip_coffee",
                1,
                "medium",
                ["a medium drip coffee with caramel and oat milk"],
                [add("caramel_syrup", "with caramel"), add("oat_milk", "oat milk")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8:15", "08:15"),
        day=("date", 10, 14, "October 14th"),
        name="Tom",
    ),
    X(
        "syn-t6-0125",
        """
c: Hi there!
c: Could I get 2 cheeseburgers with mayo and a fried egg on each, plus 3 Sprites? Pickup, paying cash.
""",
        "S P",
        items=[
            I(
                "cheeseburger",
                2,
                None,
                ["2 cheeseburgers with mayo and a fried egg on each"],
                [add("mayo", "with mayo"), offmod("a fried egg on each")],
            ),
            I("sprite", 3, None, ["3 Sprites"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t6-0126",
        """
c: Good afternoon.
c: For tomorrow at 9:45, three plain bagels and a drip coffee for pickup, please. The name is Jordan.
""",
        "S P",
        items=[
            I("bagel", 3, "plain", ["three plain bagels"]),
            I("drip_coffee", 1, None, ["a drip coffee"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 9:45", "09:45"),
        day=("tomorrow", "tomorrow"),
        name="Jordan",
    ),
    X(
        "syn-t6-0127",
        """
c: morning! ☀️
c: 1 breakfast sandwich w avocado 🥑
c: 3 large cappuccinos ☕
c: 2 croissants 🥐
c: n 2 hot chocolates no whip w hazelnut
c: ready at 10:30 pls
c: card 💳
""",
        "S P P P P P P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                None,
                ["1 breakfast sandwich w avocado"],
                [add("avocado", "w avocado")],
            ),
            I("cappuccino", 3, "large", ["3 large cappuccinos"]),
            I("croissant", 2, None, ["2 croissants"]),
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocolates no whip w hazelnut"],
                [rm("whipped_cream", "no whip"), add("hazelnut_syrup", "w hazelnut")],
            ),
        ],
        time=("clock_time", "at 10:30", "10:30"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0128",
        """
c: Hi, could I order 2 small lattes with hazelnut and 2 drip coffees with almond milk for October 13th at 8? I'll pay by card.
""",
        "P",
        items=[
            I(
                "latte",
                2,
                "small",
                ["2 small lattes with hazelnut"],
                [add("hazelnut_syrup", "with hazelnut")],
            ),
            I(
                "drip_coffee",
                2,
                None,
                ["2 drip coffees with almond milk"],
                [add("almond_milk", "with almond milk")],
            ),
        ],
        time=("clock_time", "at 8", "08:00"),
        day=("date", 10, 13, "October 13th"),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0129",
        """
c: HEY I WANT 2 MILKSHAKES
c: FOR PICKUP ON SUNDAY
c: NAME IS JUNE
""",
        "P P P",
        items=[I("milkshake", 2, None, ["2 MILKSHAKES"])],
        method="pickup",
        method_q="FOR PICKUP",
        time=("ambiguous", "ON SUNDAY"),
        day=("weekday", "sun", "SUNDAY"),
        name="June",
        name_q="JUNE",
    ),
    X(
        "syn-t6-0130",
        """
c: hey
c: large coffee w vanilla
c: a plain bagel
c: 2 small americanos
c: pickup thurs 8:20, eli, card
""",
        "S P P P P",
        items=[
            I("drip_coffee", 1, "large", ["large coffee w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("bagel", 1, "plain", ["a plain bagel"]),
            I("americano", 2, "small", ["2 small americanos"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "8:20", "08:20"),
        day=("weekday", "thu", "thurs"),
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
]
