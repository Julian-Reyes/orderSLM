"""t6 entries 0031–0040 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t6-0031",
        """
c: hey there
c: can i get a small hawaiian, no sauce, w parmesan
c: 2 personal meat lovers w fresh mozzarella
c: 2 personal supremes, a water n a can of sprite
c: deliver to 186 franklin terrace
""",
        "S P P P P",
        items=[
            I(
                "hawaiian_pizza",
                1,
                "small",
                ["a small hawaiian, no sauce, w parmesan"],
                [rm("tomato_sauce", "no sauce"), add("parmesan", "w parmesan")],
            ),
            I(
                "meat_lovers_pizza",
                2,
                "personal",
                ["2 personal meat lovers w fresh mozzarella"],
                [add("mozzarella", "w fresh mozzarella")],
            ),
            I("supreme_pizza", 2, "personal", ["2 personal supremes"]),
            I("water", 1, None, ["a water"]),
            I("sprite", 1, "can", ["a can of sprite"]),
        ],
        method="delivery",
        method_q="deliver to 186 franklin terrace",
        addr={"raw": "186 franklin terrace", "number": "186", "street": "franklin terrace"},
    ),
    X(
        "syn-t6-0032",
        """
c: Hi, can I place an order now for Monday?
b: Yes, we can take orders up to a week ahead. What would you like?
c: 3 medium pepperoni pizzas for Monday at 6, please. I'll pay by card.
""",
        "D P",
        items=[I("pepperoni_pizza", 3, "medium", ["3 medium pepperoni pizzas"])],
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "mon", "Monday"),
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0033",
        """
c: Good morning. Do the almond croissants come warm?
b: We can warm them for you if you'd like!
c: No need. For tomorrow at 8:30, could I get one banana nut muffin, 2 cinnamon raisin bagels with egg and 2 almond croissants for pickup?
c: Name is Ben, I'll pay cash.
""",
        "Q P P",
        items=[
            I("muffin", 1, "banana_nut", ["one banana nut muffin"]),
            I("bagel", 2, "cinnamon_raisin", ["2 cinnamon raisin bagels with egg"], [add("egg", "with egg")]),
            I("croissant", 2, "almond", ["2 almond croissants"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8:30", "08:30"),
        day=("tomorrow", "tomorrow"),
        pay="cash",
        pay_q="pay cash",
        name="Ben",
    ),
    X(
        "syn-t6-0034",
        """
c: hiya
c: 3 almond croissants
c: 2 of em w butter
c: oh n a breakfast sandwich too
""",
        "S P P P",
        items=[
            I("croissant", 1, "almond", ["3 almond croissants"]),
            I(
                "croissant",
                2,
                "almond",
                ["3 almond croissants", "2 of em w butter"],
                [add("butter", "w butter")],
            ),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
        ],
    ),
    X(
        "syn-t6-0035",
        """
c: hey!
c: 2 hot chocs no whip w hazelnut n almond milk
c: 3 medium lattes + a croissant
c: for tmrw 8am
c: pickup, rosa, card
""",
        "S P P P P",
        items=[
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocs no whip w hazelnut n almond milk"],
                [
                    rm("whipped_cream", "no whip"),
                    add("hazelnut_syrup", "w hazelnut"),
                    sub("whole_milk", "almond_milk", "almond milk"),
                ],
            ),
            I("latte", 3, "medium", ["3 medium lattes"]),
            I("croissant", 1, None, ["a croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "8am", "08:00"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t6-0036",
        """
c: hello
c: need some stuff for saturday
c: 3 plain croissants
c: 2 plain bagels
c: cash
""",
        "S P P P P",
        items=[
            I("croissant", 3, "plain", ["3 plain croissants"]),
            I("bagel", 2, "plain", ["2 plain bagels"]),
        ],
        time=("ambiguous", "for saturday"),
        day=("weekday", "sat", "saturday"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0037",
        """
c: Hi, do you have gluten-free pastries?
b: Sorry, we don't have gluten-free pastries on the menu.
c: Okay, then just a few croissants please. I'll pay by card.
""",
        "Q P",
        items=[I("croissant", None, None, ["a few croissants"])],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t6-0038",
        """
c: hey can i order 4 diet cokes for thurs
c: at 7:30 pls
""",
        "P P",
        items=[I("diet_coke", 4, None, ["4 diet cokes"])],
        time=("clock_time", "at 7:30", "19:30"),
        day=("weekday", "thu", "thurs"),
    ),
    X(
        "syn-t6-0039",
        """
c: hey can i get the usual
b: Sorry, I can't see past orders here. What would you like?
c: 3 hot chocolates no whip, a large cappuccino w hazelnut n oat milk
c: also 2 breakfast sandwiches n 2 everything bagels. do the bagels come toasted?
b: We can toast them for you if you'd like!
c: no thats ok. pickup for ben, cash, change for a 50
""",
        "P P P/Q P",
        items=[
            I("hot_chocolate", 3, None, ["3 hot chocolates no whip"], [rm("whipped_cream", "no whip")]),
            I(
                "cappuccino",
                1,
                "large",
                ["a large cappuccino w hazelnut n oat milk"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "oat_milk", "oat milk")],
            ),
            I("breakfast_sandwich", 2, None, ["2 breakfast sandwiches"]),
            I("bagel", 2, "everything", ["2 everything bagels"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "change for a 50"],
        change=5000,
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0040",
        """
c: Good morning! I'd like to place an order for tomorrow at 7:30 for pickup, under Grace.
c: 4 medium americanos with whole milk, an almond croissant with butter and a medium latte with almond milk. I'll pay by card.
""",
        "P P",
        items=[
            I(
                "americano",
                4,
                "medium",
                ["4 medium americanos with whole milk"],
                [add("whole_milk", "with whole milk")],
            ),
            I("croissant", 1, "almond", ["an almond croissant with butter"], [add("butter", "with butter")]),
            I(
                "latte",
                1,
                "medium",
                ["a medium latte with almond milk"],
                [sub("whole_milk", "almond_milk", "with almond milk")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 7:30", "07:30"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="pay by card",
        name="Grace",
    ),
]
