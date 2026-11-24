"""t8 syn-t8-0031–0060 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm

ENTRIES = [
    X(
        "syn-t8-0031",
        """
c: Hi, I'd like to place an order for tomorrow morning.
c: Two small lattes, please.
c: We'll be there at 10:15. I'll pay by card.
""",
        "P P P",
        items=[I("latte", 2, "small", ["Two small lattes"])],
        method="pickup",
        method_q="We'll be there",
        time=("clock_time", "at 10:15", "10:15"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="I'll pay by card",
    ),
    X(
        "syn-t8-0032",
        """
c: HEY I WANT TO ORDER FOR THURSDAY
c: 2 CHOCOLATE SHAKES AND A BACON BURGER TO 223 RIVERSIDE CT UNIT 27B
c: AT 7 PLEASE
""",
        "P P P",
        items=[
            I("milkshake", 2, "chocolate", ["2 CHOCOLATE SHAKES"]),
            I("bacon_burger", 1, None, ["A BACON BURGER"]),
        ],
        method="delivery",
        method_q="TO 223 RIVERSIDE CT UNIT 27B",
        addr={"raw": "223 RIVERSIDE CT UNIT 27B", "number": "223", "street": "RIVERSIDE CT", "unit": "27B"},
        time=("clock_time", "AT 7", "19:00"),
        day=("weekday", "thu", "THURSDAY"),
    ),
    X(
        "syn-t8-0033",
        """
c: 4 sesame bagels, 3 muffins n that thing from before, pickup for rosa, cash
""",
        "P",
        items=[
            I("bagel", 4, "sesame", ["4 sesame bagels"]),
            I("muffin", 3, None, ["3 muffins"]),
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
        pay="cash",
        pay_q="cash",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t8-0034",
        """
c: Hello!
c: I'd like 3 bacon burgers, one of them without the bacon please.
c: Are your fries salted?
b: Yes, lightly salted. We can do them without salt if you like.
c: Salted is fine. One order of fries and a Coke.
c: For pickup, the name is Tom.
""",
        "S P Q P P",
        items=[
            I("bacon_burger", 2, None, ["3 bacon burgers, one of them without the bacon"]),
            I(
                "bacon_burger",
                1,
                None,
                ["3 bacon burgers, one of them without the bacon"],
                [rm("bacon", "without the bacon")],
            ),
            I("fries", 1, None, ["One order of fries"]),
            I("coke", 1, None, ["a Coke"]),
        ],
        method="pickup",
        method_q="For pickup",
        name="Tom",
        name_q="Tom",
    ),
    X(
        "syn-t8-0035",
        """
c: 3 bagels pls
c: what kinds do u have
b: Plain, everything, sesame and cinnamon raisin.
c: ok n that thing from before too
c: asap, jordan, cash
""",
        "P Q P P",
        items=[
            I("bagel", 3, None, ["3 bagels"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t8-0036",
        """
c: hi ☀️ we're doing a team breakfast friday, like 25 ppl 🥯
c: is there someone i can talk to about setting that up?
""",
        "P HU",
        time=("ambiguous", "friday"),
        day=("weekday", "fri", "friday"),
    ),
    X(
        "syn-t8-0037",
        """
c: hey 🍕 small cheese w stuffed crust + 3 dr peppers to 197 prospect way #14c for thursday oct 22 at 6:30, card 💳
""",
        "P",
        items=[
            I(
                "cheese_pizza",
                1,
                "small",
                ["small cheese w stuffed crust"],
                [add("crust_stuffed", "stuffed crust")],
            ),
            I("dr_pepper", 3, None, ["3 dr peppers"]),
        ],
        method="delivery",
        method_q="to 197 prospect way #14c",
        addr={"raw": "197 prospect way #14c", "number": "197", "street": "prospect way", "unit": "#14c"},
        time=("clock_time", "at 6:30", "18:30"),
        day=("date", 10, 22, "oct 22"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0038",
        """
c: heyyy 👋
c: 3 veggie burgers, 2 sprites 🥤
c: n a 10 piece chicken nuggets 🐔
""",
        "S P P",
        items=[
            I("veggie_burger", 3, None, ["3 veggie burgers"]),
            I("sprite", 2, None, ["2 sprites"]),
            I(None, 1, None, ["a 10 piece chicken nuggets"], unmatched="a 10 piece chicken nuggets"),
        ],
    ),
    X(
        "syn-t8-0039",
        """
c: 2 veggie burgers no onions, 2 rings
c: n 2 regular fries
c: actually make the fries large
""",
        "P P M",
        items=[
            I("veggie_burger", 2, None, ["2 veggie burgers no onions"], [rm("onion", "no onions")]),
            I("onion_rings", 2, None, ["2 rings"]),
            I("fries", 2, "large", ["2 regular fries", "make the fries large"]),
        ],
    ),
    X(
        "syn-t8-0040",
        """
c: Hi there!
c: Could I get a milkshake, any flavor but vanilla, delivered to 5265 Sunset Way?
c: I'll pay by card.
""",
        "S P P",
        items=[I("milkshake", 1, None, ["a milkshake, any flavor but vanilla"], flag="item_variant")],
        method="delivery",
        method_q="delivered to 5265 Sunset Way",
        addr={"raw": "5265 Sunset Way", "number": "5265", "street": "Sunset Way"},
        pay="card",
        pay_q="I'll pay by card",
    ),
    X(
        "syn-t8-0041",
        """
c: hello 😎
c: a few lemonades for delivery pls 🍋
c: card
""",
        "S P P",
        items=[I("lemonade", None, None, ["a few lemonades"])],
        method="delivery",
        method_q="for delivery",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0042",
        """
c: vanilla shake
c: fries
c: bacon burger
c: n that thing from before, card
""",
        "P P P P",
        items=[
            I("milkshake", 1, "vanilla", ["vanilla shake"]),
            I("fries", 1, None, ["fries"]),
            I("bacon_burger", 1, None, ["bacon burger"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0043",
        """
c: 4 medium bbq chicken
c: no red onions, add jalapenos
c: pickup, sam
b: Got it, Sam: 4 medium BBQ Chicken Pizzas, no red onions, with jalapeños, for pickup. How would you like to pay?
c: card. yes thats right
c: wait only 3 bbq chicken
""",
        "P P P P/C M",
        items=[
            I(
                "bbq_chicken_pizza",
                3,
                "medium",
                ["4 medium bbq chicken", "no red onions, add jalapenos", "only 3 bbq chicken"],
                [rm("red_onions", "no red onions"), add("jalapenos", "add jalapenos")],
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
        "syn-t8-0044",
        """
c: ok so like
""",
        "U",
    ),
    X(
        "syn-t8-0045",
        """
c: Hi, I'd like 3 extra large cheese pizzas, one of them with stuffed crust, 3 medium veggie pizzas with bacon, and two 20 oz Dr Peppers. Pickup, paying by card.
""",
        "P",
        items=[
            I(
                "cheese_pizza",
                2,
                "extra_large",
                ["3 extra large cheese pizzas, one of them with stuffed crust"],
            ),
            I(
                "cheese_pizza",
                1,
                "extra_large",
                ["3 extra large cheese pizzas, one of them with stuffed crust"],
                [add("crust_stuffed", "with stuffed crust")],
            ),
            I(
                "veggie_pizza",
                3,
                "medium",
                ["3 medium veggie pizzas with bacon"],
                [add("bacon", "with bacon")],
            ),
            I("dr_pepper", 2, "bottle_20oz", ["two 20 oz Dr Peppers"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t8-0046",
        """
c: hey!
c: can i get a medium cap n 2 blueberry muffins for saturday
c: ill pick up at 9:30, name nico
""",
        "S P P",
        items=[
            I("cappuccino", 1, "medium", ["a medium cap"]),
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
        ],
        method="pickup",
        method_q="ill pick up",
        time=("clock_time", "at 9:30", "09:30"),
        day=("weekday", "sat", "saturday"),
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t8-0047",
        """
c: veggie pizza no sauce w jalapenos, thin
c: whats the biggest size u have
b: Extra large, 16 inches.
c: ok one of the bigger ones then
""",
        "P Q P",
        items=[
            I(
                "veggie_pizza",
                1,
                None,
                ["veggie pizza no sauce w jalapenos, thin", "one of the bigger ones"],
                [rm("tomato_sauce", "no sauce"), add("jalapenos", "w jalapenos"), add("crust_thin", "thin")],
                flag="item_variant",
            ),
        ],
    ),
    X(
        "syn-t8-0048",
        """
c: hi
c: lunch order for wednesday
c: 3 fries
c: are they crinkle cut?
b: No, ours are straight cut.
c: ok thats fine
c: to 246 grant terrace, blue door
c: at 1
c: card
""",
        "S P P Q S P P P",
        items=[I("fries", 3, None, ["3 fries"])],
        method="delivery",
        method_q="to 246 grant terrace",
        addr={
            "raw": "246 grant terrace, blue door",
            "number": "246",
            "street": "grant terrace",
            "reference": "blue door",
        },
        time=("clock_time", "at 1", "13:00"),
        day=("weekday", "wed", "wednesday"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0049",
        """
c: 4 bacon burgers 3 w mayo n an order of rings
c: 25 juniper ct apt 28b
""",
        "P P",
        items=[
            I("bacon_burger", 1, None, ["4 bacon burgers 3 w mayo"]),
            I("bacon_burger", 3, None, ["4 bacon burgers 3 w mayo"], [add("mayo", "w mayo")]),
            I("onion_rings", 1, None, ["an order of rings"]),
        ],
        method="delivery",
        method_q="25 juniper ct apt 28b",
        addr={"raw": "25 juniper ct apt 28b", "number": "25", "street": "juniper ct", "unit": "apt 28b"},
    ),
    X(
        "syn-t8-0050",
        """
c: bec
c: 2 med americanos w oat milk
c: a med latte
c: 4 croissants w butter
c: card
""",
        "P P P P P",
        items=[
            I("breakfast_sandwich", 1, None, ["bec"]),
            I("americano", 2, "medium", ["2 med americanos w oat milk"], [add("oat_milk", "w oat milk")]),
            I("latte", 1, "medium", ["a med latte"]),
            I("croissant", 4, None, ["4 croissants w butter"], [add("butter", "w butter")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0051",
        """
c: hey
c: need to order ahead for friday
c: a chocolate croissant
c: pickup at 8:45, jordan
c: card
""",
        "S P P P P",
        items=[I("croissant", 1, "chocolate", ["a chocolate croissant"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8:45", "08:45"),
        day=("weekday", "fri", "friday"),
        pay="card",
        pay_q="card",
        name="Jordan",
        name_q="jordan",
    ),
    X(
        "syn-t8-0052",
        """
c: plain bagel, 2 hot chocs, a med americano n a fruit cup, pickup at 8 for priya, card
""",
        "P",
        items=[
            I("bagel", 1, "plain", ["plain bagel"]),
            I("hot_chocolate", 2, None, ["2 hot chocs"]),
            I("americano", 1, "medium", ["a med americano"]),
            I(None, 1, None, ["a fruit cup"], unmatched="a fruit cup"),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "08:00"),
        pay="card",
        pay_q="card",
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t8-0053",
        """
c: 2 xl pepperoni w red onions n truffle oil + a water to 97 ivanhoe way #5c, card
""",
        "P",
        items=[
            I(
                "pepperoni_pizza",
                2,
                "extra_large",
                ["2 xl pepperoni w red onions n truffle oil"],
                [add("red_onions", "w red onions"), offmod("truffle oil")],
            ),
            I("water", 1, None, ["a water"]),
        ],
        method="delivery",
        method_q="to 97 ivanhoe way #5c",
        addr={"raw": "97 ivanhoe way #5c", "number": "97", "street": "ivanhoe way", "unit": "#5c"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0054",
        """
c: is the large
c: 🤔
""",
        "U U",
    ),
    X(
        "syn-t8-0055",
        """
c: morning!
c: 2 caps w vanilla, one of the bigger sizes
c: in 20 min for maya, cash
""",
        "S P P",
        items=[
            I(
                "cappuccino",
                2,
                None,
                ["2 caps w vanilla, one of the bigger sizes"],
                [add("vanilla_syrup", "w vanilla")],
                flag="item_variant",
            ),
        ],
        time=("relative", "in 20 min", None),
        pay="cash",
        pay_q="cash",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t8-0056",
        """
c: 4 single cheeseburgers
c: 2 w jalapenos
c: 3 cokes
c: pickup for marcus
c: card
""",
        "P P P P P",
        items=[
            I("cheeseburger", 2, "single", ["4 single cheeseburgers", "2 w jalapenos"]),
            I(
                "cheeseburger",
                2,
                "single",
                ["4 single cheeseburgers", "2 w jalapenos"],
                [add("jalapeno", "w jalapenos")],
            ),
            I("coke", 3, None, ["3 cokes"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t8-0057",
        """
c: an onion rings n a shake 🍦 not chocolate
c: pickup in 20 🙏
c: cash, i got a 20
""",
        "P P P",
        items=[
            I("onion_rings", 1, None, ["an onion rings"]),
            I("milkshake", 1, None, ["a shake 🍦 not chocolate"], flag="item_variant"),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="cash",
        pay_q=["cash", "i got a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0058",
        """
c: hi can i get the uhh
c: ok nvm the other one
""",
        "U U",
    ),
    X(
        "syn-t8-0059",
        """
c: #1 combo
c: fries
c: sprite
c: n a lemonade, cash, paying w a 20
""",
        "P P P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["#1 combo", "fries", "sprite"],
                combo={"side": "fries", "drink": "sprite"},
            ),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        pay="cash",
        pay_q=["cash", "paying w a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0060",
        """
c: large cheese gluten free crust, a 2 liter diet coke n a caesar salad
c: do u have ranch? to 9 magnolia rd asap, cash
""",
        "P Q/P",
        items=[
            I(
                "cheese_pizza",
                1,
                "large",
                ["large cheese gluten free crust"],
                [add("crust_gluten_free", "gluten free crust")],
            ),
            I("diet_coke", 1, "two_liter", ["a 2 liter diet coke"]),
            I(None, 1, None, ["a caesar salad"], unmatched="a caesar salad"),
        ],
        method="delivery",
        method_q="to 9 magnolia rd",
        addr={"raw": "9 magnolia rd", "number": "9", "street": "magnolia rd"},
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
]
