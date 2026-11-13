"""t7 syn-t7-0091–0120 (chats + labels by hand; see build.py)."""

from build import I, X, add, note, offmod, rm, sub

ENTRIES = [
    X(
        "syn-t7-0091",
        """
c: hi, can i get an egg sandwich, a small vanilla latte and a cinnamon raisin w butter
c: pickup for ana, card
""",
        "P P",
        items=[
            I("breakfast_sandwich", 1, "english_muffin", ["an egg sandwich"]),
            I("latte", 1, "small", ["a small vanilla latte"], [add("vanilla_syrup", "vanilla")]),
            I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin w butter"], [add("butter", "w butter")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0092",
        """
c: personal margherita w anchovies, garlic knots n a coke 🍕 pickup for ben, card
b: Got it, Ben: 1 personal Margherita Pizza with anchovies, 1 order of Garlic Knots and 1 Coke, pickup, paying by card. Is that right?
c: yes 👍
c: oh n make the margherita thin crust pls
""",
        "P C M",
        items=[
            I(
                "margherita_pizza",
                1,
                "personal",
                ["personal margherita w anchovies", "make the margherita thin crust"],
                [add("anchovies", "w anchovies"), add("crust_thin", "make the margherita thin crust")],
            ),
            I("garlic_knots", 1, None, ["garlic knots"]),
            I("coke", 1, "can", ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t7-0093",
        """
c: some small veggies w grilled chicken
c: thin crust
c: n a dr pepper, delivery
c: cash, paying w a 50
""",
        "P P P P",
        items=[
            I(
                "veggie_pizza",
                None,
                "small",
                ["some small veggies w grilled chicken", "thin crust"],
                [add("grilled_chicken", "w grilled chicken"), add("crust_thin", "thin crust")],
            ),
            I("dr_pepper", 1, "can", ["a dr pepper"]),
        ],
        method="delivery",
        method_q="delivery",
        pay="cash",
        pay_q=["cash", "paying w a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0094",
        """
c: 4 bec on bagels no cheese 🥯 pickup for maya, cash
b: Got it, Maya: 4 Breakfast Sandwiches on bagels, no cheese, pickup, paying cash. Is that right?
c: yes!
c: actually swap the sandwiches for a large cappuccino w skim ☕
""",
        "P C M",
        items=[
            I(
                "cappuccino",
                1,
                "large",
                ["a large cappuccino w skim"],
                [sub("whole_milk", "skim_milk", "w skim")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0095",
        """
c: 2 bec no egg asap 🙏
c: n that thing from before
""",
        "P P",
        items=[
            I("breakfast_sandwich", 2, "english_muffin", ["2 bec no egg"], [rm("egg", "no egg")]),
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
    ),
    X(
        "syn-t7-0096",
        """
c: hey
c: xl marg
c: no basil
c: card
c: thats all
c: ty
""",
        "S P P P S S",
        items=[I("margherita_pizza", 1, "extra_large", ["xl marg", "no basil"], [rm("basil", "no basil")])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0097",
        """
c: veggie burger w cheese n 2 onion rings
c: for the 15th, pickup at 1
c: omar, card
""",
        "P P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger w cheese"], [add("cheese", "w cheese")]),
            I("onion_rings", 2, None, ["2 onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 1", "13:00"),
        day=("date", None, 15, "the 15th"),
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t7-0098",
        """
c: 4 large drips
c: lg cap w hazelnut
c: lg hot choc no whip w oat
c: n a lg americano w caramel
c: pickup maya
""",
        "P P P P P",
        items=[
            I("drip_coffee", 4, "large", ["4 large drips"]),
            I("cappuccino", 1, "large", ["lg cap w hazelnut"], [add("hazelnut_syrup", "w hazelnut")]),
            I(
                "hot_chocolate",
                1,
                "large",
                ["lg hot choc no whip w oat"],
                [rm("whipped_cream", "no whip"), sub("whole_milk", "oat_milk", "w oat")],
            ),
            I("americano", 1, "large", ["a lg americano w caramel"], [add("caramel_syrup", "w caramel")]),
        ],
        method="pickup",
        method_q="pickup",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0099",
        """
c: Hi, I'd like to order for October 4th at 6pm: a milkshake and 3 lemonades for pickup. Name is Ana, paying by card.
""",
        "P",
        items=[
            I("milkshake", 1, None, ["a milkshake"]),
            I("lemonade", 3, None, ["3 lemonades"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 6pm", "18:00"),
        day=("date", 10, 4, "October 4th"),
        pay="card",
        pay_q="paying by card",
        name="Ana",
    ),
    X(
        "syn-t7-0100",
        """
c: the one i always get 🍔 to 247 chestnut st
b: Hi! We can't see past orders here, sorry. What would you like?
c: oh 😅 bacon burger, regular fries, 2 cokes, a sprite n a lemonade. card
""",
        "P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger"]),
            I("fries", 1, "regular", ["regular fries"]),
            I("coke", 2, None, ["2 cokes"]),
            I("sprite", 1, None, ["a sprite"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="to 247 chestnut st",
        addr={"raw": "247 chestnut st", "number": "247", "street": "chestnut st"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0101",
        """
c: hi 👋
c: veggie burger
c: can u put a fried egg on it 🍳
c: n a lemonade
c: pickup omar
c: card
""",
        "S P P P P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger", "a fried egg on it"], [offmod("a fried egg")]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t7-0102",
        """
c: A personal pepperoni with parmesan, please.
c: For pickup at 10:15.
c: Name is Ana.
c: Card.
""",
        "P P P P",
        items=[
            I(
                "pepperoni_pizza",
                1,
                "personal",
                ["A personal pepperoni with parmesan"],
                [add("parmesan", "with parmesan")],
            ),
        ],
        method="pickup",
        method_q="For pickup",
        time=("clock_time", "at 10:15", "22:15"),
        pay="card",
        pay_q="Card",
        name="Ana",
    ),
    X(
        "syn-t7-0103",
        """
c: Hi! A small cocoa with hazelnut and a choc chip muffin for pickup in 15 minutes, name Sam.
""",
        "P",
        items=[
            I(
                "hot_chocolate",
                1,
                "small",
                ["A small cocoa with hazelnut"],
                [add("hazelnut_syrup", "with hazelnut")],
            ),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("relative", "in 15 minutes", None),
        name="Sam",
    ),
    X(
        "syn-t7-0104",
        """
c: Good morning, 2 medium cappuccinos for pickup at 8:30. Name's Ivy, paying cash.
b: Got it, Ivy: 2 medium Cappuccinos, pickup at 8:30, paying cash. Is that right?
c: Yes.
c: Sorry, make that just one cappuccino.
""",
        "P C M",
        items=[I("cappuccino", 1, "medium", ["2 medium cappuccinos", "just one cappuccino"])],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 8:30", "08:30"),
        pay="cash",
        pay_q="paying cash",
        name="Ivy",
    ),
    X(
        "syn-t7-0105",
        """
c: hey
c: a medium vegetarian
c: + a 2 liter of doctor pepper
c: pickup
c: card
""",
        "S P P P P",
        items=[
            I("veggie_pizza", 1, "medium", ["a medium vegetarian"]),
            I("dr_pepper", 1, "two_liter", ["a 2 liter of doctor pepper"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0106",
        """
c: almond croissant, 2 med americanos, a lg cap w skim
c: n a drip + a small hot choc w caramel
c: asap for maya, card
""",
        "P P P",
        items=[
            I("croissant", 1, "almond", ["almond croissant"]),
            I("americano", 2, "medium", ["2 med americanos"]),
            I("cappuccino", 1, "large", ["a lg cap w skim"], [sub("whole_milk", "skim_milk", "w skim")]),
            I("drip_coffee", 1, "medium", ["a drip"]),
            I(
                "hot_chocolate",
                1,
                "small",
                ["a small hot choc w caramel"],
                [add("caramel_syrup", "w caramel")],
            ),
        ],
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0107",
        """
c: a sesame w butter pls
b: A sesame bagel with butter?
c: ya. pickup, tom
""",
        "P P",
        items=[I("bagel", 1, "sesame", ["a sesame w butter"], [add("butter", "w butter")])],
        method="pickup",
        method_q="pickup",
        name="Tom",
        name_q="tom",
    ),
    X(
        "syn-t7-0108",
        """
c: Hi, I need 6 extra large Hawaiians, half of them with feta, plus a small meat lovers, a Dr Pepper and an order of breadsticks. Pickup for Grace, card.
""",
        "P",
        items=[
            I("hawaiian_pizza", 3, "extra_large", ["6 extra large Hawaiians"]),
            I(
                "hawaiian_pizza",
                3,
                "extra_large",
                ["6 extra large Hawaiians", "half of them with feta"],
                [add("feta_cheese", "with feta")],
            ),
            I("meat_lovers_pizza", 1, "small", ["a small meat lovers"]),
            I("dr_pepper", 1, "can", ["a Dr Pepper"]),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Grace",
    ),
    X(
        "syn-t7-0109",
        """
c: is the gluten free crust actually gf
b: Yes, it's certified gluten-free, though it's baked in a shared oven.
c: ok meat lovers on gluten free
c: no beef, add banana peppers
c: 2 iced teas
c: at 8:30, cash
""",
        "Q P P P P",
        items=[
            I(
                "meat_lovers_pizza",
                1,
                None,
                ["meat lovers on gluten free", "no beef, add banana peppers"],
                [
                    add("crust_gluten_free", "on gluten free"),
                    rm("beef", "no beef"),
                    add("banana_peppers", "add banana peppers"),
                ],
            ),
            I("iced_tea", 2, "can", ["2 iced teas"]),
        ],
        time=("clock_time", "at 8:30", "20:30"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0110",
        """
c: a choc chip muffin and 4 hot chocolates, ready in 20 min, card
b: Got it: 1 chocolate chip Muffin and 4 medium Hot Chocolates, ready in 20 minutes, paying by card. Is that right?
c: yes
c: can the hot chocolates be almond milk instead?
""",
        "P C M",
        items=[
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
            I(
                "hot_chocolate",
                4,
                "medium",
                ["4 hot chocolates", "can the hot chocolates be almond milk instead"],
                [sub("whole_milk", "almond_milk", "almond milk instead")],
            ),
        ],
        time=("relative", "in 20 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0111",
        """
c: hey 🍕 can i get a medium cheese w onions n 4 20oz sprites for friday
c: pickup for ivy, card
""",
        "P P",
        items=[
            I("cheese_pizza", 1, "medium", ["a medium cheese w onions"], [add("onions", "w onions")]),
            I("sprite", 4, "bottle_20oz", ["4 20oz sprites"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("ambiguous", "for friday"),
        day=("weekday", "fri", "friday"),
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t7-0112",
        """
c: a muffin n the usual
c: card
""",
        "P P",
        items=[
            I("muffin", 1, None, ["a muffin"]),
            I(None, 1, None, ["the usual"], unmatched="the usual", flag="item_menu_match"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0113",
        """
c: 3 medium caramel lattes, do u guys do sugar free caramel? n 2 large caramel caps, card
""",
        "P/Q",
        items=[
            I("latte", 3, "medium", ["3 medium caramel lattes"], [add("caramel_syrup", "caramel")]),
            I("cappuccino", 2, "large", ["2 large caramel caps"], [add("caramel_syrup", "caramel")]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0114",
        """
c: hi
c: a cinnamon raisin bagel, do u toast them? n a medium americano
b: We can toast it for you!
c: yes toasted pls. pickup at 9:15 for eli
""",
        "S P/Q P",
        items=[
            I("bagel", 1, "cinnamon_raisin", ["a cinnamon raisin bagel", "toasted pls"], [note("toasted")]),
            I("americano", 1, "medium", ["a medium americano"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9:15", "09:15"),
        name="Eli",
        name_q="eli",
    ),
    X(
        "syn-t7-0115",
        """
c: heyy
c: a few medium supremes on stuffed crust n a diet coke
c: delivery, card
""",
        "S P P",
        items=[
            I(
                "supreme_pizza",
                None,
                "medium",
                ["a few medium supremes on stuffed crust"],
                [add("crust_stuffed", "on stuffed crust")],
            ),
            I("diet_coke", 1, "can", ["a diet coke"]),
        ],
        method="delivery",
        method_q="delivery",
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0116",
        """
c: hey 👋
c: 2 small supremes, one w garlic 🧄
c: does the hawaiian come w red sauce?
b: Yes, tomato sauce, cheese, ham and pineapple.
c: ok a large hawaiian no sauce then
c: pickup luis 💳 card
""",
        "S P Q P P",
        items=[
            I("supreme_pizza", 1, "small", ["2 small supremes"]),
            I("supreme_pizza", 1, "small", ["2 small supremes", "one w garlic"], [add("garlic", "w garlic")]),
            I("hawaiian_pizza", 1, "large", ["a large hawaiian no sauce"], [rm("tomato_sauce", "no sauce")]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Luis",
        name_q="luis",
    ),
    X(
        "syn-t7-0117",
        """
c: HI
c: ONE KNOTS AND A LARGE RONI FOR PICKUP, JUNE, CASH
""",
        "S P",
        items=[
            I("garlic_knots", 1, None, ["ONE KNOTS"]),
            I("pepperoni_pizza", 1, "large", ["A LARGE RONI"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        pay="cash",
        pay_q="CASH",
        name="June",
        name_q="JUNE",
    ),
    X(
        "syn-t7-0118",
        """
c: Can I get 3 small BBQ chicken pizzas, one of them with banana peppers?
c: Also 2 bottled waters and a 20 oz Dr Pepper.
c: Delivered to 8975 Cedar Hill Terrace.
""",
        "P P P",
        items=[
            I("bbq_chicken_pizza", 2, "small", ["3 small BBQ chicken pizzas"]),
            I(
                "bbq_chicken_pizza",
                1,
                "small",
                ["3 small BBQ chicken pizzas", "one of them with banana peppers"],
                [add("banana_peppers", "with banana peppers")],
            ),
            I("water", 2, None, ["2 bottled waters"]),
            I("dr_pepper", 1, "bottle_20oz", ["a 20 oz Dr Pepper"]),
        ],
        method="delivery",
        method_q="Delivered to 8975 Cedar Hill Terrace",
        addr={"raw": "8975 Cedar Hill Terrace", "number": "8975", "street": "Cedar Hill Terrace"},
    ),
    X(
        "syn-t7-0119",
        """
c: 2 BACON BURGERS AND A VEGGIE BURGER WITH CHEESE
c: 2 SPRITES, A COKE AND 2 LEMONADES
c: DELIVER TO 511 GRANT RD APT 28A
""",
        "P P P",
        items=[
            I("bacon_burger", 2, None, ["2 BACON BURGERS"]),
            I("veggie_burger", 1, None, ["A VEGGIE BURGER WITH CHEESE"], [add("cheese", "WITH CHEESE")]),
            I("sprite", 2, None, ["2 SPRITES"]),
            I("coke", 1, None, ["A COKE"]),
            I("lemonade", 2, None, ["2 LEMONADES"]),
        ],
        method="delivery",
        method_q="DELIVER TO 511 GRANT RD",
        addr={"raw": "511 GRANT RD APT 28A", "number": "511", "street": "GRANT RD", "unit": "APT 28A"},
    ),
    X(
        "syn-t7-0120",
        """
c: ASDKJ;LKKK
""",
        "U",
    ),
]
