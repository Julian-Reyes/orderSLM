"""t8 syn-t8-0091–0120 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t8-0091",
        """
c: hi!
c: can i order for wed morning
c: small oat latte
c: n a bec
c: pickup 8:15, leah
""",
        "S P P P P",
        items=[
            I("latte", 1, "small", ["small oat latte"], [sub("whole_milk", "oat_milk", "oat")]),
            I("breakfast_sandwich", 1, None, ["a bec"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "8:15", "08:15"),
        day=("weekday", "wed", "wed"),
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t8-0092",
        """
c: 2 veggie burgers 1 w mustard, a double cheeseburger no lettuce add avo
c: a bacon burger n 4 lemonades
""",
        "P P",
        items=[
            I("veggie_burger", 1, None, ["2 veggie burgers 1 w mustard"]),
            I("veggie_burger", 1, None, ["2 veggie burgers 1 w mustard"], [add("mustard", "w mustard")]),
            I(
                "cheeseburger",
                1,
                "double",
                ["a double cheeseburger no lettuce add avo"],
                [rm("lettuce", "no lettuce"), add("avocado", "add avo")],
            ),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("lemonade", 4, None, ["4 lemonades"]),
        ],
    ),
    X(
        "syn-t8-0093",
        """
c: hey can i get the one i always get + a few things for the office
b: Sorry, we can't see past orders here. What would you like?
c: oh ok: a banana nut muffin, 3 small americanos, 3 bec on english muffins, 3 med caps n an everything bagel. pickup for sam, cash, i have a 50
""",
        "P P",
        items=[
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
            I("americano", 3, "small", ["3 small americanos"]),
            I("breakfast_sandwich", 3, "english_muffin", ["3 bec on english muffins"]),
            I("cappuccino", 3, "medium", ["3 med caps"]),
            I("bagel", 1, "everything", ["an everything bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "i have a 50"],
        change=5000,
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t8-0094",
        """
c: HEY THERE
c: 5 DOUBLE CHEESEBURGERS, 4 OF THEM WITH NO ONIONS
c: ONE ORDER OF ONION RINGS AND A COKE
c: TO 7505 QUINCY WAY, CASH
""",
        "S P P P",
        items=[
            I("cheeseburger", 1, "double", ["5 DOUBLE CHEESEBURGERS, 4 OF THEM WITH NO ONIONS"]),
            I(
                "cheeseburger",
                4,
                "double",
                ["5 DOUBLE CHEESEBURGERS, 4 OF THEM WITH NO ONIONS"],
                [rm("onion", "NO ONIONS")],
            ),
            I("onion_rings", 1, None, ["ONE ORDER OF ONION RINGS"]),
            I("coke", 1, None, ["A COKE"]),
        ],
        method="delivery",
        method_q="TO 7505 QUINCY WAY",
        addr={"raw": "7505 QUINCY WAY", "number": "7505", "street": "QUINCY WAY"},
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t8-0095",
        """
c: hi 👋 4 bacon burgers no pickles
c: n a coke 🥤
c: do u guys use real bacon?
b: Yes, real applewood bacon!
c: yum 😋 60 glenwood ct, card
c: oops make it 3 bacon burgers
""",
        "P P Q P M",
        items=[
            I(
                "bacon_burger",
                3,
                None,
                ["4 bacon burgers no pickles", "make it 3 bacon burgers"],
                [rm("pickle", "no pickles")],
            ),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="60 glenwood ct",
        addr={"raw": "60 glenwood ct", "number": "60", "street": "glenwood ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0096",
        """
c: lg cap
c: + a strawberry banana smoothie
c: asap, cash
""",
        "P P P",
        items=[
            I("cappuccino", 1, "large", ["lg cap"]),
            I(None, 1, None, ["a strawberry banana smoothie"], unmatched="a strawberry banana smoothie"),
        ],
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0097",
        """
c: Hi, a cheeseburger, a veggie burger with cheese, a Sprite and the usual for my brother.
""",
        "P",
        items=[
            I("cheeseburger", 1, None, ["a cheeseburger"]),
            I("veggie_burger", 1, None, ["a veggie burger with cheese"], [add("cheese", "with cheese")]),
            I("sprite", 1, None, ["a Sprite"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
    ),
    X(
        "syn-t8-0098",
        """
c: Hi, I'll have the same as last time plus a veggie burger with extra ketchup, delivered at 8:15.
c: Card, please.
""",
        "P P",
        items=[
            I(
                None,
                1,
                None,
                ["the same as last time"],
                unmatched="the same as last time",
                flag="item_menu_match",
            ),
            I(
                "veggie_burger",
                1,
                None,
                ["a veggie burger with extra ketchup"],
                [add("ketchup", "extra ketchup", "extra")],
            ),
        ],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 8:15", "20:15"),
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0099",
        """
c: morning!! ☕ u guys are the best
""",
        "S",
    ),
    X(
        "syn-t8-0100",
        """
c: 2 caps w skim
c: n the usual
c: pickup at 9 for june, card
""",
        "P P P",
        items=[
            I("cappuccino", 2, None, ["2 caps w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t8-0101",
        """
c: a cap, not the small one, pickup for ben, card
""",
        "P",
        items=[I("cappuccino", 1, None, ["a cap, not the small one"], flag="item_variant")],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t8-0102",
        """
c: 2 med caps
c: pickup
c: june
c: card
b: Got it, June: 2 medium cappuccinos, pickup, paying by card. Is that right?
c: yes
c: oh can u do them w oat milk
""",
        "P P P P C M",
        items=[
            I(
                "cappuccino",
                2,
                "medium",
                ["2 med caps", "w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t8-0103",
        """
c: veggie burger, a sprite, 2 cokes n same as last time for my wife 🙏
c: asap, card 💳
""",
        "P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger"]),
            I("sprite", 1, None, ["a sprite"]),
            I("coke", 2, None, ["2 cokes"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0104",
        """
c: Hi, same as last time please.
b: Sorry, we can't see past orders here. What would you like?
c: A bacon burger, a veggie burger, three large fries, a Coke and two Sprites.
c: To 3336 Fulton Terrace, unit 6C. Card.
""",
        "P P P",
        items=[
            I("bacon_burger", 1, None, ["A bacon burger"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("fries", 3, "large", ["three large fries"]),
            I("coke", 1, None, ["a Coke"]),
            I("sprite", 2, None, ["two Sprites"]),
        ],
        method="delivery",
        method_q="To 3336 Fulton Terrace, unit 6C",
        addr={
            "raw": "3336 Fulton Terrace, unit 6C",
            "number": "3336",
            "street": "Fulton Terrace",
            "unit": "unit 6C",
        },
        pay="card",
        pay_q="Card",
    ),
    X(
        "syn-t8-0105",
        """
c: 2 small almond lattes
c: 2 plain croissants w butter
c: n a grande fruit cup, pickup eli, card
""",
        "P P P",
        items=[
            I("latte", 2, "small", ["2 small almond lattes"], [sub("whole_milk", "almond_milk", "almond")]),
            I("croissant", 2, "plain", ["2 plain croissants w butter"], [add("butter", "w butter")]),
            I(None, 1, None, ["a grande fruit cup"], unmatched="a grande fruit cup"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t8-0106",
        """
c: large veggie no olives 🍕 to 244 sycamore ct
b: Sure! Which crust would you like: regular, thin, thick, stuffed or gluten-free?
c: thick 👍 paying cash
""",
        "P P",
        items=[
            I(
                "veggie_pizza",
                1,
                "large",
                ["large veggie no olives", "thick"],
                [rm("olives", "no olives"), add("crust_thick", "thick")],
            ),
        ],
        method="delivery",
        method_q="to 244 sycamore ct",
        addr={"raw": "244 sycamore ct", "number": "244", "street": "sycamore ct"},
        pay="cash",
        pay_q="paying cash",
    ),
    X(
        "syn-t8-0107",
        """
c: Good morning!
c: Two everything bagels with tomato, two hot chocolates and a medium drip coffee. Cash.
b: Got it: 2 everything bagels with tomato, 2 hot chocolates and 1 medium drip coffee, paying cash. Is that right?
c: Sorry, only one bagel.
""",
        "S P M",
        items=[
            I(
                "bagel",
                1,
                "everything",
                ["Two everything bagels with tomato", "only one bagel"],
                [add("tomato", "with tomato")],
            ),
            I("hot_chocolate", 2, None, ["two hot chocolates"]),
            I("drip_coffee", 1, "medium", ["a medium drip coffee"]),
        ],
        pay="cash",
        pay_q="Cash",
    ),
    X(
        "syn-t8-0108",
        """
c: Hi, a personal pepperoni, 3 Sprites and 3 iced teas for 7:30, please.
c: Are the iced teas sweetened?
b: Lightly sweetened. Got it: 1 personal Pepperoni Pizza, 3 Sprites and 3 iced teas for 7:30 PM. Is that right?
c: Yes.
c: Actually, could you make the pepperoni thin crust?
""",
        "P Q C M",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "personal",
                ["a personal pepperoni", "make the pepperoni thin crust"],
                [add("crust_thin", "thin crust")],
            ),
            I("sprite", 3, None, ["3 Sprites"]),
            I("iced_tea", 3, None, ["3 iced teas"]),
        ],
        time=("clock_time", "for 7:30", "19:30"),
    ),
    X(
        "syn-t8-0109",
        """
c: HI
c: SAME AS LAST TIME, PLUS AN ORDER OF BREADSTICKS AND 3 WATERS FOR PICKUP
""",
        "S P",
        items=[
            I(None, 1, None, ["SAME AS LAST TIME"], unmatched="SAME AS LAST TIME", flag="item_menu_match"),
            I("breadsticks", 1, None, ["AN ORDER OF BREADSTICKS"]),
            I("water", 3, None, ["3 WATERS"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
    ),
    X(
        "syn-t8-0110",
        """
c: some bagels n 4 bec on english muffins
c: what bagels do u have
b: Plain, everything, sesame and cinnamon raisin.
""",
        "P Q",
        items=[
            I("bagel", None, None, ["some bagels"]),
            I("breakfast_sandwich", 4, "english_muffin", ["4 bec on english muffins"]),
        ],
    ),
    X(
        "syn-t8-0111",
        """
c: GOOD MORNING
c: 5 LARGE HOT CHOCOLATES
c: 4 WITH NO WHIP
c: AND 2 ALMOND CROISSANTS
c: PICKUP FOR BEN
""",
        "S P P P P",
        items=[
            I("hot_chocolate", 1, "large", ["5 LARGE HOT CHOCOLATES", "4 WITH NO WHIP"]),
            I(
                "hot_chocolate",
                4,
                "large",
                ["5 LARGE HOT CHOCOLATES", "4 WITH NO WHIP"],
                [rm("whipped_cream", "NO WHIP")],
            ),
            I("croissant", 2, "almond", ["2 ALMOND CROISSANTS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        name="Ben",
        name_q="BEN",
    ),
    X(
        "syn-t8-0112",
        """
c: Hello!
c: A chocolate croissant and two small cappuccinos with oat milk, please.
c: And a breakfast burrito if you have them.
c: Pickup for Leah, card.
""",
        "S P P P",
        items=[
            I("croissant", 1, "chocolate", ["A chocolate croissant"]),
            I(
                "cappuccino",
                2,
                "small",
                ["two small cappuccinos with oat milk"],
                [sub("whole_milk", "oat_milk", "with oat milk")],
            ),
            I(None, 1, None, ["a breakfast burrito"], unmatched="a breakfast burrito"),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="Leah",
    ),
    X(
        "syn-t8-0113",
        """
c: vanilla shake n 2 rings
c: 2 cheeseburgers
c: 2 bacon burgers
c: a veggie w mustard
c: n a coke
c: 18 cedar hill way unit 12 asap, card
""",
        "P P P P P P",
        items=[
            I("milkshake", 1, "vanilla", ["vanilla shake"]),
            I("onion_rings", 2, None, ["2 rings"]),
            I("cheeseburger", 2, None, ["2 cheeseburgers"]),
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("veggie_burger", 1, None, ["a veggie w mustard"], [add("mustard", "w mustard")]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="delivery",
        method_q="18 cedar hill way unit 12",
        addr={"raw": "18 cedar hill way unit 12", "number": "18", "street": "cedar hill way", "unit": "12"},
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0114",
        """
c: sm drip w caramel, sm almond latte, med cap n same as last time for my coworker ☕☕☕ card
""",
        "P",
        items=[
            I("drip_coffee", 1, "small", ["sm drip w caramel"], [add("caramel_syrup", "w caramel")]),
            I("latte", 1, "small", ["sm almond latte"], [sub("whole_milk", "almond_milk", "almond")]),
            I("cappuccino", 1, "medium", ["med cap"]),
            I(None, 1, None, ["same as last time"], unmatched="same as last time", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0115",
        """
c: HEY GUYS
c: JUST WANTED TO SAY THE BURGERS LAST NIGHT WERE AMAZING
""",
        "S S",
    ),
    X(
        "syn-t8-0116",
        """
c: A plain bagel for pickup, please.
c: The name is Priya.
c: I'll pay cash.
c: Actually, can I get a hot chocolate instead of the bagel?
""",
        "P P P M",
        items=[I("hot_chocolate", 1, None, ["a hot chocolate instead of the bagel"])],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="I'll pay cash",
        name="Priya",
        name_q="Priya",
    ),
    X(
        "syn-t8-0117",
        """
c: lg cap n an americano w hazelnut, one of the bigger ones, asap pickup keisha cash
""",
        "P",
        items=[
            I("cappuccino", 1, "large", ["lg cap"]),
            I(
                "americano",
                1,
                None,
                ["an americano w hazelnut, one of the bigger ones"],
                [add("hazelnut_syrup", "w hazelnut")],
                flag="item_variant",
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t8-0118",
        """
c: breakfast deal
c: americano n a croissant w it
c: plus another croissant w butter
c: n 4 large hot chocs w caramel no whip
c: pickup june, card
""",
        "P P P P P",
        items=[
            I(
                "coffee_pastry_combo",
                1,
                None,
                ["breakfast deal", "americano n a croissant w it"],
                combo={"drink": "americano", "pastry": "croissant"},
            ),
            I("croissant", 1, None, ["another croissant w butter"], [add("butter", "w butter")]),
            I(
                "hot_chocolate",
                4,
                "large",
                ["4 large hot chocs w caramel no whip"],
                [add("caramel_syrup", "w caramel"), rm("whipped_cream", "no whip")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t8-0119",
        """
c: hiii 🌞
c: a hot choc w coconut milk n a bec no bacon add tomato 🍅 pickup omar, cash
""",
        "S P",
        items=[
            I("hot_chocolate", 1, None, ["a hot choc w coconut milk"], [offmod("w coconut milk")]),
            I(
                "breakfast_sandwich",
                1,
                None,
                ["a bec no bacon add tomato"],
                [rm("bacon", "no bacon"), add("tomato", "add tomato")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t8-0120",
        """
c: Hi, two medium pepperonis, a bottled water and some garlic knots for delivery at 7, card.
""",
        "P",
        items=[
            I("pepperoni_pizza", 2, "medium", ["two medium pepperonis"]),
            I("water", 1, None, ["a bottled water"]),
            I("garlic_knots", None, None, ["some garlic knots"]),
        ],
        method="delivery",
        method_q="for delivery",
        time=("clock_time", "at 7", "19:00"),
        pay="card",
        pay_q="card",
    ),
]
