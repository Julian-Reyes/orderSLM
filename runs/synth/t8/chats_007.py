"""t8 syn-t8-0181–0210 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t8-0181",
        """
c: hiii can i get that thing from before 🍕
b: Sorry, we can't see past orders here. What would you like?
c: oh right 😅 a personal bbq chicken thin crust, a personal veggie w sausage, an order of knots, 3 20 oz iced teas n a diet coke
c: to 21 grant ln above the bakery, card
""",
        "P P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "personal",
                ["a personal bbq chicken thin crust"],
                [add("crust_thin", "thin crust")],
            ),
            I("veggie_pizza", 1, "personal", ["a personal veggie w sausage"], [add("sausage", "w sausage")]),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("iced_tea", 3, "bottle_20oz", ["3 20 oz iced teas"]),
            I("diet_coke", 1, None, ["a diet coke"]),
        ],
        method="delivery",
        method_q="to 21 grant ln",
        addr={
            "raw": "21 grant ln above the bakery",
            "number": "21",
            "street": "grant ln",
            "reference": "above the bakery",
        },
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0182",
        """
c: hey
c: 2 small pepperonis
c: one w mushrooms
c: n 2 diet cokes
c: card
""",
        "S P P P P",
        items=[
            I("pepperoni_pizza", 1, "small", ["2 small pepperonis", "one w mushrooms"]),
            I(
                "pepperoni_pizza",
                1,
                "small",
                ["2 small pepperonis", "one w mushrooms"],
                [add("mushrooms", "w mushrooms")],
            ),
            I("diet_coke", 2, None, ["2 diet cokes"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0183",
        """
c: hey
c: 3 coffees, 1 w vanilla, a bec on a croissant no cheese add tomato, 2 croissants n a med americano
c: pickup ben, cash
""",
        "S P P",
        items=[
            I("drip_coffee", 2, None, ["3 coffees, 1 w vanilla"]),
            I("drip_coffee", 1, None, ["3 coffees, 1 w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I(
                "breakfast_sandwich",
                1,
                "croissant",
                ["a bec on a croissant no cheese add tomato"],
                [rm("cheddar", "no cheese"), add("tomato", "add tomato")],
            ),
            I("croissant", 2, None, ["2 croissants"]),
            I("americano", 1, "medium", ["a med americano"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t8-0184",
        """
c: shake
c: what flavors
b: Vanilla, chocolate and strawberry!
c: one of the last two
c: whichever
""",
        "P Q P P",
        items=[I("milkshake", 1, None, ["shake", "one of the last two"], flag="item_variant")],
    ),
    X(
        "syn-t8-0185",
        """
c: hey!
c: a vanilla shake n some cokes delivered pls
""",
        "S P",
        items=[
            I("milkshake", 1, "vanilla", ["a vanilla shake"]),
            I("coke", None, None, ["some cokes"]),
        ],
        method="delivery",
        method_q="delivered",
    ),
    X(
        "syn-t8-0186",
        """
c: 2 lg caps
c: asap pickup
c: sam
b: Got it, Sam: 2 large cappuccinos, pickup as soon as possible. Is that right?
c: yep
c: oh just 1 cap actually
""",
        "P P P C M",
        items=[I("cappuccino", 1, "large", ["2 lg caps", "just 1 cap"])],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t8-0187",
        """
c: 2 med americanos
c: n one of those
c: the thing
c: u know
c: lol
""",
        "P P U U S",
        items=[
            I("americano", 2, "medium", ["2 med americanos"]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
    ),
    X(
        "syn-t8-0188",
        """
c: hi 👋
c: a lg americano n a few blueberry muffins 🫐
c: card
""",
        "S P P",
        items=[
            I("americano", 1, "large", ["a lg americano"]),
            I("muffin", None, "blueberry", ["a few blueberry muffins"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0189",
        """
c: 2 number 1s w mayo
c: what drinks come w it
b: Coke, Sprite or lemonade, plus fries or onion rings.
c: sprites n fries for both. 62 alder blvd in 30, cash
""",
        "P Q P",
        items=[
            I(
                "cheeseburger_combo",
                2,
                None,
                ["2 number 1s w mayo", "sprites n fries for both"],
                [add("mayo", "w mayo")],
                combo={"side": "fries", "drink": "sprite"},
            ),
        ],
        method="delivery",
        method_q="62 alder blvd",
        addr={"raw": "62 alder blvd", "number": "62", "street": "alder blvd"},
        time=("relative", "in 30", None),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0190",
        """
c: morning
c: that thing from before
b: Sorry, we can't see past orders here. What would you like?
c: cinnamon raisin bagel w tomato
c: small latte w caramel, med cap
c: 3 choc chip muffins
c: small hot choc w skim n a med drip w caramel, pickup june, card
""",
        "S P P P P P",
        items=[
            I("bagel", 1, "cinnamon_raisin", ["cinnamon raisin bagel w tomato"], [add("tomato", "w tomato")]),
            I("latte", 1, "small", ["small latte w caramel"], [add("caramel_syrup", "w caramel")]),
            I("cappuccino", 1, "medium", ["med cap"]),
            I("muffin", 3, "chocolate_chip", ["3 choc chip muffins"]),
            I(
                "hot_chocolate",
                1,
                "small",
                ["small hot choc w skim"],
                [sub("whole_milk", "skim_milk", "w skim")],
            ),
            I("drip_coffee", 1, "medium", ["a med drip w caramel"], [add("caramel_syrup", "w caramel")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    X(
        "syn-t8-0191",
        """
c: hi
c: ordering for thurs
c: just a lg latte
c: lol
c: pickup
c: 7:30
c: luis
c: card
""",
        "S P P S P P P P",
        items=[I("latte", 1, "large", ["a lg latte"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "7:30", "07:30"),
        day=("weekday", "thu", "thurs"),
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t8-0192",
        """
c: hey!
c: 2 everything bagels, 2 croissants n a peanut butter smoothie, pickup for grace
""",
        "S P",
        items=[
            I("bagel", 2, "everything", ["2 everything bagels"]),
            I("croissant", 2, None, ["2 croissants"]),
            I(None, 1, None, ["a peanut butter smoothie"], unmatched="a peanut butter smoothie"),
        ],
        method="pickup",
        method_q="pickup",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t8-0193",
        """
c: HI
c: I'LL HAVE ONE OF THOSE
b: Which item would you like?
c: SORRY. A SMALL HOT CHOCOLATE WITH OAT MILK, 2 LARGE CAPPUCCINOS WITH CARAMEL AND A PLAIN BAGEL
c: ALSO 2 LARGE AMERICANOS AND A MEDIUM LATTE
c: PICKUP IN 20 FOR MAYA, CARD
""",
        "S P P P P",
        items=[
            I(
                "hot_chocolate",
                1,
                "small",
                ["A SMALL HOT CHOCOLATE WITH OAT MILK"],
                [sub("whole_milk", "oat_milk", "WITH OAT MILK")],
            ),
            I(
                "cappuccino",
                2,
                "large",
                ["2 LARGE CAPPUCCINOS WITH CARAMEL"],
                [add("caramel_syrup", "WITH CARAMEL")],
            ),
            I("bagel", 1, "plain", ["A PLAIN BAGEL"]),
            I("americano", 2, "large", ["2 LARGE AMERICANOS"]),
            I("latte", 1, "medium", ["A MEDIUM LATTE"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("relative", "IN 20", None),
        pay="card",
        pay_q="CARD",
        name="Maya",
        name_q="MAYA",
    ),
    X(
        "syn-t8-0194",
        """
c: 4 med lattes, 2 w hazelnut ☕ + a lg americano w vanilla n 2 coffees w almond milk, pickup for leah, card 💳
""",
        "P",
        items=[
            I("latte", 2, "medium", ["4 med lattes, 2 w hazelnut"]),
            I("latte", 2, "medium", ["4 med lattes, 2 w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("americano", 1, "large", ["a lg americano w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("drip_coffee", 2, None, ["2 coffees w almond milk"], [add("almond_milk", "w almond milk")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t8-0195",
        """
c: Hi, this is for tomorrow: a medium Americano with skim, a hot chocolate and a plain bagel.
c: I'll pick it up at 10.
c: Cash. The name is Leah.
""",
        "P P P",
        items=[
            I("americano", 1, "medium", ["a medium Americano with skim"], [add("skim_milk", "with skim")]),
            I("hot_chocolate", 1, None, ["a hot chocolate"]),
            I("bagel", 1, "plain", ["a plain bagel"]),
        ],
        method="pickup",
        method_q="I'll pick it up",
        time=("clock_time", "at 10", "10:00"),
        day=("tomorrow", "tomorrow"),
        pay="cash",
        pay_q="Cash",
        name="Leah",
        name_q="Leah",
    ),
    X(
        "syn-t8-0196",
        """
c: Hi, a large fries, two Cokes and a milkshake, either chocolate or strawberry, whichever is easier.
c: For pickup, card.
""",
        "P P",
        items=[
            I("fries", 1, "large", ["a large fries"]),
            I("coke", 2, None, ["two Cokes"]),
            I("milkshake", 1, None, ["a milkshake, either chocolate or strawberry"], flag="item_variant"),
        ],
        method="pickup",
        method_q="For pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0197",
        """
c: 3 xl cheese 🧀
c: 2 xl veggie no olives
c: breadsticks, a diet coke n a dr pepper
c: 7 franklin ave, card 💳
""",
        "P P P P",
        items=[
            I("cheese_pizza", 3, "extra_large", ["3 xl cheese"]),
            I("veggie_pizza", 2, "extra_large", ["2 xl veggie no olives"], [rm("olives", "no olives")]),
            I("breadsticks", 1, None, ["breadsticks"]),
            I("diet_coke", 1, None, ["a diet coke"]),
            I("dr_pepper", 1, None, ["a dr pepper"]),
        ],
        method="delivery",
        method_q="7 franklin ave",
        addr={"raw": "7 franklin ave", "number": "7", "street": "franklin ave"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0198",
        """
c: Two chocolate croissants with butter and a muffin, any kind except blueberry.
c: Pickup for Keisha.
""",
        "P P",
        items=[
            I(
                "croissant",
                2,
                "chocolate",
                ["Two chocolate croissants with butter"],
                [add("butter", "with butter")],
            ),
            I("muffin", 1, None, ["a muffin, any kind except blueberry"], flag="item_variant"),
        ],
        method="pickup",
        method_q="Pickup",
        name="Keisha",
        name_q="Keisha",
    ),
    X(
        "syn-t8-0199",
        """
c: 3 sm hot chocs, one w caramel, a sm cap w hazelnut n skim
c: n a coffee, cash
""",
        "P P",
        items=[
            I("hot_chocolate", 2, "small", ["3 sm hot chocs, one w caramel"]),
            I(
                "hot_chocolate",
                1,
                "small",
                ["3 sm hot chocs, one w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
            I(
                "cappuccino",
                1,
                "small",
                ["a sm cap w hazelnut n skim"],
                [add("hazelnut_syrup", "w hazelnut"), sub("whole_milk", "skim_milk", "skim")],
            ),
            I("drip_coffee", 1, None, ["a coffee"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0200",
        """
c: Hi, I'd like an order of onion rings, are they gluten free?, and a second order too.
b: They're not gluten free, sorry.
c: That's okay. Pickup at 6:30, cash.
""",
        "P/Q P",
        items=[I("onion_rings", 2, None, ["an order of onion rings", "a second order too"])],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 6:30", "18:30"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0201",
        """
c: can u
c: k
c: 🙃
""",
        "U U U",
    ),
    X(
        "syn-t8-0202",
        """
c: 3 supremes, a size bigger than medium
c: an order of knots
c: pickup ana
""",
        "P P P",
        items=[
            I("supreme_pizza", 3, "large", ["3 supremes, a size bigger than medium"]),
            I("garlic_knots", 1, None, ["an order of knots"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t8-0203",
        """
c: hey 🍕
c: 4 small meat lovers gluten free crust
c: 4 2 liter diet cokes n 3 iced teas
c: cash
b: Got it: 4 small Meat Lovers Pizzas with gluten-free crust, 4 two-liter Diet Cokes and 3 iced teas, paying cash. Pickup or delivery?
c: oh nvm the pizzas, just the drinks
""",
        "S P P P M",
        items=[
            I("diet_coke", 4, "two_liter", ["4 2 liter diet cokes"]),
            I("iced_tea", 3, None, ["3 iced teas"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0204",
        """
c: hiii 🍕
c: we want 4 20 oz iced teas for saturday oct 10
c: lol just drinks for a picnic
c: to 56 oak blvd apt 25a at 2pm
c: card 💳
""",
        "S P S P P",
        items=[I("iced_tea", 4, "bottle_20oz", ["4 20 oz iced teas"])],
        method="delivery",
        method_q="to 56 oak blvd apt 25a",
        addr={"raw": "56 oak blvd apt 25a", "number": "56", "street": "oak blvd", "unit": "apt 25a"},
        time=("clock_time", "at 2pm", "14:00"),
        day=("date", 10, 10, "oct 10"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0205",
        """
c: do u take orders for tuesday? 🤔
b: Yes, you can order up to a week ahead!
c: ok a can of dr pepper delivered tues at 6:30 lol, cash
""",
        "D P",
        items=[I("dr_pepper", 1, "can", ["a can of dr pepper"])],
        method="delivery",
        method_q="delivered",
        time=("clock_time", "at 6:30", "18:30"),
        day=("weekday", "tue", "tues"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0206",
        """
c: ONION RINGS FOR PICKUP THURSDAY OCT 29 AT NOON, CASH, I'LL HAVE A 20
""",
        "P",
        items=[I("onion_rings", 1, None, ["ONION RINGS"])],
        method="pickup",
        method_q="FOR PICKUP",
        time=("clock_time", "AT NOON", "12:00"),
        day=("date", 10, 29, "OCT 29"),
        pay="cash",
        pay_q=["CASH", "I'LL HAVE A 20"],
        change=2000,
    ),
    X(
        "syn-t8-0207",
        """
c: Hi, I'd like to order for Wednesday morning: a coffee with vanilla and two medium hot chocolates.
c: Pickup at 9, please.
c: Name is Rosa.
""",
        "P P P",
        items=[
            I("drip_coffee", 1, None, ["a coffee with vanilla"], [add("vanilla_syrup", "with vanilla")]),
            I("hot_chocolate", 2, "medium", ["two medium hot chocolates"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 9", "09:00"),
        day=("weekday", "wed", "Wednesday"),
        name="Rosa",
        name_q="Rosa",
    ),
    X(
        "syn-t8-0208",
        """
c: HELLO
c: A PERSONAL MEAT LOVERS AND AN XL SUPREME WITH BANANA PEPPERS
c: TO 2126 SPRUCE DR ACROSS FROM THE PARK
c: IN 30 MIN, CASH
c: ACTUALLY SWAP THE MEAT LOVERS FOR A SMALL PEPPERONI THIN CRUST
""",
        "S P P P M",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "small",
                ["A SMALL PEPPERONI THIN CRUST"],
                [add("crust_thin", "THIN CRUST")],
            ),
            I(
                "supreme_pizza",
                1,
                "extra_large",
                ["AN XL SUPREME WITH BANANA PEPPERS"],
                [add("banana_peppers", "WITH BANANA PEPPERS")],
            ),
        ],
        method="delivery",
        method_q="TO 2126 SPRUCE DR",
        addr={
            "raw": "2126 SPRUCE DR ACROSS FROM THE PARK",
            "number": "2126",
            "street": "SPRUCE DR",
            "reference": "ACROSS FROM THE PARK",
        },
        time=("relative", "IN 30 MIN", None),
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t8-0209",
        """
c: 5 bacon burgers, 1 no lettuce
c: 2 sprites
c: pickup sam, card
""",
        "P P P",
        items=[
            I("bacon_burger", 4, None, ["5 bacon burgers, 1 no lettuce"]),
            I("bacon_burger", 1, None, ["5 bacon burgers, 1 no lettuce"], [rm("lettuce", "no lettuce")]),
            I("sprite", 2, None, ["2 sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t8-0210",
        """
c: cb combo no onions + 2 bacon burgers w mustard n a fries
c: for the combo rings n a coke
c: pickup asap, cash
""",
        "P P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["cb combo no onions", "for the combo rings n a coke"],
                [rm("onion", "no onions")],
                combo={"side": "onion_rings", "drink": "coke"},
            ),
            I("bacon_burger", 2, None, ["2 bacon burgers w mustard"], [add("mustard", "w mustard")]),
            I("fries", 1, None, ["a fries"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="cash",
        pay_q="cash",
    ),
]
