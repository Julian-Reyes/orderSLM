# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t8-0018: missing_info, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Muffin (size/flavor not stated). Never says the size or flavor of the item marked 'not stated'. Will pick it up. Never says how they'll pay. Gives their name: Luis. Says when they want it: asap. Also asks for one thing only vaguely ('one of those'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: Good morning! **[SMALL_TALK]**
- 1 customer: Could I get a muffin and one of those, as soon as possible? Pickup for Luis. **[PLACE_ORDER]**

  - L1: 1 × muffin
  - L2: 1 × off-menu 'one of those'
  - fulfillment pickup, address not_applicable, payment unknown, name Luis, decision pending
  - missing: item_variant/missing, item_menu_match/ambiguous, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0104: ambiguous_reference, claude-opus-5-5, corner-patty
Card: Refers to the first item vaguely at first ('same as last time'); the business asks which one, and the customer names it. Final order: 1 × Bacon Burger; 1 × Coke; 2 × Sprite; 1 × Veggie Burger; 3 orders of Fries (Large). Wants delivery to 3336 Fulton Terrace, unit 6C (written the way the customer would type it). Pays by card.
Card check: agrees

- 0 customer: Hi, same as last time please. **[PLACE_ORDER]**
- 1 business: Sorry, we can't see past orders here. What would you like?
- 2 customer: A bacon burger, a veggie burger, three large fries, a Coke and two Sprites. **[PLACE_ORDER]**
- 3 customer: To 3336 Fulton Terrace, unit 6C. Card. **[PLACE_ORDER]**

  - L1: 1 × bacon_burger
  - L2: 1 × veggie_burger
  - L3: 3 × fries large
  - L4: 1 × coke
  - L5: 2 × sprite
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0114: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Drip Coffee (Small 8 oz), add Caramel syrup; 1 × Latte (Small 8 oz), Almond milk instead of Whole milk; 1 × Cappuccino (Medium 12 oz). Never says whether it's pickup or delivery. Pays by card. Also asks for one thing only vaguely ('same as last time'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: sm drip w caramel, sm almond latte, med cap n same as last time for my coworker ☕☕☕ card **[PLACE_ORDER]**

  - L1: 1 × drip_coffee small add caramel_syrup
  - L2: 1 × latte small substitute whole_milk→almond_milk
  - L3: 1 × cappuccino medium
  - L4: 1 × off-menu 'same as last time'
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0122: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 2 × Bagel (Plain), add Egg. Never says whether it's pickup or delivery. Pays cash. Also asks for one thing only vaguely ('same as last time'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: 2 plain bagels w egg n same as last time **[PLACE_ORDER]**
- 1 customer: cash **[PLACE_ORDER]**

  - L1: 2 × bagel plain add egg
  - L2: 1 × off-menu 'same as last time'
  - fulfillment unknown, address not_mentioned, payment cash, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0148: two_requests, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Americano (Large 16 oz), add Vanilla syrup; 1 × Hot Chocolate (Medium 12 oz), no Whipped cream. In the same message as the first item, also asks a question about the menu. Will pick it up. Pays by card. Gives their name: Rosa. Says when they want it: a clock time (like 'at 6:30'). One customer message orders an item, asks a question in the middle, and goes on ordering after the question; every item named before and after the question is ordered.
Card check: agrees

- 0 customer: lg americano w vanilla, is the vanilla sugar free? 🤔 n a medium hot choc no whip, pickup at 1:30 for rosa, card **[PLACE_ORDER + MENU_QUESTION]**

  - L1: 1 × americano large add vanilla_syrup
  - L2: 1 × hot_chocolate medium remove whipped_cream
  - fulfillment pickup, address not_applicable, payment card, name Rosa, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0152: simple_order, claude-opus-5-5, halfmoon-pizza
Card: Orders: 1 × Supreme Pizza (Large 14-inch), no Onions. Will pick it up. Pays by card. Wants a large or catering order for a later day (tomorrow or a weekday, no clock time), names no items, and asks to talk to a person about it.
Card check: items

- 0 customer: hi we need like 15 pizzas for a party saturday **[PLACE_ORDER]**
- 1 customer: is there a manager i can talk to about a big order **[HUMAN_REQUEST]**
- 2 customer: thx **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0159: missing_info, claude-opus-5-5, corner-patty
Card: Orders: 1 × Milkshake (size/flavor not stated); 3 × Bacon Burger, no Lettuce; 1 order of Fries (Large). Never says the size or flavor of the item marked 'not stated'. Wants delivery to 9578 Dover Terrace, # 8C (written the way the customer would type it). Pays cash. Says when they want it: a clock time (like 'at 6:30'). Says the size of a sized item only vaguely ('one of the big ones', 'a bigger size', 'the larger pepperonis', 'not the small'), so more than one size fits; the chat ends before the business asks which.
Card check: agrees

- 0 customer: 3 bacon burgers no lettuce **[PLACE_ORDER]**
- 1 customer: large fries **[PLACE_ORDER]**
- 2 customer: a shake **[PLACE_ORDER]**
- 3 customer: idk the flavor, not vanilla **[PLACE_ORDER]**
- 4 customer: 9578 dover terrace #8c at 7, cash **[PLACE_ORDER]**

  - L1: 3 × bacon_burger  remove lettuce
  - L2: 1 × fries large
  - L3: 1 × milkshake
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: item_variant/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0185: missing_info, claude-opus-5-5, corner-patty
Card: Opens with a greeting before ordering. Orders: 2 × Coke; 1 × Milkshake (Vanilla). Chooses delivery but never gives an address. Never says how they'll pay. Never says how many of the first item: asks for it vaguely ('some', 'a few', 'muffins for the office'), and the chat ends before the business asks how many.
Card check: items

- 0 customer: hey! **[SMALL_TALK]**
- 1 customer: a vanilla shake n some cokes delivered pls **[PLACE_ORDER]**

  - L1: 1 × milkshake vanilla
  - L2: None × coke
  - fulfillment delivery, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_quantity/ambiguous, address/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0190: ambiguous_reference, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Refers to the first item vaguely at first ('that thing from before'); the business asks which one, and the customer names it. Final order: 1 × Bagel (Cinnamon raisin), add Tomato; 1 × Latte (Small 8 oz), add Caramel syrup; 3 × Muffin (Chocolate chip); 1 × Cappuccino (Medium 12 oz); 1 × Hot Chocolate (Small 8 oz), Skim milk instead of Whole milk; 1 × Drip Coffee (Medium 12 oz), add Caramel syrup. Will pick it up. Pays by card. Gives their name: June.
Card check: agrees

- 0 customer: morning **[SMALL_TALK]**
- 1 customer: that thing from before **[PLACE_ORDER]**
- 2 business: Sorry, we can't see past orders here. What would you like?
- 3 customer: cinnamon raisin bagel w tomato **[PLACE_ORDER]**
- 4 customer: small latte w caramel, med cap **[PLACE_ORDER]**
- 5 customer: 3 choc chip muffins **[PLACE_ORDER]**
- 6 customer: small hot choc w skim n a med drip w caramel, pickup june, card **[PLACE_ORDER]**

  - L1: 1 × bagel cinnamon_raisin add tomato
  - L2: 1 × latte small add caramel_syrup
  - L3: 1 × cappuccino medium
  - L4: 3 × muffin chocolate_chip
  - L5: 1 × hot_chocolate small substitute whole_milk→skim_milk
  - L6: 1 × drip_coffee medium add caramel_syrup
  - fulfillment pickup, address not_applicable, payment card, name June, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t8-0231: correction, claude-opus-5-5, corner-patty
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, changes the size of the Cheeseburger from Double patty to Single patty (like 'make it a single'). Their other details come before that change; nothing comes after it. Final order: 1 × Cheeseburger (Single patty); 2 × Lemonade; 3 × Milkshake (Vanilla). Will pick it up. Pays by card. Gives their name: Ben. Asks a menu question partway through.
Card check: agrees

- 0 customer: a double cheeseburger, 2 lemonades n 3 vanilla shakes 🍔 **[PLACE_ORDER]**
- 1 customer: are the shakes big? **[MENU_QUESTION]**
- 2 business: 16 oz each!
- 3 customer: nice 😎 pickup for ben, card **[PLACE_ORDER]**
- 4 customer: actually make the cheeseburger a single **[MODIFY_ORDER]**

  - L1: 1 × cheeseburger single
  - L2: 2 × lemonade
  - L3: 3 × milkshake vanilla
  - fulfillment pickup, address not_applicable, payment card, name Ben, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

