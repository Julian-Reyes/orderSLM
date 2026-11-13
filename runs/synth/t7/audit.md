# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t7-0035: multi_message_order, claude-opus-5-5, halfmoon-pizza
Card: Builds the order over several messages, a thing or two at a time: 1 × Cheese Pizza (Large 14-inch). Never says whether it's pickup or delivery. Never says how they'll pay. Names an item only by a nickname or its parts ('bec', 'bacon egg n cheese', 'a number 2', '1 on a croissant' after asking about it) with its variant said casually.
Card check: items

- 0 customer: lemme get a large plain pie **[PLACE_ORDER]**
- 1 customer: and a big meat, medium **[PLACE_ORDER]**

  - L1: 1 × cheese_pizza large
  - L2: 1 × meat_lovers_pizza medium
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0103: simple_order, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Hot Chocolate (Small 8 oz), add Hazelnut syrup; 1 × Muffin (Chocolate chip). Will pick it up. Never says how they'll pay. Gives their name: Sam. Says when they want it: a relative time (like 'in 20 min'). Names an item only by a nickname or its parts ('bec', 'bacon egg n cheese', 'a number 2', '1 on a croissant' after asking about it) with its variant said casually.
Card check: agrees

- 0 customer: Hi! A small cocoa with hazelnut and a choc chip muffin for pickup in 15 minutes, name Sam. **[PLACE_ORDER]**

  - L1: 1 × hot_chocolate small add hazelnut_syrup
  - L2: 1 × muffin chocolate_chip
  - fulfillment pickup, address not_applicable, payment unknown, name Sam, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0131: missing_info, claude-opus-5-5, corner-patty
Card: Orders: 1 × Lemonade; 1 × Coke. Wants delivery to 3160 Thornton Ct (across from the park) (written the way the customer would type it). Never says how they'll pay. Never says how many of the first item: asks for it vaguely ('some', 'a few', 'muffins for the office'), and the chat ends before the business asks how many.
Card check: items

- 0 customer: Hi, could I get some lemonades and a Coke delivered to 3160 Thornton Ct, across from the park? **[PLACE_ORDER]**

  - L1: None × lemonade
  - L2: 1 × coke
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: item_quantity/ambiguous, payment_method/missing

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

## syn-t7-0142: multi_message_order, claude-opus-5-5, morning-crumb
Card: Builds the order over several messages, a thing or two at a time: 1 × Latte (Small 8 oz), Skim milk instead of Whole milk; 1 × Drip Coffee (the customer doesn't mention a size), add Hazelnut syrup; 1 × Breakfast Sandwich (the customer doesn't mention a size), no Bacon; 1 × Muffin (Blueberry); 2 × Cappuccino (Large 16 oz), Skim milk instead of Whole milk. Will pick it up. Pays by card. Gives their name: Eli.
Card check: agrees

- 0 customer: sm latte w skim, a drip w hazelnut **[PLACE_ORDER]**
- 1 customer: bec no bacon n a blueberry muffin **[PLACE_ORDER]**
- 2 customer: 2 lg caps w skim too **[PLACE_ORDER]**
- 3 customer: pickup eli, card **[PLACE_ORDER]**

  - L1: 1 × latte small substitute whole_milk→skim_milk
  - L2: 1 × drip_coffee medium add hazelnut_syrup
  - L3: 1 × breakfast_sandwich english_muffin remove bacon
  - L4: 1 × muffin blueberry
  - L5: 2 × cappuccino large substitute whole_milk→skim_milk
  - fulfillment pickup, address not_applicable, payment card, name Eli, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0153: implicit_category, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Americano (Small 8 oz), add Skim milk; 1 × Hot Chocolate (the customer doesn't mention a size). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Never says whether it's pickup or delivery. Pays by card. Names items without category words or only vaguely ('a veggie', 'a strawberry', 'something to snack on'); the menu or the business's reply settles each one.
Card check: agrees

- 0 customer: sm americano w skim **[PLACE_ORDER]**
- 1 customer: n a cocoa **[PLACE_ORDER]**
- 2 customer: card **[PLACE_ORDER]**
- 3 customer: ty **[SMALL_TALK]**

  - L1: 1 × americano small add skim_milk
  - L2: 1 × hot_chocolate medium
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0178: two_requests, claude-opus-5-5, corner-patty
Card: Orders: 2 orders of Fries (the customer doesn't mention a size). In the same message as the first item, also asks a question about the menu. Never says whether it's pickup or delivery. Pays cash. Says when they want it: a clock time (like 'at 6:30'). One customer message orders an item, asks a question in the middle, and goes on ordering after the question; every item named before and after the question is ordered.
Card check: items

- 0 customer: 2 fries, are they seasoned? and 2 cheeseburgers, at 8, cash **[PLACE_ORDER + MENU_QUESTION]**

  - L1: 2 × fries regular
  - L2: 2 × cheeseburger single
  - fulfillment unknown, address not_mentioned, payment cash, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0185: missing_info, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Muffin (Blueberry). Never says whether it's pickup or delivery. Pays by card. Also asks for one thing only vaguely ('that thing from before'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: hi! 2 blueberry muffins n which pastry is the most popular? **[PLACE_ORDER + MENU_QUESTION]**
- 1 business: The chocolate croissant and the banana nut muffin are tied!
- 2 customer: ok one of those too, card **[PLACE_ORDER]**

  - L1: 2 × muffin blueberry
  - L2: 1 × off-menu 'one of those'
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0188: correction, claude-opus-5-5, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, asks for the Hawaiian Pizza with Gluten-free crust (like 'make it gluten-free crust'). Their other details come before that change; nothing comes after it. Final order: 1 × Hawaiian Pizza (Medium 12-inch), no House cheese blend, add Gluten-free crust. Will pick it up. Pays cash.
Card check: agrees

- 0 customer: medium hawaiian **[PLACE_ORDER]**
- 1 customer: no cheese **[PLACE_ORDER]**
- 2 customer: pickup **[PLACE_ORDER]**
- 3 customer: cash **[PLACE_ORDER]**
- 4 customer: make it gluten free crust **[MODIFY_ORDER]**

  - L1: 1 × hawaiian_pizza medium remove cheese, add crust_gluten_free
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t7-0232: simple_order, claude-opus-5-5, corner-patty
Card: Orders: 2 orders of Onion Rings; 1 × Coke. Wants delivery to 40 Lakeview Terrace, unit 2C (written the way the customer would type it). Never says how they'll pay. Says when they want it: asap. Asks a menu question partway through. Names an item only by a nickname or its parts ('bec', 'bacon egg n cheese', 'a number 2', '1 on a croissant' after asking about it) with its variant said casually.
Card check: agrees

- 0 customer: do u have curly fries **[MENU_QUESTION]**
- 1 business: Sorry, just regular fries and onion rings.
- 2 customer: ok 2 rings n a cola then, asap to 40 lakeview terrace unit 2c **[PLACE_ORDER]**

  - L1: 2 × onion_rings
  - L2: 1 × coke
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

