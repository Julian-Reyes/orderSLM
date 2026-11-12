"""fresh3 a-fresh3-051–080 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm

ENTRIES = [
    F(
        "a-fresh3-051",
        """
c: hey
c: is the uhh
c: thing w the
c: ok nvm the other one
""",
        "S U U U",
        start="Tue 08:40",
    ),
    F(
        "a-fresh3-052",
        """
c: hello dear 😊 i'd like to order a large cheese pizza and a large hawaiian for my grandson's birthday on the 21st at 5:30
c: please deliver to 3 sycamore ln 🎂
""",
        "P P",
        start="Mon 14:00",
        items=[
            I("cheese_pizza", 1, "large", ["a large cheese pizza"]),
            I("hawaiian_pizza", 1, "large", ["a large hawaiian"]),
        ],
        method="delivery",
        method_q="deliver to 3 sycamore ln",
        time=("clock_time", "at 5:30", "17:30"),
        day=("date", None, 21, "the 21st"),
        addr={"raw": "3 sycamore ln", "number": "3", "street": "sycamore ln"},
    ),
    F(
        "a-fresh3-053",
        """
c: can i order now for friday?
b: Yes, we take orders up to a week ahead. What would you like?
c: 2 veggie burgers n 2 lemonades friday at 6:30 to 77 oak st
""",
        "D P",
        start="Tue 15:00",
        items=[
            I("veggie_burger", 2, None, ["2 veggie burgers"]),
            I("lemonade", 2, None, ["2 lemonades"]),
        ],
        method="delivery",
        method_q="to 77 oak st",
        time=("clock_time", "at 6:30", "18:30"),
        day=("weekday", "fri", "friday"),
        addr={"raw": "77 oak st", "number": "77", "street": "oak st"},
    ),
    F(
        "a-fresh3-054",
        """
c: 5 medium hot chocolates
c: 3 w caramel
""",
        "P P",
        start="Wed 10:10",
        items=[
            I("hot_chocolate", 2, "medium", ["5 medium hot chocolates"]),
            I(
                "hot_chocolate",
                3,
                "medium",
                ["5 medium hot chocolates", "3 w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
        ],
    ),
    F(
        "a-fresh3-055",
        """
c: hey there
c: can i get a double cheeseburger n a vanilla shake, card
""",
        "S P",
        start="Thu 17:45",
        items=[
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
            I("milkshake", 1, "vanilla", ["a vanilla shake"]),
        ],
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-056",
        """
c: do u have whole bean coffee to take home?
b: Sorry, we don't sell whole bean coffee, only drinks and food on the menu.
c: ok then 6 large coffees for the party at 11
""",
        "Q P",
        start="Mon 07:40",
        items=[I("drip_coffee", 6, "large", ["6 large coffees"])],
        time=("clock_time", "at 11", "11:00"),
    ),
    F(
        "a-fresh3-057",
        """
c: hey
c: 1 large margherita
c: n is the bbq chicken spicy, if not add a medium one
b: It isn't spicy: BBQ sauce, cheese, grilled chicken and red onions.
c: ok add it
c: pickup
c: card
""",
        "S P P/Q P P P",
        start="Fri 18:30",
        items=[
            I("margherita_pizza", 1, "large", ["1 large margherita"]),
            I("bbq_chicken_pizza", 1, "medium", ["add a medium one", "ok add it"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        annotation="Message 2 adds a pizza on a condition and asks about it: PLACE_ORDER + MENU_QUESTION; 'ok add it' "
        "after the answer keeps it.",
    ),
    F(
        "a-fresh3-058",
        """
c: morning
c: 4 lattes
c: medium
c: n 2 blueberry muffins
c: pickup for lena
c: card
c: sorry make it 5 lattes
""",
        "S P P P P P M",
        start="Thu 08:05",
        items=[
            I("latte", 5, "medium", ["4 lattes", "medium", "make it 5 lattes"]),
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Lena",
        name_q="lena",
    ),
    F(
        "a-fresh3-059",
        """
c: hey 🎉 6 cheeseburgers n 3 large fries for pickup
c: paying card 💳
b: Got it: 6 Cheeseburgers and 3 large Fries for pickup, paying by card. Is that right?
c: yep 👍
c: oh n add bacon to all the burgers 🥓
""",
        "P P C M",
        start="Sat 12:30",
        items=[
            I(
                "cheeseburger",
                6,
                None,
                ["6 cheeseburgers", "add bacon to all the burgers"],
                [add("bacon", "add bacon")],
            ),
            I("fries", 3, "large", ["3 large fries"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="paying card",
        annotation="As fresh 041: the added topping comes after the yes, so it is a change to the placed order.",
    ),
    F(
        "a-fresh3-060",
        """
c: Hi, could I get a medium pepperoni delivered to the Lakeview Inn, 900 Lakeview Blvd, room 12, tonight at 8?
c: Actually, we'll be out tonight. Could you make it tomorrow at 8 instead?
""",
        "P M",
        start="Sat 16:00",
        items=[I("pepperoni_pizza", 1, "medium", ["a medium pepperoni"])],
        method="delivery",
        method_q="delivered to the Lakeview Inn",
        time=("clock_time", "at 8", "20:00"),
        day=("tomorrow", "tomorrow"),
        addr={
            "raw": "the Lakeview Inn, 900 Lakeview Blvd, room 12",
            "number": "900",
            "street": "Lakeview Blvd",
            "unit": "room 12",
            "reference": "the Lakeview Inn",
        },
    ),
    F(
        "a-fresh3-061",
        """
c: hi
c: 3 bacon burgers
c: do they come w cheese
b: Yes, the bacon burger comes with cheese.
c: ok cool n 3 cokes
c: deliver to 1200 harbor dr, cash
b: Got it: 3 Bacon Burgers and 3 Cokes, delivered to 1200 Harbor Dr, paying cash. Is that right?
c: yep thats it
""",
        "S P Q P P C",
        start="Tue 12:10",
        items=[
            I("bacon_burger", 3, None, ["3 bacon burgers"]),
            I("coke", 3, None, ["3 cokes"]),
        ],
        method="delivery",
        method_q="deliver to 1200 harbor dr",
        addr={"raw": "1200 harbor dr", "number": "1200", "street": "harbor dr"},
        pay="cash",
        pay_q="cash",
        decision="confirmed",
        decision_q="yep thats it",
    ),
    F(
        "a-fresh3-062",
        """
c: hi ☀️ for tmrw at 12:15 can i get 3 breakfast sandwiches on croissants n 3 medium lattes for pickup, name is omar 🙏
""",
        "P",
        start="Wed 13:00",
        items=[
            I("breakfast_sandwich", 3, "croissant", ["3 breakfast sandwiches on croissants"]),
            I("latte", 3, "medium", ["3 medium lattes"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 12:15", "12:15"),
        day=("tomorrow", "tmrw"),
        name="Omar",
        name_q="omar",
    ),
    F(
        "a-fresh3-063",
        """
c: HEY ARE YOU OPEN SUNDAYS
b: Yes, we're open every day from 7 am to 3 pm.
c: KKKKJJJ;;;LL
""",
        "D U",
        start="Fri 11:20",
    ),
    F(
        "a-fresh3-064",
        """
c: hey can i get 4 veggie burgers n 4 sprites
c: deliver to 88 bayview st at 12:30
c: card
c: actually make it 1:15 instead, meeting got pushed
""",
        "P P P M",
        start="Mon 11:15",
        items=[
            I("veggie_burger", 4, None, ["4 veggie burgers"]),
            I("sprite", 4, None, ["4 sprites"]),
        ],
        method="delivery",
        method_q="deliver to 88 bayview st",
        time=("clock_time", "1:15", "13:15"),
        addr={"raw": "88 bayview st", "number": "88", "street": "bayview st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-065",
        """
c: hey 🍕 a large veggie to 47 vine st, card, oh n can u add artichokes on it
""",
        "P",
        start="Thu 18:50",
        items=[I("veggie_pizza", 1, "large", ["a large veggie"], [offmod("add artichokes on it")])],
        method="delivery",
        method_q="to 47 vine st",
        addr={"raw": "47 vine st", "number": "47", "street": "vine st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-066",
        """
c: hi need some stuff for a party
c: 12 muffins, 6 blueberry 6 choc chip
c: do u have decaf?
b: Sorry, no decaf on our menu.
c: ok then 4 large hot chocolates
c: pickup at 1, name ruby
""",
        "P P Q P P",
        start="Thu 10:00",
        items=[
            I("muffin", 6, "blueberry", ["12 muffins", "6 blueberry"]),
            I("muffin", 6, "chocolate_chip", ["12 muffins", "6 choc chip"]),
            I("hot_chocolate", 4, "large", ["4 large hot chocolates"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 1", "13:00"),
        name="Ruby",
        name_q="ruby",
    ),
    F(
        "a-fresh3-067",
        """
c: yo
c: party order: 2 xl pepperoni, 1 xl supreme, 1 lg cheese w mushrooms, 3 orders of garlic knots n 2 2-liter cokes
c: card
""",
        "S P P",
        start="Sat 17:30",
        items=[
            I("pepperoni_pizza", 2, "extra_large", ["2 xl pepperoni"]),
            I("supreme_pizza", 1, "extra_large", ["1 xl supreme"]),
            I("cheese_pizza", 1, "large", ["1 lg cheese w mushrooms"], [add("mushrooms", "w mushrooms")]),
            I("garlic_knots", 3, None, ["3 orders of garlic knots"]),
            I("coke", 2, "two_liter", ["2 2-liter cokes"]),
        ],
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh3-068",
        """
c: Hi, it's me again.
c: I'd like my usual for Thursday: a double cheeseburger with no onions and a large fries.
c: Pickup at 12:15.
c: Card, as always.
""",
        "S P P P",
        start="Tue 12:00",
        items=[
            I(
                "cheeseburger",
                1,
                "double",
                ["a double cheeseburger with no onions"],
                [rm("onion", "with no onions")],
            ),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("clock_time", "at 12:15", "12:15"),
        day=("weekday", "thu", "Thursday"),
        pay="card",
        pay_q="Card",
        annotation="'my usual' is spelled out in the same message, so nothing is unclear.",
    ),
    F(
        "a-fresh3-069",
        """
c: YO
c: 2 CHEESEBURGERS
c: 1 VEGGIE BURGER W BACON
c: 2 ORDERS OF RINGS
c: DELIVER TO 1844 CAMPUS DR ROOM 12
c: CARD
""",
        "S P P P P P",
        start="Wed 21:20",
        items=[
            I("cheeseburger", 2, None, ["2 CHEESEBURGERS"]),
            I("veggie_burger", 1, None, ["1 VEGGIE BURGER W BACON"], [add("bacon", "W BACON")]),
            I("onion_rings", 2, None, ["2 ORDERS OF RINGS"]),
        ],
        method="delivery",
        method_q="DELIVER TO 1844 CAMPUS DR ROOM 12",
        addr={"raw": "1844 CAMPUS DR ROOM 12", "number": "1844", "street": "CAMPUS DR", "unit": "ROOM 12"},
        pay="card",
        pay_q="CARD",
    ),
    F(
        "a-fresh3-070",
        """
c: hhhhhh,,,mmm nnn
""",
        "U",
        start="Sun 20:10",
    ),
    F(
        "a-fresh3-071",
        """
c: hi 🙂 if i pay cash can the driver break a 50?
b: Yes, just let us know the bill when you order.
c: great thank u! 💵
""",
        "PQ S",
        start="Mon 18:00",
    ),
    F(
        "a-fresh3-072",
        """
c: hey where is my order
c: ordered 20 min ago for pickup, name raj, train in 10 min
""",
        "ST ST!t",
        start="Tue 08:50",
    ),
    F(
        "a-fresh3-073",
        """
c: Hi, I was charged twice for my delivery last night, could you refund one of the charges?
""",
        "R!n",
        start="Thu 13:30",
    ),
    F(
        "a-fresh3-074",
        """
c: Hi, could I get 2 bagels with cream cheese, one plain and one everything, at 2:30?
c: I'll pay with card.
""",
        "P P",
        start="Mon 09:00",
        items=[
            I(
                "bagel",
                1,
                "plain",
                ["2 bagels with cream cheese", "one plain"],
                [add("cream_cheese", "with cream cheese")],
            ),
            I(
                "bagel",
                1,
                "everything",
                ["2 bagels with cream cheese", "one everything"],
                [add("cream_cheese", "with cream cheese")],
            ),
        ],
        time=("clock_time", "at 2:30", "14:30"),
        pay="card",
        pay_q="pay with card",
        annotation="'at 2:30' at a café open 7-15: only 14:30 is open.",
    ),
    F(
        "a-fresh3-075",
        """
c: hi 🙂
c: can i get a medium lat
""",
        "S U",
        start="Wed 07:30",
        annotation="Cut off mid-word: UNKNOWN, as fresh 001 and fresh2 090.",
    ),
    F(
        "a-fresh3-076",
        """
c: 2 lg pepperoni
c: deliver to 66 fulton st
c: at 7
c: wait not tonight, sat at 7
""",
        "P P P M",
        start="Thu 17:00",
        items=[I("pepperoni_pizza", 2, "large", ["2 lg pepperoni"])],
        method="delivery",
        method_q="deliver to 66 fulton st",
        time=("clock_time", "at 7", "19:00"),
        day=("weekday", "sat", "sat"),
        addr={"raw": "66 fulton st", "number": "66", "street": "fulton st"},
    ),
    F(
        "a-fresh3-077",
        """
c: hello
c: 2 cheeseburgers and a bacon burger please
c: do you have chicken sandwiches
b: Sorry, we don't have chicken sandwiches. Would you like anything else?
c: then a veggie burger, 2 shakes and 2 orders of fries
b: Which flavors for the shakes, and regular or large fries?
c: 2 vanilla, regular fries. pickup please
""",
        "S P Q P P",
        start="Fri 12:40",
        items=[
            I("cheeseburger", 2, None, ["2 cheeseburgers"]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("milkshake", 2, "vanilla", ["2 shakes", "2 vanilla"]),
            I("fries", 2, "regular", ["2 orders of fries", "regular fries"]),
        ],
        method="pickup",
        method_q="pickup",
    ),
    F(
        "a-fresh3-078",
        """
c: hi
c: sorry to bother
c: just checking on a pickup order
c: under the name lee
c: no rush
""",
        "S S ST ST ST",
        start="Sat 19:20",
    ),
    F(
        "a-fresh3-079",
        """
c: SETTLE A BET
c: IS A HOT DOG A SANDWICH???
""",
        "S O",
        start="Sun 11:15",
    ),
    F(
        "a-fresh3-080",
        """
c: hey need food for a bday tmrw
c: 4 cheeseburgers, 2 veggie burgers n 6 lemonades
c: pickup at 3, card
""",
        "P P P",
        start="Sat 15:00",
        items=[
            I("cheeseburger", 4, None, ["4 cheeseburgers"]),
            I("veggie_burger", 2, None, ["2 veggie burgers"]),
            I("lemonade", 6, None, ["6 lemonades"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 3", "15:00"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
]
