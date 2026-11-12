"""t6 entries 0229–0240 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t6-0229",
        """
c: Hi, a veggie pizza without mushrooms, delivered to 283 Lakeview Blvd in about 40 minutes.
c: I'll pay cash.
""",
        "P P",
        items=[
            I(
                "veggie_pizza",
                1,
                None,
                ["a veggie pizza without mushrooms"],
                [rm("mushrooms", "without mushrooms")],
            )
        ],
        method="delivery",
        method_q="delivered to 283 Lakeview Blvd",
        time=("relative", "in about 40 minutes", None),
        addr={"raw": "283 Lakeview Blvd", "number": "283", "street": "Lakeview Blvd"},
        pay="cash",
        pay_q="pay cash",
    ),
    X(
        "syn-t6-0230",
        """
c: an order of garlic knots for pickup tmrw 🧄 name tom
""",
        "P",
        items=[I("garlic_knots", 1, None, ["an order of garlic knots"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "tmrw"),
        day=("tomorrow", "tmrw"),
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t6-0231",
        """
c: Hello, 3 small lattes, 2 of them with whipped cream, and 2 breakfast sandwiches on a croissant with tomato.
c: Pickup for Marcus, paying cash, I'll need change for a 50.
""",
        "P P",
        items=[
            I("latte", 1, "small", ["3 small lattes"]),
            I(
                "latte",
                2,
                "small",
                ["3 small lattes", "2 of them with whipped cream"],
                [add("whipped_cream", "with whipped cream")],
            ),
            I(
                "breakfast_sandwich",
                2,
                "croissant",
                ["2 breakfast sandwiches on a croissant with tomato"],
                [add("tomato", "with tomato")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q=["paying cash", "change for a 50"],
        change=5000,
        name="Marcus",
    ),
    X(
        "syn-t6-0232",
        """
c: what bagels do u have? 🥯
b: Plain, everything, sesame and cinnamon raisin.
c: ok some bagels n a blueberry muffin 😊
c: pickup for sam, card
""",
        "Q P P",
        items=[
            I("bagel", None, None, ["some bagels"]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t6-0233",
        """
c: small supreme
c: w truffle oil
c: pickup ben
c: card
""",
        "P P P P",
        items=[I("supreme_pizza", 1, "small", ["small supreme", "w truffle oil"], [offmod("w truffle oil")])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0234",
        """
c: hi 👋 do u have hazelnut?
b: Yes, we have hazelnut syrup!
c: yay 2 medium americanos w hazelnut for tmrw at 9 pls, pickup for maya ☕
""",
        "Q P",
        items=[
            I(
                "americano",
                2,
                "medium",
                ["2 medium americanos w hazelnut"],
                [add("hazelnut_syrup", "w hazelnut")],
            )
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        day=("tomorrow", "tmrw"),
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t6-0235",
        """
c: hey
c: small veggie pizza no onions
c: for sunday
c: deliver to 11 franklin blvd apt 23a
""",
        "S P P P",
        items=[I("veggie_pizza", 1, "small", ["small veggie pizza no onions"], [rm("onions", "no onions")])],
        method="delivery",
        method_q="deliver to 11 franklin blvd",
        time=("ambiguous", "for sunday"),
        day=("weekday", "sun", "sunday"),
        addr={
            "raw": "11 franklin blvd apt 23a",
            "number": "11",
            "street": "franklin blvd",
            "unit": "apt 23a",
        },
    ),
    X(
        "syn-t6-0236",
        """
c: 2 diet cokes for tmrw at 6 🥤
c: thx!
""",
        "P S",
        items=[I("diet_coke", 2, None, ["2 diet cokes"])],
        time=("clock_time", "at 6", "18:00"),
        day=("tomorrow", "tmrw"),
    ),
    X(
        "syn-t6-0237",
        """
c: is gluten free crust available in large?
b: Yes, gluten-free crust is available on any size.
c: ok large pepperoni no pepperoni on gluten free crust lol
c: n a diet coke
c: deliver to 598 juniper rd unit 26c at 6, card
c: wait can we do monday at 6 instead
""",
        "Q P P P M",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "large",
                ["large pepperoni no pepperoni on gluten free crust"],
                [rm("pepperoni", "no pepperoni"), add("crust_gluten_free", "on gluten free crust")],
            ),
            I("diet_coke", 1, None, ["a diet coke"]),
        ],
        method="delivery",
        method_q="deliver to 598 juniper rd",
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "mon", "monday"),
        addr={"raw": "598 juniper rd unit 26c", "number": "598", "street": "juniper rd", "unit": "unit 26c"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0238",
        """
c: hi 😊 same as last time pls
b: Sorry, I can't see past orders here. What would you like?
c: oops 😅 a blueberry muffin, an almond croissant w butter
c: a small americano w vanilla n a breakfast sandwich no egg
c: pickup for nico, cash
""",
        "P P P P",
        items=[
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
            I("croissant", 1, "almond", ["an almond croissant w butter"], [add("butter", "w butter")]),
            I("americano", 1, "small", ["a small americano w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich no egg"], [rm("egg", "no egg")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t6-0239",
        """
c: a latte at 11:45 pls, card
""",
        "P",
        items=[I("latte", 1, None, ["a latte"])],
        time=("clock_time", "at 11:45", "11:45"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0240",
        """
c: hi a latte w whipped cream
c: n a small coffee w hazelnut n oat milk
c: pickup for sam, cash
""",
        "P P P",
        items=[
            I("latte", 1, None, ["a latte w whipped cream"], [add("whipped_cream", "w whipped cream")]),
            I(
                "drip_coffee",
                1,
                "small",
                ["a small coffee w hazelnut n oat milk"],
                [add("hazelnut_syrup", "w hazelnut"), add("oat_milk", "oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Sam",
        name_q="sam",
    ),
]
