"""fresh5 a-fresh5-001–028 (chats + gold by hand; see build.py)."""

from build import F, I, add, offmod, rm

ENTRIES = [
    F(
        "a-fresh5-001",
        """
c: hi ☕ what muffins do u have?
b: Blueberry, chocolate chip and banana nut!
c: a blueberry n one of the other ones 🧁 pickup for wren
c: oh n make it 2 blueberry
""",
        "Q P M",
        start="Tue 08:40",
        items=[
            I("muffin", 2, "blueberry", ["a blueberry", "make it 2 blueberry"]),
            I("muffin", 1, None, ["one of the other ones"], flag="item_variant"),
        ],
        method="pickup",
        method_q="pickup",
        name="Wren",
        name_q="wren",
        annotation="'one of the other ones' after three flavors were listed fits chocolate chip or banana nut: "
        "item_variant/ambiguous.",
    ),
    F(
        "a-fresh5-002",
        """
c: hey 👋
c: what time do u close tonight? 🍔
c: n r u open sunday?
""",
        "S D D",
        start="Wed 20:15",
    ),
    F(
        "a-fresh5-003",
        """
c: hi
c: need pizza tmrw
c: 2 large pepperoni
c: n a large cheese
c: 2 liter coke
c: deliver to 415 spruce st
c: at 6:30
""",
        "S P P P P P P",
        start="Thu 13:20",
        items=[
            I("pepperoni_pizza", 2, "large", ["2 large pepperoni"]),
            I("cheese_pizza", 1, "large", ["a large cheese"]),
            I("coke", 1, "two_liter", ["2 liter coke"]),
        ],
        method="delivery",
        method_q="deliver to 415 spruce st",
        addr={"raw": "415 spruce st", "number": "415", "street": "spruce st"},
        time=("clock_time", "at 6:30", "18:30"),
        day=("tomorrow", "tmrw"),
        annotation="The day is in the second message, the time in the last: tomorrow at 18:30 (open 12-23).",
    ),
    F(
        "a-fresh5-004",
        """
c: hey 🍕 an xl meat lovers n 2 orders of garlic knots for pickup
b: Got it: 1 extra large Meat Lovers Pizza and 2 orders of Garlic Knots, pickup. How would you like to pay?
c: hmm actually thats too pricey for me rn 😕 cancel it pls
c: sorry!
""",
        "P X S",
        start="Fri 18:45",
        items=[
            I("meat_lovers_pizza", 1, "extra_large", ["an xl meat lovers"]),
            I("garlic_knots", 2, None, ["2 orders of garlic knots"]),
        ],
        method="pickup",
        method_q="for pickup",
        decision="cancelled",
        decision_q="cancel it",
    ),
    F(
        "a-fresh5-005",
        """
c: QUICK QUESTION
c: HOW MANY PLAYERS ARE ON A SOCCER TEAM?
""",
        "S O",
        start="Sat 10:05",
    ),
    F(
        "a-fresh5-006",
        """
c: IS THIS THE NAIL SALON NEXT DOOR?
c: NEED TO BOOK FOR 3PM
""",
        "O O",
        start="Mon 14:30",
    ),
    F(
        "a-fresh5-007",
        """
c: hi 🍕 3 medium margheritas
c: 2 of them thin crust
c: to 88 kensington ave apt 4
c: card 💳
""",
        "P P P P",
        start="Tue 19:10",
        items=[
            I("margherita_pizza", 1, "medium", ["3 medium margheritas", "2 of them thin crust"]),
            I(
                "margherita_pizza",
                2,
                "medium",
                ["3 medium margheritas", "2 of them thin crust"],
                [add("crust_thin", "thin crust")],
            ),
        ],
        method="delivery",
        method_q="to 88 kensington ave apt 4",
        addr={"raw": "88 kensington ave apt 4", "number": "88", "street": "kensington ave", "unit": "apt 4"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-008",
        """
c: Hi, I'd like two bacon burgers and a large fries delivered to 77 Orchard Rd on Dec 3 at 12:30, paying by card.
""",
        "P",
        start="Mon 15:00",
        items=[
            I("bacon_burger", 2, None, ["two bacon burgers"]),
            I("fries", 1, "large", ["a large fries"]),
        ],
        method="delivery",
        method_q="delivered to 77 Orchard Rd",
        addr={"raw": "77 Orchard Rd", "number": "77", "street": "Orchard Rd"},
        time=("clock_time", "at 12:30", "12:30"),
        day=("date", 12, 3, "Dec 3"),
        pay="card",
        pay_q="paying by card",
    ),
    F(
        "a-fresh5-009",
        """
c: med americano, a plain croissant n a choc chip muffin, card
b: Got it: 1 medium Americano, 1 plain croissant and 1 chocolate chip muffin, paying by card. Is that right?
c: yep
c: actually drop the muffin
""",
        "P C M",
        start="Wed 09:15",
        items=[
            I("americano", 1, "medium", ["med americano"]),
            I("croissant", 1, "plain", ["a plain croissant"]),
        ],
        pay="card",
        pay_q="card",
        annotation="The yes came while pickup/delivery was still missing, and the removal resets it: pending.",
    ),
    F(
        "a-fresh5-010",
        """
c: hiya ☀️ a large hot choc n an everything bagel w cream cheese 🥯
c: pickup for june, paying cash 💵
""",
        "P P",
        start="Thu 08:05",
        items=[
            I("hot_chocolate", 1, "large", ["a large hot choc"]),
            I(
                "bagel",
                1,
                "everything",
                ["an everything bagel w cream cheese"],
                [add("cream_cheese", "w cream cheese")],
            ),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="paying cash",
        name="June",
        name_q="june",
    ),
    F(
        "a-fresh5-011",
        """
c: Hello, I'm ordering for a team lunch.
c: Two large pepperoni pizzas, one large veggie pizza with no olives, one medium Hawaiian, two orders of breadsticks and a 2-liter Sprite, please.
c: Deliver to 1200 Harbor Blvd, suite 5.
c: I'll pay by card.
""",
        "P P P P",
        start="Wed 12:20",
        items=[
            I("pepperoni_pizza", 2, "large", ["Two large pepperoni pizzas"]),
            I(
                "veggie_pizza",
                1,
                "large",
                ["one large veggie pizza with no olives"],
                [rm("olives", "no olives")],
            ),
            I("hawaiian_pizza", 1, "medium", ["one medium Hawaiian"]),
            I("breadsticks", 2, None, ["two orders of breadsticks"]),
            I("sprite", 1, "two_liter", ["a 2-liter Sprite"]),
        ],
        method="delivery",
        method_q="Deliver to 1200 Harbor Blvd, suite 5",
        addr={
            "raw": "1200 Harbor Blvd, suite 5",
            "number": "1200",
            "street": "Harbor Blvd",
            "unit": "suite 5",
        },
        pay="card",
        pay_q="I'll pay by card",
    ),
    F(
        "a-fresh5-012",
        """
c: hey i ordered 2 cheeseburgers for pickup under kai, already paid online, got the screenshot
c: i can show it when i get there
""",
        "PC PC",
        start="Thu 17:40",
        order=False,
        annotation="A claim about an order placed earlier, not in this chat: PAYMENT_CLAIM, no gold order.",
    ),
    F(
        "a-fresh5-013",
        """
c: hi! a medium cappuccino n a plain bagel for pickup, name's ada, card 💳 n can u add honey to the bagel? 🍯
""",
        "P",
        start="Fri 10:30",
        items=[
            I("cappuccino", 1, "medium", ["a medium cappuccino"]),
            I("bagel", 1, "plain", ["a plain bagel", "add honey to the bagel"], [offmod("honey")]),
        ],
        method="pickup",
        method_q="for pickup",
        pay="card",
        pay_q="card",
        name="Ada",
        name_q="ada",
    ),
    F(
        "a-fresh5-014",
        """
c: large bbq chicken n a 20 oz dr pepper
c: to 503 fulton st
c: cash
c: actually swap the bbq chicken for a large supreme
""",
        "P P P M",
        start="Sat 18:30",
        items=[
            I("supreme_pizza", 1, "large", ["a large supreme"]),
            I("dr_pepper", 1, "bottle_20oz", ["a 20 oz dr pepper"]),
        ],
        method="delivery",
        method_q="to 503 fulton st",
        addr={"raw": "503 fulton st", "number": "503", "street": "fulton st"},
        pay="cash",
        pay_q="cash",
    ),
    F(
        "a-fresh5-015",
        """
c: 2 DOUBLE CHEESEBURGERS AND A STRAWBERRY SHAKE
c: DO THE BURGERS COME WITH PICKLES?
b: Yes, pickles come on every burger. We can leave them off.
c: LEAVE THEM OFF PLEASE. DELIVER TO 40 RIVERSIDE DR, CASH
""",
        "P Q P",
        start="Sun 13:10",
        items=[
            I(
                "cheeseburger",
                2,
                "double",
                ["2 DOUBLE CHEESEBURGERS", "LEAVE THEM OFF"],
                [rm("pickle", "LEAVE THEM OFF")],
            ),
            I("milkshake", 1, "strawberry", ["A STRAWBERRY SHAKE"]),
        ],
        method="delivery",
        method_q="DELIVER TO 40 RIVERSIDE DR",
        addr={"raw": "40 RIVERSIDE DR", "number": "40", "street": "RIVERSIDE DR"},
        pay="cash",
        pay_q="CASH",
        annotation="Leaving off the pickles before any confirmation adds a detail: PLACE_ORDER.",
    ),
    F(
        "a-fresh5-016",
        """
c: hey
c: medium pepperoni
c: n an order of knots, do u deliver to the east side?
b: Yes, within 5 miles of the shop!
c: eh ill just pick it up
c: card
""",
        "S P P/D P P",
        start="Mon 18:00",
        items=[
            I("pepperoni_pizza", 1, "medium", ["medium pepperoni"]),
            I("garlic_knots", 1, None, ["an order of knots"]),
        ],
        method="pickup",
        method_q="pick it up",
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-017",
        """
c: good morning ☀️
c: 2 sm lattes, a chocolate croissant n a sesame bagel, pickup for theo
c: oh skip the bagel 🙏
""",
        "S P M",
        start="Tue 07:45",
        items=[
            I("latte", 2, "small", ["2 sm lattes"]),
            I("croissant", 1, "chocolate", ["a chocolate croissant"]),
        ],
        method="pickup",
        method_q="pickup",
        name="Theo",
        name_q="theo",
    ),
    F(
        "a-fresh5-018",
        """
c: ok weird q but settling a bet
c: how tall is the empire state building
""",
        "S O",
        start="Wed 16:20",
    ),
    F(
        "a-fresh5-019",
        """
c: GOOD MORNING!
c: A SMALL AMERICANO AND A BANANA NUT MUFFIN FOR PICKUP, NAME IS ROSS, CARD
b: Got it, Ross: 1 small Americano and 1 banana nut muffin, pickup, paying by card. Is that right?
c: YES
c: SORRY MAKE THE AMERICANO A LARGE
""",
        "S P C M",
        start="Thu 08:20",
        items=[
            I("americano", 1, "large", ["A SMALL AMERICANO", "MAKE THE AMERICANO A LARGE"]),
            I("muffin", 1, "banana_nut", ["A BANANA NUT MUFFIN"]),
        ],
        method="pickup",
        method_q="FOR PICKUP",
        pay="card",
        pay_q="CARD",
        name="Ross",
        name_q="ROSS",
    ),
    F(
        "a-fresh5-020",
        """
c: 2 single cheeseburgers n a fries 🍟
c: card 💳
c: oh make the burgers doubles n the fries a large 🍔
""",
        "P P M",
        start="Fri 12:50",
        items=[
            I("cheeseburger", 2, "double", ["2 single cheeseburgers", "make the burgers doubles"]),
            I("fries", 1, "large", ["a fries", "the fries a large"]),
        ],
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-021",
        """
c: hi 😊 a lg latte n 2 almond croissants for pickup at 10, name is ivy
c: card 💳
c: oh wait can we make it saturday at 10 instead? not in today 🙈
c: ty!
""",
        "P P M S",
        start="Tue 08:30",
        items=[
            I("latte", 1, "large", ["a lg latte"]),
            I("croissant", 2, "almond", ["2 almond croissants"]),
        ],
        method="pickup",
        method_q="for pickup",
        time=("clock_time", "at 10", "10:00"),
        day=("weekday", "sat", "saturday"),
        pay="card",
        pay_q="card",
        name="Ivy",
        name_q="ivy",
        annotation="Moved from today to Saturday at 10 before any confirmation: MODIFY_ORDER, day sat.",
    ),
    F(
        "a-fresh5-022",
        """
c: yo
c: putting in an order for friday
c: 2 large supremes
c: an order of breadsticks
c: 3 cans of sprite
c: to 92 bayview ave
c: at 7:30
""",
        "S P P P P P P",
        start="Mon 16:00",
        items=[
            I("supreme_pizza", 2, "large", ["2 large supremes"]),
            I("breadsticks", 1, None, ["an order of breadsticks"]),
            I("sprite", 3, "can", ["3 cans of sprite"]),
        ],
        method="delivery",
        method_q="to 92 bayview ave",
        addr={"raw": "92 bayview ave", "number": "92", "street": "bayview ave"},
        time=("clock_time", "at 7:30", "19:30"),
        day=("weekday", "fri", "friday"),
    ),
    F(
        "a-fresh5-023",
        """
c: 4 BACON BURGERS, 2 WITH NO TOMATO
c: PICKUP
c: CARD
""",
        "P P P",
        start="Wed 12:40",
        items=[
            I("bacon_burger", 2, None, ["4 BACON BURGERS, 2 WITH NO TOMATO"]),
            I("bacon_burger", 2, None, ["4 BACON BURGERS, 2 WITH NO TOMATO"], [rm("tomato", "NO TOMATO")]),
        ],
        method="pickup",
        method_q="PICKUP",
        pay="card",
        pay_q="CARD",
    ),
    F(
        "a-fresh5-024",
        """
c: hey r u guys hiring
c: id like to apply for delivery driver
""",
        "O O",
        start="Thu 15:10",
    ),
    F(
        "a-fresh5-025",
        """
c: a veggie burger n onion rings, is the veggie burger vegan?
b: The patty is vegan, but it comes with mayo. We can leave it off.
c: no mayo then
c: pickup for nora, cash
""",
        "P/Q P P",
        start="Fri 13:30",
        items=[
            I("veggie_burger", 1, None, ["a veggie burger", "no mayo"], [rm("mayo", "no mayo")]),
            I("onion_rings", 1, None, ["onion rings"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="cash",
        pay_q="cash",
        name="Nora",
        name_q="nora",
    ),
    F(
        "a-fresh5-026",
        """
c: lg hawaiian, med meat lovers n an order of knots
c: 2 dr peppers too
c: 640 larkin st, card
""",
        "P P P",
        start="Sat 19:00",
        items=[
            I("hawaiian_pizza", 1, "large", ["lg hawaiian"]),
            I("meat_lovers_pizza", 1, "medium", ["med meat lovers"]),
            I("garlic_knots", 1, None, ["an order of knots"]),
            I("dr_pepper", 2, None, ["2 dr peppers"]),
        ],
        method="delivery",
        method_q="640 larkin st",
        addr={"raw": "640 larkin st", "number": "640", "street": "larkin st"},
        pay="card",
        pay_q="card",
    ),
    F(
        "a-fresh5-027",
        """
c: medium pepperoni w arugula
c: n a can of diet coke
c: is the diet coke cold?
b: Yes, straight from the fridge!
c: cool, pickup for sasha, card
""",
        "P P Q P",
        start="Sun 17:00",
        items=[
            I("pepperoni_pizza", 1, "medium", ["medium pepperoni w arugula"], [offmod("w arugula")]),
            I("diet_coke", 1, "can", ["a can of diet coke"]),
        ],
        method="pickup",
        method_q="pickup",
        pay="card",
        pay_q="card",
        name="Sasha",
        name_q="sasha",
    ),
    F(
        "a-fresh5-028",
        """
c: hi
c: so
c: can i get
c: the one w
c: the choc
""",
        "S U U U U",
        start="Mon 09:00",
        annotation="Fragments that never name an item: UNKNOWN, no order.",
    ),
]
