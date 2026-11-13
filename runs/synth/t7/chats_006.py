"""t7 syn-t7-0121–0150 (chats + labels by hand; see build.py)."""

from build import I, X, add, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t7-0121",
        """
c: yo lemme get th
c: 🍔🍔??
""",
        "U U",
    ),
    X(
        "syn-t7-0122",
        """
c: hey
c: 2 orders of breadsticks n a medium pepperoni
c: pickup for marcus
c: cash
b: Got it, Marcus: 2 orders of Breadsticks and 1 medium Pepperoni Pizza, pickup, paying cash. Is that right?
c: yep
c: actually just 1 breadsticks
""",
        "S P P P C M",
        items=[
            I("breadsticks", 1, None, ["2 orders of breadsticks", "just 1 breadsticks"]),
            I("pepperoni_pizza", 1, "medium", ["a medium pepperoni"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t7-0123",
        """
c: xl veggie w ham n 2 cans of coke, pickup, cash w a 50
b: Got it: 1 extra large Veggie Pizza with ham and 2 Cokes (cans), pickup, paying cash. Is that right?
c: yes
c: can u make the veggie thin crust
""",
        "P C M",
        items=[
            I(
                "veggie_pizza",
                1,
                "extra_large",
                ["xl veggie w ham", "make the veggie thin crust"],
                [add("ham", "w ham"), add("crust_thin", "thin crust")],
            ),
            I("coke", 2, "can", ["2 cans of coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q=["cash", "w a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0124",
        """
c: lg cap
c: 3 drips
c: are the croissants fresh today
b: Yes, baked this morning!
c: ok a plain croissant
c: n 2 bec on croissants no cheese w tomato
c: + a choc chip muffin
c: pickup in 25, keisha, card
""",
        "P P Q P P P P",
        items=[
            I("cappuccino", 1, "large", ["lg cap"]),
            I("drip_coffee", 3, "medium", ["3 drips"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
            I(
                "breakfast_sandwich",
                2,
                "croissant",
                ["2 bec on croissants no cheese w tomato"],
                [rm("cheddar", "no cheese"), add("tomato", "w tomato")],
            ),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 25", None),
        pay="card",
        pay_q="card",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t7-0125",
        """
c: the one i always get
b: Hi! We can't see past orders here, sorry. What would you like?
c: large bbq chicken w ham
c: medium meat lovers no ham w green peppers
c: a sprite n 2 diet cokes
""",
        "P P P P",
        items=[
            I("bbq_chicken_pizza", 1, "large", ["large bbq chicken w ham"], [add("ham", "w ham")]),
            I(
                "meat_lovers_pizza",
                1,
                "medium",
                ["medium meat lovers no ham w green peppers"],
                [rm("ham", "no ham"), add("green_peppers", "w green peppers")],
            ),
            I("sprite", 1, "can", ["a sprite"]),
            I("diet_coke", 2, "can", ["2 diet cokes"]),
        ],
    ),
    X(
        "syn-t7-0126",
        """
c: 3 small hot chocs no whip w almond milk, a small cap n 2 choc chip muffins
c: pickup at 12, marcus, card
c: make it 2 hot chocs not 3
""",
        "P P M",
        items=[
            I(
                "hot_chocolate",
                2,
                "small",
                ["3 small hot chocs no whip w almond milk", "make it 2 hot chocs not 3"],
                [rm("whipped_cream", "no whip"), sub("whole_milk", "almond_milk", "w almond milk")],
            ),
            I("cappuccino", 1, "small", ["a small cap"]),
            I("muffin", 2, "chocolate_chip", ["2 choc chip muffins"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12", "12:00"),
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t7-0127",
        """
c: hey
c: 3 small hot chocolates
c: 2 of those no whip
c: n a small latte
c: pickup
c: sam
c: card
""",
        "S P P P P P P",
        items=[
            I("hot_chocolate", 1, "small", ["3 small hot chocolates"]),
            I(
                "hot_chocolate",
                2,
                "small",
                ["3 small hot chocolates", "2 of those no whip"],
                [rm("whipped_cream", "no whip")],
            ),
            I("latte", 1, "small", ["a small latte"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sam",
        name_q="sam",
    ),
    X(
        "syn-t7-0128",
        """
c: is the veggie burger vegan? 🌱
b: The patty is plant-based, but it comes with mayo; we can leave it off.
c: ok 6 veggie burgers, 4 of em no tomato
c: + a cheeseburger n 2 regular fries
c: to 1122 alder st, card 💳
""",
        "Q P P P",
        items=[
            I("veggie_burger", 2, None, ["6 veggie burgers"]),
            I(
                "veggie_burger",
                4,
                None,
                ["6 veggie burgers", "4 of em no tomato"],
                [rm("tomato", "no tomato")],
            ),
            I("cheeseburger", 1, "single", ["a cheeseburger"]),
            I("fries", 2, "regular", ["2 regular fries"]),
        ],
        method="delivery",
        method_q="to 1122 alder st",
        addr={"raw": "1122 alder st", "number": "1122", "street": "alder st"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0129",
        """
c: 3 chocolate croissants, a small cap w skim, a hot choc w hazelnut n a bec no bacon ☕ pickup in 20 for tom, card
c: oh n skip the sandwich 🙏
""",
        "P M",
        items=[
            I("croissant", 3, "chocolate", ["3 chocolate croissants"]),
            I("cappuccino", 1, "small", ["a small cap w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
            I("hot_chocolate", 1, "medium", ["a hot choc w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="card",
        pay_q="card",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0130",
        """
c: hey 👋 that thing from before pls
b: Hi! We can't see past orders here, sorry. What would you like?
c: haha ok 😅 an xl margherita no mozzarella, 3 breadsticks n a garlic knots
c: + 2 cans of dr pepper n 3 2-liter sprites 🥤
""",
        "P P P",
        items=[
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["an xl margherita no mozzarella"],
                [rm("mozzarella", "no mozzarella")],
            ),
            I("breadsticks", 3, None, ["3 breadsticks"]),
            I("garlic_knots", 1, None, ["a garlic knots"]),
            I("dr_pepper", 2, "can", ["2 cans of dr pepper"]),
            I("sprite", 3, "two_liter", ["3 2-liter sprites"]),
        ],
    ),
    X(
        "syn-t7-0131",
        """
c: Hi, could I get some lemonades and a Coke delivered to 3160 Thornton Ct, across from the park?
""",
        "P",
        items=[
            I("lemonade", None, None, ["some lemonades"]),
            I("coke", 1, None, ["a Coke"]),
        ],
        method="delivery",
        method_q="delivered to 3160 Thornton Ct",
        addr={
            "raw": "3160 Thornton Ct, across from the park",
            "number": "3160",
            "street": "Thornton Ct",
            "reference": "across from the park",
        },
    ),
    X(
        "syn-t7-0132",
        """
c: HI, THIS ORDER IS FOR OCTOBER 24
c: 2 ORDERS OF ONION RINGS
c: AND 2 DOUBLE CHEESEBURGERS
c: AT 7PM
c: CARD
""",
        "P P P P P",
        items=[
            I("onion_rings", 2, None, ["2 ORDERS OF ONION RINGS"]),
            I("cheeseburger", 2, "double", ["2 DOUBLE CHEESEBURGERS"]),
        ],
        time=("clock_time", "AT 7PM", "19:00"),
        day=("date", 10, 24, "OCTOBER 24"),
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0133",
        """
c: a few small lattes n a small americano
c: pickup for nico
""",
        "P P",
        items=[
            I("latte", None, "small", ["a few small lattes"]),
            I("americano", 1, "small", ["a small americano"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t7-0134",
        """
c: large pineapple pizza on thin crust
c: n knots
c: thats it
""",
        "P P S",
        items=[
            I(
                "hawaiian_pizza",
                1,
                "large",
                ["large pineapple pizza on thin crust"],
                [add("crust_thin", "on thin crust")],
            ),
            I("garlic_knots", 1, None, ["knots"]),
        ],
    ),
    X(
        "syn-t7-0135",
        """
c: 6 veggie burgers, one w jalapenos
c: 4 onion rings, a fries, 4 cokes
c: deliver to 59 magnolia rd unit 30, card
""",
        "P P P",
        items=[
            I("veggie_burger", 5, None, ["6 veggie burgers"]),
            I(
                "veggie_burger",
                1,
                None,
                ["6 veggie burgers", "one w jalapenos"],
                [add("jalapeno", "w jalapenos")],
            ),
            I("onion_rings", 4, None, ["4 onion rings"]),
            I("fries", 1, "regular", ["a fries"]),
            I("coke", 4, None, ["4 cokes"]),
        ],
        method="delivery",
        method_q="deliver to 59 magnolia rd",
        addr={"raw": "59 magnolia rd unit 30", "number": "59", "street": "magnolia rd", "unit": "unit 30"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0136",
        """
c: 5 CROISSANTS, ONE WITH BUTTER, AND 2 CHOCOLATE CHIP MUFFINS
c: ASAP FOR GRACE, PICKUP, CASH
""",
        "P P",
        items=[
            I("croissant", 4, "plain", ["5 CROISSANTS"]),
            I("croissant", 1, "plain", ["5 CROISSANTS", "ONE WITH BUTTER"], [add("butter", "WITH BUTTER")]),
            I("muffin", 2, "chocolate_chip", ["2 CHOCOLATE CHIP MUFFINS"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("asap", "ASAP", None),
        pay="cash",
        pay_q="CASH",
        name="Grace",
        name_q="GRACE",
    ),
    X(
        "syn-t7-0137",
        """
c: hi
c: bec no cheese, can i get it on gluten free bread? if not english muffin is fine
b: Sorry, no gluten-free bread. English muffin it is!
c: ok + a medium latte
c: pickup grace
c: card
""",
        "S P/Q P P P",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["bec no cheese", "english muffin is fine"],
                [rm("cheddar", "no cheese")],
            ),
            I("latte", 1, "medium", ["a medium latte"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t7-0138",
        """
c: a blueberry muffin n a medium cappuccino w honey
c: pickup for keisha
""",
        "P P",
        items=[
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
            I("cappuccino", 1, "medium", ["a medium cappuccino w honey"], [offmod("w honey")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t7-0139",
        """
c: Hi there.
c: 3 single cheeseburgers, 2 onion rings and a vanilla shake for pickup, cash.
c: Oh, and add mayo to all the cheeseburgers.
""",
        "S P P",
        items=[
            I(
                "cheeseburger",
                3,
                "single",
                ["3 single cheeseburgers", "add mayo to all the cheeseburgers"],
                [add("mayo", "add mayo")],
            ),
            I("onion_rings", 2, None, ["2 onion rings"]),
            I("milkshake", 1, "vanilla", ["a vanilla shake"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0140",
        """
c: 4 veggie burgers (1 w ketchup), a bacon burger, onion rings n fries 🍔🍟 pickup for tom, card
""",
        "P",
        items=[
            I("veggie_burger", 3, None, ["4 veggie burgers"]),
            I("veggie_burger", 1, None, ["4 veggie burgers", "1 w ketchup"], [add("ketchup", "w ketchup")]),
            I("bacon_burger", 1, None, ["a bacon burger"]),
            I("onion_rings", 1, None, ["onion rings"]),
            I("fries", 1, "regular", ["fries"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0141",
        """
c: small cheese pizza no sauce
c: deliver to 26 willow creek terrace at 1:30
c: cash
b: Got it: 1 small Cheese Pizza with no sauce, delivered to 26 Willow Creek Terrace at 1:30 PM, paying cash. Is that right?
c: ya
c: oh make it gluten free crust pls
""",
        "P P P C M",
        items=[
            I(
                "cheese_pizza",
                1,
                "small",
                ["small cheese pizza no sauce", "make it gluten free crust"],
                [rm("tomato_sauce", "no sauce"), add("crust_gluten_free", "gluten free crust")],
            ),
        ],
        method="delivery",
        method_q="deliver to 26 willow creek terrace",
        time=("clock_time", "at 1:30", "13:30"),
        addr={"raw": "26 willow creek terrace", "number": "26", "street": "willow creek terrace"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0142",
        """
c: sm latte w skim, a drip w hazelnut
c: bec no bacon n a blueberry muffin
c: 2 lg caps w skim too
c: pickup eli, card
""",
        "P P P P",
        items=[
            I("latte", 1, "small", ["sm latte w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
            I("drip_coffee", 1, "medium", ["a drip w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("breakfast_sandwich", 1, "english_muffin", ["bec no bacon"], [rm("bacon", "no bacon")]),
            I("muffin", 1, "blueberry", ["a blueberry muffin"]),
            I("cappuccino", 2, "large", ["2 lg caps w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t7-0143",
        """
c: 3 veggie pizzas
c: n that thing from before
c: card
""",
        "P P P",
        items=[
            I("veggie_pizza", 3, None, ["3 veggie pizzas"]),
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
        "syn-t7-0144",
        """
c: 2 garlic knots, do they come w marinara? 🍝 n a large cheese, deliver to 84 sunset dr, cash 💵
""",
        "P/Q",
        items=[
            I("garlic_knots", 2, None, ["2 garlic knots"]),
            I("cheese_pizza", 1, "large", ["a large cheese"]),
        ],
        method="delivery",
        method_q="deliver to 84 sunset dr",
        addr={"raw": "84 sunset dr", "number": "84", "street": "sunset dr"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0145",
        """
c: can i get the hal
c: n
""",
        "U U",
    ),
    X(
        "syn-t7-0146",
        """
c: 2 sesame bagels w avocado n one of those 😊
c: in 20 min, cash, i have a 20
""",
        "P P",
        items=[
            I("bagel", 2, "sesame", ["2 sesame bagels w avocado"], [add("avocado", "w avocado")]),
            I(None, 1, None, ["one of those"], unmatched="one of those", flag="item_menu_match"),
        ],
        time=("relative", "in 20 min", None),
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
    ),
    X(
        "syn-t7-0147",
        """
c: 3 strawberry shakes n a veggie burger no tomato w a fried egg
c: to 78 riverside st apt 8a
c: cash
""",
        "P P P",
        items=[
            I("milkshake", 3, "strawberry", ["3 strawberry shakes"]),
            I(
                "veggie_burger",
                1,
                None,
                ["a veggie burger no tomato w a fried egg"],
                [rm("tomato", "no tomato"), offmod("w a fried egg")],
            ),
        ],
        method="delivery",
        method_q="to 78 riverside st",
        addr={"raw": "78 riverside st apt 8a", "number": "78", "street": "riverside st", "unit": "apt 8a"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0148",
        """
c: do the shakes come in sizes
b: One size: vanilla, chocolate or strawberry.
c: ok 2 vanilla shakes, 2 veggie burgers no pickles, a lemonade n a sprite for pickup
b: Got it: 2 vanilla Milkshakes, 2 Veggie Burgers with no pickles, 1 Lemonade and 1 Sprite, for pickup. Is that right?
c: yes
c: actually no sprite
""",
        "Q P C M",
        items=[
            I("milkshake", 2, "vanilla", ["2 vanilla shakes"]),
            I("veggie_burger", 2, None, ["2 veggie burgers no pickles"], [rm("pickle", "no pickles")]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="pickup",
        method_q="for pickup",
    ),
    X(
        "syn-t7-0149",
        """
c: hi
c: medium cap
c: 3 large lattes
c: all w whipped cream
c: n a drip
c: oh n hazelnut in the cap
""",
        "S P P P P P",
        items=[
            I(
                "cappuccino",
                1,
                "medium",
                ["medium cap", "hazelnut in the cap"],
                [add("hazelnut_syrup", "hazelnut")],
            ),
            I(
                "latte",
                3,
                "large",
                ["3 large lattes", "all w whipped cream"],
                [add("whipped_cream", "w whipped cream")],
            ),
            I("drip_coffee", 1, "medium", ["a drip"]),
        ],
    ),
    X(
        "syn-t7-0150",
        """
c: bacon burger for pickup sunday
c: thx
""",
        "P S",
        items=[I("bacon_burger", 1, None, ["bacon burger"])],
        method="pickup",
        method_q="for pickup",
        time=("ambiguous", "sunday"),
        day=("weekday", "sun", "sunday"),
    ),
]
