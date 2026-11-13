"""t7 syn-t7-0151–0180 (chats + labels by hand; see build.py)."""

from build import I, X, add, rm, sub

ENTRIES = [
    X(
        "syn-t7-0151",
        """
c: 2 personal hawaiians, 2 2-liter cokes n a can of diet coke 🍍 pickup asap for maya, card
b: Got it, Maya: 2 personal Hawaiian Pizzas, 2 Coke 2-liters and 1 Diet Coke (can), pickup as soon as possible, paying by card. Is that right?
c: yes!
c: oh skip the diet coke 🙏
""",
        "P C M",
        items=[
            I("hawaiian_pizza", 2, "personal", ["2 personal hawaiians"]),
            I("coke", 2, "two_liter", ["2 2-liter cokes"]),
        ],
        method="pickup",
        method_q="pickup",
        time=("asap", "asap", None),
        pay="card",
        pay_q="card",
        name="Maya",
        name_q="maya",
    ),
    X(
        "syn-t7-0152",
        """
c: one of ur bigger margheritas, no mozzarella, thin crust + a medium meat lovers n 2 sprites
c: to 312 riverside terrace, card 💳
""",
        "P P",
        items=[
            I(
                "margherita_pizza",
                1,
                None,
                ["one of ur bigger margheritas, no mozzarella, thin crust"],
                [rm("mozzarella", "no mozzarella"), add("crust_thin", "thin crust")],
                flag="item_variant",
            ),
            I("meat_lovers_pizza", 1, "medium", ["a medium meat lovers"]),
            I("sprite", 2, "can", ["2 sprites"]),
        ],
        method="delivery",
        method_q="to 312 riverside terrace",
        addr={"raw": "312 riverside terrace", "number": "312", "street": "riverside terrace"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0153",
        """
c: sm americano w skim
c: n a cocoa
c: card
c: ty
""",
        "P P P S",
        items=[
            I("americano", 1, "small", ["sm americano w skim"], [add("skim_milk", "w skim")]),
            I("hot_chocolate", 1, "medium", ["a cocoa"]),
        ],
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0154",
        """
c: 3 veggie burgers 2 w ketchup
c: cheeseburger no onions, 2 bacon burgers, 2 lemonades
c: to 1398 clement st #21b at 6, cash
""",
        "P P P",
        items=[
            I("veggie_burger", 1, None, ["3 veggie burgers"]),
            I("veggie_burger", 2, None, ["3 veggie burgers", "2 w ketchup"], [add("ketchup", "w ketchup")]),
            I("cheeseburger", 1, "single", ["cheeseburger no onions"], [rm("onion", "no onions")]),
            I("bacon_burger", 2, None, ["2 bacon burgers"]),
            I("lemonade", 2, None, ["2 lemonades"]),
        ],
        method="delivery",
        method_q="to 1398 clement st",
        time=("clock_time", "at 6", "18:00"),
        addr={"raw": "1398 clement st #21b", "number": "1398", "street": "clement st", "unit": "#21b"},
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0155",
        """
c: 3 PEPPERONI WITH FETA ON THICK CRUST AND 2 XL CHEESE
c: ASAP TO 979 FULTON BLVD, CASH
""",
        "P P",
        items=[
            I(
                "pepperoni_pizza",
                3,
                None,
                ["3 PEPPERONI WITH FETA ON THICK CRUST"],
                [add("feta_cheese", "WITH FETA"), add("crust_thick", "ON THICK CRUST")],
            ),
            I("cheese_pizza", 2, "extra_large", ["2 XL CHEESE"]),
        ],
        method="delivery",
        method_q="TO 979 FULTON BLVD",
        time=("asap", "ASAP", None),
        addr={"raw": "979 FULTON BLVD", "number": "979", "street": "FULTON BLVD"},
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t7-0156",
        """
c: hi, order for saturday at 8: 3 lattes, 4 everything bagels n a hot choc no whip
c: pickup for leah
""",
        "P P",
        items=[
            I("latte", 3, None, ["3 lattes"]),
            I("bagel", 4, "everything", ["4 everything bagels"]),
            I("hot_chocolate", 1, "medium", ["a hot choc no whip"], [rm("whipped_cream", "no whip")]),
        ],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 8", "08:00"),
        day=("weekday", "sat", "saturday"),
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t7-0157",
        """
c: hey there
c: 3 cbs, a bacon cheeseburger n 2 plant burgers no lettuce
c: deliver to 4594 delancey pl apt 2b
c: card
""",
        "S P P P",
        items=[
            I("cheeseburger", 3, "single", ["3 cbs"]),
            I("bacon_burger", 1, None, ["a bacon cheeseburger"]),
            I("veggie_burger", 2, None, ["2 plant burgers no lettuce"], [rm("lettuce", "no lettuce")]),
        ],
        method="delivery",
        method_q="deliver to 4594 delancey pl",
        addr={"raw": "4594 delancey pl apt 2b", "number": "4594", "street": "delancey pl", "unit": "apt 2b"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0158",
        """
c: 6 BACON BURGERS
c: HALF WITH MAYO
c: 2 LEMONADES, A COKE AND 4 SPRITES
c: DELIVER TO 9509 PROSPECT ST AT 3:30
c: CARD
""",
        "P P P P P",
        items=[
            I("bacon_burger", 3, None, ["6 BACON BURGERS"]),
            I("bacon_burger", 3, None, ["6 BACON BURGERS", "HALF WITH MAYO"], [add("mayo", "WITH MAYO")]),
            I("lemonade", 2, None, ["2 LEMONADES"]),
            I("coke", 1, None, ["A COKE"]),
            I("sprite", 4, None, ["4 SPRITES"]),
        ],
        method="delivery",
        method_q="DELIVER TO 9509 PROSPECT ST",
        time=("clock_time", "AT 3:30", "15:30"),
        addr={"raw": "9509 PROSPECT ST", "number": "9509", "street": "PROSPECT ST"},
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0159",
        """
c: 2 onion rings n a lemonade 🧅🍋
c: cash
c: actually just 1 onion rings
""",
        "P P M",
        items=[
            I("onion_rings", 1, None, ["2 onion rings", "just 1 onion rings"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0160",
        """
c: Hello!
c: An extra large margherita, a large veggie with no cheese, and an extra large cheese pizza with no sauce, ready in 30 minutes please.
b: Got it: 1 extra large Margherita Pizza, 1 large Veggie Pizza with no cheese and 1 extra large Cheese Pizza with no sauce, ready in 30 minutes. Is that right?
c: Yes, that's right.
c: Could you add garlic to the margherita?
""",
        "S P C M",
        items=[
            I(
                "margherita_pizza",
                1,
                "extra_large",
                ["An extra large margherita", "add garlic to the margherita"],
                [add("garlic", "add garlic")],
            ),
            I("veggie_pizza", 1, "large", ["a large veggie with no cheese"], [rm("cheese", "no cheese")]),
            I(
                "cheese_pizza",
                1,
                "extra_large",
                ["an extra large cheese pizza with no sauce"],
                [rm("tomato_sauce", "no sauce")],
            ),
        ],
        time=("relative", "in 30 minutes", None),
    ),
    X(
        "syn-t7-0161",
        """
c: hey
c: 2 vanilla shakes
c: pickup at 7:45 for keisha
c: card
""",
        "S P P P",
        items=[I("milkshake", 2, "vanilla", ["2 vanilla shakes"])],
        method="pickup",
        method_q="pickup",
        time=("clock_time", "at 7:45", "19:45"),
        pay="card",
        pay_q="card",
        name="Keisha",
        name_q="keisha",
    ),
    X(
        "syn-t7-0162",
        """
c: what comes in the #1? 🍔
b: The Cheeseburger Combo: a cheeseburger with a side (fries or onion rings) and a drink (Coke, Sprite or lemonade).
c: ok a #1 w rings n a sprite
c: + a regular fries 🍟
""",
        "Q P P",
        items=[
            I(
                "cheeseburger_combo",
                1,
                None,
                ["a #1 w rings n a sprite"],
                combo={"side": "onion_rings", "drink": "sprite"},
            ),
            I("fries", 1, "regular", ["a regular fries"]),
        ],
    ),
    X(
        "syn-t7-0163",
        """
c: Hi!
c: 4 personal meat lovers, 2 of them with fresh mozzarella, 2 extra large margheritas with no mozzarella, a medium pepperoni with no cheese on gluten-free crust, and a Sprite. Pickup for Eli, card.
""",
        "S P",
        items=[
            I("meat_lovers_pizza", 2, "personal", ["4 personal meat lovers"]),
            I(
                "meat_lovers_pizza",
                2,
                "personal",
                ["4 personal meat lovers", "2 of them with fresh mozzarella"],
                [add("mozzarella", "with fresh mozzarella")],
            ),
            I(
                "margherita_pizza",
                2,
                "extra_large",
                ["2 extra large margheritas with no mozzarella"],
                [rm("mozzarella", "no mozzarella")],
            ),
            I(
                "pepperoni_pizza",
                1,
                "medium",
                ["a medium pepperoni with no cheese on gluten-free crust"],
                [rm("cheese", "no cheese"), add("crust_gluten_free", "on gluten-free crust")],
            ),
            I("sprite", 1, "can", ["a Sprite"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Eli",
    ),
    X(
        "syn-t7-0164",
        """
c: 6 small drips
c: do u have vanilla syrup
b: Yes, we do!
c: 5 of the drips w vanilla then, + a croissant, 2 small americanos n a large latte
c: pickup ana
""",
        "P Q P P",
        items=[
            I("drip_coffee", 1, "small", ["6 small drips"]),
            I(
                "drip_coffee",
                5,
                "small",
                ["6 small drips", "5 of the drips w vanilla"],
                [add("vanilla_syrup", "w vanilla")],
            ),
            I("croissant", 1, "plain", ["a croissant"]),
            I("americano", 2, "small", ["2 small americanos"]),
            I("latte", 1, "large", ["a large latte"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Ana",
        name_q="ana",
    ),
    X(
        "syn-t7-0165",
        """
c: Hi, a veggie burger and a double cheeseburger.
c: Also onion rings and fries.
c: Pickup as soon as possible.
c: Cash, I'll have a 50.
""",
        "P P P P",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger"]),
            I("cheeseburger", 1, "double", ["a double cheeseburger"]),
            I("onion_rings", 1, None, ["onion rings"]),
            I("fries", 1, "regular", ["fries"]),
        ],
        method="pickup",
        method_q="Pickup",
        time=("asap", "as soon as possible", None),
        pay="cash",
        pay_q=["Cash", "I'll have a 50"],
        change=5000,
    ),
    X(
        "syn-t7-0166",
        """
c: 2 SHAKES, ONION RINGS AND A BACON BURGER NO ONIONS WITH JALAPENOS
c: TO 920 KENSINGTON PL AT 7:30, CARD
""",
        "P P",
        items=[
            I("milkshake", 2, None, ["2 SHAKES"]),
            I("onion_rings", 1, None, ["ONION RINGS"]),
            I(
                "bacon_burger",
                1,
                None,
                ["A BACON BURGER NO ONIONS WITH JALAPENOS"],
                [rm("onion", "NO ONIONS"), add("jalapeno", "WITH JALAPENOS")],
            ),
        ],
        method="delivery",
        method_q="TO 920 KENSINGTON PL",
        time=("clock_time", "AT 7:30", "19:30"),
        addr={"raw": "920 KENSINGTON PL", "number": "920", "street": "KENSINGTON PL"},
        pay="card",
        pay_q="CARD",
    ),
    X(
        "syn-t7-0167",
        """
c: 3 bec on english muffins
c: 2 small americanos n a plain bagel
c: a large hot choc w oat milk n a medium latte w almond
c: + a choc chip muffin, pickup for rosa
""",
        "P P P P",
        items=[
            I("breakfast_sandwich", 3, "english_muffin", ["3 bec on english muffins"]),
            I("americano", 2, "small", ["2 small americanos"]),
            I("bagel", 1, "plain", ["a plain bagel"]),
            I(
                "hot_chocolate",
                1,
                "large",
                ["a large hot choc w oat milk"],
                [sub("whole_milk", "oat_milk", "w oat milk")],
            ),
            I(
                "latte",
                1,
                "medium",
                ["a medium latte w almond"],
                [sub("whole_milk", "almond_milk", "w almond")],
            ),
            I("muffin", 1, "chocolate_chip", ["a choc chip muffin"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Rosa",
        name_q="rosa",
    ),
    X(
        "syn-t7-0168",
        """
c: sesame w tomato
c: cash
""",
        "P P",
        items=[I("bagel", 1, "sesame", ["sesame w tomato"], [add("tomato", "w tomato")])],
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0169",
        """
c: MUFFINS FOR THE OFFICE PLEASE, PICKUP FOR OMAR, CASH
""",
        "P",
        items=[I("muffin", None, None, ["MUFFINS FOR THE OFFICE"])],
        method="pickup",
        method_q="PICKUP",
        pay="cash",
        pay_q="CASH",
        name="Omar",
        name_q="OMAR",
    ),
    X(
        "syn-t7-0170",
        """
c: hi
c: lg latté
c: w whip
c: pickup leah
c: card
""",
        "S P P P P",
        items=[I("latte", 1, "large", ["lg latté", "w whip"], [add("whipped_cream", "w whip")])],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Leah",
        name_q="leah",
    ),
    X(
        "syn-t7-0171",
        """
c: Hi there!
c: Three small lattes, two of them with caramel, and a medium cappuccino with skim. Pickup for Luis.
""",
        "S P",
        items=[
            I("latte", 1, "small", ["Three small lattes"]),
            I(
                "latte",
                2,
                "small",
                ["Three small lattes", "two of them with caramel"],
                [add("caramel_syrup", "with caramel")],
            ),
            I(
                "cappuccino",
                1,
                "medium",
                ["a medium cappuccino with skim"],
                [sub("whole_milk", "skim_milk", "with skim")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        name="Luis",
    ),
    X(
        "syn-t7-0172",
        """
c: a shake, a coke n same as last time
c: asap to 7991 orchard pl #18b
""",
        "P P",
        items=[
            I("milkshake", 1, None, ["a shake"]),
            I("coke", 1, None, ["a coke"]),
            I(
                None,
                1,
                None,
                ["same as last time"],
                unmatched="same as last time",
                flag="item_menu_match",
            ),
        ],
        method="delivery",
        method_q="to 7991 orchard pl",
        time=("asap", "asap", None),
        addr={"raw": "7991 orchard pl #18b", "number": "7991", "street": "orchard pl", "unit": "#18b"},
    ),
    X(
        "syn-t7-0173",
        """
c: large fries n a lemonade
c: for the 27th at 12:30
c: deliver to 4094 alder pl #27b
c: card
""",
        "P P P P",
        items=[
            I("fries", 1, "large", ["large fries"]),
            I("lemonade", 1, None, ["a lemonade"]),
        ],
        method="delivery",
        method_q="deliver to 4094 alder pl",
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", None, 27, "the 27th"),
        addr={"raw": "4094 alder pl #27b", "number": "4094", "street": "alder pl", "unit": "#27b"},
        pay="card",
        pay_q="card",
    ),
    X(
        "syn-t7-0174",
        """
c: yo
c: does the bacon burger come w cheese
b: Yes, it does.
c: 4 bacon burgers then, 3 no cheese
c: n a coke
c: pickup marcus
c: card
""",
        "S Q P P P P",
        items=[
            I("bacon_burger", 1, None, ["4 bacon burgers"]),
            I("bacon_burger", 3, None, ["4 bacon burgers", "3 no cheese"], [rm("cheese", "no cheese")]),
            I("coke", 1, None, ["a coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Marcus",
        name_q="marcus",
    ),
    X(
        "syn-t7-0175",
        """
c: Hi!
c: 4 chocolate croissants, a sesame bagel and a breakfast sandwich with no egg.
c: Pickup for Eli, card.
c: Actually, make it 3 chocolate croissants.
""",
        "S P P M",
        items=[
            I("croissant", 3, "chocolate", ["4 chocolate croissants", "make it 3 chocolate croissants"]),
            I("bagel", 1, "sesame", ["a sesame bagel"]),
            I(
                "breakfast_sandwich",
                1,
                "english_muffin",
                ["a breakfast sandwich with no egg"],
                [rm("egg", "no egg")],
            ),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Eli",
    ),
    X(
        "syn-t7-0176",
        """
c: Hi, I'd like 3 double cheeseburgers with no ketchup, 3 regular fries and a milkshake.
c: Pickup for Luis, card.
""",
        "P P",
        items=[
            I(
                "cheeseburger",
                3,
                "double",
                ["3 double cheeseburgers with no ketchup"],
                [rm("ketchup", "no ketchup")],
            ),
            I("fries", 3, "regular", ["3 regular fries"]),
            I("milkshake", 1, None, ["a milkshake"]),
        ],
        method="pickup",
        method_q="Pickup",
        pay="card",
        pay_q="card",
        name="Luis",
    ),
    X(
        "syn-t7-0177",
        """
c: 4 croissants, 3 w butter
c: is the breakfast sandwich good on a croissant?
b: It's one of our favorites!
c: ok 1 on a croissant too
c: pickup asap, ivy, card
""",
        "P Q P P",
        items=[
            I("croissant", 1, "plain", ["4 croissants"]),
            I("croissant", 3, "plain", ["4 croissants", "3 w butter"], [add("butter", "w butter")]),
            I("breakfast_sandwich", 1, "croissant", ["1 on a croissant"]),
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
        "syn-t7-0178",
        """
c: 2 fries, are they seasoned? and 2 cheeseburgers, at 8, cash
""",
        "P/Q",
        items=[
            I("fries", 2, "regular", ["2 fries"]),
            I("cheeseburger", 2, "single", ["2 cheeseburgers"]),
        ],
        time=("clock_time", "at 8", "20:00"),
        pay="cash",
        pay_q="cash",
    ),
    X(
        "syn-t7-0179",
        """
c: HELLO
c: 4 SMALL CAPPUCCINOS, CASH
c: ADD CARAMEL TO ALL OF THEM PLEASE
""",
        "S P P",
        items=[
            I(
                "cappuccino",
                4,
                "small",
                ["4 SMALL CAPPUCCINOS", "ADD CARAMEL TO ALL OF THEM"],
                [add("caramel_syrup", "ADD CARAMEL")],
            ),
        ],
        pay="cash",
        pay_q="CASH",
    ),
    X(
        "syn-t7-0180",
        """
c: hey
c: 2 shakes, a lemonade n a veggie burger no lettuce
c: to 4 kensington rd
c: cash
""",
        "S P P P",
        items=[
            I("milkshake", 2, None, ["2 shakes"]),
            I("lemonade", 1, None, ["a lemonade"]),
            I("veggie_burger", 1, None, ["a veggie burger no lettuce"], [rm("lettuce", "no lettuce")]),
        ],
        method="delivery",
        method_q="to 4 kensington rd",
        addr={"raw": "4 kensington rd", "number": "4", "street": "kensington rd"},
        pay="cash",
        pay_q="cash",
    ),
]
