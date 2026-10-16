# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-p1-0001: status_question, deepseek-flash@none, halfmoon-pizza
Card: Placed an order earlier (not in this chat) and asks where it is or when it will arrive.
Card check: agrees

- 0 customer: hey i ordered like 40 mins ago where is it rn **[ORDER_STATUS]**
- 1 business: hey! can u give me the name on the order so i can check for u?
- 2 customer: it's jamie, pls lemme know when it's gonna get here thx **[ORDER_STATUS]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0002: correction, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. First asks for 3 × Drip Coffee (Small 8 oz) (plus anything else below), then changes the quantity to 2. Final order: 2 × Drip Coffee (Small 8 oz). Will pick it up. Pays by card. Gives their name: Ana. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: HEY!! MORNING!! **[SMALL_TALK]**
- 1 customer: NEED 3 SMALL DRIP COFFEES FOR A MEETING!! **[PLACE_ORDER]**
- 2 customer: ACTUALLY MAKE IT 2 SMALL DRIP COFFEES!! SORRY, PEOPLE BAILED! **[MODIFY_ORDER]**
- 3 business: Got it! 2 small drip coffees. What name should I put on it?
- 4 customer: ANA! AND I'LL GRAB IT IN 20 MIN! I'LL PAY BY CARD!! **[PLACE_ORDER]**

  - L1: 2 × drip_coffee small
  - fulfillment pickup, address not_applicable, payment card, name Ana, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0003: implicit_category, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 1 order of Fries. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Wants delivery and gives a made-up street address (number and street, maybe an apt). Pays by card. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: can u do fries rn **[PLACE_ORDER]**
- 2 business: Hi! Yes we can. Regular or large?
- 3 customer: regular pls **[MODIFY_ORDER]**
- 4 customer: delivery to 418 Maple St apt 3B **[PLACE_ORDER]**
- 5 business: Got it, delivery to 418 Maple St apt 3B. Payment by card?
- 6 customer: yep card **[PLACE_ORDER]**
- 7 customer: want it in like 20 min thx **[PLACE_ORDER]**

  - L1: 1 × fries regular
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0004: multi_message_order, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 1 × Croissant, add Butter; 1 × Croissant (Plain), add Butter; 2 × Americano (Small 8 oz). Will pick it up. Pays by card. Gives their name: Ben. Says when they want it: asap.
Card check: items, labels (expected labels not found: SMALL_TALK)

- 0 customer: Hello, I would like to place an order for pickup, please. My name is Ben. **[PLACE_ORDER]**
- 1 business: Hi Ben! What can I get started for you?
- 2 customer: I would like one croissant with butter, please. **[PLACE_ORDER]**
- 3 business: Got it. Anything else?
- 4 customer: Yes, I also need one plain croissant with butter, and two small Americanos. I will be paying with card and need this as soon as possible. **[PLACE_ORDER]**

  - L1: 2 × croissant plain add butter
  - L2: 2 × americano small
  - fulfillment pickup, address not_applicable, payment card, name Ben, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0005: cancellation, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 2 orders of Garlic Knots (6 pieces each); 1 × Veggie Pizza (Medium 12-inch). Then cancels the whole order before it is placed (the last customer message is the cancellation). Will pick it up. Never says how they'll pay.
Card check: agrees

- 0 customer: Hi, I would like to order two orders of Garlic Knots and one medium Veggie Pizza. **[PLACE_ORDER]**
- 1 business: Hello! I have two orders of Garlic Knots and one medium Veggie Pizza for you. Would you like anything else today?
- 2 customer: Actually, I am so sorry, but something just came up and I need to cancel this order entirely. Please disregard. **[CANCEL_ORDER]**

  - L1: 2 × garlic_knots
  - L2: 1 × veggie_pizza medium
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0006: implicit_category, deepseek-flash@none, halfmoon-pizza
Card: Orders: 1 × Meat Lovers Pizza (Medium 12-inch), no Tomato sauce. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Wants delivery and gives a made-up street address (number and street, maybe an apt). Pays by card.
Card check: agrees

- 0 customer: yo u guys still open **[DELIVERY_QUESTION]**
- 1 business: yep, we're open till 11! what can i get u?
- 2 customer: cool just finished an exam lol. lemme get a medium meat lovers, no tomato sauce pls. delivering to 412 ashbury ave apt 6, payin by card thx **[PLACE_ORDER + SMALL_TALK]**

  - L1: 1 × meat_lovers_pizza medium remove tomato_sauce
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0007: cancellation, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Muffin (Banana nut); 1 × Croissant (Almond). Then cancels the whole order before it is placed (the last customer message is the cancellation). Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: Hi, I just finished my exam and I'd like to order a banana nut muffin and an almond croissant, please. **[PLACE_ORDER]**
- 1 business: Congrats on finishing your exam! So that's 1 banana nut muffin and 1 almond croissant?
- 2 customer: Yes, that's right. Thank you. **[CONFIRM_ORDER]**
- 3 business: Great, anything else to add?
- 4 customer: Actually, I'm going to cancel this order. Sorry about that, I changed my mind. **[CANCEL_ORDER]**

  - L1: 1 × muffin banana_nut
  - L2: 1 × croissant almond
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0009: cancellation, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Croissant (Chocolate), add Butter; 1 × Bagel (Everything); 1 × Muffin (Banana nut). Then cancels the whole order before it is placed (the last customer message is the cancellation). Will pick it up. Never says how they'll pay. Gives their name: Ben.
Card check: agrees

- 0 customer: HEY!! MORNING!! **[SMALL_TALK]**
- 1 business: Good morning! What can we get started for you?
- 2 customer: OK SO WE'RE DECIDING TOGETHER OVER HERE LOL!! CAN WE DO 2 CHOCOLATE CROISSANTS WITH BUTTER ON THEM?? **[PLACE_ORDER]**
- 3 customer: AND 1 EVERYTHING BAGEL!! **[PLACE_ORDER]**
- 4 customer: OH AND 1 BANANA NUT MUFFIN!! THAT'S IT!! **[PLACE_ORDER]**
- 5 business: Got it — 2 chocolate croissants with butter, 1 everything bagel, and 1 banana nut muffin. What name should I put this under?
- 6 customer: BEN!! **[PLACE_ORDER]**
- 7 business: Thanks Ben! We'll have that ready for pickup.
- 8 customer: WAIT ACTUALLY CANCEL THE WHOLE THING!! SORRY!! **[CANCEL_ORDER]**

  - L1: 2 × croissant chocolate add butter
  - L2: 1 × bagel everything
  - L3: 1 × muffin banana_nut
  - fulfillment unknown, address not_mentioned, payment unknown, name Ben, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0010: correction, gemini-3.1-flash-lite@minimal, morning-crumb
Card: First asks for 3 × Americano (Medium 12 oz), add Hazelnut syrup (plus anything else below), then swaps it for 2 × Cappuccino (Large 16 oz), add Vanilla syrup. Final order: 2 × Cappuccino (Large 16 oz), add Vanilla syrup; 1 × Cappuccino (Small 8 oz), Skim milk instead of Whole milk. Will pick it up. Pays cash. Gives their name: Keisha.
Card check: agrees

- 0 customer: Good morning. May I please place an order for three medium 12 oz Americanos with hazelnut syrup? **[PLACE_ORDER]**
- 1 business: Good morning! I can certainly help you with that. Anything else for you today?
- 2 customer: Actually, please excuse me, but I have changed my mind. Could I get two large 16 oz cappuccinos with vanilla syrup instead? **[MODIFY_ORDER]**
- 3 business: No problem at all. I have updated those to two large cappuccinos with vanilla syrup. Would you like to add anything else?
- 4 customer: Yes, thank you. Could I also add one small 8 oz cappuccino, but with skim milk instead of the usual whole milk, please? **[PLACE_ORDER]**
- 5 business: Certainly, one small cappuccino with skim milk is added. Is there anything else you need, or are you all set?
- 6 customer: That will be all, thank you. My name is Keisha, and I will be picking this up and paying with cash. **[PLACE_ORDER]**

  - L1: 2 × cappuccino large add vanilla_syrup
  - L2: 1 × cappuccino small substitute whole_milk→skim_milk
  - fulfillment pickup, address not_applicable, payment cash, name Keisha, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0012: implicit_category, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 2 × Diet Coke (Bottle 20 oz); 1 order of Breadsticks (4 pieces each). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Wants delivery and gives a made-up street address (number and street, maybe an apt). Pays by card.
Card check: agrees

- 0 customer: hey can i get 2 bottles of diet coke and an order of breadsticks pls **[PLACE_ORDER]**
- 1 business: Sure thing! Is that for pickup or delivery?
- 2 customer: delivery to 42 maple lane apt 3b thx also gonna pay w card **[PLACE_ORDER]**

  - L1: 2 × diet_coke bottle_20oz
  - L2: 1 × breadsticks
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0013: simple_order, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 2 × Coke (2-liter bottle); 3 × Veggie Pizza (Personal 8-inch); 1 × Diet Coke (Bottle 20 oz). Wants delivery and gives a made-up street address (number and street, maybe an apt). Pays by card.
Card check: agrees

- 0 customer: yo can i get 3 veggie personal pizzas and 2 2-liter cokes pls **[PLACE_ORDER]**
- 1 business: Sure thing! Anything else for you today?
- 2 customer: oh yeah lemme get a 20oz diet coke too. for delivery at 442 maple ave apt 3. paying w card thx **[PLACE_ORDER]**

  - L1: 3 × veggie_pizza personal
  - L2: 2 × coke two_liter
  - L3: 1 × diet_coke bottle_20oz
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0014: correction_after_confirmation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. First orders 2 orders of Garlic Knots (6 pieces each) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 order of Garlic Knots (6 pieces each). Wants delivery and gives a made-up street address (number and street, maybe an apt). Pays cash.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: HI!! hope ur open still!! **[SMALL_TALK]**
- 1 business: Hi there! Yes we're open until 11. What can I get started for you?
- 2 customer: I WANT 2 ORDERS OF GARLIC KNOTS PLEASE!!! 6 pieces each **[PLACE_ORDER]**
- 3 business: Got it, 2 orders of garlic knots, 6 pieces each. Anything else?
- 4 customer: NO WAIT ACTUALLY JUST 1 ORDER!! sorry im so scatterbrained today **[MODIFY_ORDER]**
- 5 customer: 1 order of garlic knots, 6 pieces, thats it!! **[MODIFY_ORDER]**
- 6 business: No problem! So just 1 order of garlic knots, 6 pieces. Delivery or pickup?
- 7 customer: DELIVERY PLEASE!! 418 Maple Ave apt 3B **[PLACE_ORDER]**
- 8 business: Perfect, delivering to 418 Maple Ave apt 3B. How are you paying?
- 9 customer: CASH!! ill have it ready at the door thx so much **[PLACE_ORDER]**

  - L1: 1 × garlic_knots
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0018: simple_order, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 1 × Lemonade; 2 × Coke. Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50).
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: lemme get a lemonade **[PLACE_ORDER]**
- 2 business: Hi! Sure, anything else?
- 3 customer: 2 cokes pls **[PLACE_ORDER]**
- 4 customer: pickup. paying cash, do u have change for a 50? **[PLACE_ORDER + PAYMENT_QUESTION]**

  - L1: 1 × lemonade
  - L2: 2 × coke
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p1-0042: two_requests, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 2 × Lemonade. In the same message as the first item, also asks a question about the menu. Never says whether it's pickup or delivery. Pays cash, and asks for change for a bill (a 20 or a 50).
Card check: agrees

- 0 customer: hey lemme get 2 lemonade pls. do u guys have any vegan options rn? **[PLACE_ORDER + MENU_QUESTION]**
- 1 business: Hi! Lemonade x2, got it. Sorry, no vegan burgers, but the Veggie Burger is meatless. It has mayo though, so not fully vegan.
- 2 customer: ok thx. u take cash right **[PAYMENT_QUESTION]**
- 3 business: Yes, we take cash or card.
- 4 customer: cool i got a 50 so can u make sure u have change for that **[PLACE_ORDER]**

  - L1: 2 × lemonade
  - fulfillment unknown, address not_mentioned, payment cash, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

