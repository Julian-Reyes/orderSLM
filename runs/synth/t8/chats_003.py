"""t8 syn-t8-0061–0090 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t8-0061",
        """
c: DO YOU HAVE OAT MILK FOR THE HOT CHOCOLATE?
b: Yes, we can make it with oat milk.
c: OK 3 HOT CHOCOLATES WITH OAT MILK, A SESAME BAGEL WITH EGG AND A COFFEE. PICKUP FOR JUNE, CARD
b: Got it, June: 3 hot chocolates with oat milk, 1 sesame bagel with egg and 1 drip coffee, pickup, paying by card. Is that right?
c: YUP
""",
        "Q P C",
        items=[
            I(
                "hot_chocolate",
                3,
                None,
                ["3 HOT CHOCOLATES WITH OAT MILK"],
                [sub("whole_milk", "oat_milk", "WITH OAT MILK")],
            ),
            I("bagel", 1, "sesame", ["A SESAME BAGEL WITH EGG"], [add("egg", "WITH EGG")]),
            I("drip_coffee", 1, None, ["A COFFEE"]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
        name="June",
        name_q="JUNE",
        decision="confirmed",
        decision_q="YUP",
    ),
    X(
        "syn-t8-0062",
        """
c: 2 supremes, the bigger size, n 2 cokes. pickup for ben, card
""",
        "P",
        items=[
            I("supreme_pizza", 2, None, ["2 supremes, the bigger size"], flag="item_variant"),
            I("coke", 2, None, ["2 cokes"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Ben",
        name_q="ben",
    ),
    X(
        "syn-t8-0063",
        """
c: hey is
c: ??
c: hm
""",
        "U U U",
    ),
    X(
        "syn-t8-0064",
        """
c: good morning ☀️
c: small cappuccino for pickup, name's grace
c: actually swap that for 2 large drip coffees w vanilla ☕☕
""",
        "S P M",
        items=[
            I(
                "drip_coffee",
                2,
                "large",
                ["2 large drip coffees w vanilla"],
                [add("vanilla_syrup", "w vanilla")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        name="Grace",
        name_q="grace",
    ),
    X(
        "syn-t8-0065",
        """
c: veggie burger
c: n a single cheeseburger w bacon
c: n a family size fries
c: pickup in 20, cash, i have a 20
""",
        "P P P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger"]),
            I("cheeseburger", 1, "single", ["a single cheeseburger w bacon"], [add("bacon", "w bacon")]),
            I("fries", 1, None, ["a family size fries"], unmatched_variant="family size"),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 20", None),
        pay="cash",
        pay_q=["cash", "i have a 20"],
        change=2000,
    ),
    X(
        "syn-t8-0066",
        """
c: 2 double cheeseburgers no pickles n a regular fries
c: do u have mustard?
b: Yes, we have mustard!
c: k n the one i always get too, delivery at 6:30, card
""",
        "P Q P",
        items=[
            I(
                "cheeseburger",
                2,
                "double",
                ["2 double cheeseburgers no pickles"],
                [rm("pickle", "no pickles")],
            ),
            I("fries", 1, "regular", ["a regular fries"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="delivery",
        time=("clock_time", "at 6:30", "18:30"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0067",
        """
c: 2 medium margheritas
c: one w no fresh mozz
c: is the basil fresh?
b: Yes, fresh basil every day.
c: cool
c: 3 iced teas 20 oz n 2 dr peppers
c: 113 willow creek st, card
""",
        "P P Q S P P",
        items=[
            I("margherita_pizza", 1, "medium", ["2 medium margheritas", "one w no fresh mozz"]),
            I(
                "margherita_pizza",
                1,
                "medium",
                ["2 medium margheritas", "one w no fresh mozz"],
                [rm("mozzarella", "no fresh mozz")],
            ),
            I("iced_tea", 3, "bottle_20oz", ["3 iced teas 20 oz"]),
            I("dr_pepper", 2, None, ["2 dr peppers"]),
        ],
        method="delivery",
        method_q="113 willow creek st",
        addr={"raw": "113 willow creek st", "number": "113", "street": "willow creek st"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0068",
        """
c: hey
c: 2 med americanos w vanilla n a plain bagel
c: pickup, nico, cash
b: Got it, Nico: 2 medium Americanos with vanilla and 1 plain bagel, pickup, paying cash. Is that right?
c: ya
c: oh sorry just 1 americano
""",
        "S P P C M",
        items=[
            I(
                "americano",
                1,
                "medium",
                ["2 med americanos w vanilla", "just 1 americano"],
                [add("vanilla_syrup", "w vanilla")],
            ),
            I("bagel", 1, "plain", ["a plain bagel"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Nico",
        name_q="nico",
    ),
    X(
        "syn-t8-0069",
        """
c: 2 lg drips w vanilla, a plain bagel w avo n a mango smoothie
c: pickup at 10:30 for priya, cash
""",
        "P P",
        items=[
            I("drip_coffee", 2, "large", ["2 lg drips w vanilla"], [add("vanilla_syrup", "w vanilla")]),
            I("bagel", 1, "plain", ["a plain bagel w avo"], [add("avocado", "w avo")]),
            I(None, 1, None, ["a mango smoothie"], unmatched="a mango smoothie"),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 10:30", "10:30"),
        pay="cash",
        pay_q="cash",
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t8-0070",
        """
c: hi
c: can i get a coffee, is it a dark roast?, n a plain croissant
b: It's a medium roast!
c: ok cool
c: pickup
c: ana
""",
        "S P/Q S P P",
        items=[
            I("drip_coffee", 1, None, ["a coffee"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t8-0071",
        """
c: sesame bagel w avo
c: lg americano
c: bec
c: n a breakfast burrito, card
""",
        "P P P P",
        items=[
            I("bagel", 1, "sesame", ["sesame bagel w avo"], [add("avocado", "w avo")]),
            I("americano", 1, "large", ["lg americano"]),
            I("breakfast_sandwich", 1, None, ["bec"]),
            I(None, 1, None, ["a breakfast burrito"], unmatched="a breakfast burrito"),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0072",
        """
c: Hi, I'd like the one I always get and two cans of Sprite.
b: Sorry, we can't see past orders here. What would you like?
c: It's the same as always. Delivery, I'll pay cash.
""",
        "P P",
        items=[
            I(
                None,
                1,
                None,
                ["the one I always get"],
                unmatched="the one I always get",
                flag="item_menu_match",
            ),
            I("sprite", 2, "can", ["two cans of Sprite"]),
        ],
        method="delivery",
        method_q="Delivery",
        pay="cash",
        pay_q="I'll pay cash",
    ),
    X(
        "syn-t8-0073",
        """
c: bacon burger no tomato
c: n a shake, one of the non vanilla ones
c: 31 prospect st apt 30a, cash
""",
        "P P P",
        items=[
            I("bacon_burger", 1, None, ["bacon burger no tomato"], [rm("tomato", "no tomato")]),
            I("milkshake", 1, None, ["a shake, one of the non vanilla ones"], flag="item_variant"),
        ],
        method="delivery",
        method_q="31 prospect st apt 30a",
        addr={"raw": "31 prospect st apt 30a", "number": "31", "street": "prospect st", "unit": "apt 30a"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0074",
        """
c: lemonades
c: a bunch
c: for the team
c: card
""",
        "P P P P",
        items=[I("lemonade", None, None, ["lemonades", "a bunch"])],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0075",
        """
c: Hi, I'd like the same as last time, please.
b: Sorry, we can't see past orders here. What would you like?
c: A large veggie pizza, two medium pepperonis with thick crust, two orders of garlic knots and a can of iced tea.
c: For pickup, paying by card.
""",
        "P P P",
        items=[
            I("veggie_pizza", 1, "large", ["A large veggie pizza"]),
            I(
                "pepperoni_pizza",
                2,
                "medium",
                ["two medium pepperonis with thick crust"],
                [add("crust_thick", "thick crust")],
            ),
            I("garlic_knots", 2, None, ["two orders of garlic knots"]),
            I("iced_tea", 1, "can", ["a can of iced tea"]),
        ],
        method="pickup",
        method_q="For pickup",
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t8-0076",
        """
c: Hello! I'd like to order a BBQ chicken pizza with no cheese for Wednesday, delivered to 6651 Kensington Blvd, apt 13B.
c: A medium, please, and around 6 is good. Actually let's say 6 exactly.
""",
        "P P",
        items=[
            I(
                "bbq_chicken_pizza",
                1,
                "medium",
                ["a BBQ chicken pizza with no cheese", "A medium"],
                [rm("cheese", "no cheese")],
            ),
        ],
        method="delivery",
        method_q="delivered to 6651 Kensington Blvd, apt 13B",
        addr={
            "raw": "6651 Kensington Blvd, apt 13B",
            "number": "6651",
            "street": "Kensington Blvd",
            "unit": "apt 13B",
        },
        time=("clock_time", "6 exactly", "18:00"),
        day=("weekday", "wed", "Wednesday"),
    ),
    X(
        "syn-t8-0077",
        """
c: Hi, a margherita with stuffed crust, an extra large hawaiian with no ham and an order of breadsticks.
c: How big is your large?
b: Large is 14 inches and extra large is 16.
c: Then one of the larger two for the margherita. Pickup for Nico, card.
""",
        "P Q P",
        items=[
            I(
                "margherita_pizza",
                1,
                None,
                ["a margherita with stuffed crust", "one of the larger two for the margherita"],
                [add("crust_stuffed", "stuffed crust")],
                flag="item_variant",
            ),
            I(
                "hawaiian_pizza",
                1,
                "extra_large",
                ["an extra large hawaiian with no ham"],
                [rm("ham", "no ham")],
            ),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Nico",
        name_q="Nico",
    ),
    X(
        "syn-t8-0078",
        """
c: plain croissant w butter
c: n a venti chai latte
c: pickup priya, card
""",
        "P P P",
        items=[
            I("croissant", 1, "plain", ["plain croissant w butter"], [add("butter", "w butter")]),
            I(None, 1, None, ["a venti chai latte"], unmatched="a venti chai latte"),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Priya",
        name_q="priya",
    ),
    X(
        "syn-t8-0079",
        """
c: 2 banana nut muffins
c: pickup
c: asap
c: ivy
c: card
c: actually no muffins, a bec on a bagel no cheese instead
""",
        "P P P P P M",
        items=[
            I(
                "breakfast_sandwich",
                1,
                "bagel",
                ["a bec on a bagel no cheese"],
                [rm("cheddar", "no cheese")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
    ),
    X(
        "syn-t8-0080",
        """
c: Good morning!
c: I'd like to order a coffee for tomorrow.
c: Is your coffee decaf available?
b: Sorry, we only have regular drip coffee.
c: Regular is fine. I'll be by at 8, paying by card.
""",
        "S P Q P",
        items=[I("drip_coffee", 1, None, ["a coffee"])],
        method="pickup",
        method_q="I'll be by",
        time=("clock_time", "at 8", "08:00"),
        day=("tomorrow", "tomorrow"),
        pay="card",
        pay_q="paying by card",
    ),
    X(
        "syn-t8-0081",
        """
c: yo
c: a lemonade
c: n the one i always get
c: ty
""",
        "S P P S",
        items=[
            I("lemonade", 1, None, ["a lemonade"]),
            I(
                None,
                1,
                None,
                ["the one i always get"],
                unmatched="the one i always get",
                flag="item_menu_match",
            ),
        ],
    ),
    X(
        "syn-t8-0082",
        """
c: 😶
""",
        "U",
    ),
    X(
        "syn-t8-0083",
        """
c: HELLO
c: A SMALL DRIP COFFEE AND 2 HOT CHOCOLATES WITH SKIM AND VANILLA
c: ALSO A BREAKFAST SANDWICH AND A CROISSANT
c: AND A LARGE LATTE WITH ALMOND MILK AND CARAMEL
""",
        "S P P P",
        items=[
            I("drip_coffee", 1, "small", ["A SMALL DRIP COFFEE"]),
            I(
                "hot_chocolate",
                2,
                None,
                ["2 HOT CHOCOLATES WITH SKIM AND VANILLA"],
                [sub("whole_milk", "skim_milk", "WITH SKIM"), add("vanilla_syrup", "VANILLA")],
            ),
            I("breakfast_sandwich", 1, None, ["A BREAKFAST SANDWICH"]),
            I("croissant", 1, None, ["A CROISSANT"]),
            I(
                "latte",
                1,
                "large",
                ["A LARGE LATTE WITH ALMOND MILK AND CARAMEL"],
                [sub("whole_milk", "almond_milk", "WITH ALMOND MILK"), add("caramel_syrup", "CARAMEL")],
            ),
        ],
    ),
    X(
        "syn-t8-0084",
        """
c: hey 🍔 ordering for tuesday oct 20
c: a bacon burger no bacon w avocado 🥑
c: a coke n a chocolate shake 🥤
c: to 2359 willow creek st at 12:30, card 💳
""",
        "P P P P",
        items=[
            I(
                "bacon_burger",
                1,
                None,
                ["a bacon burger no bacon w avocado"],
                [rm("bacon", "no bacon"), add("avocado", "w avocado")],
            ),
            I("coke", 1, None, ["a coke"]),
            I("milkshake", 1, "chocolate", ["a chocolate shake"]),
        ],
        method="delivery",
        method_q="to 2359 willow creek st",
        addr={"raw": "2359 willow creek st", "number": "2359", "street": "willow creek st"},
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", 10, 20, "oct 20"),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0085",
        """
c: can i order ahead for saturday?
b: Yes, you can order up to a week ahead!
c: great, 3 banana nut muffins, a croissant n a coffee w vanilla, pickup sat at 9, omar, card
""",
        "D P",
        items=[
            I("muffin", 3, "banana_nut", ["3 banana nut muffins"]),
            I("croissant", 1, None, ["a croissant"]),
            I("drip_coffee", 1, None, ["a coffee w vanilla"], [add("vanilla_syrup", "w vanilla")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 9", "09:00"),
        day=("weekday", "sat", "sat"),
        pay="card",
        pay_q="card",
        name="Omar",
        name_q="omar",
    ),
    X(
        "syn-t8-0086",
        """
c: hiya
c: lemme get that thing from before
b: Sorry, we can't see past orders here. What would you like?
c: oh ok. 4 lemonades, a veggie burger, an order of rings, 2 regular fries n a coke
c: cash, got a 50
""",
        "S P P P",
        items=[
            I("lemonade", 4, None, ["4 lemonades"]),
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("onion_rings", 1, None, ["an order of rings"]),
            I("fries", 2, "regular", ["2 regular fries"]),
            I("coke", 1, None, ["a coke"]),
        ],
        pay="cash",
        pay_q=["cash", "got a 50"],
        change=5000,
    ),
    X(
        "syn-t8-0087",
        """
c: 2 waters n a sprite 💧
c: in 30 min, card 💳
b: Got it: 2 bottled waters and 1 Sprite, ready in 30 minutes, paying by card. Pickup or delivery?
c: pickup. yes thats all
c: wait swap the sprite for 2 personal cheese pizzas 🍕
""",
        "P P P M",
        items=[
            I("water", 2, None, ["2 waters"]),
            I("cheese_pizza", 2, "personal", ["2 personal cheese pizzas"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("relative", "in 30 min", None),
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0088",
        """
c: hey
c: 4 orders of breadsticks n 3 sprites, pickup, cash
b: Got it: 4 orders of Breadsticks and 3 Sprites (cans), pickup, paying cash. Is that right?
c: yep
c: oh make the sprites 2 liters
""",
        "S P C M",
        items=[
            I("breadsticks", 4, None, ["4 orders of breadsticks"]),
            I("sprite", 3, "two_liter", ["3 sprites", "make the sprites 2 liters"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t8-0089",
        """
c: 6 large bbq chicken
c: 3 w gluten free crust
c: a small hawaiian w black olives n stuffed crust
c: 3 orders of knots n a water
c: 581 hawthorne rd
c: card
""",
        "P P P P P P",
        items=[
            I("bbq_chicken_pizza", 3, "large", ["6 large bbq chicken", "3 w gluten free crust"]),
            I(
                "bbq_chicken_pizza",
                3,
                "large",
                ["6 large bbq chicken", "3 w gluten free crust"],
                [add("crust_gluten_free", "gluten free crust")],
            ),
            I(
                "hawaiian_pizza",
                1,
                "small",
                ["a small hawaiian w black olives n stuffed crust"],
                [add("olives", "w black olives"), add("crust_stuffed", "stuffed crust")],
            ),
            I("garlic_knots", 3, None, ["3 orders of knots"]),
            I("water", 1, None, ["a water"]),
        ],
        method="delivery",
        method_q="581 hawthorne rd",
        addr={"raw": "581 hawthorne rd", "number": "581", "street": "hawthorne rd"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t8-0090",
        """
c: ordering for tmrw lunch
c: veggie burger
c: n a shake
c: pickup at 12
c: card
""",
        "P P P P P",
        items=[
            I("veggie_burger", 1, None, ["veggie burger"]),
            I("milkshake", 1, None, ["a shake"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 12", "12:00"),
        day=("tomorrow", "tmrw"),
        pay="card",
        pay_q="card",
    ),
]
