"""t5 entries 0001–0012 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm

ENTRIES = [
    X(
        "syn-t5-0001",
        """
c: hey
c: can i get a coffee and two small americanos
c: pickup at 9:15 for ivy, paying cash
b: Got it: 1 drip coffee and 2 small americanos for pickup at 9:15, name Ivy, paying cash. Is that right?
c: yep
c: oh wait make the coffee w almond milk pls
""",
        "S P P C M",
        items=[
            I(
                "drip_coffee",
                1,
                None,
                ["a coffee", "make the coffee w almond milk"],
                [add("almond_milk", "w almond milk")],
            ),
            I("americano", 2, "small", ["two small americanos"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "9:15", "09:15"),
        pay="cash",
        pay_q="paying cash",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t5-0002",
        """
c: yo can i get three margheritas no basil
c: and an xl pepperoni n three orders of garlic knots
c: pickup, card
""",
        "P P P",
        items=[
            I("margherita_pizza", 3, None, ["three margheritas"], [rm("basil", "no basil")]),
            I("pepperoni_pizza", 1, "extra_large", ["an xl pepperoni"]),
            I("garlic_knots", 3, None, ["three orders of garlic knots"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0003",
        """
c: can i get some large hawaiians, a medium cheese w pineapple and an xl veggie w spinach thin crust for pickup
""",
        "P",
        items=[
            I("hawaiian_pizza", None, "large", ["some large hawaiians"]),
            I("cheese_pizza", 1, "medium", ["a medium cheese"], [add("pineapple", "w pineapple")]),
            I(
                "veggie_pizza",
                1,
                "extra_large",
                ["an xl veggie"],
                [add("spinach", "w spinach"), add("crust_thin", "thin crust")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
    ),
    X(
        "syn-t5-0004",
        """
c: HI!!! CAN I GET A SMALL PEPPERONI WITH PINEAPPLE, AN ORDER OF BREADSTICKS AND A DR PEPPER!
c: PICKING IT UP, PAYING CASH, CHANGE FOR A 50 PLEASE!
c: ACTUALLY SCRATCH THE DR PEPPER!!
""",
        "P P M",
        items=[
            I("pepperoni_pizza", 1, "small", ["A SMALL PEPPERONI"], [add("pineapple", "WITH PINEAPPLE")]),
            I("breadsticks", 1, None, ["AN ORDER OF BREADSTICKS"]),
        ],
        method="pickup",
        method_q="PICKING IT UP",
        pay="cash",
        pay_q=["PAYING CASH", "CHANGE FOR A 50"],
        change=5000,
    ),
    X(
        "syn-t5-0005",
        """
c: heyy
c: lemme get two small americanos one w caramel n a large coffee w vanilla, pickup for marcus
""",
        "S P",
        items=[
            I("americano", 1, "small", ["two small americanos"]),
            I(
                "americano",
                1,
                "small",
                ["two small americanos", "one w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
            I("drip_coffee", 1, "large", ["a large coffee"], [add("vanilla_syrup", "w vanilla")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t5-0006",
        """
c: Good evening!
c: I'd like two small veggie pizzas with no cheese and two medium Hawaiian pizzas on gluten free crust.
c: I'll pay by card.
b: Two small veggie pizzas with no cheese and two medium Hawaiian pizzas on gluten-free crust, paying by card. Is that correct?
c: Yes, that's correct.
c: Actually, could you make it just one veggie pizza?
""",
        "S P P C M",
        items=[
            I(
                "veggie_pizza",
                1,
                "small",
                ["two small veggie pizzas", "just one veggie pizza"],
                [rm("cheese", "no cheese")],
            ),
            I(
                "hawaiian_pizza",
                2,
                "medium",
                ["two medium Hawaiian pizzas"],
                [add("crust_gluten_free", "gluten free crust")],
            ),
        ],
        pay="card",
        pay_q="pay by card",
    ),
    X(
        "syn-t5-0007",
        """
c: hi can i get a medium coffee
c: w oat milk pls
c: thx
""",
        "P P S",
        items=[
            I("drip_coffee", 1, "medium", ["a medium coffee", "w oat milk"], [add("oat_milk", "w oat milk")])
        ],
    ),
    X(
        "syn-t5-0008",
        """
c: hey there 👋 putting in an order for the office today 🍔
""",
        "P",
    ),
    X(
        "syn-t5-0009",
        """
c: can i get 3 bacon burgers 1 with no cheese and a sprite
c: deliver to 582 juniper ct
c: card
""",
        "P P P",
        items=[
            I("bacon_burger", 2, None, ["3 bacon burgers"]),
            I("bacon_burger", 1, None, ["3 bacon burgers", "1 with no cheese"], [rm("cheese", "no cheese")]),
            I("sprite", 1, None, ["a sprite"]),
        ],
        method="delivery",
        method_q="deliver to 582 juniper ct",
        addr={"raw": "582 juniper ct", "number": "582", "street": "juniper ct"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0010",
        """
c: hi
c: do u guys have diet coke
b: Sorry, just Coke, Sprite and lemonade!
c: ok then a 20 oz coke, onion rings and fries
c: deliver asap to 23 fairmont dr, card
""",
        "S Q P P",
        items=[
            I("coke", 1, None, ["a 20 oz coke"], unmatched_variant="20 oz"),
            I("onion_rings", 1, None, ["onion rings"]),
            I("fries", 1, None, ["fries"]),
        ],
        method="delivery",
        method_q="deliver",
        time=("asap", "asap", None),
        addr={"raw": "23 fairmont dr", "number": "23", "street": "fairmont dr"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t5-0011",
        """
c: GOOD MORNING!
c: I WOULD LIKE ONE LARGE AMERICANO PLEASE!
c: I WILL PICK IT UP. MY NAME IS JUNE.
b: One large Americano for pickup, name June. Is that right?
c: YES, THANK YOU!
c: OH! COULD YOU PUT SKIM MILK IN IT PLEASE!
""",
        "S P P C M",
        items=[
            I(
                "americano",
                1,
                "large",
                ["ONE LARGE AMERICANO", "PUT SKIM MILK IN IT"],
                [add("skim_milk", "SKIM MILK")],
            ),
        ],
        method="pickup",
        method_q="I WILL PICK IT UP",
        name="June",
        name_q="JUNE",
    ),
    X(
        "syn-t5-0012",
        """
c: Hello, I'd like to place an order for pickup.
c: Two cheeseburgers, one of them with mayo.
c: And two vanilla milkshakes.
c: I'll pay cash.
""",
        "P P P P",
        items=[
            I("cheeseburger", 1, None, ["Two cheeseburgers"]),
            I(
                "cheeseburger",
                1,
                None,
                ["Two cheeseburgers", "one of them with mayo"],
                [add("mayo", "with mayo")],
            ),
            I("milkshake", 2, "vanilla", ["two vanilla milkshakes"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="pay cash",
    ),
]
