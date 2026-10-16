# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-m1-0019: correction, deepseek-flash@none, food-court
Card: First asks for 1 × Iced Tea (the customer doesn't mention a size) (plus anything else below), then swaps it for 1 × Drip Coffee (Medium 12 oz), add Hazelnut syrup, add Whole milk. Final order: 1 × Drip Coffee (Medium 12 oz), add Hazelnut syrup, add Whole milk; 1 × Hawaiian Pizza (Small 10-inch), no Tomato sauce; 1 × Veggie Burger. Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: items

- 0 customer: hey guys 😅 rough morning over here **[SMALL_TALK]**
- 1 business: hey! haha we've all been there 😄 what can we get you?
- 2 customer: can i get an iced tea? and a small hawaiian pizza with no tomato sauce 🙏 **[PLACE_ORDER]**
- 3 business: got it — 1 iced tea and a small Hawaiian pizza, no tomato sauce. anything else?
- 4 customer: oh wait actually scratch the iced tea 😬 can i swap it for a medium drip coffee instead? **[MODIFY_ORDER]**
- 5 business: no problem! medium drip coffee it is. anything in it?
- 6 customer: yes plz, hazelnut syrup and whole milk 🙌 also add a veggie burger **[PLACE_ORDER]**
- 7 business: sounds good! so that's a medium drip coffee with hazelnut syrup and whole milk, a small Hawaiian pizza with no tomato sauce, and a veggie burger. all set?
- 8 customer: yep thats everything, thank you!! 🧡 **[CONFIRM_ORDER]**

  - L1: 1 × iced_tea can
  - L2: 1 × hawaiian_pizza small remove tomato_sauce
  - L3: 1 × drip_coffee medium add hazelnut_syrup, add whole_milk
  - L4: 1 × veggie_burger
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

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

## syn-m1-0043: correction_after_confirmation, deepseek-flash@none, food-court
Card: Opens with a greeting before ordering. First orders 2 × Meat Lovers Pizza (Small 10-inch), add Onions (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 × Croissant (the customer doesn't mention a size). Final order: 1 × Croissant (the customer doesn't mention a size). Will pick it up. Pays by card. Gives their name: Jordan.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey! 👋 **[SMALL_TALK]**
- 1 business: Hi there! What can we get started for you?
- 2 customer: movie night got sprung on me last min 😅 gonna need 2 small meat lovers pizzas w onions pls **[PLACE_ORDER]**
- 3 business: Got it — 2 small Meat Lovers pizzas with onions added. Anything else?
- 4 customer: yep thats it thx! **[SMALL_TALK]**
- 5 business: Just to confirm: 2 small Meat Lovers pizzas, onions added. Sound right?
- 6 customer: actually hold up, change of plans 😬 lemme just do 1 croissant instead **[MODIFY_ORDER]**
- 7 business: No problem! So that's 1 croissant. Will that be pickup or delivery?
- 8 customer: pickup pls, paying by card **[PLACE_ORDER]**
- 9 business: Great — 1 croissant, pickup, card. Can I get a name for the order?
- 10 customer: Jordan 🙂 **[PLACE_ORDER]**

  - L2: 1 × croissant plain
  - fulfillment pickup, address not_applicable, payment card, name Jordan, decision pending
  - missing: nothing

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
- 6 customer: That's it, ty! **[CONFIRM_ORDER]**

  - L1: 1 × half pepperoni_pizza / half cheese_pizza large add sausage
  - L2: 1 × milkshake vanilla
  - L3: 1 × milkshake chocolate
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0074: unclear_message, claude-haiku-5-5@off-low, food-court
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: yo dude just got carried by my teammate ggg 🎮🔥 lmao wait sry b **[SMALL_TALK]**
- 1 business: Hi! Thanks for reaching out to Food Court. Are you looking to place an order?
- 2 customer: ya hol on need one sec the 3rd ca 🎮😂 respawn timer **[SMALL_TALK]**

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

  - L1: 1 × off-menu 'large chicken noodle soup'
  - L2: 2 × off-menu 'orange juices'
  - L3: 2 × cheeseburger single remove onion
  - L4: 1 × fries large
  - L5: 1 × milkshake chocolate
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, item_menu_match/off_menu, fulfillment_method/missing, payment_method/missing

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

## syn-m1-0154: unclear_message, deepseek-flash@none, food-court
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: u up rn **[DELIVERY_QUESTION]**
- 2 customer: thin crust lg half mush half **[PLACE_ORDER]**
- 3 business: Hey! We're open. What can I get started for you?
- 4 customer: pls thx gonna send in a **[SMALL_TALK]**
- 5 customer: wait sorry pocket tex **[SMALL_TALK]**
- 6 customer: were still deciding **[SMALL_TALK]**
- 7 business: No worries, take your time! Just let me know when you're ready.
- 8 customer: kk thx **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0158: simple_order, deepseek-flash@none, food-court
Card: Orders: 1 × Latte (Large 16 oz). Wants delivery to 7597 Ivanhoe Ln (written the way the customer would type it). Never says how they'll pay. Asks a menu question partway through.
Card check: item_details

- 0 customer: Hello! I'd like to order a large latte, please. **[PLACE_ORDER]**
- 1 business: Hi there! One large latte. Can I get you anything else?
- 2 customer: Does the latte come with whole milk by default? I'm watching my calories, so I'd like to know my options. **[MENU_QUESTION]**
- 3 business: Yes, the latte comes with whole milk. You can swap it for skim, oat, or almond milk if you'd prefer.
- 4 customer: Skim milk would be great, thank you. **[PLACE_ORDER]**
- 5 business: Got it. One large latte with skim milk. Is that for pickup or delivery?
- 6 customer: Delivery, please. My address is 7597 Ivanhoe Ln. **[PLACE_ORDER]**

  - L1: 1 × latte large substitute whole_milk→skim_milk
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
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

## syn-m1-0197: refund_request, gemini-3.1-flash-lite@minimal, food-court
Card: Got an earlier order (not in this chat) where the croissant was squashed, and asks for their money back.
Card check: agrees

- 0 customer: Hello, I placed an order earlier and the croissant arrived squashed. Could I please get a refund for that item? **[REFUND_REQUEST]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0244: out_of_scope, claude-haiku-5-5@off-low, food-court
Card: Asks something unrelated to ordering food (a job, parking, a lost item, the wifi, a donation). Does not order.
Card check: agrees

- 0 customer: hi there! 😊 lemme ask u something real quick, do u guys have a donation box or know where i could drop off old books for a school library? thx so much 🙏 **[OUT_OF_SCOPE]**

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

## syn-m1-0252: combo, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 2 × Coffee & Pastry, drink: Drip Coffee, pastry: Muffin; 2 × Hawaiian Pizza (Small 10-inch). Picks every combo choice. Wants delivery to 43 Magnolia St, unit 15A (written the way the customer would type it). Never says how they'll pay.
Card check: agrees

- 0 customer: Hey there! **[SMALL_TALK]**
- 1 customer: Need an order for the shop pls **[SMALL_TALK]**
- 2 business: Hi! We can definitely help you with that. What can I get started for you?
- 3 customer: Gonna need two coffee & pastry combos **[PLACE_ORDER]**
- 4 customer: Drip coffee and muffins for both **[PLACE_ORDER]**
- 5 customer: Plus two small Hawaiian pizzas **[PLACE_ORDER]**
- 6 business: Got it. So that is two Coffee & Pastry combos with Drip Coffee and muffins, plus two 10-inch Hawaiian pizzas. Where will this be delivered to?
- 7 customer: 43 Magnolia St unit 15A **[PLACE_ORDER]**
- 8 customer: Thx! **[SMALL_TALK]**

  - L1: 2 × coffee_pastry_combo   drink=drip_coffee, pastry=muffin
  - L2: 2 × hawaiian_pizza small
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: combo_choice/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0259: multi_message_order, deepseek-flash@none, food-court
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 1 × Coke (the customer doesn't mention a size); 2 orders of Onion Rings. Wants delivery to 54 Thornton Dr, unit 6 (written the way the customer would type it). Pays by card.
Card check: agrees

- 0 customer: YO!!! WHATS UP **[SMALL_TALK]**
- 1 business: Hey! What can I get for you?
- 2 customer: CAN I GET A COKE **[PLACE_ORDER]**
- 3 customer: AND 2 ONION RINGS!! **[PLACE_ORDER]**
- 4 business: Got it! One Coke and two orders of Onion Rings. Anything else?
- 5 customer: THATS IT. DELIVER TO 54 THORNTON DR UNIT 6 PLS **[CONFIRM_ORDER + PLACE_ORDER]**
- 6 business: Sure thing! And how would you like to pay?
- 7 customer: CARD!! MY MOM SAID ITS OK **[PLACE_ORDER]**

  - L1: 1 × coke can
  - L2: 2 × onion_rings
  - fulfillment delivery, address provided, payment card, name –, decision confirmed
  - missing: nothing

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
- 6 customer: nah thats it. name is sam thx **[SMALL_TALK + PLACE_ORDER]**

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
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, payment_method/missing

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
- 10 customer: yes its on there by default **[PLACE_ORDER]**
- 11 customer: so take that off **[MODIFY_ORDER]**
- 12 business: Thanks! Just so I have it right: 1 Dr Pepper 20 oz bottle, and 4 Pepperoni Pizzas, Large 14-inch, no pepperoni, with green peppers added. Is that right?
- 13 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × dr_pepper bottle_20oz
  - L3: 4 × pepperoni_pizza large remove pepperoni, add green_peppers
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0298: out_of_scope, deepseek-flash@none, food-court
Card: Asks something unrelated to ordering food (a job, parking, a lost item, the wifi, a donation). Does not order.
Card check: agrees

- 0 customer: hey do u guys have wifi in the seating area? hosting a movie night last min and forgot to check lol **[OUT_OF_SCOPE]**
- 1 business: hey! yes we do, free wifi for customers 🙂
- 2 customer: perfect thx gonna swing by later **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0303: out_of_scope, deepseek-flash@none, food-court
Card: Asks something unrelated to ordering food (a job, parking, a lost item, the wifi, a donation). Does not order.
Card check: agrees

- 0 customer: hey do you guys have wifi **[OUT_OF_SCOPE]**
- 1 business: hey! yes we do, free wifi — network is FoodCourtGuest, password is on the receipt
- 2 customer: sweet **[SMALL_TALK]**
- 3 customer: also random q **[SMALL_TALK]**
- 4 customer: did someone turn in a lost item? i think i left my blue notebook here last night **[OUT_OF_SCOPE]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0311: payment_claim, claude-haiku-5-5@off-low, food-court
Card: Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent the money on the app') and asks whether the payment went through. Does not order anything new.
Card check: agrees

- 0 customer: HELLO?? I PAID ONLINE FOR MY ORDER ALREADY!!! DID THE PAYMENT GO THROUGH?? PLEASE TELL ME!! **[PAYMENT_CLAIM]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0316: correction, deepseek-flash@none, food-court
Card: Opens with a greeting before ordering. First asks for 2 × Margherita Pizza (Medium 12-inch), no Basil, add House cheese blend (plus anything else below), then swaps it for 3 orders of Onion Rings. Final order: 3 orders of Onion Rings. Will pick it up. Never says how they'll pay. Gives their name: Ben.
Card check: agrees

- 0 customer: HEY HEY!! **[SMALL_TALK]**
- 1 customer: OK SO I NEED TWO MEDIUM MARGHERITA PIZZAS, NO BASIL, BUT THROW ON THE HOUSE CHEESE BLEND TOO **[PLACE_ORDER]**
- 2 business: Got it — 2 medium Margherita pizzas, no basil, add house cheese blend. Anything else?
- 3 customer: ACTUALLY SCRATCH THAT **[MODIFY_ORDER]**
- 4 customer: CAN I JUST GET THREE ORDERS OF ONION RINGS INSTEAD? PICKING IT UP, NAME'S BEN **[MODIFY_ORDER]**

  - L2: 3 × onion_rings
  - fulfillment pickup, address not_applicable, payment unknown, name Ben, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0319: payment_claim, gemini-3.1-flash-lite@minimal, food-court
Card: Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent the money on the app') and asks whether the payment went through. Does not order anything new.
Card check: agrees

- 0 customer: hello there just wondering if u could check on my order from earlier today **[ORDER_STATUS]**
- 1 business: Hi! Sure, can you let me know the name on the order?
- 2 customer: its mary smith i already paid online using the app just wanted to check if the payment went thru okay thx so much **[ORDER_STATUS + PAYMENT_CLAIM]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0341: multi_message_order, deepseek-flash@none, food-court
Card: Builds the order over several messages, a thing or two at a time: 1 × Breakfast Sandwich (On a bagel), add Tomato; 1 × Iced Tea (Can 12 oz); 1 × Americano (Small 8 oz). Wants delivery to 93 Quincy Terrace, apt 29A (written the way the customer would type it). Pays by card. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: Hey, can I get a breakfast sandwich? On a bagel please, with tomato added. **[PLACE_ORDER]**
- 1 business: Got it, one breakfast sandwich on a bagel with tomato.
- 2 customer: Also an iced tea, the 12 oz can. **[PLACE_ORDER]**
- 3 business: Sounds good. Anything else?
- 4 customer: An Americano too, small. **[PLACE_ORDER]**
- 5 business: So that's a breakfast sandwich on a bagel with tomato, an iced tea can, and a small Americano. Is that everything?
- 6 customer: Yes, that's the order. **[CONFIRM_ORDER]**
- 7 business: Great, and how did you want to get it?
- 8 customer: Delivery to 93 Quincy Terrace, apt 29A. Paying by card. **[PLACE_ORDER]**
- 9 business: Perfect. When would you like it?
- 10 customer: In 20 min please. **[PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich bagel add tomato
  - L2: 1 × iced_tea can
  - L3: 1 × americano small
  - fulfillment delivery, address provided, payment card, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0369: contextual_yes, claude-haiku-5-5@off-low, food-court
Card: Orders: 4 × Cheeseburger (Double patty); 1 × Milkshake (Strawberry). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash. Gives their name: Tom. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: Hello, I would like to place an order for pickup, please. **[PLACE_ORDER]**
- 1 business: Hi there! Sure, what can I get started for you?
- 2 customer: I need four cheeseburgers with a double patty, please. They are for my two hungry kids and me. **[PLACE_ORDER]**
- 3 business: Got it, 4 double patty cheeseburgers. Anything else?
- 4 customer: Yes, one strawberry milkshake, please. **[PLACE_ORDER]**
- 5 business: Okay, so that's 4 Cheeseburgers (Double patty) and 1 Strawberry Milkshake. Is that right?
- 6 customer: Yes, that is correct. **[CONFIRM_ORDER]**

  - L1: 4 × cheeseburger double
  - L2: 1 × milkshake strawberry
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-m1-0370: contextual_yes, gemini-3.1-flash-lite@minimal, food-court
Card: Orders: 1 × Lemonade. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash. Gives their name: Marcus. Says when they want it: asap. Asks a menu question partway through.
Card check: agrees

- 0 customer: hey can i get a lemonade pls **[PLACE_ORDER]**
- 1 customer: also do u guys have iced coffee? **[MENU_QUESTION]**
- 2 business: we have drip coffee, lattes, cappuccinos, and americanos! shall i add anything besides the 1 lemonade?
- 3 customer: no just the lemonade for marcus thx **[PLACE_ORDER]**
- 4 business: got it, 1 lemonade for marcus. is that all for your order?
- 5 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × lemonade
  - fulfillment unknown, address not_mentioned, payment unknown, name Marcus, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

