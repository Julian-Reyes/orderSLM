# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-m1-0024: contextual_yes, deepseek-flash@none, food-court
Card: Orders: 2 × Supreme Pizza (Small 10-inch), add Basil. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays by card. Gives their name: Rosa.
Card check: agrees

- 0 customer: hey r u open rn **[DELIVERY_QUESTION]**
- 1 business: we sure are! what can i get started for you?
- 2 customer: gonna need 2 small supreme pizzas w extra basil on both pls, name's rosa, gonna pick it up n pay by card **[PLACE_ORDER]**
- 3 business: got it! 2 small 10-inch Supreme Pizzas with added basil, pickup, name Rosa, paying by card. is that right?
- 4 customer: yep **[CONFIRM_ORDER]**

  - L1: 2 × supreme_pizza small add basil
  - fulfillment pickup, address not_applicable, payment card, name Rosa, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0030: correction_after_confirmation, gemini-3.1-flash-lite@minimal, food-court
Card: First orders 3 × Veggie Burger, no Tomato (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 2. Final order: 2 × Veggie Burger, no Tomato; 1 × Latte (Medium 12 oz); 3 × Bacon Burger. Wants delivery to 555 Chestnut Way (written the way the customer would type it). Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: Hey there! Can I get 3 veggie burgers pls? No tomato on those thx 😊 **[PLACE_ORDER]**
- 1 business: Hi! Sure thing, that's 3 Veggie Burgers without tomato. Anything else for you today?
- 2 customer: Actually wait, can we do 2 of those veggie burgers instead? And add 1 medium 12oz latte and 3 bacon burgers too. Delivery to 555 Chestnut Way in 20 min pls! 🍔☕ **[MODIFY_ORDER]**

  - L1: 2 × veggie_burger  remove tomato
  - L2: 1 × latte medium
  - L3: 3 × bacon_burger
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0038: small_talk, claude-haiku-5-5@off-low, food-court
Card: Only greets, thanks the business or chats briefly. No request.
Card check: agrees

- 0 customer: HI!!! THANKS FOR BEING OPEN LATE, YOU GUYS ARE LIFESAVERS!!! **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0044: small_talk, gemini-3.1-flash-lite@minimal, food-court
Card: Only greets, thanks the business or chats briefly. No request.
Card check: items

- 0 customer: Hey there! **[SMALL_TALK]**
- 1 customer: My friend is super sick rn. **[SMALL_TALK]**
- 2 customer: Can I get a large pepperoni pizza? **[PLACE_ORDER]**
- 3 customer: Plus two milkshakes, one vanilla and one chocolate. Thx! **[PLACE_ORDER]**
- 4 business: Hello! I have a large pepperoni pizza and two milkshakes, one vanilla and one chocolate. Is that everything for you?
- 5 customer: Yes, actually lemme change the pizza to half sausage. **[MODIFY_ORDER]**
- 6 customer: That's it, ty! **[SMALL_TALK]**

  - L1: 1 × half pepperoni_pizza / half cheese_pizza large add sausage
  - L2: 1 × milkshake vanilla
  - L3: 1 × milkshake chocolate
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0069: small_talk, deepseek-flash@none, food-court
Card: Only greets, thanks the business or chats briefly. No request.
Card check: agrees

- 0 customer: hey its me again lol **[SMALL_TALK]**
- 1 business: hey! good to hear from you 😊 what can we get started for you?
- 2 customer: nothin rn just sayin hi, gonna come thru later tho thx **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0079: menu_question, claude-haiku-5-5@off-low, food-court
Card: Only asks one or two questions about the menu (what comes on something, sizes, what's good, whether they have something). Does not order.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 business: Hi! Welcome, what can I get you?
- 2 customer: wait **[SMALL_TALK]**
- 3 customer: what comes on the veggie pizza **[MENU_QUESTION]**
- 4 customer: like is it all veggies **[MENU_QUESTION]**
- 5 business: Veggie Pizza comes with tomato sauce, house cheese blend, green peppers, onions, mushrooms, black olives and tomatoes. You can add extras too.
- 6 customer: ok ok **[SMALL_TALK]**
- 7 customer: and do u guys have a couple of sizes for the latte **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0115: refund_request, deepseek-flash@none, food-court
Card: Got an earlier order (not in this chat) where the sprite was missing, and asks for their money back.
Card check: items

- 0 customer: Hello. I would like to place an order for a sick friend. Can I get one large chicken noodle soup and a couple of orange juices? **[PLACE_ORDER]**
- 1 business: Hi! I'm sorry, but we don't have chicken noodle soup or orange juice on our menu. We have burgers, pizzas, sandwiches, coffee, and pastries.
- 2 customer: Oh, that's too bad. Then can I get two cheeseburgers with no onions and a large fries? **[PLACE_ORDER]**
- 3 business: Sure. Two cheeseburgers with no onions and a large fries. Anything else?
- 4 customer: Yes, please add a chocolate milkshake. And one more thing — my previous order was missing a Sprite, so I would like a refund for that. **[PLACE_ORDER + REFUND_REQUEST]**

  - L1: 2 × cheeseburger single remove onion
  - L2: 1 × fries large
  - L3: 1 × milkshake chocolate
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0116: correction_after_confirmation, deepseek-flash@none, food-court
Card: First orders 2 × Diet Coke (Can 12 oz) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 × Diet Coke (Can 12 oz); 1 × Bottled Water; 4 × Cheese Pizza (Medium 12-inch), no House cheese blend, add Spinach. Will pick it up. Pays by card. Gives their name: Nico. Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: yo u guys open rn **[DELIVERY_QUESTION]**
- 1 business: hey! yep we're open till 11. what can i get u?
- 2 customer: ok so lemme get two diet cokes, can **[PLACE_ORDER]**
- 3 customer: and a bottled water too **[PLACE_ORDER]**
- 4 business: got it - 2 diet cokes (can) and a bottled water. anything else?
- 5 customer: yeah quick q - can i do a cheese pizza without the house cheese blend **[PLACE_ORDER]**
- 6 business: yep no problem, we can leave the cheese blend off. want anything added instead?
- 7 customer: spinach pls. and make it four of those, medium **[MODIFY_ORDER + PLACE_ORDER]**
- 8 business: so thats 2 diet cokes (can), 1 bottled water, and 4 medium cheese pizzas with no house cheese blend, add spinach. sound right?
- 9 customer: yep thats it **[CONFIRM_ORDER]**
- 10 customer: wait actually just one diet coke not two **[MODIFY_ORDER]**
- 11 business: no worries! so 1 diet coke (can), 1 bottled water, 4 medium cheese pizzas no cheese blend with spinach
- 12 customer: perfect. we'll pick it up, paying by card **[MODIFY_ORDER]**
- 13 customer: name's nico btw, thx **[MODIFY_ORDER]**

  - L1: 1 × diet_coke can
  - L2: 1 × water
  - L3: 4 × cheese_pizza medium remove cheese_halfmoon, add spinach
  - fulfillment pickup, address not_applicable, payment card, name nico, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0130: ambiguous_reference, claude-haiku-5-5@off-low, food-court
Card: Opens with a greeting before ordering. Refers to the first item vaguely at first ('same as last time'); the business asks which one, and the customer names it. Final order: 1 × Meat Lovers Pizza (Extra large 16-inch); 1 × Diet Coke (Can 12 oz). Will pick it up. Never says how they'll pay. Gives their name: Priya.
Card check: items

- 0 customer: HEY!!! IS THIS THE FOOD COURT?? **[SMALL_TALK]**
- 1 business: Hi there! Yes, this is the Food Court ordering chat. What can I get started for you?
- 2 customer: OMG OK SO I NEED THE SAME THING AS LAST TIME!!! ANDD A COKE!! 1 CAN!!! MOVIE NIGHT EMERGENCY LOL **[PLACE_ORDER]**
- 3 business: Happy to help! Which one was last time? Pizza, burger, something else?
- 4 customer: THE MEAT LOVERS PIZZA!!! EXTRA LARGE 16 INCH PLEASE!!! ITS FOR 6 PPL 😅 PICKUP WHEN CAN I COME??? MY NAME IS PRIYA **[PLACE_ORDER + DELIVERY_QUESTION]**

  - L2: 1 × coke can
  - L3: 1 × meat_lovers_pizza extra_large
  - fulfillment pickup, address not_applicable, payment unknown, name PRIYA, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0143: correction_after_confirmation, claude-haiku-5-5@off-low, food-court
Card: First orders 1 × Milkshake (Vanilla) (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 × Cappuccino (Large 16 oz), add Vanilla syrup. Final order: 1 × Cappuccino (Large 16 oz), add Vanilla syrup; 1 × Dr Pepper (the customer doesn't mention a size). Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: one **[PLACE_ORDER]**
- 2 customer: milkshake **[PLACE_ORDER]**
- 3 customer: vanilla **[PLACE_ORDER]**
- 4 business: Hi! Got one vanilla milkshake. Anything else?
- 5 customer: no wait **[MODIFY_ORDER]**
- 6 customer: actually can i get a large cappuccino instead **[MODIFY_ORDER]**
- 7 business: Sure, what would you like to order?
- 8 customer: one large cappuccino **[PLACE_ORDER]**
- 9 customer: 16 oz **[PLACE_ORDER]**
- 10 customer: add vanilla syrup pls **[PLACE_ORDER]**
- 11 business: Got it: one Cappuccino, large 16 oz, with vanilla syrup. Want to add anything else?
- 12 customer: yes **[SMALL_TALK]**
- 13 customer: a dr pepper **[PLACE_ORDER]**

  - L1: 1 × cappuccino large add vanilla_syrup
  - L2: 1 × dr_pepper can
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0145: correction_after_confirmation, gemini-3.1-flash-lite@minimal, food-court
Card: First orders 1 × Latte (Large 16 oz) (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 3 × Lemonade. Final order: 3 × Lemonade. Never says whether it's pickup or delivery. Pays by card. Asks a menu question partway through.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: Hello there! **[SMALL_TALK]**
- 1 customer: Could I please order a latte? **[PLACE_ORDER]**
- 2 customer: Large size, please. **[PLACE_ORDER]**
- 3 customer: Also, do u have any herbal tea? **[MENU_QUESTION]**
- 4 business: Hello! I'm sorry, we don't have herbal tea on our menu. We do have one large latte ready for your order, though. Would you like anything else?
- 5 customer: Oh, no thank you. **[SMALL_TALK]**
- 6 customer: Actually, lemme change that. **[MODIFY_ORDER]**
- 7 customer: Can I get three lemonades instead? **[MODIFY_ORDER]**
- 8 business: Certainly. I have updated your order to three lemonades. Is there anything else I can get for you today?
- 9 customer: No, that's all. Thx! **[SMALL_TALK]**
- 10 customer: I'll be paying with my card. **[PLACE_ORDER]**

  - L1: 3 × lemonade
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0146: ambiguous_reference, gemini-3.1-flash-lite@minimal, food-court
Card: Refers to the first item vaguely at first ('one of those'); the business asks which one, and the customer names it. Final order: 1 × Veggie Burger, add Jalapeños. Will pick it up. Never says how they'll pay. Gives their name: Grace. Asks a menu question partway through.
Card check: agrees

- 0 customer: HEY!! CAN I GET ONE OF THOSE BURGERS PLEASE? **[PLACE_ORDER]**
- 1 business: Sure! Which burger would you like today?
- 2 customer: THE VEGGIE ONE!! ALSO DO YOU HAVE JALAPEÑOS YOU CAN THROW ON THERE? **[PLACE_ORDER + MENU_QUESTION]**
- 3 business: Yes, we can add jalapeños to the Veggie Burger for you.
- 4 customer: AWESOME!! SO THAT IS ONE VEGGIE BURGER WITH JALAPEÑOS. IM GRACE AND ILL BE BY TO PICK IT UP LATER! **[PLACE_ORDER]**

  - L2: 1 × veggie_burger  add jalapeno
  - fulfillment pickup, address not_applicable, payment unknown, name Grace, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0171: cancellation, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 1 × Cheeseburger (the customer doesn't mention a size); 1 × Latte (Large 16 oz), Oat milk instead of Whole milk; 2 × Lemonade. Then cancels the whole order before it is placed (the last customer message is the cancellation). Wants delivery to 7875 Wexford St (written the way the customer would type it). Pays by card. Says when they want it: asap.
Card check: agrees

- 0 customer: hey! can i get a cheeseburger, a large latte w oat milk, and 2 lemonades? for delivery to 7875 wexford st asap pls 🙏 **[PLACE_ORDER]**
- 1 business: Sure thing! That's one cheeseburger, one large oat milk latte, and two lemonades for delivery to 7875 Wexford St. Will you be paying with card or cash today?
- 2 customer: oh wait actually sorry, can we just cancel that whole order? woke up a bit confused lol. thanks anyway! **[CANCEL_ORDER]**

  - L1: 1 × cheeseburger single
  - L2: 1 × latte large substitute whole_milk→oat_milk
  - L3: 2 × lemonade
  - fulfillment delivery, address provided, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0189: unclear_message, deepseek-flash@none, food-court
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: heyy is this the pizza spot?? 😄 **[SMALL_TALK]**
- 1 customer: ok so i was walking by n saw the sign n was like ooo 😍 do u guys still have the... the one with the uhhh the melty thing on top?? 🙈 sorry lol **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0194: menu_question, claude-haiku-5-5@off-low, food-court
Card: Only asks one or two questions about the menu (what comes on something, sizes, what's good, whether they have something). Does not order.
Card check: agrees

- 0 customer: hey u guys still do the lemonade combo thing or nah **[MENU_QUESTION]**
- 1 business: Hi! Yes we still have the Cheeseburger Combo, it comes with a side and a drink, and lemonade is one of the drink options. Anything else you wanted to know?
- 2 customer: ok cool and what comes on the cheeseburger like does it come w tomato n stuff **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0246: payment_question, claude-haiku-5-5@off-low, food-court
Card: Only asks how they can pay (cash, card, an app). Does not order.
Card check: agrees

- 0 customer: HELLO?? IS ANYONE THERE?? I NEED TO KNOW HOW I CAN PAY!! **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0248: two_requests, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 4 × Margherita Pizza (Personal 8-inch). In the same message as the first item, also asks a question about the menu. Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: agrees

- 0 customer: hey, can i get 4 personal margherita pizzas? also do u guys still have the bacon burger? **[PLACE_ORDER + MENU_QUESTION]**
- 1 business: Hello! Yes, we still have the bacon burger available. I have those 4 personal margherita pizzas down for you.
- 2 customer: cool, actually just the 4 pizzas is fine thx **[MODIFY_ORDER]**

  - L1: 4 × margherita_pizza personal
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0260: correction_after_confirmation, claude-haiku-5-5@off-low, food-court
Card: Opens with a greeting before ordering. First orders 2 × Bacon Burger, no Onions (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 × Bacon Burger, no Onions. Will pick it up. Never says how they'll pay. Gives their name: Sam.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey hi there **[SMALL_TALK]**
- 1 business: Hi! Welcome to the Food Court. What can I get started for you?
- 2 customer: lemme get 2 bacon burgers no onions pls **[PLACE_ORDER]**
- 3 business: Got it: 2 Bacon Burgers, no onions. Is that right?
- 4 customer: yea that works but wait actually just 1 not 2 sorry **[MODIFY_ORDER]**
- 5 business: No problem, so 1 Bacon Burger, no onions. Anything else?
- 6 customer: nah thats it. name is sam thx **[PLACE_ORDER]**

  - L1: 1 × bacon_burger  remove onion
  - fulfillment unknown, address not_mentioned, payment unknown, name Sam, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0273: off_menu, claude-haiku-5-5@off-low, food-court
Card: Opens with a greeting before ordering. Orders: 1 × Latte (Medium 12 oz), add Vanilla syrup; 1 × cannoli (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Wants delivery to 4 Fairmont Ct (written the way the customer would type it). Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: items

- 0 customer: hey hows it going **[SMALL_TALK]**
- 1 business: Hi there! Doing well, thanks. What can I get started for you?
- 2 customer: lemme get a medium latte w vanilla syrup pls **[PLACE_ORDER]**
- 3 business: Got it, medium latte with vanilla syrup. Anything else?
- 4 customer: yea also a cannoli, u guys still have those rn? two of em if u do

can u deliver to 4 fairmont ct, gonna need it in like 20 min thx **[PLACE_ORDER + MENU_QUESTION]**

  - L1: 1 × latte medium add vanilla_syrup
  - L2: 2 × off-menu 'cannoli'
  - fulfillment unknown, address provided, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0275: simple_order, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 2 × Sprite (Bottle 20 oz). Will pick it up. Pays cash. Gives their name: Sam.
Card check: agrees

- 0 business: Hi! Thanks for messaging Food Court. How can I help you today?
- 1 customer: hey **[SMALL_TALK]**
- 2 customer: need 2 sprite bottles pls **[PLACE_ORDER]**
- 3 customer: the 20oz ones **[PLACE_ORDER]**
- 4 business: Sure thing. Just to confirm, that's 2 Sprite (Bottle 20 oz)?
- 5 customer: yup. that's it. name is Sam. paying cash when i pick up **[CONFIRM_ORDER + PLACE_ORDER]**
- 6 customer: thx! **[SMALL_TALK]**

  - L1: 2 × sprite bottle_20oz
  - fulfillment pickup, address not_applicable, payment cash, name Sam, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0277: correction_after_confirmation, gemini-3.1-flash-lite@minimal, food-court
Card: First orders 3 × Lemonade (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 2. Final order: 2 × Lemonade. Wants delivery to 777 Birch Pl (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50).
Card check: agrees

- 0 customer: hey... rough sunday here. need help. can i get 3 lemonades pls **[PLACE_ORDER]**
- 1 business: Hi! We can get that started for you. Just to confirm, that is 3 Lemonades?
- 2 customer: yep **[CONFIRM_ORDER]**
- 3 customer: actually wait sry, lemme just do 2 lemonades instead. also need delivery to 777 birch pl **[MODIFY_ORDER]**
- 4 business: No problem! Updating that to 2 Lemonades for delivery to 777 Birch Pl.
- 5 customer: thx. also paying cash, pls bring change for a 20 **[PLACE_ORDER]**

  - L1: 2 × lemonade
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0281: contextual_yes, claude-haiku-5-5@off-low, food-court
Card: Orders: 1 × Dr Pepper (Bottle 20 oz); 4 × Pepperoni Pizza (Large 14-inch), no Pepperoni, add Green peppers. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Wants delivery to 49 Lakeview Terrace (across from the park) (written the way the customer would type it). Never says how they'll pay. Says when they want it: a clock time (like 'at 6:30'). Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: u still taking orders **[DELIVERY_QUESTION]**
- 2 customer: lemme get a dr pepper **[PLACE_ORDER]**
- 3 business: Hi! Yes we are. Which size for the Dr Pepper? We have 12 oz can, 20 oz bottle, or 2-liter.
- 4 customer: 20 oz bottle pls **[PLACE_ORDER]**
- 5 customer: and 4 large pizzas **[PLACE_ORDER]**
- 6 customer: pepperoni pizza **[PLACE_ORDER]**
- 7 customer: but no pepperoni lol **[MODIFY_ORDER]**
- 8 customer: add green peppers instead **[MODIFY_ORDER]**
- 9 business: Got it. Can I ask, does the Pepperoni Pizza come with pepperoni by default? Just want to be sure what you mean by no pepperoni.
- 10 customer: yes its on there by default **[MODIFY_ORDER]**
- 11 customer: so take that off **[MODIFY_ORDER]**
- 12 business: Thanks! Just so I have it right: 1 Dr Pepper 20 oz bottle, and 4 Pepperoni Pizzas, Large 14-inch, no pepperoni, with green peppers added. Is that right?
- 13 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × dr_pepper bottle_20oz
  - L2: 4 × pepperoni_pizza large remove pepperoni, add green_peppers
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0293: out_of_scope, gemini-3.1-flash-lite@minimal, food-court
Card: Asks something unrelated to ordering food (a job, parking, a lost item, the wifi, a donation). Does not order.
Card check: agrees

- 0 customer: Hi, I just finished an exam and was wondering if you happen to have a lost and found? I think I left my water bottle there earlier today. **[OUT_OF_SCOPE]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0296: implicit_category, deepseek-flash@none, food-court
Card: Orders: 1 order of Fries (the customer doesn't mention a size). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: hey u guys open rn? **[DELIVERY_QUESTION]**
- 1 business: we are! what can we get started for you?
- 2 customer: sweet lemme get some fries pls **[PLACE_ORDER]**
- 3 business: got it, one order of fries. anything else?
- 4 customer: nah thats it thx, gonna pay w card **[PLACE_ORDER + SMALL_TALK]**

  - L1: 1 × fries regular
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0312: implicit_category, claude-haiku-5-5@off-low, food-court
Card: Orders: 1 × Cappuccino (Small 8 oz), add Caramel syrup; 1 × Breakfast Sandwich (the customer doesn't mention a size), no Cheddar; 1 × Cheeseburger (the customer doesn't mention a size), no Onions. Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Never says whether it's pickup or delivery. Pays cash.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: need food for me and the 2 kids **[SMALL_TALK]**
- 2 customer: small cappuccino w caramel pls **[PLACE_ORDER]**
- 3 customer: breakfast sandwich no cheddar **[PLACE_ORDER]**
- 4 customer: and a cheeseburger no onions thx **[PLACE_ORDER]**
- 5 business: Hi! Sure, let's get that going.
- 6 business: Got it: small cappuccino with caramel syrup, a breakfast sandwich without cheddar, and a cheeseburger without onions. Anything else?
- 7 customer: yep that's it **[CONFIRM_ORDER]**

  - L1: 1 × cappuccino small add caramel_syrup
  - L2: 1 × breakfast_sandwich english_muffin remove cheddar
  - L3: 1 × cheeseburger single remove onion
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0314: unclear_message, deepseek-flash@none, food-court
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: agrees

- 0 business: Hey! What can I get for you today? 😊
- 1 customer: hiii so my roommate and I were gonna do— **[UNKNOWN]**
- 2 customer: omg soryy cat stepped on my phoen 😭 ywah we were trying to figure out the menu, what do you reccomnd for 2 ppl **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0318: correction, deepseek-flash@none, food-court
Card: First asks for 1 × Meat Lovers Pizza (Large 14-inch) (plus anything else below), then swaps it for 2 × Bottled Water. Final order: 2 × Bottled Water; 1 × Diet Coke (the customer doesn't mention a size). Will pick it up. Pays by card. Gives their name: Ivy. Says when they want it: a relative time (like 'in 20 min').
Card check: item_details

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: u guys open rn? **[DELIVERY_QUESTION]**
- 2 business: hey! yep we're open till 11 :)
- 3 customer: cool lemme get a large meat lovers pizza pls **[PLACE_ORDER]**
- 4 business: got it — 1 large 14-inch Meat Lovers. anything else?
- 5 customer: wait scratch that actually **[MODIFY_ORDER]**
- 6 customer: swap the pizza for 2 bottled waters **[MODIFY_ORDER]**
- 7 customer: and a diet coke too **[PLACE_ORDER]**
- 8 business: no prob! so that's 2 bottled waters + 1 Diet Coke. what size on the Diet Coke?
- 9 customer: regular's fine **[PLACE_ORDER]**
- 10 customer: pickup btw **[PLACE_ORDER]**
- 11 customer: name's Ivy **[PLACE_ORDER]**
- 12 customer: and I'm gonna swing by in 20 min **[PLACE_ORDER]**
- 13 customer: paying by card **[PLACE_ORDER]**

  - L1: 2 × water
  - L2: 1 × diet_coke
  - fulfillment pickup, address not_applicable, payment card, name Ivy, decision pending
  - missing: item_variant/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0340: simple_order, deepseek-flash@none, food-court
Card: Orders: 1 × Sprite (Can 12 oz). Wants delivery to 268 Chestnut Ln (written the way the customer would type it). Never says how they'll pay.
Card check: agrees

- 0 customer: CAN WE GET ONE SPRITE?? THE 12 OZ CAN!! DELIEVRY TO 268 CHESTNUT LN PLZ!!! **[PLACE_ORDER]**
- 1 business: Got it — 1 Sprite, 12 oz can. That's for delivery to 268 Chestnut Ln?
- 2 customer: YES EXACTLY!! ONE SPRITE CAN!! THATS ALL!! **[CONFIRM_ORDER]**

  - L1: 1 × sprite can
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0347: correction_after_confirmation, deepseek-flash@none, food-court
Card: Opens with a greeting before ordering. First orders 2 × Veggie Burger, add Bacon (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 × Veggie Burger, add Bacon; 1 × Margherita Pizza (Personal 8-inch). Will pick it up. Pays by card. Gives their name: Jordan. Says when they want it: a relative time (like 'in 20 min').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: Hi there! **[SMALL_TALK]**
- 1 customer: I'm ordering for a friend who's under the weather, so I'd like 2 Veggie Burgers with bacon added. **[PLACE_ORDER]**
- 2 customer: Could you also add a personal 8-inch Margherita Pizza? **[PLACE_ORDER]**
- 3 business: Hi! Got it so far: 2 Veggie Burgers with bacon, and 1 personal 8-inch Margherita Pizza. Anything else?
- 4 customer: Yes, that sounds right. Actually, change the burgers to just 1, please. **[MODIFY_ORDER]**
- 5 customer: I'll pick it up and pay by card. Name's Jordan, and I'd like it in about 20 minutes. **[PLACE_ORDER]**

  - L1: 1 × veggie_burger  add bacon
  - L2: 1 × margherita_pizza personal
  - fulfillment pickup, address not_applicable, payment card, name Jordan, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0370: contextual_yes, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 1 × Lemonade. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash. Gives their name: Marcus. Says when they want it: asap. Asks a menu question partway through.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey can i get a lemonade pls **[PLACE_ORDER]**
- 1 customer: also do u guys have iced coffee? **[MENU_QUESTION]**
- 2 business: we have drip coffee, lattes, cappuccinos, and americanos! shall i add anything besides the 1 lemonade?
- 3 customer: no just the lemonade for marcus thx **[PLACE_ORDER]**
- 4 business: got it, 1 lemonade for marcus. is that all for your order?
- 5 customer: yep **[SMALL_TALK]**

  - L1: 1 × lemonade
  - fulfillment unknown, address not_mentioned, payment unknown, name Marcus, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

