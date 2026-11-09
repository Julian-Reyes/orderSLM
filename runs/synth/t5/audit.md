# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t5-0050: missing_info, claude-opus-5-5, halfmoon-pizza
Card: Orders: 1 order of Breadsticks (4 pieces each). Never says whether it's pickup or delivery. Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min'). Also asks for one thing only vaguely ('same as last time'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: order of breadsticks **[PLACE_ORDER]**
- 2 customer: and same as last time **[PLACE_ORDER]**
- 3 customer: in like 30 min **[PLACE_ORDER]**
- 4 customer: thx **[SMALL_TALK]**

  - L1: 1 × breadsticks
  - L2: 1 × off-menu 'same as last time'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0116: simple_order, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Cappuccino (Medium 12 oz); 1 × Cappuccino (Medium 12 oz), add Vanilla syrup; 1 × Drip Coffee (Medium 12 oz), add Oat milk. Will pick it up. Never says how they'll pay. Gives their name: Ivy. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: Good morning! **[SMALL_TALK]**
- 1 customer: Two medium cappuccinos, one with vanilla, and a medium coffee with oat milk, please. For pickup, under Ivy. **[PLACE_ORDER]**

  - L1: 1 × cappuccino medium
  - L2: 1 × cappuccino medium add vanilla_syrup
  - L3: 1 × drip_coffee medium add oat_milk
  - fulfillment pickup, address not_applicable, payment unknown, name Ivy, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0165: multi_message_order, claude-opus-5-5, morning-crumb
Card: Builds the order over several messages, a thing or two at a time: 1 × Drip Coffee (the customer doesn't mention a size), add Vanilla syrup, add Whole milk. Never says whether it's pickup or delivery. Pays by card. Says when they want it: asap. Asks a menu question partway through. Orders a coffee drink with a milk choice said casually ('with oat milk', 'almond pls', 'black').
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: whats in the house coffee **[MENU_QUESTION]**
- 2 business: It's a medium roast drip, black unless you add milk!
- 3 customer: ok one coffee **[PLACE_ORDER]**
- 4 customer: w vanilla **[PLACE_ORDER]**
- 5 customer: and whole milk **[PLACE_ORDER]**
- 6 customer: card asap **[PLACE_ORDER]**

  - L1: 1 × drip_coffee medium add vanilla_syrup, add whole_milk
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0179: simple_order, claude-opus-5-5, corner-patty
Card: Orders: 2 × Cheeseburger (the customer doesn't mention a size); 1 × Veggie Burger; 1 × Coke. Will pick it up. Pays by card. Says a size as a number with a unit (like '2 liter', '12 inch' or '16 oz'), ordering just one.
Card check: agrees

- 0 customer: 2 cheeseburgers **[PLACE_ORDER]**
- 1 customer: veggie burger n a 16 oz coke **[PLACE_ORDER]**
- 2 customer: pickup, card **[PLACE_ORDER]**

  - L1: 2 × cheeseburger single
  - L2: 1 × veggie_burger
  - L3: 1 × coke
  - fulfillment pickup, address not_applicable, payment card, name –, decision pending
  - missing: item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0180: simple_order, claude-opus-5-5, corner-patty
Card: Orders: 1 × Bacon Burger, add Mayo; 1 × Cheeseburger (Single patty); 2 orders of Onion Rings. Will pick it up. Pays cash. Says when they want it: a clock time (like 'at 6:30'). Says a size as a number with a unit (like '2 liter', '12 inch' or '16 oz'), ordering just one.
Card check: items

- 0 customer: hi! bacon burger w mayo, a single cheeseburger, 2 onion rings and a 12 oz lemonade 🍋 **[PLACE_ORDER]**
- 1 customer: pickup at 6, cash 💵 **[PLACE_ORDER]**

  - L1: 1 × bacon_burger  add mayo
  - L2: 1 × cheeseburger single
  - L3: 2 × onion_rings
  - L4: 1 × lemonade
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0193: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Croissant (Chocolate). Never says whether it's pickup or delivery. Pays cash. Says when they want it: a clock time (like 'at 6:30'). Also asks for one thing only vaguely ('one of those'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: Could I have a chocolate croissant and one of those? **[PLACE_ORDER]**
- 1 customer: I'll pay cash. **[PLACE_ORDER]**
- 2 customer: Ready at 11, please. **[PLACE_ORDER]**

  - L1: 1 × croissant chocolate
  - L2: 1 × off-menu 'one of those'
  - fulfillment unknown, address not_mentioned, payment cash, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0225: simple_order, claude-opus-5-5, halfmoon-pizza
Card: Only one or two short customer messages: a greeting that says they want to order (for the office, the family, the crew…) without naming any item yet. The chat ends there, before the business replies.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: gonna place an order for the fam tonight **[PLACE_ORDER]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0229: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Muffin (size/flavor not stated); 1 × Latte (Small 8 oz). Never says the size or flavor of the item marked 'not stated'. Will pick it up. Pays cash. Gives their name: Tara. Says when they want it: asap. Also asks for one thing only vaguely ('the one I always get'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: a muffin, a small latte n the one i always get, pickup asap for tara, cash **[PLACE_ORDER]**

  - L1: 1 × muffin
  - L2: 1 × latte small
  - L3: 1 × off-menu 'the one i always get'
  - fulfillment pickup, address not_applicable, payment cash, name Tara, decision pending
  - missing: item_variant/missing, item_menu_match/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0247: missing_info, claude-opus-5-5, corner-patty
Card: Orders: 2 × Milkshake (size/flavor not stated). Never says the size or flavor of the item marked 'not stated'. Wants delivery to 31 Prospect Rd, unit 3 (written the way the customer would type it). Never says how they'll pay. Also asks for one thing only vaguely ('that thing from before'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: 2 milkshakes **[PLACE_ORDER]**
- 1 customer: and that thing from before **[PLACE_ORDER]**
- 2 customer: 31 prospect rd unit 3 **[PLACE_ORDER]**

  - L1: 2 × milkshake
  - L2: 1 × off-menu 'that thing from before'
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: item_variant/missing, item_menu_match/ambiguous, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0287: multi_message_order, claude-opus-5-5, corner-patty
Card: Builds the order over several messages, a thing or two at a time: 1 × Veggie Burger; 2 × Veggie Burger, no Lettuce; 2 orders of Fries (Large). Will pick it up. Never says how they'll pay. Gives their name: June. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: 3 veggie burgers **[PLACE_ORDER]**
- 1 customer: 2 no lettuce **[PLACE_ORDER]**
- 2 customer: 2 large fries **[PLACE_ORDER]**
- 3 customer: pickup for june **[PLACE_ORDER]**

  - L1: 1 × veggie_burger
  - L2: 2 × veggie_burger  remove lettuce
  - L3: 2 × fries large
  - fulfillment pickup, address not_applicable, payment unknown, name June, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

