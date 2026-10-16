# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-b1-0044: small_talk, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Only greets, thanks the business or chats briefly. No request.
Card check: items, labels (expected labels not found: SMALL_TALK)

- 0 customer: Hi, I would like to place an order for one large pepperoni pizza, please. **[PLACE_ORDER]**
- 1 business: Hello! I can help you with that. Just to confirm, you would like one large pepperoni pizza?
- 2 customer: Yes, that is correct, thank you so much. **[CONFIRM_ORDER]**

  - L1: 1 × pepperoni_pizza large
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0083: correction_after_confirmation, deepseek-flash@none, corner-patty
Card: First orders 2 × Veggie Burger (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 × Veggie Burger; 1 × Lemonade. Will pick it up. Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: item_details, labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: HEY NEED 2 VEGGIE BURGERS!! NO ONIONS NO PICKLES!! AND A LEMONADE!!! **[PLACE_ORDER]**
- 1 business: Got it: 2 Veggie Burgers with no onions and no pickles, and 1 Lemonade. Is that correct?
- 2 customer: YEAH THATS RIGHT BUT MAKE IT JUST 1 VEGGIE BURGER INSTEAD OF 2!! STILL KEEP THE LEMONADE!!! **[MODIFY_ORDER]**
- 3 customer: ALSO ILL PICK IT UP IN 20 MIN!! **[MODIFY_ORDER]**

  - L1: 1 × veggie_burger  remove onion, remove pickle
  - L2: 1 × lemonade
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0139: cancellation, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Breakfast Sandwich (the customer doesn't mention a size), no Bacon. Then cancels the whole order before it is placed (the last customer message is the cancellation). Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: hey can i get a breakfast sandwich pls no bacon thx **[PLACE_ORDER]**
- 1 business: Sure! Which one would you like, English muffin, croissant, or bagel?
- 2 customer: nvm actually cancel that order pls, gonna skip it rn **[CANCEL_ORDER]**

  - L1: 1 × breakfast_sandwich english_muffin remove bacon
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0280: cancellation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Orders: 2 × Hawaiian Pizza (Large 14-inch), no Pineapple. Then cancels the whole order before it is placed (the last customer message is the cancellation). Wants delivery to 51 Spruce Rd (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50).
Card check: agrees

- 0 customer: Hi, can I order 2 hawaiian pizzas? Large 14-inch please. Can you leave off the pineapple on both? **[PLACE_ORDER]**
- 1 business: Sure! So that's 2 large Hawaiian pizzas, 14-inch, no pineapple on either. Anything else?
- 2 customer: Yes that's right. Actually wait, I have to cancel this whole order, sorry. Something came up with the baby and I can't do it right now. **[CANCEL_ORDER + CONFIRM_ORDER]**
- 3 business: No problem at all, I've cancelled it. Hope everything's ok!
- 4 customer: Thanks, we're fine, just tired lol. Will try again later. **[SMALL_TALK]**

  - L1: 2 × hawaiian_pizza large remove pineapple
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0289: correction_after_confirmation, deepseek-flash@none, halfmoon-pizza
Card: First orders 1 × Meat Lovers Pizza (Personal 8-inch) (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 2 × Sprite (Bottle 20 oz). Final order: 2 × Sprite (Bottle 20 oz); 3 orders of Breadsticks (4 pieces each); 1 × Diet Coke (2-liter bottle). Wants delivery to 637 Juniper Ct (written the way the customer would type it). Never says how they'll pay. Says when they want it: a clock time (like 'at 6:30').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey guys 😅 rough morning over here **[SMALL_TALK]**
- 1 business: Hey! Happy Sunday 😄 What can we get started for you?
- 2 customer: can i get one meat lovers, personal 8 inch please **[PLACE_ORDER]**
- 3 business: Got it — 1 Meat Lovers Pizza, Personal 8-inch. Anything else with that?
- 4 customer: yes thats right ✅ but actually scratch the pizza, can i swap it for two sprites? bottle ones **[MODIFY_ORDER]**
- 5 business: No problem! So that's 2 Sprite, 20 oz bottles. Anything else?
- 6 customer: and three orders of breadsticks, plus a diet coke 2 liter 🙏 deliver to 637 juniper ct, want it at 6:30 **[PLACE_ORDER]**

  - L2: 2 × sprite bottle_20oz
  - L3: 3 × breadsticks
  - L4: 1 × diet_coke two_liter
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0331: correction_after_confirmation, deepseek-flash@none, halfmoon-pizza
Card: First orders 1 × Veggie Pizza (Small 10-inch) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 4. Final order: 4 × Veggie Pizza (Small 10-inch); 1 × Margherita Pizza (Small 10-inch); 1 × Supreme Pizza (Personal 8-inch). Wants delivery to 1488 Ridgecrest St (written the way the customer would type it). Pays by card. Says when they want it: a clock time (like 'at 6:30'). Asks a menu question partway through.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey can i get 1 small veggie pizza **[PLACE_ORDER]**
- 1 customer: also 1 small margherita and 1 personal supreme **[PLACE_ORDER]**
- 2 business: got it! 1 small veggie, 1 small margherita, 1 personal supreme. want delivery or pickup?
- 3 customer: delivery pls to 1488 ridgecrest st **[PLACE_ORDER]**
- 4 business: sure thing! and what time do u want it?
- 5 customer: at 6:30 thx. also does the veggie come w mushrooms? **[PLACE_ORDER + MENU_QUESTION]**
- 6 business: yep, our veggie comes with green peppers, onions, mushrooms, black olives & tomatoes
- 7 customer: can u change the veggie to 4 smalls instead of 1 **[MODIFY_ORDER]**
- 8 business: so that's 4 small veggie pizzas, 1 small margherita, and 1 personal supreme, delivery to 1488 ridgecrest st at 6:30. paying by card?
- 9 customer: yep card. thx! **[PLACE_ORDER]**

  - L1: 4 × veggie_pizza small
  - L2: 1 × margherita_pizza small
  - L3: 1 × supreme_pizza personal
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0339: implicit_category, deepseek-flash@none, corner-patty
Card: Orders: 1 order of Fries (the customer doesn't mention a size); 2 × Lemonade. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Eli. Says when they want it: asap.
Card check: items

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: need some fries **[PLACE_ORDER]**
- 2 customer: 2 lemonades too **[PLACE_ORDER]**
- 3 customer: picking up for my buddy, he's sick **[PLACE_ORDER]**
- 4 business: got it! fries and 2 lemonades for pickup. name for the order?
- 5 customer: Eli. asap pls **[PLACE_ORDER]**
- 6 customer: paying cash, can u break a 20? **[PLACE_ORDER]**

  - L1: None × fries regular
  - L2: 2 × lemonade
  - fulfillment pickup, address not_applicable, payment cash, name Eli, decision pending
  - missing: item_quantity/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0438: unclear_message, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items

- 0 customer: hey u guys open? **[DELIVERY_QUESTION]**
- 1 business: Hi there! Yes, we're open until 11pm. What can I get for you?
- 2 customer: i need pizza for the kids **[PLACE_ORDER]**
- 3 customer: lemme get **[UNKNOWN]**
- 4 customer: hshdjsjs kdkfksks **[UNKNOWN]**
- 5 customer: jdjsks **[UNKNOWN]**

  - L1: 1 × cheese_pizza
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_variant/missing, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0518: contextual_yes, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Orders: 1 order of Garlic Knots (6 pieces each); 1 × Diet Coke (the customer doesn't mention a size). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Wants delivery to 200 Brookside Blvd, # 28C (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50). Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: hi **[SMALL_TALK]**
- 1 customer: my friend is sick **[SMALL_TALK]**
- 2 customer: want to order something for him **[PLACE_ORDER]**
- 3 business: Hi! Sorry to hear your friend isn't feeling well. What can I get started for you?
- 4 customer: garlic knots **[PLACE_ORDER]**
- 5 customer: the 6 piece ones **[PLACE_ORDER]**
- 6 customer: 1 order **[PLACE_ORDER]**
- 7 customer: and a diet coke **[PLACE_ORDER]**
- 8 business: Got it: 1 order of Garlic Knots (6 pieces each) and 1 Diet Coke. Is that right?
- 9 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × garlic_knots
  - L2: 1 × diet_coke can
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0563: simple_order, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Americano (Small 8 oz); 1 × Latte (Medium 12 oz). Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: yo, good morning! can we get some coffee? **[PLACE_ORDER]**
- 1 business: Good morning! Happy to help, what can I get started for you?
- 2 customer: thx! lemme get 2 small americanos and a medium latte pls **[PLACE_ORDER]**

  - L1: 2 × americano small
  - L2: 1 × latte medium
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0698: implicit_category, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Croissant (Chocolate); 3 × Bagel (Everything); 1 × Hot Chocolate (Small 8 oz), Oat milk instead of Whole milk. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Never says whether it's pickup or delivery. Pays by card. Asks a menu question partway through.
Card check: agrees

- 0 customer: Hi, good morning. Is the kitchen still making food or should I come back? **[MENU_QUESTION]**
- 1 business: Good morning! We're open until 3pm, so you're fine. What can I get started for you?
- 2 customer: Could I get one chocolate croissant, and three everything bagels please. Also a small hot chocolate with oat milk instead of the regular milk. Do you pay by card here? **[PLACE_ORDER + PAYMENT_QUESTION]**
- 3 business: Yes, card or cash both work. So that's 1 chocolate croissant, 3 everything bagels, and 1 small hot chocolate with oat milk instead of whole milk. Is that everything?
- 4 customer: That's everything, thanks. **[SMALL_TALK]**

  - L1: 1 × croissant chocolate
  - L2: 3 × bagel everything
  - L3: 1 × hot_chocolate small substitute whole_milk→oat_milk
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0798: small_talk, deepseek-flash@none, corner-patty
Card: Only greets, thanks the business or chats briefly. No request.
Card check: labels (expected labels not found: SMALL_TALK)

- 0 customer: hey r u open rn **[DELIVERY_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0889: unclear_message, claude-haiku-5-5@off-low, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: yo u open rn? lemme get smth fr gonna be **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes we're open until 10pm tonight. What can I get for you?
- 2 customer: ccheesebu ghgr pls  wth jalap **[PLACE_ORDER]**

  - L1: 1 × cheeseburger single add jalapeno
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0892: unclear_message, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: Hey there! 👋 Need to grab some stuff for the kiddos. **[SMALL_TALK]**
- 1 business: Hi! We're ready when you are. What can we get for you today?
- 2 customer: Oh geez, so srry my pocket went crazy there for a sec! 😅😅 I think I hit like 8000 buttons. **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0962: correction, claude-haiku-5-5@off-low, halfmoon-pizza
Card: First asks for 3 × Iced Tea (the customer doesn't mention a size) (plus anything else below), then changes the quantity to 2. Final order: 2 × Iced Tea (the customer doesn't mention a size); 2 × Margherita Pizza (Extra large 16-inch); 3 × Supreme Pizza (Large 14-inch), no Mushrooms. Will pick it up. Pays cash. Gives their name: Eli. Says when they want it: asap.
Card check: agrees

- 0 customer: hey lemme get 3 iced tea pls **[PLACE_ORDER]**
- 1 business: Sure! Would you like anything else with that?
- 2 customer: yea 2 margherita extra large **[PLACE_ORDER]**
- 3 business: Got it, 2 Margherita Extra large 16-inch. Anything else?
- 4 customer: oh wait actually make the tea 2 not 3 thx **[MODIFY_ORDER]**
- 5 business: No problem, 2 iced tea now. Anything else?
- 6 customer: 3 supreme large but no mushrooms pls **[PLACE_ORDER]**
- 7 business: 3 Supreme Large 14-inch, no mushrooms. So your order is 2 iced tea, 2 Margherita Extra large, and 3 Supreme Large with no mushrooms. Is that right?
- 8 customer: yes thats it. ill pick up. paying cash. name is eli, need it asap thx **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 2 × iced_tea can
  - L2: 2 × margherita_pizza extra_large
  - L3: 3 × supreme_pizza large remove mushrooms
  - fulfillment pickup, address not_applicable, payment cash, name eli, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0975: missing_info, gemini-3.1-flash-lite@minimal, corner-patty
Card: Orders: 1 order of Onion Rings; 2 × Cheeseburger (the customer doesn't mention a size). Chooses delivery but never gives an address. Pays by card.
Card check: agrees

- 0 customer: HI! I NEED TO ORDER FOR OUR MEETING PLEASE!! **[SMALL_TALK]**
- 1 business: Hi there! What can I get started for you today?
- 2 customer: I NEED 2 CHEESEBURGERS AND 1 ORDER OF ONION RINGS!! WE WANT DELIVERY AND WILL PAY BY CARD!! **[PLACE_ORDER]**
- 3 business: Got it, that is 2 Cheeseburgers and an order of Onion Rings for delivery, paying by card. Is that everything?
- 4 customer: YES THAT IS ALL THANK YOU!!! **[CONFIRM_ORDER]**

  - L1: 2 × cheeseburger single
  - L2: 1 × onion_rings
  - fulfillment delivery, address not_mentioned, payment card, name –, decision pending
  - missing: address/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1045: contextual_yes, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Latte (Small 8 oz). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash. Gives their name: Sam. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey! **[SMALL_TALK]**
- 1 customer: first time here, tryna get a latte **[PLACE_ORDER]**
- 2 customer: small pls **[PLACE_ORDER]**
- 3 customer: im sam, gonna grab it in 20 min **[PLACE_ORDER]**
- 4 customer: paying cash **[PLACE_ORDER]**
- 5 business: Hey Sam! Welcome in. So that's 1 small Latte, and you'll pick it up in about 20 minutes — sound right?
- 6 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × latte small
  - fulfillment pickup, address not_applicable, payment cash, name Sam, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1062: multi_message_order, claude-haiku-5-5@off-low, morning-crumb
Card: Builds the order over several messages, a thing or two at a time: 1 × Breakfast Sandwich (the customer doesn't mention a size); 1 × Hot Chocolate (Medium 12 oz), add Caramel syrup, Almond milk instead of Whole milk; 1 × Croissant (the customer doesn't mention a size). Will pick it up. Pays cash. Gives their name: Eli.
Card check: item_details

- 0 customer: Hi, good morning. I'd like to order a breakfast sandwich, please. **[PLACE_ORDER]**
- 1 business: Good morning! Sure, which bread would you like it on? We have English muffin, croissant, or bagel.
- 2 customer: Croissant would be good, thanks. **[PLACE_ORDER]**
- 3 business: Got it, breakfast sandwich on a croissant. Anything else?
- 4 customer: Yes, I'd also like a hot chocolate, medium size. **[PLACE_ORDER]**
- 5 business: Medium hot chocolate, sounds good. Any changes to it?
- 6 customer: Can you add caramel syrup and use almond milk instead of whole milk? **[PLACE_ORDER]**
- 7 business: Yep, medium hot chocolate with caramel syrup and almond milk. Anything else?
- 8 customer: One more, a croissant as well. Plain is fine. **[PLACE_ORDER]**
- 9 business: Plain croissant added. So that's a breakfast sandwich on a croissant, a medium hot chocolate with caramel and almond milk, and a plain croissant. Will that be all?
- 10 customer: That's everything. I'll pick it up. Can I pay cash? The name is Eli. **[PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich croissant
  - L2: 1 × hot_chocolate medium add caramel_syrup, substitute whole_milk→almond_milk
  - L3: 1 × croissant plain
  - fulfillment pickup, address not_applicable, payment cash, name Eli, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1073: simple_order, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Breakfast Sandwich (the customer doesn't mention a size); 1 × Latte (Medium 12 oz). Will pick it up. Pays cash. Gives their name: Nico.
Card check: item_details

- 0 customer: hey morning crub cafe i need an order for pick up plz **[PLACE_ORDER]**
- 1 business: Good morning! What can I get for you today?
- 2 customer: lemme get a breakfast sandwich on a bagel and a medium latte pls. im nico and ill pay cash when i get there thx **[PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich bagel
  - L2: 1 × latte medium
  - fulfillment pickup, address not_applicable, payment cash, name Nico, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1075: multi_message_order, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Builds the order over several messages, a thing or two at a time: 2 × Breakfast Sandwich (On a bagel), no Bacon; 1 × Cappuccino (Small 8 oz). Will pick it up. Pays cash. Gives their name: Rosa. Says when they want it: asap. Asks a menu question partway through.
Card check: agrees

- 0 customer: hey! im rosa **[SMALL_TALK]**
- 1 customer: ordering for me and my dad **[SMALL_TALK]**
- 2 business: Hi Rosa! What can I get started for you?
- 3 customer: 2 breakfast sandwiches **[PLACE_ORDER]**
- 4 customer: both on a bagel **[PLACE_ORDER]**
- 5 customer: can u leave the bacon off both? **[PLACE_ORDER]**
- 6 business: Sure thing. Anything else?
- 7 customer: wait do u have oat milk for the coffee? **[MENU_QUESTION]**
- 8 business: We do!
- 9 customer: sweet **[SMALL_TALK]**
- 10 customer: also a small cappuccino **[PLACE_ORDER]**
- 11 customer: is it ready asap? **[PLACE_ORDER]**
- 12 business: Got it: 2 breakfast sandwiches on a bagel with no bacon, and 1 small cappuccino. We can have that ready for you right away!
- 13 customer: perfect, ill pay cash when i pick up! **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 2 × breakfast_sandwich bagel remove bacon
  - L2: 1 × cappuccino small
  - fulfillment pickup, address not_applicable, payment cash, name Rosa, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1094: payment_claim, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent the money on the app') and asks whether the payment went through. Does not order anything new.
Card check: agrees

- 0 customer: HEY GUYS! QUICK QUESTION!!! **[SMALL_TALK]**
- 1 business: Hi there! How can I help you today?
- 2 customer: I PAID FOR MY EARLIER ORDER ON THE APP ALREADY, DID THAT GO THROUGH OKAY??? **[PAYMENT_CLAIM]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1095: off_menu, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 1 × Iced Tea (the customer doesn't mention a size); 1 × buffalo wings (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Will pick it up. Pays by card.
Card check: items

- 0 customer: hey u guys open? **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes, we are open until 11pm. What can we get for you?
- 2 customer: cool. **[SMALL_TALK]**
- 3 customer: can i get an iced tea **[PLACE_ORDER]**
- 4 customer: and some buffalo wings pls **[PLACE_ORDER]**
- 5 customer: dying rn so thx **[SMALL_TALK]**

  - L1: 1 × iced_tea can
  - L2: None × off-menu 'buffalo wings'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1121: payment_question, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Only asks how they can pay (cash, card, an app). Does not order.
Card check: agrees

- 0 customer: yo u guys open rn **[DELIVERY_QUESTION]**
- 1 business: Hi there! We are open until 11pm. How can I help you?
- 2 customer: cool hey just wonderin what ways i can pay there? like do u take cards or cash or is there an app i gotta use **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1187: missing_info, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Breakfast Sandwich (On a bagel); 1 × Drip Coffee (Small 8 oz); 1 × Americano (Small 8 oz), add Caramel syrup. Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: agrees

- 0 customer: hi!! 👶 one handed rn so bear w me lol. can i get a breakfast sandwich on a bagel 🥯 and a small drip coffee, and a small americano w caramel syrup pls ☕️ **[PLACE_ORDER]**
- 1 business: Hi! Sure thing. Just to confirm: 1 Breakfast Sandwich on a bagel, 1 Small Drip Coffee, and 1 Small Americano with caramel syrup. Is that everything?
- 2 customer: yes that's it!! thank u so much 🙏 **[CONFIRM_ORDER]**

  - L1: 1 × breakfast_sandwich bagel
  - L2: 1 × drip_coffee small
  - L3: 1 × americano small add caramel_syrup
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1209: unclear_message, claude-haiku-5-5@off-low, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items

- 0 customer: I would like the Cheeseburger with no onions and extra pickles, if that is possible, and also swap the **[PLACE_ORDER]**
- 1 customer: jalap bu the wrt **[UNKNOWN]**

  - L1: 1 × cheeseburger single remove onion, add pickle
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1212: payment_question, deepseek-flash@none, halfmoon-pizza
Card: Only asks how they can pay (cash, card, an app). Does not order.
Card check: agrees

- 0 customer: hey what can i pay with rn **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1249: combo, deepseek-flash@none, corner-patty
Card: Orders: 1 × Cheeseburger Combo, no Lettuce, add Bacon, side: Onion Rings, drink: Coke; 1 × Bacon Burger. Picks every combo choice. Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Maya.
Card check: agrees

- 0 customer: Hello, I would like to place an order for pickup. **[PLACE_ORDER]**
- 1 business: Hi! Sure, what can I get started for you?
- 2 customer: I'll take one Cheeseburger Combo with no lettuce and add bacon. For the combo, I'd like Onion Rings as the side and a Coke as the drink. I also need one Bacon Burger. **[PLACE_ORDER]**
- 3 business: Got it: one Cheeseburger Combo with no lettuce, add bacon, Onion Rings, and a Coke, plus one Bacon Burger. Anything else?
- 4 customer: That's everything. I'll pay cash, and could you make change for a $50 bill? The name for the order is Maya. **[PLACE_ORDER]**

  - L1: 1 × cheeseburger_combo  remove lettuce, add bacon side=onion_rings, drink=coke
  - L2: 1 × bacon_burger
  - fulfillment pickup, address not_applicable, payment cash, name Maya, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1253: implicit_category, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 1 × Cheese Pizza (Medium 12-inch); 1 order of Garlic Knots (6 pieces each); 1 order of Breadsticks (4 pieces each). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Will pick it up. Pays cash. Gives their name: Ana.
Card check: items

- 0 customer: hiii 👋 hope u guys are open! **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes we're open 😊 What can I get started for you?
- 2 customer: ok so one medium cheese pizza 🍕 plus a couple of garlic knots and like a order of breadsticks too!! 🙌 pickup under Ana pls, paying cash 💵 **[PLACE_ORDER]**

  - L1: 1 × cheese_pizza medium
  - L2: None × garlic_knots
  - L3: 1 × breadsticks
  - fulfillment pickup, address not_applicable, payment cash, name Ana, decision pending
  - missing: item_quantity/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1276: payment_claim, deepseek-flash@none, morning-crumb
Card: Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent the money on the app') and asks whether the payment went through. Does not order anything new.
Card check: agrees

- 0 customer: Hello, I placed an order with you earlier and paid online. Can you check whether the payment went through? **[PAYMENT_CLAIM + PAYMENT_QUESTION]**
- 1 business: Hi! Sure, I can look into that. What name was the earlier order under?
- 2 customer: It was under Coach Daniels. I just want to confirm the payment went through, because I haven't ordered anything new. **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1352: order_problem, deepseek-flash@none, halfmoon-pizza
Card: Got an earlier order (not in this chat) with a problem: the bottled water was cold. Complains. Does not order anything new.
Card check: agrees

- 0 customer: HEY. MY ORDER EARLIER, THE BOTTLED WATER WAS ICE COLD. LIKE STRAIGHT OUT THE FRIDGE COLD **[ORDER_PROBLEM]**
- 1 business: Hey, sorry about that! Cold water is usually kind of the point, haha. What was wrong with it exactly?
- 2 customer: IM HUNGOVER OK. I NEED ROOM TEMP WATER. ICE COLD JUST MAKES ME FEEL WORSE!! CAN U NOT DO THAT NEXT TIME **[ORDER_PROBLEM]**
- 3 business: Got it — sorry, we didn't know. Next time just leave a note on your order asking for it not chilled and we'll keep it out of the fridge for you. Anything you want to order now?
- 4 customer: NAH IM GOOD. JUST WANTED TO COMPLAIN. THX **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

