# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t7-0036: unclear_message, claude-opus-5-5, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: agrees

- 0 customer: Hi, could I get two dou **[UNKNOWN]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0062: simple_order, claude-opus-5-5, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 1 × Dr Pepper (the customer doesn't mention a size). Wants delivery to 59 Ivanhoe St (above the bakery) (written the way the customer would type it). Pays by card. Asks a menu question partway through. Names an item only by a nickname or its parts ('bec', 'bacon egg n cheese', 'a number 2', '1 on a croissant' after asking about it) with its variant said casually.
Card check: items

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: is the big meat spicy **[MENU_QUESTION]**
- 2 business: No, the Meat Lovers isn't spicy: pepperoni, sausage, ham, bacon and beef.
- 3 customer: ok a large big meat **[PLACE_ORDER]**
- 4 customer: n a dr pepper **[PLACE_ORDER]**
- 5 customer: 59 ivanhoe st above the bakery, delivery, card **[PLACE_ORDER]**

  - L1: 1 × meat_lovers_pizza large
  - L2: 1 × dr_pepper can
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0063: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 2 × Muffin (size/flavor not stated); 1 × Breakfast Sandwich (On a bagel), add Tomato. Never says the size or flavor of the item marked 'not stated'. Will pick it up. Pays by card. Gives their name: Rosa. The order is for a later day (tomorrow or a weekday) but the customer never says a time; the chat ends before the business asks.
Card check: agrees

- 0 customer: for tomorrow pls: 2 muffins n a bec on a bagel w tomato **[PLACE_ORDER]**
- 1 customer: pickup, rosa, card **[PLACE_ORDER]**

  - L1: 2 × muffin
  - L2: 1 × breakfast_sandwich bagel add tomato
  - fulfillment pickup, address not_applicable, payment card, name Rosa, decision pending
  - missing: item_variant/missing, requested_time/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0086: simple_order, claude-opus-5-5, morning-crumb
Card: Orders: 2 × Bagel (Everything); 4 × Bagel (Everything), add Butter; 1 × Drip Coffee (the customer doesn't mention a size); 3 × Muffin (Banana nut). Will pick it up. Never says how they'll pay. Gives their name: Ana. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: 6 everything bagels, 4 w butter, a drip n 3 banana nut muffins ☕ **[PLACE_ORDER]**
- 1 customer: pickup for ana 😊 **[PLACE_ORDER]**

  - L1: 2 × bagel everything
  - L2: 4 × bagel everything add butter
  - L3: 1 × drip_coffee medium
  - L4: 3 × muffin banana_nut
  - fulfillment pickup, address not_applicable, payment unknown, name Ana, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0137: two_requests, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Breakfast Sandwich (On an English muffin), no Cheddar. In the same message as the first item, also asks a question about the menu. Will pick it up. Pays by card. Gives their name: Grace. One customer message orders an item, asks a question in the middle, and goes on ordering after the question; every item named before and after the question is ordered.
Card check: items

- 0 customer: hi **[SMALL_TALK]**
- 1 customer: bec no cheese, can i get it on gluten free bread? if not english muffin is fine **[PLACE_ORDER + MENU_QUESTION]**
- 2 business: Sorry, no gluten-free bread. English muffin it is!
- 3 customer: ok + a medium latte **[PLACE_ORDER]**
- 4 customer: pickup grace **[PLACE_ORDER]**
- 5 customer: card **[PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich english_muffin remove cheddar
  - L2: 1 × latte medium
  - fulfillment pickup, address not_applicable, payment card, name Grace, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0187: simple_order, claude-opus-5-5, corner-patty
Card: Orders: 1 order of Fries (the customer doesn't mention a size); 1 × Sprite; 1 × Veggie Burger. Will pick it up. Pays by card. Gives their name: Tara. Says when they want it: a clock time (like 'at 6:30'). Asks for sriracha on the Veggie Burger, as if the place has it (it isn't on the menu).
Card check: agrees

- 0 customer: veggie burger w sriracha, fries n a sprite **[PLACE_ORDER]**
- 1 customer: pickup at 6:30 for tara **[PLACE_ORDER]**
- 2 customer: card **[PLACE_ORDER]**

  - L1: 1 × veggie_burger  add w sriracha
  - L2: 1 × fries regular
  - L3: 1 × sprite
  - fulfillment pickup, address not_applicable, payment card, name Tara, decision pending
  - missing: item_modification/off_menu

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0188: correction, claude-opus-5-5, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, asks for the Hawaiian Pizza with Gluten-free crust (like 'make it gluten-free crust'). Their other details come before that change; nothing comes after it. Final order: 1 × Hawaiian Pizza (Medium 12-inch), no House cheese blend, add Gluten-free crust. Will pick it up. Pays cash.
Card check: labels (expected labels not found: MODIFY_ORDER)

- 0 customer: medium hawaiian **[PLACE_ORDER]**
- 1 customer: no cheese **[PLACE_ORDER]**
- 2 customer: pickup **[PLACE_ORDER]**
- 3 customer: cash **[PLACE_ORDER]**
- 4 customer: make it gluten free crust **[PLACE_ORDER]**

  - L1: 1 × hawaiian_pizza medium remove cheese, add crust_gluten_free
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0207: simple_order, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Breakfast Sandwich (On a croissant). Will pick it up. Pays by card. Gives their name: Keisha. Says when they want it: asap. Asks for lavender syrup on the Breakfast Sandwich, as if the place has it (it isn't on the menu).
Card check: agrees

- 0 customer: bec on a croissant w lavender syrup **[PLACE_ORDER]**
- 1 customer: asap pickup keisha, card **[PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich croissant add w lavender syrup
  - fulfillment pickup, address not_applicable, payment card, name Keisha, decision pending
  - missing: item_modification/off_menu

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0209: implicit_category, claude-opus-5-5, halfmoon-pizza
Card: Orders: 1 × Diet Coke (2-liter bottle). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Wants delivery to 9484 Thornton Ln (written the way the customer would type it). Never says how they'll pay. Names items without category words or only vaguely ('a veggie', 'a strawberry', 'something to snack on'); the menu or the business's reply settles each one.
Card check: items

- 0 customer: can i get a 2 liter of diet n a large pepperoni to 9484 thornton ln **[PLACE_ORDER]**

  - L1: 1 × diet_coke two_liter
  - L2: 1 × pepperoni_pizza large
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0230: correction, claude-opus-5-5, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, adds BBQ sauce to the Hawaiian Pizza. Their other details come before that change; nothing comes after it. Final order: 1 × Bottled Water; 1 × Sprite (the customer doesn't mention a size); 1 × Hawaiian Pizza (Small 10-inch), add BBQ sauce. Wants delivery to 43 Vine Ave (side entrance) (written the way the customer would type it). Pays cash. Asks a menu question partway through.
Card check: labels (expected labels not found: MODIFY_ORDER)

- 0 customer: does the hawaiian have bbq sauce? **[MENU_QUESTION]**
- 1 business: No, it has tomato sauce, cheese, ham and pineapple.
- 2 customer: ok a small hawaiian, a water n a sprite to 43 vine ave, side entrance. cash **[PLACE_ORDER]**
- 3 customer: actually add bbq sauce to the hawaiian **[PLACE_ORDER]**

  - L1: 1 × hawaiian_pizza small add bbq_sauce
  - L2: 1 × water
  - L3: 1 × sprite can
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

