"""fresh4 a-fresh4-057–084 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm, sub

ENTRIES = [
    F(
        "a-fresh4-057",
        """
c: Hi, could I get the big burger and two regular fries?
c: Delivered to 210 Ocean Ave.
c: Cash, please.
""",
        "P P P",
        start="Fri 21:00",
        items=[
            I(None, 1, None, ["the big burger"], unmatched="the big burger", flag="item_menu_match"),
            I("fries", 2, "regular", ["two regular fries"]),
        ],
        method="delivery",
        method_q="Delivered to 210 Ocean Ave",
        addr={"raw": "210 Ocean Ave", "number": "210", "street": "Ocean Ave"},
        pay="cash",
        pay_q="Cash",
        annotation="'the big burger' fits the double cheeseburger or the bacon burger (as fresh2 049): unclear, asked.",
    ),
    F(
        "a-fresh4-058",
        """
c: cheeseburger
c: n regular fries
c: pickup
c: cash
b: Got it: 1 Cheeseburger and 1 regular Fries, pickup, paying cash. Is that right?
c: ye
c: make the fries large tho
""",
        "P P P P C M",
        start="Tue 21:20",
        items=[
            I("cheeseburger", 1, "single", ["cheeseburger"]),
            I("fries", 1, "large", ["regular fries", "make the fries large"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-059",
        """
c: Hi, I'd like to order for Friday: a large meat lovers and a large veggie.
c: Pickup at 7:30 pm.
c: Paying cash, thanks.
""",
        "P P P",
        start="Mon 13:30",
        items=[
            I("meat_lovers_pizza", 1, "large", ["a large meat lovers"]),
            I("veggie_pizza", 1, "large", ["a large veggie"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 7:30 pm", "19:30"),
        day=("weekday", "fri", "Friday"),
        pay="cash",
        pay_q="Paying cash",
    ),
    F(
        "a-fresh4-060",
        """
c: hi! 🎉 6 chocolate croissants n 6 blueberry muffins for sunday, pickup for gwen 🥐
""",
        "P",
        start="Wed 13:00",
        items=[
            I("croissant", 6, "chocolate", ["6 chocolate croissants"]),
            I("muffin", 6, "blueberry", ["6 blueberry muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for sunday"),
        day=("weekday", "sun", "sunday"),
        name="Gwen",
        name_q="gwen",
    ),
    F(
        "a-fresh4-061",
        """
c: GOOD AFTERNOON
c: DO YOU HAVE DIET COKE?
b: Sorry, no Diet Coke. We have Coke, Sprite and lemonade.
c: ALRIGHT. TWO CHEESEBURGERS, A LARGE FRIES AND A DR PEPPER THEN
c: FOR PICKUP
""",
        "S Q P P",
        start="Sun 15:10",
        items=[
            I("cheeseburger", 2, "single", ["TWO CHEESEBURGERS"]),
            I("fries", 1, "large", ["A LARGE FRIES"]),
            I(None, 1, None, ["A DR PEPPER"], unmatched="A DR PEPPER"),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        annotation="Corner Patty has no Dr Pepper: an off-menu line, asked.",
    ),
    F(
        "a-fresh4-062",
        """
c: medium pepperoni w jalapenos for pickup, cash 🍕
c: oh can u do mushrooms instead of jalapenos 🍄
""",
        "P M",
        start="Sun 18:30",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "medium",
                ["medium pepperoni w jalapenos", "mushrooms instead of jalapenos"],
                [add("mushrooms", "mushrooms instead of jalapenos")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-063",
        """
c: hi, 2 lg lattes n 2 plain bagels for pickup, name tess
c: do u have gluten free bagels?
b: Sorry, not at the moment.
c: ah ok
c: nvm then, cancel it pls, we'll grab something elsewhere
""",
        "P Q S X",
        start="Thu 07:30",
        items=[
            I("latte", 2, "large", ["2 lg lattes"]),
            I("bagel", 2, "plain", ["2 plain bagels"]),
        ],
        method="pickup",
        method_q="for pickup",
        name="Tess",
        name_q="tess",
        decision="cancelled",
        decision_q="cancel it",
    ),
    F(
        "a-fresh4-064",
        """
c: hey!
c: 4 cheeseburgers for the party, 2 w grilled mushrooms on top, n 2 lg fries
c: pickup in 30, card
""",
        "S P P",
        start="Sat 16:00",
        items=[
            I("cheeseburger", 2, "single", ["4 cheeseburgers"]),
            I(
                "cheeseburger",
                2,
                "single",
                ["4 cheeseburgers", "2 w grilled mushrooms on top"],
                [offmod("w grilled mushrooms on top")],
            ),
            I("fries", 2, "large", ["2 lg fries"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 30", None),
        pay="card",
        pay_q="card",
        annotation="Grilled mushrooms aren't on the menu: a not_on_menu add on two of the four, asked.",
    ),
    F(
        "a-fresh4-065",
        """
c: 2 VEGGIE BURGERS AND ONION RINGS FOR PICKUP NOW, ACTUALY NO MAKE THAT TOMOROW AT 1PM
""",
        "P",
        start="Tue 20:30",
        items=[
            I("veggie_burger", 2, None, ["2 VEGGIE BURGERS"]),
            I("onion_rings", 1, None, ["ONION RINGS"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        time=("clock_time", "AT 1PM", "13:00"),
        day=("tomorrow", "TOMOROW"),
        annotation="'now' is replaced in the same message by tomorrow at 1 pm.",
    ),
    F(
        "a-fresh4-066",
        """
c: hi i ordered a lg latte for pickup under bo n already paid, got a screenshot
c: also do u have oat milk
""",
        "PC Q",
        start="Fri 09:40",
        order=False,
        annotation="A claim about an order not in this chat: PAYMENT_CLAIM about the placed order; no gold order.",
    ),
    F(
        "a-fresh4-067",
        """
c: hi
c: lg americano
c: n a sesame bagel
c: name is rui
c: card
c: can u put honey on the bagel
""",
        "S P P P P P",
        start="Sun 11:00",
        items=[
            I("americano", 1, "large", ["lg americano"]),
            I("bagel", 1, "sesame", ["a sesame bagel", "honey on the bagel"], [offmod("honey")]),
        ],
        pay="card",
        pay_q="card",
        name="Rui",
        name_q="rui",
    ),
    F(
        "a-fresh4-068",
        """
c: hey!
c: for the party: 4 lg lattes, 2 hot chocs no whip, 6 choc croissants, 4 blueberry muffins n 3 everything bagels w cream cheese, name is wes
""",
        "S P",
        start="Sat 08:10",
        items=[
            I("latte", 4, "large", ["4 lg lattes"]),
            I("hot_chocolate", 2, "medium", ["2 hot chocs no whip"], [rm("whipped_cream", "no whip")]),
            I("croissant", 6, "chocolate", ["6 choc croissants"]),
            I("muffin", 4, "blueberry", ["4 blueberry muffins"]),
            I(
                "bagel",
                3,
                "everything",
                ["3 everything bagels w cream cheese"],
                [add("cream_cheese", "w cream cheese")],
            ),
        ],
        name="Wes",
        name_q="wes",
    ),
    F(
        "a-fresh4-069",
        """
c: HI I PLACED AN ORDER EARLIER AND ALREADY PAID ONLINE, JUST LETTING YOU KNOW
""",
        "PC",
        start="Wed 19:00",
        order=False,
    ),
    F(
        "a-fresh4-070",
        """
c: hey
c: 2 lg pepperoni n a lg veggie for pickup, card
""",
        "S P",
        start="Thu 12:05",
        items=[
            I("pepperoni_pizza", 2, "large", ["2 lg pepperoni"]),
            I("veggie_pizza", 1, "large", ["a lg veggie"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh4-071",
        """
c: medium supreme pls 🍕
c: n add a garlic knots, r they vegan? 🌱
c: cash 💵
""",
        "P P/Q P",
        start="Mon 20:40",
        items=[
            I("supreme_pizza", 1, "medium", ["medium supreme"]),
            I("garlic_knots", 1, None, ["a garlic knots"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-072",
        """
c: Hi, does the veggie burger come with cheese?
b: It doesn't, but you can add cheese.
c: OK, 3 veggie burgers with cheese, 3 cokes, pickup at 12:45. Card.
c: Actually, please swap the cokes for lemonades.
""",
        "Q P M",
        start="Mon 12:00",
        items=[
            I("veggie_burger", 3, None, ["3 veggie burgers with cheese"], [add("cheese", "with cheese")]),
            I("lemonade", 3, None, ["3 cokes", "swap the cokes for lemonades"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:45", "12:45"),
        pay="card",
        pay_q="Card",
    ),
    F(
        "a-fresh4-073",
        """
c: hi 👋
c: can i order for tomorrow? if so 2 bacon burgers n a choc shake, pickup at 12:30 🍔
""",
        "S P/D",
        start="Wed 21:30",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("milkshake", 1, "chocolate", ["a choc shake"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12:30", "12:30"),
        day=("tomorrow", "tomorrow"),
        annotation="Asks whether they can order ahead and orders in the same message: PLACE_ORDER + secondary "
        "DELIVERY_QUESTION.",
    ),
    F(
        "a-fresh4-074",
        """
c: hi my bagel this morning had sesame on it
c: i told them no sesame, im allergic, luckily i noticed b4 eating
""",
        "PR PR",
        start="Tue 12:30",
        order=False,
        annotation="Nobody is hurt (noticed before eating): urgency normal.",
    ),
    F(
        "a-fresh4-075",
        """
c: ARE YOU HIRING DELIVERY DRIVERS?
""",
        "O",
        start="Thu 15:00",
    ),
    F(
        "a-fresh4-076",
        """
c: med latte w lavender syrup pls 💜 n a plain croissant
c: pickup for nora 😊
""",
        "P P",
        start="Fri 10:20",
        items=[
            I("latte", 1, "medium", ["med latte w lavender syrup"], [offmod("w lavender syrup")]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Nora",
        name_q="nora",
    ),
    F(
        "a-fresh4-077",
        """
c: 2 xl pepperoni
c: n a xl hawaiian
c: + some drinks
b: Which drinks, and how many? We have Coke, Diet Coke, Sprite, Dr Pepper and iced tea.
c: 2 liter coke n 2 liter sprite. pickup
""",
        "P P P P",
        start="Sat 20:10",
        items=[
            I("pepperoni_pizza", 2, "extra_large", ["2 xl pepperoni"]),
            I("hawaiian_pizza", 1, "extra_large", ["a xl hawaiian"]),
            I("coke", 1, "two_liter", ["2 liter coke"]),
            I("sprite", 1, "two_liter", ["2 liter sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        annotation="'some drinks' is settled by the next message: the vague line is dropped.",
    ),
    F(
        "a-fresh4-078",
        """
c: hi can i get a double, a bacon n 2 rings
c: to 5 grove st
""",
        "P P",
        start="Sun 13:40",
        items=[
            I("cheeseburger", 1, "double", ["a double"]),
            I("bacon_burger", 1, None, ["a bacon"]),
            I("onion_rings", 2, None, ["2 rings"]),
        ],
        method="delivery",
        method_q="to 5 grove st",
        addr={"raw": "5 grove st", "number": "5", "street": "grove st"},
        annotation="Items by name only: 'a double' is the double cheeseburger, 'a bacon' the bacon burger, "
        "'rings' the onion rings.",
    ),
    F(
        "a-fresh4-079",
        """
c: a latte, one of the bigger ones
c: n a choc chip muffin
c: pickup for ivo
""",
        "P P P",
        start="Mon 07:50",
        items=[
            I("latte", 1, None, ["a latte, one of the bigger ones"], flag="item_variant"),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ivo",
        name_q="ivo",
        annotation="'one of the bigger ones' fits medium or large: the size is unclear, asked.",
    ),
    F(
        "a-fresh4-080",
        """
c: where is my order?? been waiting 50 min
c: ordered under kev, delivery to 9 bay st
""",
        "ST ST",
        start="Fri 20:00",
        order=False,
    ),
    F(
        "a-fresh4-081",
        """
c: order for tmrw at 12:30: 4 lg cheese n 2 lg pepperoni, is there a discount for big orders?
c: cash
""",
        "P/Q P",
        start="Wed 16:40",
        items=[
            I("cheese_pizza", 4, "large", ["4 lg cheese"]),
            I("pepperoni_pizza", 2, "large", ["2 lg pepperoni"]),
        ],
        time=("clock_time", "at 12:30", "12:30"),
        day=("tomorrow", "tmrw"),
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-082",
        """
c: Hello,
c: I would like to order two cheeseb
""",
        "S U",
        start="Tue 14:10",
        annotation="Cut off mid-word: UNKNOWN (as fresh 001, fresh3 075).",
    ),
    F(
        "a-fresh4-083",
        """
c: Four small cappuccinos, two of them with skim milk, please.
c: Pickup for Marco.
""",
        "P P",
        start="Thu 07:15",
        items=[
            I("cappuccino", 2, "small", ["Four small cappuccinos"]),
            I(
                "cappuccino",
                2,
                "small",
                ["Four small cappuccinos", "two of them with skim milk"],
                [sub("whole_milk", "skim_milk", "with skim milk")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        name="Marco",
    ),
    F(
        "a-fresh4-084",
        """
c: Hello, two large cheese pizzas with sausage for pickup.
c: Name is Graham.
c: Paying by card.
c: Sorry, could you do pepperoni instead of sausage on both?
""",
        "P P P M",
        start="Tue 12:15",
        items=[
            I(
                "cheese_pizza",
                2,
                "large",
                ["two large cheese pizzas with sausage", "pepperoni instead of sausage on both"],
                [add("pepperoni", "pepperoni instead of sausage")],
            ),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="Paying by card",
        name="Graham",
    ),
]
