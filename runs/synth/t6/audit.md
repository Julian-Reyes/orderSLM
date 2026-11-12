# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t6-0031: multi_message_order, claude-opus-5-5, halfmoon-pizza
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 1 × Hawaiian Pizza (Small 10-inch), no Tomato sauce, add Parmesan; 2 × Meat Lovers Pizza (Personal 8-inch), add Fresh mozzarella; 2 × Supreme Pizza (Personal 8-inch); 1 × Bottled Water; 1 × Sprite (Can 12 oz). Wants delivery to 186 Franklin Terrace (written the way the customer would type it). Never says how they'll pay.
Card check: agrees

- 0 customer: hey there **[SMALL_TALK]**
- 1 customer: can i get a small hawaiian, no sauce, w parmesan **[PLACE_ORDER]**
- 2 customer: 2 personal meat lovers w fresh mozzarella **[PLACE_ORDER]**
- 3 customer: 2 personal supremes, a water n a can of sprite **[PLACE_ORDER]**
- 4 customer: deliver to 186 franklin terrace **[PLACE_ORDER]**

  - L1: 1 × hawaiian_pizza small remove tomato_sauce, add parmesan
  - L2: 2 × meat_lovers_pizza personal add mozzarella
  - L3: 2 × supreme_pizza personal
  - L4: 1 × water
  - L5: 1 × sprite can
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0048: missing_info, claude-opus-5-5, halfmoon-pizza
Card: Orders: 3 × BBQ Chicken Pizza (Extra large 16-inch), add Anchovies; 2 × Dr Pepper (the customer doesn't mention a size); 2 × Margherita Pizza (Personal 8-inch), add Gluten-free crust. Wants delivery to 968 Mission Ct, # 13A (written the way the customer would type it). Never says how they'll pay. Also asks for one thing only vaguely ('the one I always get'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: 3 XL BBQ CHICKEN WITH ANCHOVIES, 2 DR PEPPERS AND 2 PERSONAL MARGHERITAS ON GLUTEN FREE CRUST **[PLACE_ORDER]**
- 1 customer: AND THE ONE I ALWAYS GET. DELIVER TO 968 MISSION CT #13A **[PLACE_ORDER]**

  - L1: 3 × bbq_chicken_pizza extra_large add anchovies
  - L2: 2 × dr_pepper can
  - L3: 2 × margherita_pizza personal add crust_gluten_free
  - L4: 1 × off-menu 'THE ONE I ALWAYS GET'
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: item_menu_match/ambiguous, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0054: implicit_category, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Muffin (Banana nut); 1 × Latte (Medium 12 oz), add Whipped cream. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Will pick it up. Never says how they'll pay. Gives their name: Ivy. Says when they want it: asap. Names items without category words or only vaguely ('a veggie', 'a strawberry', 'something to snack on'); the menu or the business's reply settles each one.
Card check: agrees

- 0 customer: can i grab a banana nut n a medium latte w whip **[PLACE_ORDER]**
- 1 business: Do you mean a banana nut muffin?
- 2 customer: yep the muffin. asap for pickup, name ivy **[PLACE_ORDER]**

  - L1: 1 × muffin banana_nut
  - L2: 1 × latte medium add whipped_cream
  - fulfillment pickup, address not_applicable, payment unknown, name Ivy, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0097: missing_info, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Drip Coffee (the customer doesn't mention a size). Will pick it up. Never says how they'll pay. Gives their name: Ben. Says when they want it: asap. Also asks for one thing only vaguely ('the usual'), with nothing earlier in the chat saying what it is; the chat ends before the business asks which.
Card check: items

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: a coffee **[PLACE_ORDER]**
- 2 customer: n the usual **[PLACE_ORDER]**
- 3 customer: asap **[PLACE_ORDER]**
- 4 customer: pickup, ben **[PLACE_ORDER]**

  - L1: 1 × drip_coffee medium
  - L2: 1 × off-menu 'the usual'
  - fulfillment pickup, address not_applicable, payment unknown, name Ben, decision pending
  - missing: item_menu_match/ambiguous, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0136: combo, claude-opus-5-5, morning-crumb
Card: Orders: 3 × Coffee & Pastry, drink: Drip Coffee, pastry: Croissant; 4 × Drip Coffee (Small 8 oz). Picks every combo choice. Will pick it up. Pays by card. Gives their name: Maya. Besides the combo's own picks, also orders one more drink or side as a separate item.
Card check: agrees

- 0 customer: 3 coffee n pastry deals **[PLACE_ORDER]**
- 1 customer: w drip coffee n a croissant each **[PLACE_ORDER]**
- 2 customer: plus 4 small coffees on the side **[PLACE_ORDER]**
- 3 customer: pickup, maya, card **[PLACE_ORDER]**

  - L1: 3 × coffee_pastry_combo   drink=drip_coffee, pastry=croissant
  - L2: 4 × drip_coffee small
  - fulfillment pickup, address not_applicable, payment card, name Maya, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0173: missing_info, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Bagel (Cinnamon raisin); 2 × Americano (Small 8 oz). Never says whether it's pickup or delivery. Pays cash. Says when they want it: a relative time (like 'in 20 min'). Never says how many of the first item: asks for it vaguely ('some', 'a few', 'muffins for the office'), and the chat ends before the business asks how many.
Card check: items

- 0 customer: morning **[SMALL_TALK]**
- 1 customer: some cinnamon raisin bagels **[PLACE_ORDER]**
- 2 customer: 2 small americanos **[PLACE_ORDER]**
- 3 customer: in 15 min **[PLACE_ORDER]**
- 4 customer: cash **[PLACE_ORDER]**

  - L1: None × bagel cinnamon_raisin
  - L2: 2 × americano small
  - fulfillment unknown, address not_mentioned, payment cash, name –, decision pending
  - missing: item_quantity/ambiguous, fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0181: multi_message_order, claude-opus-5-5, corner-patty
Card: Builds the order over several messages, a thing or two at a time: 1 × Bacon Burger. Wants delivery to 877 Delancey Terrace (written the way the customer would type it). Pays by card. Says when they want it: a clock time (like 'at 6:30'). Asks for coleslaw on the Bacon Burger, as if the place has it (it isn't on the menu).
Card check: agrees

- 0 customer: bacon burger **[PLACE_ORDER]**
- 1 customer: w coleslaw on it **[PLACE_ORDER]**
- 2 customer: deliver to 877 delancey terrace **[PLACE_ORDER]**
- 3 customer: at 9 **[PLACE_ORDER]**
- 4 customer: card **[PLACE_ORDER]**

  - L1: 1 × bacon_burger  add w coleslaw on it
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: item_modification/off_menu

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0187: missing_info, claude-opus-5-5, corner-patty
Card: Orders: 1 × Coke. Will pick it up. Never says how they'll pay. Asks a menu question partway through. The order is for a later day named by its weekday (like 'saturday at 7', 'for fri 11:30'), not today.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: r u open on tuesdays? 🤔 **[DELIVERY_QUESTION]**
- 1 business: Yes, we're open every day from 11 am to 10 pm.
- 2 customer: cool 😎 then a coke for pickup tuesday at 5 **[PLACE_ORDER]**

  - L1: 1 × coke
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0216: correction, claude-opus-5-5, halfmoon-pizza
Card: First orders the items below plus 1 × Hawaiian Pizza (Personal 8-inch). Then, in the very last customer message, removes the 1 × Hawaiian Pizza (Personal 8-inch) from the order. Their other details come before that change; nothing comes after it. Final order: 1 × Dr Pepper (Can 12 oz); 1 order of Garlic Knots (6 pieces each); 3 × Supreme Pizza (Medium 12-inch), no Mushrooms, add Olive oil, add Thick crust. Will pick it up. Pays cash.
Card check: agrees

- 0 customer: 3 medium supremes no mushrooms w olive oil n thick crust 🍕 **[PLACE_ORDER]**
- 1 customer: + a personal hawaiian, an order of garlic knots n a can of dr pepper, pickup, cash 💵 **[PLACE_ORDER]**
- 2 customer: actually skip the hawaiian 🙅 **[MODIFY_ORDER]**

  - L1: 3 × supreme_pizza medium remove mushrooms, add olive_oil, add crust_thick
  - L2: 1 × garlic_knots
  - L3: 1 × dr_pepper can
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t6-0232: missing_info, claude-opus-5-5, morning-crumb
Card: Orders: 3 × Bagel (size/flavor not stated); 1 × Muffin (Blueberry). Never says the size or flavor of the item marked 'not stated'. Will pick it up. Pays by card. Gives their name: Sam. Asks a menu question partway through. Never says how many of the first item: asks for it vaguely ('some', 'a few', 'muffins for the office'), and the chat ends before the business asks how many.
Card check: items

- 0 customer: what bagels do u have? 🥯 **[MENU_QUESTION]**
- 1 business: Plain, everything, sesame and cinnamon raisin.
- 2 customer: ok some bagels n a blueberry muffin 😊 **[PLACE_ORDER]**
- 3 customer: pickup for sam, card **[PLACE_ORDER]**

  - L1: None × bagel
  - L2: 1 × muffin blueberry
  - fulfillment pickup, address not_applicable, payment card, name Sam, decision pending
  - missing: item_quantity/ambiguous, item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

