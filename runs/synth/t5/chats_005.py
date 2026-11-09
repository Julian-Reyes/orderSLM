"""t5 entries 0101–0130 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t5-0101",
        """
c: 2 hot chocolates w hazelnut n almond milk
c: and 2 small coffees
c: pickup in 15 for marcus, card
""",
        "P P P",
        items=[
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocolates"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "almond_milk", "almond milk")],
            ),
            I("drip_coffee", 2, "small", ["2 small coffees"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 15", None),
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t5-0102",
        """
c: can i get some bagels asap
""",
        "P",
        items=[I("bagel", None, None, ["some bagels"])],
        time=("asap", "asap", None),
    ),
    X(
        "syn-t5-0103",
        """
c: HEY HALFMOON!
c: WE NEED TO ORDER FOR THE WHOLE TEAM TONIGHT!
""",
        "S P",
    ),
    X(
        "syn-t5-0104",
        """
c: 5 large hawaiians, 2 of em no ham
c: 3 large margheritas
c: 2 orders of knots
c: pickup, card
""",
        "P P P P",
        items=[
            I("hawaiian_pizza", 3, "large", ["5 large hawaiians"]),
            I("hawaiian_pizza", 2, "large", ["5 large hawaiians", "2 of em no ham"], [rm("ham", "no ham")]),
            I("margherita_pizza", 3, "large", ["3 large margheritas"]),
            I("garlic_knots", 2, None, ["2 orders of knots"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0105",
        """
c: bbq chicken pizza and 2 large supremes to 282 grant blvd, card
""",
        "P",
        items=[
            I("bbq_chicken_pizza", 1, None, ["bbq chicken pizza"]),
            I("supreme_pizza", 2, "large", ["2 large supremes"]),
        ],
        method="delivery",
        method_q="to 282 grant blvd",
        addr={"raw": "282 grant blvd", "number": "282", "street": "grant blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0106",
        """
c: Hi, could I get two lattes?
c: I'll pick them up. My name is Keisha.
c: I'll pay by card.
""",
        "P P P",
        items=[I("latte", 2, None, ["two lattes"])],
        method="pickup",
        method_q="pick them up",
        pay="card",
        pay_q="pay by card",
        name="Keisha",
    ),
    X(
        "syn-t5-0107",
        """
c: knots
c: 2 iced teas
c: water
c: and that thing from before, delivery, card
""",
        "P P P P",
        items=[
            I("garlic_knots", 1, None, ["knots"]),
            I("iced_tea", 2, None, ["2 iced teas"]),
            I("water", 1, None, ["water"]),
            I(
                None,
                1,
                None,
                ["that thing from before"],
                unmatched="that thing from before",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="delivery",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0108",
        """
c: Hi, does the veggie burger come with cheese?
b: It doesn't, but you can add cheese.
c: Okay. Five veggie burgers, three of them without tomato.
c: Two lemonades as well.
c: And a bacon burger without tomato and a Coke.
c: Pickup, and I'll pay by card.
""",
        "Q P P P P",
        items=[
            I("veggie_burger", 2, None, ["Five veggie burgers"]),
            I(
                "veggie_burger",
                3,
                None,
                ["Five veggie burgers", "three of them without tomato"],
                [rm("tomato", "without tomato")],
            ),
            I("lemonade", 2, None, ["Two lemonades"]),
            I("bacon_burger", 1, None, ["a bacon burger"], [rm("tomato", "without tomato")]),
            I("coke", 1, None, ["a Coke"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0109",
        """
c: supreme pizza
c: + a sprite
c: 816 dover terrace apt 16a
""",
        "P P P",
        items=[I("supreme_pizza", 1, None, ["supreme pizza"]), I("sprite", 1, None, ["a sprite"])],
        method="delivery",
        method_q="816 dover terrace apt 16a",
        addr={"raw": "816 dover terrace apt 16a", "number": "816", "street": "dover terrace", "unit": "16a"},
    ),
    X(
        "syn-t5-0110",
        """
c: hi! a breakfast sandwich, 2 large lattes w hazelnut and the one i always get 😊 card, at 9:30
""",
        "P",
        items=[
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
            I("latte", 2, "large", ["2 large lattes"], [add("hazelnut_syrup", "w hazelnut")]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        time=("clock_time", "at 9:30", "09:30"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0111",
        """
c: Hello, I'd like a few extra large Hawaiian pizzas with stuffed crust.
c: For pickup, as soon as possible.
c: Thanks!
""",
        "P P S",
        items=[
            I(
                "hawaiian_pizza",
                None,
                "extra_large",
                ["a few extra large Hawaiian pizzas"],
                [add("crust_stuffed", "with stuffed crust")],
            ),
        ],
        method="pickup",
        method_q="For pickup",
        time=("asap", "as soon as possible", None),
    ),
    X(
        "syn-t5-0112",
        """
c: Hi there!
c: Four veggie pizzas delivered to 9244 Ivanhoe Dr, please.
""",
        "S P",
        items=[I("veggie_pizza", 4, None, ["Four veggie pizzas"])],
        method="delivery",
        method_q="delivered to 9244 Ivanhoe Dr",
        addr={"raw": "9244 Ivanhoe Dr", "number": "9244", "street": "Ivanhoe Dr"},
    ),
    X(
        "syn-t5-0113",
        """
c: hi ☕ do u have decaf?
b: Sorry, no decaf right now!
c: ok no worries, 2 lattes and a medium americano then 😊
c: pickup for keisha, cash
""",
        "Q P P",
        items=[I("latte", 2, None, ["2 lattes"]), I("americano", 1, "medium", ["a medium americano"])],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t5-0114",
        """
c: breakfast sandwich on a croissant
c: and a large coffee black
c: pickup for sam
""",
        "P P P",
        items=[
            I("breakfast_sandwich", 1, "croissant", ["breakfast sandwich on a croissant"]),
            I("drip_coffee", 1, "large", ["a large coffee"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t5-0115",
        """
c: 2 chocolate croissants w butter, a medium cappuccino and a breakfast sandwich, pickup for ana, cash
b: 2 chocolate croissants with butter, a medium cappuccino and a breakfast sandwich, pickup for Ana, cash. Right?
c: yup
c: actually drop the sandwich
""",
        "P C M",
        items=[
            I("croissant", 2, "chocolate", ["2 chocolate croissants"], [add("butter", "w butter")]),
            I("cappuccino", 1, "medium", ["a medium cappuccino"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t5-0116",
        """
c: Good morning!
c: Two medium cappuccinos, one with vanilla, and a medium coffee with oat milk, please. For pickup, under Ivy.
""",
        "S P",
        items=[
            I("cappuccino", 1, "medium", ["Two medium cappuccinos"]),
            I(
                "cappuccino",
                1,
                "medium",
                ["Two medium cappuccinos", "one with vanilla"],
                [add("vanilla_syrup", "with vanilla")],
            ),
            I("drip_coffee", 1, "medium", ["a medium coffee"], [add("oat_milk", "with oat milk")]),
        ],
        method="pickup",
        method_q="For pickup",
        name="Ivy",
    ),
    X(
        "syn-t5-0117",
        """
c: Hello!
c: I'd like two personal pepperoni pizzas.
c: One of them with garlic.
c: And two orders of garlic knots.
c: I'll pick it up.
c: Paying cash.
""",
        "S P P P P P",
        items=[
            I("pepperoni_pizza", 1, "personal", ["two personal pepperoni pizzas"]),
            I(
                "pepperoni_pizza",
                1,
                "personal",
                ["two personal pepperoni pizzas", "One of them with garlic"],
                [add("garlic", "with garlic")],
            ),
            I("garlic_knots", 2, None, ["two orders of garlic knots"]),
        ],
        method="pickup",
        method_q="I'll pick it up",
        pay="cash",
        pay_q="Paying cash",
    ),
    X(
        "syn-t5-0118",
        """
c: Hi, I'd like three extra large supreme pizzas, one without onions.
c: Also a small cheese pizza and two Dr Peppers.
c: Delivery to 999 Vine Ave as soon as possible.
c: I'll pay by card.
c: Thank you.
""",
        "P P P P S",
        items=[
            I("supreme_pizza", 2, "extra_large", ["three extra large supreme pizzas"]),
            I(
                "supreme_pizza",
                1,
                "extra_large",
                ["three extra large supreme pizzas", "one without onions"],
                [rm("onions", "without onions")],
            ),
            I("cheese_pizza", 1, "small", ["a small cheese pizza"]),
            I("dr_pepper", 2, None, ["two Dr Peppers"]),
        ],
        method="delivery",
        method_q="Delivery to 999 Vine Ave",
        time=("asap", "as soon as possible", None),
        addr={"raw": "999 Vine Ave", "number": "999", "street": "Vine Ave"},
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0119",
        """
c: hey 👋 can i grab some cokes?
c: thanks!!
""",
        "P S",
        items=[I("coke", None, None, ["some cokes"])],
    ),
    X(
        "syn-t5-0120",
        """
c: breakfast sandwich on a bagel and a medium latte w oat milk
c: pickup for luis
""",
        "P P",
        items=[
            I("breakfast_sandwich", 1, "bagel", ["breakfast sandwich on a bagel"]),
            I("latte", 1, "medium", ["a medium latte"], [sub("whole_milk", "oat_milk", "w oat milk")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t5-0121",
        """
c: heyy
c: 3 fries and the one i always get, at 7:15
""",
        "S P",
        items=[
            I("fries", 3, None, ["3 fries"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        time=("clock_time", "at 7:15", "19:15"),
    ),
    X(
        "syn-t5-0122",
        """
c: Could I get three medium lattes, one with caramel, a breakfast sandwich on a croissant, and a hot chocolate?
c: Thank you!
""",
        "P S",
        items=[
            I("latte", 2, "medium", ["three medium lattes"]),
            I(
                "latte",
                1,
                "medium",
                ["three medium lattes", "one with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
            I("breakfast_sandwich", 1, "croissant", ["a breakfast sandwich on a croissant"]),
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
        ],
    ),
    X(
        "syn-t5-0123",
        """
c: SOME BREADSTICKS, FOUR PERSONAL BBQ CHICKEN PIZZAS NO BBQ SAUCE ON THIN CRUST AND A PERSONAL CHEESE! DELIVERY ASAP, CARD!
""",
        "P",
        items=[
            I("breadsticks", None, None, ["SOME BREADSTICKS"]),
            I(
                "bbq_chicken_pizza",
                4,
                "personal",
                ["FOUR PERSONAL BBQ CHICKEN PIZZAS"],
                [rm("bbq_sauce", "NO BBQ SAUCE"), add("crust_thin", "THIN CRUST")],
            ),
            I("cheese_pizza", 1, "personal", ["A PERSONAL CHEESE"]),
        ],
        method="delivery",
        method_q="DELIVERY",
        time=("asap", "ASAP", None),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0124",
        """
c: A LARGE COFFEE WITH CARAMEL AND ALMOND MILK PLEASE!
c: CARD, AT 8:45!
""",
        "P P",
        items=[
            I(
                "drip_coffee",
                1,
                "large",
                ["A LARGE COFFEE"],
                [add("caramel_syrup", "WITH CARAMEL"), add("almond_milk", "ALMOND MILK")],
            ),
        ],
        time=("clock_time", "AT 8:45", "08:45"),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t5-0125",
        """
c: hey 🍕 putting together an order for game night!
""",
        "P",
    ),
    X(
        "syn-t5-0126",
        """
c: hii 😊 some milkshakes to 4 grant blvd pls
c: card 💳
""",
        "P P",
        items=[I("milkshake", None, None, ["some milkshakes"])],
        method="delivery",
        method_q="to 4 grant blvd",
        addr={"raw": "4 grant blvd", "number": "4", "street": "grant blvd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0127",
        """
c: Hi, can I get a 20 oz Diet Coke?
c: And one of those too.
c: That's all.
""",
        "P P S",
        items=[
            I("diet_coke", 1, "bottle_20oz", ["a 20 oz Diet Coke"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
    ),
    X(
        "syn-t5-0128",
        """
c: hey
c: do u have gluten free crust
b: We do! Any pizza can be gluten-free.
c: ok cool. 6 small cheese pizzas 4 no sauce, an xl hawaiian w chicken, an xl bbq chicken n a small meat lovers
c: pickup at 8, cash
""",
        "S Q P P",
        items=[
            I("cheese_pizza", 2, "small", ["6 small cheese pizzas"]),
            I(
                "cheese_pizza",
                4,
                "small",
                ["6 small cheese pizzas", "4 no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
            I("hawaiian_pizza", 1, "extra_large", ["an xl hawaiian"], [add("grilled_chicken", "w chicken")]),
            I("bbq_chicken_pizza", 1, "extra_large", ["an xl bbq chicken"]),
            I("meat_lovers_pizza", 1, "small", ["a small meat lovers"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "20:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t5-0129",
        """
c: small margherita w red onions
c: 2 orders of breadsticks
c: 2 personal supremes
c: large hawaiian w olives thick crust
c: 224 riverside ave, cash, change for a 50
c: nah scratch the hawaiian
""",
        "P P P P P M",
        items=[
            I("margherita_pizza", 1, "small", ["small margherita"], [add("red_onions", "w red onions")]),
            I("breadsticks", 2, None, ["2 orders of breadsticks"]),
            I("supreme_pizza", 2, "personal", ["2 personal supremes"]),
        ],
        method="delivery",
        method_q="224 riverside ave",
        addr={"raw": "224 riverside ave", "number": "224", "street": "riverside ave"},
        pay="cash",
        pay_q=["cash", "change for a 50"],
        change=5000,
    ),
    X(
        "syn-t5-0130",
        """
c: hey ☺️ 2 hot chocolates, no whip, with vanilla + a choc chip muffin
c: pickup for june
c: oh wait no muffin actually 🙈
""",
        "P P M",
        items=[
            I(
                "hot_chocolate",
                2,
                None,
                ["2 hot chocolates"],
                [rm("whipped_cream", "no whip"), add("vanilla_syrup", "with vanilla")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="June",
        name_q="june",
    ),
]
