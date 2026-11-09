# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t5-0001: correction_after_confirmation, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. First orders the items below, but with the earlier version of the changed one. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, asks for the Drip Coffee with Almond milk (like 'make it almond milk'). Their other details come before that change; nothing comes after it. Final order: 1 × Drip Coffee (the customer doesn't mention a size), add Almond milk; 2 × Americano (Small 8 oz). Will pick it up. Pays cash. Gives their name: Ivy. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: can i get a coffee and two small americanos **[PLACE_ORDER]**
- 2 customer: pickup at 9:15 for ivy, paying cash **[PLACE_ORDER]**
- 3 business: Got it: 1 drip coffee and 2 small americanos for pickup at 9:15, name Ivy, paying cash. Is that right?
- 4 customer: yep **[CONFIRM_ORDER]**
- 5 customer: oh wait make the coffee w almond milk pls **[MODIFY_ORDER]**

  - L1: 1 × drip_coffee medium add almond_milk
  - L2: 2 × americano small
  - fulfillment pickup, address not_applicable, payment cash, name Ivy, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0002: missing_info, claude-opus-5-5, halfmoon-pizza
Card: Orders: 3 × Margherita Pizza (size/flavor not stated), no Basil; 1 × Pepperoni Pizza (Extra large 16-inch); 3 orders of Garlic Knots (6 pieces each). Never says the size or flavor of the item marked 'not stated'. Will pick it up. Pays by card.
Card check: agrees

- 0 customer: yo can i get three margheritas no basil **[PLACE_ORDER]**
- 1 customer: and an xl pepperoni n three orders of garlic knots **[PLACE_ORDER]**
- 2 customer: pickup, card **[PLACE_ORDER]**

  - L1: 3 × margherita_pizza  remove basil
  - L2: 1 × pepperoni_pizza extra_large
  - L3: 3 × garlic_knots
  - fulfillment pickup, address not_applicable, payment card, name –, decision pending
  - missing: item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0003: missing_info, claude-opus-5-5, halfmoon-pizza
Card: Orders: 3 × Hawaiian Pizza (Large 14-inch); 1 × Cheese Pizza (Medium 12-inch), add Pineapple; 1 × Veggie Pizza (Extra large 16-inch), add Spinach, add Thin crust. Will pick it up. Never says how they'll pay. Never says how many of the first item: asks for it vaguely ('some', 'a few', 'muffins for the office'), and the chat ends before the business asks how many.
Card check: items

- 0 customer: can i get some large hawaiians, a medium cheese w pineapple and an xl veggie w spinach thin crust for pickup **[PLACE_ORDER]**

  - L1: None × hawaiian_pizza large
  - L2: 1 × cheese_pizza medium add pineapple
  - L3: 1 × veggie_pizza extra_large add spinach, add crust_thin
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: item_quantity/ambiguous, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0004: correction, claude-opus-5-5, halfmoon-pizza
Card: First orders the items below plus 1 × Dr Pepper (the customer doesn't mention a size). Then, in the very last customer message, removes the 1 × Dr Pepper (the customer doesn't mention a size) from the order. Their other details come before that change; nothing comes after it. Final order: 1 × Pepperoni Pizza (Small 10-inch), add Pineapple; 1 order of Breadsticks (4 pieces each). Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50).
Card check: agrees

- 0 customer: HI!!! CAN I GET A SMALL PEPPERONI WITH PINEAPPLE, AN ORDER OF BREADSTICKS AND A DR PEPPER! **[PLACE_ORDER]**
- 1 customer: PICKING IT UP, PAYING CASH, CHANGE FOR A 50 PLEASE! **[PLACE_ORDER]**
- 2 customer: ACTUALLY SCRATCH THE DR PEPPER!! **[MODIFY_ORDER]**

  - L1: 1 × pepperoni_pizza small add pineapple
  - L2: 1 × breadsticks
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0006: correction_after_confirmation, claude-opus-5-5, halfmoon-pizza
Card: Opens with a greeting before ordering. First orders the items below, but with the earlier version of the changed one. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, changes the Veggie Pizza from 2 to 1. Their other details come before that change; nothing comes after it. Final order: 1 × Veggie Pizza (Small 10-inch), no House cheese blend; 2 × Hawaiian Pizza (Medium 12-inch), add Gluten-free crust. Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: Good evening! **[SMALL_TALK]**
- 1 customer: I'd like two small veggie pizzas with no cheese and two medium Hawaiian pizzas on gluten free crust. **[PLACE_ORDER]**
- 2 customer: I'll pay by card. **[PLACE_ORDER]**
- 3 business: Two small veggie pizzas with no cheese and two medium Hawaiian pizzas on gluten-free crust, paying by card. Is that correct?
- 4 customer: Yes, that's correct. **[CONFIRM_ORDER]**
- 5 customer: Actually, could you make it just one veggie pizza? **[MODIFY_ORDER]**

  - L1: 1 × veggie_pizza small remove cheese
  - L2: 2 × hawaiian_pizza medium add crust_gluten_free
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0007: simple_order, claude-opus-5-5, morning-crumb
Card: Orders: 1 × Drip Coffee (Medium 12 oz). Never says whether it's pickup or delivery. Never says how they'll pay. Orders a coffee drink with a milk choice said casually ('with oat milk', 'almond pls', 'black').
Card check: item_details

- 0 customer: hi can i get a medium coffee **[PLACE_ORDER]**
- 1 customer: w oat milk pls **[PLACE_ORDER]**
- 2 customer: thx **[SMALL_TALK]**

  - L1: 1 × drip_coffee medium add oat_milk
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0009: simple_order, claude-opus-5-5, corner-patty
Card: Orders: 2 × Bacon Burger; 1 × Bacon Burger, no American cheese; 1 × Sprite. Wants delivery to 582 Juniper Ct (written the way the customer would type it). Pays by card. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: can i get 3 bacon burgers 1 with no cheese and a sprite **[PLACE_ORDER]**
- 1 customer: deliver to 582 juniper ct **[PLACE_ORDER]**
- 2 customer: card **[PLACE_ORDER]**

  - L1: 2 × bacon_burger
  - L2: 1 × bacon_burger  remove cheese
  - L3: 1 × sprite
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0010: simple_order, claude-opus-5-5, corner-patty
Card: Opens with a greeting before ordering. Orders: 1 × Coke; 1 order of Onion Rings; 1 order of Fries (the customer doesn't mention a size). Wants delivery to 23 Fairmont Dr (written the way the customer would type it). Pays by card. Says when they want it: asap. Asks a menu question partway through. Says a size as a number with a unit (like '2 liter', '12 inch' or '16 oz'), ordering just one.
Card check: agrees

- 0 customer: hi **[SMALL_TALK]**
- 1 customer: do u guys have diet coke **[MENU_QUESTION]**
- 2 business: Sorry, just Coke, Sprite and lemonade!
- 3 customer: ok then a 20 oz coke, onion rings and fries **[PLACE_ORDER]**
- 4 customer: deliver asap to 23 fairmont dr, card **[PLACE_ORDER]**

  - L1: 1 × coke
  - L2: 1 × onion_rings
  - L3: 1 × fries regular
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0011: correction_after_confirmation, claude-opus-5-5, morning-crumb
Card: Opens with a greeting before ordering. First orders the items below, but with the earlier version of the changed one. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, asks for the Americano with Skim milk (like 'make it skim milk'). Their other details come before that change; nothing comes after it. Final order: 1 × Americano (Large 16 oz), add Skim milk. Will pick it up. Never says how they'll pay. Gives their name: June.
Card check: agrees

- 0 customer: GOOD MORNING! **[SMALL_TALK]**
- 1 customer: I WOULD LIKE ONE LARGE AMERICANO PLEASE! **[PLACE_ORDER]**
- 2 customer: I WILL PICK IT UP. MY NAME IS JUNE. **[PLACE_ORDER]**
- 3 business: One large Americano for pickup, name June. Is that right?
- 4 customer: YES, THANK YOU! **[CONFIRM_ORDER]**
- 5 customer: OH! COULD YOU PUT SKIM MILK IN IT PLEASE! **[MODIFY_ORDER]**

  - L1: 1 × americano large add skim_milk
  - fulfillment pickup, address not_applicable, payment unknown, name June, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t5-0012: multi_message_order, claude-opus-5-5, corner-patty
Card: Builds the order over several messages, a thing or two at a time: 1 × Cheeseburger (Single patty); 1 × Cheeseburger (Single patty), add Mayo; 2 × Milkshake (Vanilla). Will pick it up. Pays cash. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: Hello, I'd like to place an order for pickup. **[PLACE_ORDER]**
- 1 customer: Two cheeseburgers, one of them with mayo. **[PLACE_ORDER]**
- 2 customer: And two vanilla milkshakes. **[PLACE_ORDER]**
- 3 customer: I'll pay cash. **[PLACE_ORDER]**

  - L1: 1 × cheeseburger single
  - L2: 1 × cheeseburger single add mayo
  - L3: 2 × milkshake vanilla
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

