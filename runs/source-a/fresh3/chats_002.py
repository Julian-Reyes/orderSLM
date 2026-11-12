"""fresh3 a-fresh3-021–050 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm, sub

ENTRIES = [
    F(
        "a-fresh3-021",
        """
c: does the cheeseburger come w pickles
b: Yes: cheese, lettuce, tomato, onion, pickles and ketchup.
c: ok 3 cheeseburgers no pickles, pickup, card
""",
        "Q P",
        start="Mon 12:30",
        items=[I("cheeseburger", 3, None, ["3 cheeseburgers no pickles"], [rm("pickle", "no pickles")])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-022",
        """
c: 3 cheeseburgers, 1 of them a double, pickup paying cash
""",
        "P",
        start="Tue 18:00",
        items=[
            I("cheeseburger", 2, None, ["3 cheeseburgers"]),
            I("cheeseburger", 1, "double", ["3 cheeseburgers", "1 of them a double"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="paying cash",
        annotation="Corner Patty has no milk or crust; the patty plays that part: 3 cheeseburgers, 1 double.",
    ),
    F(
        "a-fresh3-023",
        """
c: hiii 🍕 a large pepperoni for pickup at 8 pls, card
c: omg nvm my friends already got food 😅 cancel it pls
""",
        "P X",
        start="Fri 19:15",
        items=[I("pepperoni_pizza", 1, "large", ["a large pepperoni"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8", "20:00"),
        pay="card",
        pay_q="card",
        decision="cancelled",
        decision_q="cancel it",
    ),
    F(
        "a-fresh3-024",
        """
c: Hi, I'd like a medium latte and the same as last time for my colleague.
b: I'm sorry, I can't see past orders here. What did your colleague have?
c: I'm not sure, I'll ask her. Actually, make my latte a large.
""",
        "P M",
        start="Wed 11:40",
        items=[
            I("latte", 1, "large", ["a medium latte", "make my latte a large"]),
            I(
                None,
                1,
                None,
                ["the same as last time"],
                unmatched="the same as last time",
                flag="item_menu_match",
            ),
        ],
        annotation="The colleague's order is never settled: unmatched, ambiguous.",
    ),
    F(
        "a-fresh3-025",
        """
c: HI, 2 VEGGIE BURGERS AND A LEMONADE FOR PICKUP
c: CASH
b: Got it: 2 Veggie Burgers and 1 Lemonade for pickup, paying cash. Is that right?
c: YES
c: OH AND ADD ONION RINGS
""",
        "P P C M",
        start="Thu 12:50",
        items=[
            I("veggie_burger", 2, None, ["2 VEGGIE BURGERS"]),
            I("lemonade", 1, None, ["A LEMONADE"]),
            I("onion_rings", 1, None, ["ONION RINGS"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        pay="cash",
        pay_q="CASH",
    ),
    F(
        "a-fresh3-026",
        """
c: good evening, i would like 3 medium supreme pizzas please
c: but please leave the olives off two of them
c: delivered to 618 brookside ln
c: i will pay with card, thank you
""",
        "P P P P",
        start="Sat 18:40",
        items=[
            I("supreme_pizza", 1, "medium", ["3 medium supreme pizzas"]),
            I(
                "supreme_pizza",
                2,
                "medium",
                ["3 medium supreme pizzas", "leave the olives off two of them"],
                [rm("olives", "leave the olives off")],
            ),
        ],
        method="delivery",
        method_q="delivered to 618 brookside ln",
        addr={"raw": "618 brookside ln", "number": "618", "street": "brookside ln"},
        pay="card",
        pay_q="pay with card",
    ),
    F(
        "a-fresh3-027",
        """
c: hi can i get 2 medium cappuccinos
c: n a cinnamon raisin bagel
c: pickup for dana, card
c: oh n can u put peanut butter on the bagel
""",
        "P P P P",
        start="Tue 12:10",
        items=[
            I("cappuccino", 2, "medium", ["2 medium cappuccinos"]),
            I(
                "bagel",
                1,
                "cinnamon_raisin",
                ["a cinnamon raisin bagel", "put peanut butter on the bagel"],
                [offmod("put peanut butter on the bagel")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Dana",
        name_q="dana",
    ),
    F(
        "a-fresh3-028",
        """
c: Hi, a large BBQ chicken pizza and two cans of Dr Pepper for pickup at 6:15.
c: I'll pay cash.
""",
        "P P",
        start="Wed 17:20",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["a large BBQ chicken pizza"]),
            I("dr_pepper", 2, "can", ["two cans of Dr Pepper"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6:15", "18:15"),
        pay="cash",
        pay_q="pay cash",
    ),
    F(
        "a-fresh3-029",
        """
c: good morning dear
c: i need to place an order for my book club if you dont mind: 4 medium drip coffees, 2 with almond milk, a large hot chocolate, 3 blueberry muffins, 2 plain croissants and a sesame bagel with cream cheese
c: the name is margaret, i will pick it up at 10
c: i will pay cash
""",
        "S P P P",
        start="Thu 08:30",
        items=[
            I("drip_coffee", 2, "medium", ["4 medium drip coffees"]),
            I(
                "drip_coffee",
                2,
                "medium",
                ["4 medium drip coffees", "2 with almond milk"],
                [add("almond_milk", "with almond milk")],
            ),
            I("hot_chocolate", 1, "large", ["a large hot chocolate"]),
            I("muffin", 3, "blueberry", ["3 blueberry muffins"]),
            I("croissant", 2, "plain", ["2 plain croissants"]),
            I(
                "bagel",
                1,
                "sesame",
                ["a sesame bagel with cream cheese"],
                [add("cream_cheese", "with cream cheese")],
            ),
        ],
        method="pickup",
        method_q="pick it up",
        time=("clock_time", "at 10", "10:00"),
        pay="cash",
        pay_q="pay cash",
        name="Margaret",
        name_q="margaret",
    ),
    F(
        "a-fresh3-030",
        """
c: do u have gluten free crust
b: Yes, gluten-free crust is available on any pizza.
c: 🤔
""",
        "Q U",
        start="Mon 16:45",
    ),
    F(
        "a-fresh3-031",
        """
c: Hi, can I get 2 bacon burgers and a chocolate shake for pickup at 7:30?
c: Paying by card.
""",
        "P P",
        start="Sat 13:40",
        items=[
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 7:30", "19:30"),
        pay="card",
        pay_q="Paying by card",
    ),
    F(
        "a-fresh3-032",
        """
c: Hello, I'm in town for a conference and we need breakfast for about 60 people on Friday.
c: Is there someone I could speak with about catering?
b: Of course, I'll ask our manager to reach out to you here.
c: Thank you, I'll wait to hear from them.
""",
        "P HU@n S@n",
        start="Tue 10:15",
        time=("ambiguous", "on Friday"),
        day=("weekday", "fri", "Friday"),
        annotation="As fresh 050 and fresh2 089: an order announced with no items is PLACE_ORDER (empty gold order, "
        "asked), then a request for staff. 'on Friday' with no time: ambiguous, day fri (2026-11-12 rule).",
    ),
    F(
        "a-fresh3-033",
        """
c: 2 cheeseburgers
c: n that one u had on special last week
c: actually make the cheeseburgers doubles
c: deliver to 55 ivanhoe st
""",
        "P P M P",
        start="Fri 21:10",
        items=[
            I("cheeseburger", 2, "double", ["2 cheeseburgers", "make the cheeseburgers doubles"]),
            I(
                None,
                1,
                None,
                ["that one u had on special last week"],
                unmatched="that one u had on special last week",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="deliver to 55 ivanhoe st",
        addr={"raw": "55 ivanhoe st", "number": "55", "street": "ivanhoe st"},
    ),
    F(
        "a-fresh3-034",
        """
c: hi do u have any dairy free milk
b: We have oat milk and almond milk.
c: ok a few lattes w oat milk then
c: n a banana nut muffin
""",
        "Q P P",
        start="Wed 09:30",
        items=[
            I(
                "latte",
                None,
                None,
                ["a few lattes w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
    ),
    F(
        "a-fresh3-035",
        """
c: DO YOU GUYS HAVE STUFFED CRUST?
b: Yes, stuffed crust is available on any pizza.
c: GREAT, 2 LARGE PEPPERONI WITH STUFFED CRUST
c: READY AT 6:45 PLEASE
c: CARD
""",
        "Q P P P",
        start="Tue 13:10",
        items=[
            I(
                "pepperoni_pizza",
                2,
                "large",
                ["2 LARGE PEPPERONI WITH STUFFED CRUST"],
                [add("crust_stuffed", "WITH STUFFED CRUST")],
            )
        ],
        time=("clock_time", "AT 6:45", "18:45"),
        pay="card",
        pay_q="CARD",
    ),
    F(
        "a-fresh3-036",
        """
c: hello, i would like to order 2 medium cheese pizzas for my grandchildren
c: it is for saturday please
c: i will pay cash
""",
        "P P P",
        start="Wed 16:00",
        items=[I("cheese_pizza", 2, "medium", ["2 medium cheese pizzas"])],
        time=("ambiguous", "for saturday"),
        day=("weekday", "sat", "saturday"),
        pay="cash",
        pay_q="pay cash",
    ),
    F(
        "a-fresh3-037",
        """
c: hey can i order lunch for the office for nov 19
c: 5 cheeseburgers n 5 sprites
c: at 12:30, card
""",
        "P P P",
        start="Mon 11:30",
        items=[
            I("cheeseburger", 5, None, ["5 cheeseburgers"]),
            I("sprite", 5, None, ["5 sprites"]),
        ],
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", 11, 19, "nov 19"),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-038",
        """
c: Hi, I'd like a veggie burger and onion rings delivered to 302 Quincy St.
c: I'll pay by card.
c: Sorry, please cancel that. My roommate just ordered for both of us.
""",
        "P P X",
        start="Thu 19:00",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        method="delivery",
        method_q="delivered to 302 Quincy St",
        addr={"raw": "302 Quincy St", "number": "302", "street": "Quincy St"},
        pay="card",
        pay_q="pay by card",
        decision="cancelled",
        decision_q="cancel that",
    ),
    F(
        "a-fresh3-039",
        """
c: hey 👋
c: which burger is the biggest
b: The double cheeseburger and the bacon burger are our biggest.
c: ok the big one then, delivered to 14 alder ct
""",
        "S Q P",
        start="Sun 18:20",
        items=[I(None, 1, None, ["the big one"], unmatched="the big one", flag="item_menu_match")],
        method="delivery",
        method_q="delivered to 14 alder ct",
        addr={"raw": "14 alder ct", "number": "14", "street": "alder ct"},
        annotation="Two burgers were named as the biggest: 'the big one' is still unclear (as fresh2 049).",
    ),
    F(
        "a-fresh3-040",
        """
c: hi a large cappuccino n a plain croissant for pickup, name jo
c: paying cash
b: Got it, Jo: 1 large cappuccino and 1 plain croissant for pickup, paying cash. Is that right?
c: yep
c: actually ill pay w card
""",
        "P P C M!o",
        start="Fri 08:20",
        items=[
            I("cappuccino", 1, "large", ["a large cappuccino"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="ill pay w card",
        name="Jo",
        name_q="jo",
    ),
    F(
        "a-fresh3-041",
        """
c: good afternoon 😊 does the hawaiian have ham?
b: Yes, ham and pineapple.
c: lovely, one medium hawaiian delivered to 140 orchard ln at 6 please 🍍
c: oh dear, i just remembered we're out tonight. could it be thursday at 6 instead?
""",
        "Q P M",
        start="Tue 15:30",
        items=[I("hawaiian_pizza", 1, "medium", ["one medium hawaiian"])],
        method="delivery",
        method_q="delivered to 140 orchard ln",
        time=("clock_time", "at 6", "18:00"),
        day=("weekday", "thu", "thursday"),
        addr={"raw": "140 orchard ln", "number": "140", "street": "orchard ln"},
    ),
    F(
        "a-fresh3-042",
        """
c: hey 2 lg pepperoni n an order of breadsticks to 501 union st, card
b: Got it: 2 large Pepperoni Pizzas and 1 order of Breadsticks, delivered to 501 Union St, paying by card. Is that right?
c: ya
c: oh wait no breadsticks
""",
        "P C M",
        start="Thu 12:20",
        items=[I("pepperoni_pizza", 2, "large", ["2 lg pepperoni"])],
        method="delivery",
        method_q="to 501 union st",
        addr={"raw": "501 union st", "number": "501", "street": "union st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-043",
        """
c: hello there
c: something warm for my grandson, not coffee
b: We have hot chocolate! Would that work?
c: perfect, a small one
c: and a plain croissant
c: pickup, name is harold
c: card
""",
        "S P P P P P",
        start="Sat 10:40",
        items=[
            I("hot_chocolate", 1, "small", ["something warm", "a small one"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Harold",
        name_q="harold",
        annotation="'something warm, not coffee' is settled by the business's offer and 'perfect': hot chocolate.",
    ),
    F(
        "a-fresh3-044",
        """
c: HI! PARTY TOMORROW
c: NEED 6 BLUEBERRY MUFFINS
c: AND 6 CHOCOLATE CROISSANTS
c: PICKUP AT 9:30 TOMORROW MORNING
c: NAME IS SUE, CARD
""",
        "S P P P P",
        start="Fri 11:00",
        items=[
            I("muffin", 6, "blueberry", ["6 BLUEBERRY MUFFINS"]),
            I("croissant", 6, "chocolate", ["6 CHOCOLATE CROISSANTS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT 9:30", "09:30"),
        day=("tomorrow", "TOMORROW"),
        pay="card",
        pay_q="CARD",
        name="Sue",
        name_q="SUE",
    ),
    F(
        "a-fresh3-045",
        """
c: Hi there!
c: Could I get one of your larger pepperoni pizzas? Not sure which size.
""",
        "S P",
        start="Mon 17:05",
        items=[I("pepperoni_pizza", 1, None, ["one of your larger pepperoni pizzas"], flag="item_variant")],
        annotation="'one of your larger' fits large or extra large: the size is stated unclearly (ambiguous), asked.",
    ),
    F(
        "a-fresh3-046",
        """
c: Hello! Could we get 4 cheeseburgers, two of them without onions?
c: Delivered to the Grant Hotel, 200 Grant Ave, room 418.
c: We'll pay cash.
""",
        "P P P",
        start="Wed 19:30",
        items=[
            I("cheeseburger", 2, None, ["4 cheeseburgers"]),
            I(
                "cheeseburger",
                2,
                None,
                ["4 cheeseburgers", "two of them without onions"],
                [rm("onion", "without onions")],
            ),
        ],
        method="delivery",
        method_q="Delivered to the Grant Hotel",
        addr={
            "raw": "the Grant Hotel, 200 Grant Ave, room 418",
            "number": "200",
            "street": "Grant Ave",
            "unit": "room 418",
            "reference": "the Grant Hotel",
        },
        pay="cash",
        pay_q="pay cash",
    ),
    F(
        "a-fresh3-047",
        """
c: hey can i get a large americano n a breakfast sandwich for pickup wednesday
c: name kim
c: card
""",
        "P P P",
        start="Mon 14:00",
        items=[
            I("americano", 1, "large", ["a large americano"]),
            I("breakfast_sandwich", 1, None, ["a breakfast sandwich"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "wednesday"),
        day=("weekday", "wed", "wednesday"),
        pay="card",
        pay_q="card",
        name="Kim",
        name_q="kim",
    ),
    F(
        "a-fresh3-048",
        """
c: medium meat lovers w pesto drizzle n a 20 oz sprite
c: pickup at 7, card
""",
        "P P",
        start="Thu 16:50",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                "medium",
                ["medium meat lovers w pesto drizzle"],
                [offmod("w pesto drizzle")],
            ),
            I("sprite", 1, "bottle_20oz", ["a 20 oz sprite"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7", "19:00"),
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-049",
        """
c: QUICK QUESTION FOR MY PARTY GAME: HOW MANY PLAYERS ARE ON A BASEBALL TEAM?
""",
        "O",
        start="Sat 16:00",
    ),
    F(
        "a-fresh3-050",
        """
c: hello
c: one cheeseburger please
c: and regular fries
c: pickup, cash
b: Got it: 1 Cheeseburger and 1 regular Fries for pickup, paying cash. Is that right?
c: yes
c: could you make the fries large instead
""",
        "S P P P C M",
        start="Tue 13:15",
        items=[
            I("cheeseburger", 1, None, ["one cheeseburger"]),
            I("fries", 1, "large", ["regular fries", "make the fries large"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
]
