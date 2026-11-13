"""t7 syn-t7-0001–0010 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t7-0001",
        """
c: hi 🍕 can we get 4 iced teas n something bready to munch on
b: For bread sides we have Garlic Knots (6 per order) and Breadsticks (4 per order). Which would you like?
c: the sticks 👍 one order. deliver to 7119 lakeview blvd, cash, paying w a 20
""",
        "P P",
        items=[
            I("iced_tea", 4, "can", ["4 iced teas"]),
            I("breadsticks", 1, None, ["the sticks", "one order"]),
        ],
        method="delivery",
        method_q="deliver to 7119 lakeview blvd",
        addr={"raw": "7119 lakeview blvd", "number": "7119", "street": "lakeview blvd"},
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0002",
        """
c: Hello there.
c: I'd like 4 personal Hawaiian pizzas, 3 of them on thick crust.
c: Also 3 personal veggie pizzas with basil on gluten-free crust.
c: Pickup, name is Tom. I'll pay cash with a 50.
""",
        "S P P P",
        items=[
            I("hawaiian_pizza", 1, "personal", ["4 personal Hawaiian pizzas"]),
            I(
                "hawaiian_pizza",
                3,
                "personal",
                ["4 personal Hawaiian pizzas", "3 of them on thick crust"],
                [add("crust_thick", "on thick crust")],
            ),
            I(
                "veggie_pizza",
                3,
                "personal",
                ["3 personal veggie pizzas"],
                [add("basil", "with basil"), add("crust_gluten_free", "on gluten-free crust")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="cash",
        pay_q=["I'll pay cash", "with a 50"],
        change=5000,
        name="Tom",
    ),
    X(
        "syn-t7-0003",
        """
c: hey 👋 the usual pls + 2 large veggies 🍕
b: Hi! We can't see past orders here, sorry. What's your usual?
c: oh lol 😅 a personal margherita w the house cheese, a personal supreme w anchovies n an order of knots
c: pickup, card 💳
""",
        "P P P",
        items=[
            I("veggie_pizza", 2, "large", ["2 large veggies"]),
            I(
                "margherita_pizza",
                1,
                "personal",
                ["a personal margherita w the house cheese"],
                [add("cheese", "w the house cheese")],
            ),
            I(
                "supreme_pizza",
                1,
                "personal",
                ["a personal supreme w anchovies"],
                [add("anchovies", "w anchovies")],
            ),
            I("garlic_knots", 1, None, ["an order of knots"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0004",
        """
c: Hi, can I get 6 extra large Hawaiian pizzas, 2 of them on gluten-free crust?
c: Plus an extra large cheese and an extra large meat lovers with no bacon.
c: Pickup in 40 minutes, paying by card.
""",
        "P P P",
        items=[
            I("hawaiian_pizza", 4, "extra_large", ["6 extra large Hawaiian pizzas"]),
            I(
                "hawaiian_pizza",
                2,
                "extra_large",
                ["6 extra large Hawaiian pizzas", "2 of them on gluten-free crust"],
                [add("crust_gluten_free", "on gluten-free crust")],
            ),
            I("cheese_pizza", 1, "extra_large", ["an extra large cheese"]),
            I(
                "meat_lovers_pizza",
                1,
                "extra_large",
                ["an extra large meat lovers with no bacon"],
                [rm("bacon", "no bacon")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        time=("relative", "in 40 minutes", None),
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t7-0005",
        """
c: heyyy 😊
c: 2 pepperonis, a medium margherita, breadsticks n the one i always get 🙏
c: deliver to 8200 sunset blvd #7b, cash, i got a 50 💵
""",
        "S P P",
        items=[
            I("pepperoni_pizza", 2, None, ["2 pepperonis"]),
            I("margherita_pizza", 1, "medium", ["a medium margherita"]),
            I("breadsticks", 1, None, ["breadsticks"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="deliver to 8200 sunset blvd",
        addr={"raw": "8200 sunset blvd #7b", "number": "8200", "street": "sunset blvd", "unit": "#7b"},
        pay="cash",
        pay_q=["cash", "i got a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0006",
        """
c: Hi there.
c: Could I get a large roni and a small marg?
c: And one order of bread sticks.
c: Pickup please.
c: Name is Maya.
c: Card.
""",
        "S P P P P P",
        items=[
            I("pepperoni_pizza", 1, "large", ["a large roni"]),
            I("margherita_pizza", 1, "small", ["a small marg"]),
            I("breadsticks", 1, None, ["one order of bread sticks"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="Card",
        name="Maya",
    ),
    X(
        "syn-t7-0007",
        """
c: hi can i get a small caramel latte, do you have almond milk? if yes a small americano with almond milk too
b: Yes, we have almond milk!
c: perfect. pickup, name jordan
""",
        "P/Q P",
        items=[
            I("latte", 1, "small", ["a small caramel latte"], [add("caramel_syrup", "caramel")]),
            I(
                "americano",
                1,
                "small",
                ["a small americano with almond milk"],
                [add("almond_milk", "with almond milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t7-0008",
        """
c: lg americano
c: choc chip muffin
c: n one of those
c: at 9:15
c: cash
""",
        "P P P P P",
        items=[
            I("americano", 1, "large", ["lg americano"]),
            I("muffin", 1, "chocolate_chip", ["choc chip muffin"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        time=("clock_time", "at 9:15", "09:15"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0009",
        """
c: hey
c: 2 bec on english muffins no egg
c: 2 sm caps w oat milk
c: pickup leah card
c: wait almond instead of oat on the caps
""",
        "S P P P M",
        items=[
            I(
                "breakfast_sandwich",
                2,
                "english_muffin",
                ["2 bec on english muffins no egg"],
                [rm("egg", "no egg")],
            ),
            I(
                "cappuccino",
                2,
                "small",
                ["2 sm caps w oat milk", "almond instead of oat on the caps"],
                [sub("whole_milk", "almond_milk", "almond instead of oat")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t7-0010",
        """
c: yo
c: a cappuccino n 3 small americanos
c: pickup for dev
c: cash, have a 20
""",
        "S P P P",
        items=[
            I("cappuccino", 1, None, ["a cappuccino"]),
            I("americano", 3, "small", ["3 small americanos"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "have a 20"],
        change=2000,
        name="Dev",
        name_q="dev",
    ),
]
