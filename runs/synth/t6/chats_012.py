"""t6 entries 0111–0120 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t6-0111",
        """
c: hi
c: order for wed
c: medium supreme
c: an order of garlic knots
c: large bbq chicken w jalapenos
c: cash, paying w a 100
""",
        "S P P P P P",
        items=[
            I("supreme_pizza", 1, "medium", ["medium supreme"]),
            I("garlic_knots", 1, None, ["an order of garlic knots"]),
            I(
                "bbq_chicken_pizza",
                1,
                "large",
                ["large bbq chicken w jalapenos"],
                [add("jalapenos", "w jalapenos")],
            ),
        ],
        time=("ambiguous", "for wed"),
        day=("weekday", "wed", "wed"),
        pay="cash",
        pay_q=["cash", "paying w a 100"],
        change=10000,
    ),
    X(
        "syn-t6-0112",
        """
c: hi 👋
c: 2 cokes in the 20 oz bottles pls 🥤
c: pickup, grace, card 💳
c: actually just 1 coke 🙏
""",
        "S P P M",
        items=[I("coke", 1, "bottle_20oz", ["2 cokes in the 20 oz bottles", "just 1 coke"])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t6-0113",
        """
c: does the margherita have fresh mozzarella? 🧀
b: Yes, it has tomato sauce, fresh mozzarella, basil and olive oil.
c: ok an xl margherita w no mozzarella then, for nov 3rd at 7 🍕 deliver to 53 brookside ct, cash 💵
""",
        "Q P",
        items=[
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["an xl margherita w no mozzarella"],
                [rm("mozzarella", "w no mozzarella")],
            )
        ],
        method="delivery",
        method_q="deliver to 53 brookside ct",
        time=("clock_time", "at 7", "19:00"),
        day=("date", 11, 3, "nov 3rd"),
        addr={"raw": "53 brookside ct", "number": "53", "street": "brookside ct"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t6-0114",
        """
c: hey 🙂 what flavors do the shakes come in?
b: Vanilla, chocolate or strawberry.
c: cool, 2 shakes for pickup 🥤
c: name ben, card 💳
""",
        "Q P P",
        items=[I("milkshake", 2, None, ["2 shakes"])],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t6-0115",
        """
c: hii 👋
c: can i order now for sunday?
b: Yes, we take orders up to a week ahead!
c: yay 🙌 a lemonade n 2 cokes for sunday at 2
c: deliver to 1026 prospect way, above the bakery 🥐 card 💳
""",
        "S D P P",
        items=[
            I("lemonade", 1, None, ["a lemonade"]),
            I("coke", 2, None, ["2 cokes"]),
        ],
        method="delivery",
        method_q="deliver to 1026 prospect way",
        time=("clock_time", "at 2", "14:00"),
        day=("weekday", "sun", "sunday"),
        addr={
            "raw": "1026 prospect way, above the bakery",
            "number": "1026",
            "street": "prospect way",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0116",
        """
c: hey
c: a milkshake n same as last time
c: deliver to 6953 glenwood way
c: side entrance pls
""",
        "S P P P",
        items=[
            I("milkshake", 1, None, ["a milkshake"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        method="delivery",
        method_q="deliver to 6953 glenwood way",
        addr={"raw": "6953 glenwood way", "number": "6953", "street": "glenwood way"},
        notes=[("side entrance", "side entrance pls")],
    ),
    X(
        "syn-t6-0117",
        """
c: hey
c: can i get a sprite
c: for pickup saturday
c: marcus
c: card
""",
        "S P P P P",
        items=[I("sprite", 1, None, ["a sprite"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "saturday"),
        day=("weekday", "sat", "saturday"),
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t6-0118",
        """
c: 4 large cheese pizzas
c: 1 of em no sauce
c: n a large bbq chicken w sausage, stuffed crust
c: deliver asap to 64 union blvd
c: card
""",
        "P P P P P",
        items=[
            I("cheese_pizza", 3, "large", ["4 large cheese pizzas"]),
            I(
                "cheese_pizza",
                1,
                "large",
                ["4 large cheese pizzas", "1 of em no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I(
                "bbq_chicken_pizza",
                1,
                "large",
                ["a large bbq chicken w sausage, stuffed crust"],
                [add("sausage", "w sausage"), add("crust_stuffed", "stuffed crust")],
            ),
        ],
        method="delivery",
        method_q="deliver asap to 64 union blvd",
        time=("asap", "asap", None),
        addr={"raw": "64 union blvd", "number": "64", "street": "union blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t6-0119",
        """
c: can i get a personal supreme w thick crust n arugula on top, in like 20 min? paying card
""",
        "P",
        items=[
            I(
                "supreme_pizza",
                1,
                "personal",
                ["a personal supreme w thick crust n arugula on top"],
                [add("crust_thick", "w thick crust"), offmod("arugula on top")],
            )
        ],
        time=("relative", "in like 20 min", None),
        pay="card",
        pay_q="paying card",
    ),
    X(
        "syn-t6-0120",
        """
c: hi 🫐 can i get 3 of the blueberry ones
b: The blueberry muffins? Sure!
c: yes those 😊 pickup for ben, cash
""",
        "P P",
        items=[I("muffin", 3, "blueberry", ["3 of the blueberry ones"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
]
