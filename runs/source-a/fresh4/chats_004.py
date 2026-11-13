"""fresh4 a-fresh4-085–110 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm, sub

ENTRIES = [
    F(
        "a-fresh4-085",
        """
c: Hi, just wanted to say the pizza last night was fantastic.
c: Thanks to the whole team!
""",
        "S S",
        start="Sun 13:00",
    ),
    F(
        "a-fresh4-086",
        """
c: is the veggie burger gluten free? 🌾
b: The patty is, but the bun isn't. We don't have gluten-free buns, sorry.
c: ok a veggie burger n a large fries to 27 oak st 🍔
c: w avocado n a fried egg on the burger pls 🍳
""",
        "Q P P",
        start="Wed 18:50",
        items=[
            I(
                "veggie_burger",
                1,
                None,
                ["a veggie burger", "w avocado n a fried egg on the burger"],
                [add("avocado", "w avocado"), offmod("a fried egg")],
            ),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="delivery",
        method_q="to 27 oak st",
        addr={"raw": "27 oak st", "number": "27", "street": "oak st"},
    ),
    F(
        "a-fresh4-087",
        """
c: a few croissants
c: n a lg drip
c: pickup for ana
""",
        "P P P",
        start="Sat 10:30",
        items=[
            I("croissant", None, "plain", ["a few croissants"]),
            I("drip_coffee", 1, "large", ["a lg drip"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    F(
        "a-fresh4-088",
        """
c: hey
c: order for the 27th
c: 3 med lattes
c: 2 bec on croissants
c: pickup at 8
c: name is dmitri
""",
        "S P P P P P",
        start="Mon 12:40",
        items=[
            I("latte", 3, "medium", ["3 med lattes"]),
            I("breakfast_sandwich", 2, "croissant", ["2 bec on croissants"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "08:00"),
        day=("date", None, 27, "the 27th"),
        name="Dmitri",
        name_q="dmitri",
    ),
    F(
        "a-fresh4-089",
        """
c: hi my garlic knots never came with the delivery last night 😕 can i get a refund for them?
""",
        "R",
        start="Thu 13:30",
        order=False,
    ),
    F(
        "a-fresh4-090",
        """
c: random but whats the capital of australia
c: my friend says sydney lol
""",
        "O O",
        start="Mon 14:20",
    ),
    F(
        "a-fresh4-091",
        """
c: hey
c: u guys open til 10?
b: Yes, we're open until 10 PM!
c: ?
""",
        "S D U",
        start="Tue 18:00",
    ),
    F(
        "a-fresh4-092",
        """
c: HI
c: 6 BACON BURGERS
c: 3 WITH NO TOMATO
c: AND 6 COKES PLEASE
""",
        "S P P P",
        start="Sat 12:40",
        items=[
            I("bacon_burger", 3, None, ["6 BACON BURGERS"]),
            I("bacon_burger", 3, None, ["6 BACON BURGERS", "3 WITH NO TOMATO"], [rm("tomato", "NO TOMATO")]),
            I("coke", 6, None, ["6 COKES"]),
        ],
    ),
    F(
        "a-fresh4-093",
        """
c: lg margherita n a lg hawaiian to 52 vine st, card
b: Got it: 1 large Margherita Pizza and 1 large Hawaiian Pizza, delivered to 52 Vine St, paying by card. Is that right?
c: yes
""",
        "P C",
        start="Fri 19:20",
        items=[
            I("margherita_pizza", 1, "large", ["lg margherita"]),
            I("hawaiian_pizza", 1, "large", ["a lg hawaiian"]),
        ],
        method="delivery",
        method_q="to 52 vine st",
        addr={"raw": "52 vine st", "number": "52", "street": "vine st"},
        pay="card",
        pay_q="card",
        decision="confirmed",
        decision_q="yes",
    ),
    F(
        "a-fresh4-094",
        """
c: good morning ☀️
c: for the family: 2 hot chocs, a large latte w hazelnut, 2 blueberry muffins, a chocolate croissant n a plain bagel w butter 🥯
c: name is rosa
c: thank u! 😊
""",
        "S P P S",
        start="Sun 08:20",
        items=[
            I("hot_chocolate", 2, "medium", ["2 hot chocs"]),
            I("latte", 1, "large", ["a large latte w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I("muffin", 2, "blueberry", ["2 blueberry muffins"]),
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
            I("bagel", 1, "plain", ["a plain bagel w butter"], [add("butter", "w butter")]),
        ],
        name="Rosa",
        name_q="rosa",
    ),
    F(
        "a-fresh4-095",
        """
c: hi! is there someone i can talk to about a big catering order? ☕
c: like 80 ppl next week 🙏
""",
        "HU HU",
        start="Tue 10:10",
        order=False,
    ),
    F(
        "a-fresh4-096",
        """
c: Hi, I'd like a half pepperoni, half veggie pizza.
c: And two orders of breadsticks.
c: Please deliver to 900 Market St, 4th floor.
c: Paying by card.
""",
        "P P P P",
        start="Wed 12:50",
        items=[
            I(
                None,
                1,
                None,
                ["a half pepperoni, half veggie pizza"],
                halves=[("pepperoni_pizza", []), ("veggie_pizza", [])],
            ),
            I("breadsticks", 2, None, ["two orders of breadsticks"]),
        ],
        method="delivery",
        method_q="deliver to 900 Market St",
        addr={"raw": "900 Market St, 4th floor", "number": "900", "street": "Market St", "unit": "4th floor"},
        pay="card",
        pay_q="Paying by card",
        annotation="Half-and-half with no size: the size is missing, asked.",
    ),
    F(
        "a-fresh4-097",
        """
c: is the almond croissant sweet?
b: Lightly sweet, with almond cream inside.
c: ok 2 almond croissants n a med latte, pickup for june, card
""",
        "Q P",
        start="Tue 08:10",
        items=[
            I("croissant", 2, "almond", ["2 almond croissants"]),
            I("latte", 1, "medium", ["a med latte"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="June",
        name_q="june",
    ),
    F(
        "a-fresh4-098",
        """
c: JJJKKL NNNN
""",
        "U",
        start="Wed 20:30",
    ),
    F(
        "a-fresh4-099",
        """
c: hi
c: does the veggie burger have nuts in it
b: No nuts in the Veggie Burger.
c: ok thx
""",
        "S Q S",
        start="Thu 14:30",
    ),
    F(
        "a-fresh4-100",
        """
c: Hello, I'd like a few large pepperoni pizzas.
c: And a 2-liter Coke.
c: I'll pay cash.
""",
        "P P P",
        start="Fri 21:40",
        items=[
            I("pepperoni_pizza", None, "large", ["a few large pepperoni pizzas"]),
            I("coke", 1, "two_liter", ["a 2-liter Coke"]),
        ],
        pay="cash",
        pay_q="I'll pay cash",
    ),
    F(
        "a-fresh4-101",
        """
c: Hi, a large americano with oat milk and a banana nut muffin for pickup, please.
c: Name is Owen, paying by card.
""",
        "P P",
        start="Tue 09:00",
        items=[
            I(
                "americano",
                1,
                "large",
                ["a large americano with oat milk"],
                [add("oat_milk", "with oat milk")],
            ),
            I("muffin", 1, "banana_nut", ["a banana nut muffin"]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="paying by card",
        name="Owen",
    ),
    F(
        "a-fresh4-102",
        """
c: hey 👋
c: can i get a #1 w fries for pickup 🍔
""",
        "S P",
        start="Sun 17:20",
        items=[I("cheeseburger_combo", 1, None, ["a #1 w fries"], combo={"side": "fries"})],
        method="pickup",
        method_q="for pickup",
        annotation="The combo's drink is never chosen: combo_choice missing, asked.",
    ),
    F(
        "a-fresh4-103",
        """
c: yo 🍔 food for the dorm
c: 3 cheeseburgers n 2 bacon burgers
c: + shakes
b: Which flavors, and how many? Vanilla, chocolate or strawberry.
c: 2 chocolate 1 strawberry 🍓
c: n 3 large fries
""",
        "P P P P P",
        start="Fri 21:10",
        items=[
            I("cheeseburger", 3, "single", ["3 cheeseburgers"]),
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("milkshake", 2, "chocolate", ["shakes", "2 chocolate"]),
            I("milkshake", 1, "strawberry", ["shakes", "1 strawberry"]),
            I("fries", 3, "large", ["3 large fries"]),
        ],
        annotation="'+ shakes' is settled by the next message (2 chocolate, 1 strawberry).",
    ),
    F(
        "a-fresh4-104",
        """
c: whats the diff between the meat lovers n the supreme
b: Meat Lovers is all meat; the Supreme has pepperoni, sausage and veggies.
c: ok a large meat lovers to 66 cedar ln
c: actually make it the other one
""",
        "Q P M",
        start="Mon 19:30",
        items=[I("supreme_pizza", 1, "large", ["a large meat lovers", "make it the other one"])],
        method="delivery",
        method_q="to 66 cedar ln",
        addr={"raw": "66 cedar ln", "number": "66", "street": "cedar ln"},
        annotation="'the other one' after two pizzas were compared is the supreme: resolved, not ambiguous.",
    ),
    F(
        "a-fresh4-105",
        """
c: do u have decaf?
b: Sorry, no decaf at the moment.
c: ok a med hot choc n a bec for pickup at 1:30, name is pam
""",
        "Q P",
        start="Wed 10:30",
        items=[
            I("hot_chocolate", 1, "medium", ["a med hot choc"]),
            I("breakfast_sandwich", 1, "english_muffin", ["a bec"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 1:30", "13:30"),
        name="Pam",
        name_q="pam",
        annotation="'at 1:30' at 10:30, open 7-15: 13:30.",
    ),
    F(
        "a-fresh4-106",
        """
c: I WOULD LIKE TO ORDER FOR TOMMOROW: 2 CHEESEBURGERS AND A VANILLA SHAKE, PICKUP AT NOON
c: THANK YOU
""",
        "P S",
        start="Mon 16:30",
        items=[
            I("cheeseburger", 2, "single", ["2 CHEESEBURGERS"]),
            I("milkshake", 1, "vanilla", ["A VANILLA SHAKE"]),
        ],
        method="pickup",
        method_q="PICKUP",
        time=("clock_time", "AT NOON", "12:00"),
        day=("tomorrow", "TOMMOROW"),
    ),
    F(
        "a-fresh4-107",
        """
c: Hi there!
c: A large pepperoni and garlic knots delivered to 18 Fir St, please. Card.
c: Oh no, my plans just changed.
c: Please cancel the order, sorry about that.
""",
        "S P S X",
        start="Sat 19:00",
        items=[
            I("pepperoni_pizza", 1, "large", ["A large pepperoni"]),
            I("garlic_knots", 1, None, ["garlic knots"]),
        ],
        method="delivery",
        method_q="delivered to 18 Fir St",
        addr={"raw": "18 Fir St", "number": "18", "street": "Fir St"},
        pay="card",
        pay_q="Card",
        decision="cancelled",
        decision_q="cancel the order",
    ),
    F(
        "a-fresh4-108",
        """
c: hello 😊 does the bacon burger come with cheese?
b: Yes, it comes with cheese!
c: wonderful, one bacon burger and a lemonade please, delivered to 12 Rose Ln. cash 💵
b: Got it: 1 Bacon Burger and 1 Lemonade, delivered to 12 Rose Ln, paying cash. Is that right?
c: yes thank you 🙏
c: oh dear, it's 21 Rose Ln, not 12! sorry 🙈
""",
        "Q P C M",
        start="Thu 17:40",
        items=[
            I("bacon_burger", 1, None, ["one bacon burger"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="delivered to 12 Rose Ln",
        addr={"raw": "21 Rose Ln", "number": "21", "street": "Rose Ln"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh4-109",
        """
c: hi ☕
c: a large cappuccino w almond milk pls
c: n a plain croissant, can i pay w apple pay? 📱
c: name is lea
""",
        "S P P/PQ P",
        start="Fri 11:10",
        items=[
            I(
                "cappuccino",
                1,
                "large",
                ["a large cappuccino w almond milk"],
                [sub("whole_milk", "almond_milk", "w almond milk")],
            ),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        name="Lea",
        name_q="lea",
    ),
    F(
        "a-fresh4-110",
        """
c: hey can i get 2 lg drips n 2 bluebery muffins
c: for wednesday
c: at 7:30
c: name is tom
""",
        "P P P P",
        start="Thu 13:00",
        items=[
            I("drip_coffee", 2, "large", ["2 lg drips"]),
            I("muffin", 2, "blueberry", ["2 bluebery muffins"]),
        ],
        time=("clock_time", "at 7:30", "07:30"),
        day=("weekday", "wed", "wednesday"),
        name="Tom",
        name_q="tom",
    ),
]
