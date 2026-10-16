# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-p3-0003: payment_claim, deepseek-flash@none, corner-patty
Card: Says they already paid for an earlier order (on the phone, online or in the app) and asks whether it went through. Does not order anything new.
Card check: labels (expected labels not found: PAYMENT_CLAIM)

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: i ordered like 20 min ago over the phone **[ORDER_STATUS]**
- 2 customer: did it go thru? **[ORDER_STATUS]**
- 3 business: Hey! What name was the order under?
- 4 customer: sam **[UNKNOWN]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0004: simple_order, deepseek-flash@none, corner-patty
Card: Orders: 4 × Coke. Wants delivery to 234 Larkin Ln (written the way the customer would type it). Pays by card.
Card check: agrees

- 0 customer: hey can i get four cokes delivered to 234 larkin ln pls, paying by card **[PLACE_ORDER]**

  - L1: 4 × coke
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0072: delivery_question, claude-haiku-5-5@off-low, corner-patty
Card: Only asks about delivery or pickup (delivery area, fee, how long it takes, opening hours). Does not order.
Card check: agrees

- 0 customer: hey 🎮 do u guys deliver? im not trying to leave my setup lol **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes, we offer delivery as well as pickup 😊 Are you in our delivery area?
- 2 customer: idk how do i check that 😅 also how long does delivery usually take and is there a fee?? **[DELIVERY_QUESTION]**
- 3 business: You can enter your address at checkout and it'll tell you if we deliver there. Delivery times vary, and the fee is shown before you pay. We're open 11:00 to 22:00 today.
- 4 customer: ok cool 👍 thx, ill check back later when im done with my match 🎮 **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0085: multi_message_order, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Builds the order over several messages, a thing or two at a time: 1 × Veggie Pizza (Extra large 16-inch); 3 × Supreme Pizza (Small 10-inch), no Sausage; 1 × Diet Coke (no size mentioned by anyone: the regular one). Wants delivery to 33 Delancey Ave (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50). Says when they want it: a clock time (like 'at 6:30'). Asks a menu question partway through.
Card check: agrees

- 0 customer: hey u guys open for delivery rn **[DELIVERY_QUESTION]**
- 1 business: yes we are! what can i get for u?
- 2 customer: gonna order for my sick friend so need some food pls can i get a 16 inch veggie pizza **[PLACE_ORDER]**
- 3 customer: also 3 small supreme pizzas but can u leave the sausage off those **[PLACE_ORDER]**
- 4 customer: do u guys have diet coke **[MENU_QUESTION]**
- 5 business: we sure do! so that is one extra large veggie, three small supreme pizzas without sausage, and a diet coke. is that all?
- 6 customer: yeah that works can u send it to 33 delancey ave **[CONFIRM_ORDER + PLACE_ORDER]**
- 7 customer: can u get it there by 630 and i need change for a 50 **[PLACE_ORDER]**
- 8 business: got it. we will have that to 33 delancey ave by 6:30 and will make sure the driver has change for a 50.
- 9 customer: thx so much **[SMALL_TALK]**

  - L1: 1 × veggie_pizza extra_large
  - L2: 3 × supreme_pizza small remove sausage
  - L3: 1 × diet_coke can
  - fulfillment delivery, address provided, payment cash, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0113: payment_question, claude-haiku-5-5@off-low, corner-patty
Card: Only asks how they can pay (cash, card, an app). Does not order.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: lemme ask rn **[SMALL_TALK]**
- 2 customer: can i pay w cash or u only take card? or an app? **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0115: ambiguous_reference, deepseek-flash@none, corner-patty
Card: Refers to the first item vaguely at first ('same as last time'); the business asks which one, and the customer names it. Final order: 2 × Cheeseburger (Double patty). Wants delivery to 590 Spruce Pl (written the way the customer would type it). Never says how they'll pay.
Card check: items

- 0 customer: yo u guys open rn **[DELIVERY_QUESTION]**
- 1 business: yep we're open til 10! what can we get u
- 2 customer: lemme get the same as last time pls 😅 **[PLACE_ORDER]**
- 3 business: haha gotta be more specific, which one was that?
- 4 customer: the cheeseburger, the double patty one **[PLACE_ORDER]**
- 5 business: got it — 2 double patty cheeseburgers. anything else?
- 6 customer: nah thats it thx, deliver to 590 spruce pl **[PLACE_ORDER]**

  - L1: 1 × cheeseburger double
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0123: off_menu, deepseek-flash@none, corner-patty
Card: Orders: 1 × Cheeseburger (Single patty); 1 × Lemonade; 1 × chicken nuggets (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Never says whether it's pickup or delivery. Pays by card. Asks a menu question partway through.
Card check: items

- 0 customer: hey do u guys have chicken nuggets **[MENU_QUESTION]**
- 1 business: hey! not sure yet, let me check on that for u. anything else i can get started on?
- 2 customer: k lemme get a single cheeseburger and a lemonade pls **[PLACE_ORDER]**
- 3 business: got it! one single patty cheeseburger and a lemonade. just to make sure, is that everything so far?
- 4 customer: yea thats it thx **[SMALL_TALK]**

  - L1: 1 × cheeseburger single
  - L2: 1 × lemonade
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0144: contextual_yes, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Orders: 4 × Coke (no size mentioned by anyone: the regular one). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays by card. Asks a menu question partway through.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: lemme get 4 cokes **[PLACE_ORDER]**
- 2 customer: u got those rn? **[MENU_QUESTION]**
- 3 business: Hi! Yes, we have Coke. Just to confirm: 4 Coke, is that right?
- 4 customer: wait **[SMALL_TALK]**
- 5 customer: do the cans come in the 2 liter thing or **[MENU_QUESTION]**
- 6 business: Coke comes in 12 oz can, 20 oz bottle, or 2-liter bottle. What did you want?
- 7 customer: ok the regular one is fine **[PLACE_ORDER]**
- 8 customer: yep that's it **[CONFIRM_ORDER]**

  - L1: 4 × coke can
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0160: correction, claude-haiku-5-5@off-low, corner-patty
Card: First asks for 1 order of Onion Rings (plus anything else below), then swaps it for 1 order of Onion Rings. Final order: 1 order of Onion Rings; 3 orders of Fries (no size mentioned by anyone: the regular one); 1 × Sprite. Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: items

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: lemme get one onion rings pls **[PLACE_ORDER]**
- 2 customer: and fries **[PLACE_ORDER]**
- 3 business: Hi! Sure, 1 onion rings and fries. How many fries?
- 4 customer: three fries **[PLACE_ORDER]**
- 5 customer: wait **[SMALL_TALK]**
- 6 customer: actually scratch the onion rings **[MODIFY_ORDER]**
- 7 customer: make it onion rings instead of the fries pls **[MODIFY_ORDER]**
- 8 business: No problem, so 1 onion rings, 3 fries, got it. Anything to drink?
- 9 customer: a sprite thx **[PLACE_ORDER]**

  - L2: 3 × onion_rings
  - L3: 1 × sprite
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0194: correction, claude-haiku-5-5@off-low, halfmoon-pizza
Card: First asks for 1 × Bottled Water (plus anything else below), then swaps it for 1 × Pepperoni Pizza (Personal 8-inch), add Tomatoes, add Stuffed crust. Final order: 1 × Pepperoni Pizza (Personal 8-inch), add Tomatoes, add Stuffed crust; 1 × Iced Tea (no size mentioned by anyone: the regular one); 1 × Supreme Pizza (Medium 12-inch), add Ham. Wants delivery to 5711 Sycamore Dr, apt 6B (written the way the customer would type it). Pays by card.
Card check: item_details

- 0 customer: hey lemme get 1 bottled water pls 🙏 **[PLACE_ORDER]**
- 1 business: Sure! Anything else with that?
- 2 customer: oh wait actually can u swap that for a personal pepperoni pizza instead?? 😅 **[MODIFY_ORDER]**
- 3 business: Of course. Personal 8-inch pepperoni, got it. Any extras on it?
- 4 customer: add tomatoes and stuffed crust pls. also gonna need 1 iced tea (regular) and a medium supreme w ham added, thx 🍕 **[PLACE_ORDER]**

  - L1: 1 × pepperoni_pizza personal add tomatoes, add crust_stuffed
  - L2: 1 × iced_tea
  - L3: 1 × supreme_pizza medium add ham
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_variant/missing, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0205: correction_after_confirmation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: First orders 3 × BBQ Chicken Pizza (Large 14-inch) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 2. Final order: 2 × BBQ Chicken Pizza (Large 14-inch); 2 × Sprite (no size mentioned by anyone: the regular one); 1 × Diet Coke (2-liter bottle). Wants delivery to 9106 Riverside Dr, # 18A (written the way the customer would type it). Pays by card.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey lemme get 3 bbq chicken pizzas large pls **[PLACE_ORDER]**
- 1 business: Hi! Sure. Let me confirm: 3 BBQ Chicken Pizza, Large 14-inch. Anything else?
- 2 customer: wait actually make that 2 not 3 sorry **[MODIFY_ORDER]**
- 3 business: No problem, 2 BBQ Chicken Pizza, Large 14-inch. Anything to drink?
- 4 customer: yea 2 sprites and a diet coke 2 liter thx **[PLACE_ORDER]**
- 5 business: Got it: 2 BBQ Chicken Pizza (Large 14-inch), 2 Sprite, 1 Diet Coke (2-liter bottle). Delivery or pickup?
- 6 customer: delivery pls 9106 riverside dr # 18A **[PLACE_ORDER]**

  - L1: 2 × bbq_chicken_pizza large
  - L2: 2 × sprite can
  - L3: 1 × diet_coke two_liter
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0248: multi_message_order, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 2 × Americano (Large 16 oz); 1 × Bagel (Cinnamon raisin). Never says whether it's pickup or delivery. Pays by card. Says when they want it: asap.
Card check: agrees

- 0 customer: hey good morning **[SMALL_TALK]**
- 1 business: good morning! what can we get started for you?
- 2 customer: lemme get 2 large americanos pls **[PLACE_ORDER]**
- 3 business: got it, 2 large americanos. anything else?
- 4 customer: ya and a cinnamon raisin bagel **[PLACE_ORDER]**
- 5 business: sure thing! so that's 2 large americanos and 1 cinnamon raisin bagel?
- 6 customer: yep thats it. gonna pay by card **[CONFIRM_ORDER + PLACE_ORDER]**
- 7 business: sounds good, we'll have it ready at the counter for you.
- 8 customer: thx, need it asap **[PLACE_ORDER]**

  - L1: 2 × americano large
  - L2: 1 × bagel cinnamon_raisin
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0256: correction, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. First asks for 2 × Drip Coffee (Medium 12 oz), add Almond milk (plus anything else below), then changes the quantity to 1. Final order: 1 × Drip Coffee (Medium 12 oz), add Almond milk; 1 × Croissant (Chocolate). Will pick it up. Never says how they'll pay. Gives their name: Maya.
Card check: agrees

- 0 customer: hey morning **[SMALL_TALK]**
- 1 business: Hi there! How can I help you today?
- 2 customer: lemme get 2 med drip coffees w almond milk pls **[PLACE_ORDER]**
- 3 business: Sure thing, two medium drip coffees with almond milk. Anything else for you?
- 4 customer: wait sry actually just change that to 1 med drip coffee w almond milk and can i add a chocolate croissant too **[MODIFY_ORDER]**
- 5 business: No problem! I have one medium drip coffee with almond milk and one chocolate croissant. Is that all for today?
- 6 customer: yup thx its maya **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 1 × drip_coffee medium add almond_milk
  - L2: 1 × croissant chocolate
  - fulfillment unknown, address not_mentioned, payment unknown, name Maya, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0280: refund_request, gemini-3.1-flash-lite@minimal, corner-patty
Card: Got an earlier order (not in this chat) where the onion rings was the wrong one, and asks for their money back.
Card check: items

- 0 customer: HEY CORNER PATTY! MY LAST ORDER HAD THE WRONG ONION RINGS, I NEED A REFUND FOR THOSE ASAP! **[ORDER_PROBLEM + REFUND_REQUEST]**
- 1 business: Hi there! I am so sorry about that mix-up. Please let me process that refund for you right now.
- 2 customer: THANKS! ALSO CAN I GET THREE CHEESEBURGER COMBOS WITH FRIES AND COKES FOR THE TEAM PLEASE!!! **[PLACE_ORDER + SMALL_TALK]**

  - L1: 3 × cheeseburger_combo   side=fries, drink=coke
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0283: correction_after_confirmation, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: First orders 1 order of Breadsticks (4 pieces each) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 4. Final order: 4 orders of Breadsticks (4 pieces each). Will pick it up. Pays cash. Says when they want it: a relative time (like 'in 20 min').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: Hey! Hosting a movie night, can I get one order of breadsticks pls? 🍿 **[PLACE_ORDER]**
- 1 business: Hi! Sure thing, one order of breadsticks. Anything else for you?
- 2 customer: Actually wait, lemme change that to 4 orders of breadsticks please! Thx :) **[MODIFY_ORDER]**
- 3 business: No problem! I have updated that to 4 orders of breadsticks for you. When would you like to swing by to pick them up?
- 4 customer: In 20 min works! Gonna pay cash when I get there, see ya soon! 🍕 **[PLACE_ORDER]**

  - L1: 4 × breadsticks
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0284: status_question, deepseek-flash@none, halfmoon-pizza
Card: Placed an order earlier (not in this chat) and asks where it is or when it will arrive.
Card check: items

- 0 customer: hey i ordered a lil while ago for my friend whos sick, any idea when its gonna get here **[ORDER_STATUS]**
- 1 business: Hey! Sorry to hear your friend isn't feeling great. Let me check on that for you real quick.
- 2 customer: thx, its a large cheese pizza and a large pepperoni pizza **[ORDER_STATUS]**
- 3 business: Thanks, that helps me find it. We're running a bit behind tonight, should be heading your way soon. Anything else you need?
- 4 customer: ok cool pls hurry if u can, also could u add a 2 liter coke to it rn? my friend could really use it **[MODIFY_ORDER]**

  - L1: 1 × coke two_liter
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0297: two_requests, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Latte (Small 8 oz), add Vanilla syrup, Oat milk instead of Whole milk; 2 × Cappuccino (Small 8 oz), add Vanilla syrup; 3 × Breakfast Sandwich (no size mentioned by anyone: the regular one). In the same message as the first item, also asks a question about the menu. Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Jordan.
Card check: items

- 0 customer: Hi there! My partner and I are deciding what to get. Quick question first: do the breakfast sandwiches come on a bagel as well, or only the English muffin? **[MENU_QUESTION]**
- 1 business: Hi! Yes, the breakfast sandwich comes on an English muffin, a croissant, or a bagel. Do you have a preference?
- 2 customer: Oh good, that helps. We'll go with the regular one. Can we get one small latte, and could it have vanilla syrup with oat milk instead of whole milk? **[PLACE_ORDER]**
- 3 business: Sure, one small latte with vanilla syrup and oat milk instead of whole milk. Anything else?
- 4 customer: Yes, two small cappuccinos with vanilla syrup, and three breakfast sandwiches. We'll pick it up. We're paying cash, and could you tell us if you can change a fifty? We'll be giving you a twenty if not. Our name is Jordan. **[PLACE_ORDER + PAYMENT_QUESTION]**

  - L1: 1 × breakfast_sandwich english_muffin
  - L2: 1 × latte small add vanilla_syrup, substitute whole_milk→oat_milk
  - L3: 2 × cappuccino small add vanilla_syrup
  - L4: 3 × breakfast_sandwich english_muffin
  - fulfillment pickup, address not_applicable, payment cash, name Jordan, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0298: status_question, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Placed an order earlier (not in this chat) and asks where it is or when it will arrive.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: checking on my order **[ORDER_STATUS]**
- 2 customer: it was supposed to be here by now, where is it? **[ORDER_STATUS]**
- 3 business: Hi there! I'm sorry for the confusion, but we are a pickup-only location and don't offer delivery services. Are you perhaps looking for an order you placed for pickup?
- 4 customer: oh shoot **[SMALL_TALK]**
- 5 customer: my bad **[SMALL_TALK]**
- 6 customer: im heading over to grab it now **[ORDER_STATUS]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0314: missing_info, gemini-3.1-flash-lite@minimal, corner-patty
Card: Orders: 1 × Lemonade. Will pick it up. Never says how they'll pay. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: Hello, I would like to order one lemonade for pickup at one o'clock. **[PLACE_ORDER]**
- 1 business: Hi there! I have one lemonade for pickup at 1:00. Is that correct?
- 2 customer: Yes, that is correct. **[CONFIRM_ORDER]**

  - L1: 1 × lemonade
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0316: correction_after_confirmation, gemini-3.1-flash-lite@minimal, morning-crumb
Card: First orders 1 × Latte (Large 16 oz) (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 2 × Drip Coffee (no size mentioned by anyone: the regular one), add Skim milk. Final order: 2 × Drip Coffee (no size mentioned by anyone: the regular one), add Skim milk. Will pick it up. Pays by card. Gives their name: June.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 business: hey! welcome to morning crumb café, what can i get for u?
- 1 customer: hey lemme get a large latte pls **[PLACE_ORDER]**
- 2 business: got it, one large latte. anything else for u today?
- 3 customer: nah thats it, thx **[SMALL_TALK]**
- 4 business: great, i have one large latte for you. should i start making that?
- 5 customer: wait actually change that to 2 drip coffees w skim milk instead pls **[MODIFY_ORDER]**
- 6 business: no prob, switching that to 2 drip coffees with skim milk. is that all for you?
- 7 customer: yup name is june picking up later and payin w card **[PLACE_ORDER]**

  - L1: 2 × drip_coffee medium add skim_milk
  - fulfillment pickup, address not_applicable, payment card, name June, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0332: correction_after_confirmation, gemini-3.1-flash-lite@minimal, corner-patty
Card: First orders 2 × Lemonade (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 order of Onion Rings. Final order: 1 order of Onion Rings; 1 × Sprite. Wants delivery to 398 Fairmont Blvd (written the way the customer would type it). Pays by card.
Card check: items, labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: HEY!! I NEED 2 LEMONADES AND SOME ONION RINGS PLZ!!! **[PLACE_ORDER]**
- 1 business: Hey there! Just to confirm, you would like 2 Lemonades and 1 order of Onion Rings?
- 2 customer: WAIT NO SORRY!! SCRATCH THE LEMONADES!! JUST GIVE ME THE ONION RINGS AND 1 SPRITE!! SEND IT TO 398 FAIRMONT BLVD!! PAYING CARD!! **[MODIFY_ORDER]**

  - L2: None × onion_rings
  - L3: 1 × sprite
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: item_quantity/ambiguous

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0343: simple_order, deepseek-flash@none, halfmoon-pizza
Card: Orders: 1 × Diet Coke (Can 12 oz). Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: need a diet coke **[PLACE_ORDER]**
- 2 customer: just one **[PLACE_ORDER]**
- 3 business: Hey! One Diet Coke — what size can I put you down for?
- 4 customer: can pls **[PLACE_ORDER]**

  - L1: 1 × diet_coke can
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0365: contextual_yes, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Orders: 3 × Breakfast Sandwich (no size mentioned by anyone: the regular one); 1 × Bagel (Cinnamon raisin). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash. Gives their name: Rosa.
Card check: items

- 0 customer: hey r u guys open rn **[DELIVERY_QUESTION]**
- 1 business: hey! yep, we're open till 3. what can i get u?
- 2 customer: ok cool lemme get 3 breakfast sandwiches pls, no tomato on any of em and can u do avocado on 2 of em **[PLACE_ORDER]**
- 3 customer: oh and a cinamon raisin bagel too **[PLACE_ORDER]**
- 4 business: got it — 3 breakfast sandwiches (no tomato, avocado on 2) and 1 cinnamon raisin bagel. is that right?
- 5 customer: yep **[CONFIRM_ORDER]**
- 6 business: cool, see u soon! what name should i put it under?
- 7 customer: rosa, and ill pay cash when i pickup thx **[PLACE_ORDER]**

  - L1: 2 × breakfast_sandwich english_muffin remove tomato, add avocado
  - L2: 1 × breakfast_sandwich english_muffin remove tomato
  - L3: 1 × bagel cinnamon_raisin
  - fulfillment pickup, address not_applicable, payment cash, name rosa, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0369: contextual_yes, claude-haiku-5-5@off-low, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Bagel (Cinnamon raisin), add Egg; 3 × Hot Chocolate (Medium 12 oz); 4 × Croissant (no size mentioned by anyone: the regular one), add Butter. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays by card. Gives their name: Omar.
Card check: agrees

- 0 customer: GOOD MORNING!! I hope you are all doing wonderfully this lovely day! **[SMALL_TALK]**
- 1 business: Good morning! Welcome to Morning Crumb Café. What can I get started for you?
- 2 customer: THANK YOU VERY MUCH! I would like TWO cinnamon raisin bagels, please, and could you put an EGG on both of them? **[PLACE_ORDER]**
- 3 business: Sure thing! Two cinnamon raisin bagels with egg. Anything else?
- 4 customer: Yes please! THREE hot chocolates in the MEDIUM size, and FOUR plain croissants with BUTTER on them, if you would be so kind! **[PLACE_ORDER]**
- 5 business: Got it. So that's: 2 cinnamon raisin bagels with egg, 3 medium hot chocolates, and 4 plain croissants with butter. Is that right?
- 6 customer: YEP! **[CONFIRM_ORDER]**

  - L1: 2 × bagel cinnamon_raisin add egg
  - L2: 3 × hot_chocolate medium
  - L3: 4 × croissant plain add butter
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0406: missing_info, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 2 orders of Onion Rings. Never says whether it's pickup or delivery. Pays cash. Asks a menu question partway through.
Card check: agrees

- 0 customer: Hi, I need to order 2 orders of onion rings, please. Working from home and in a rush. **[PLACE_ORDER]**
- 1 business: Hi! Sure, 2 orders of Onion Rings. Anything else with that?
- 2 customer: Quick question, do the onion rings come with any dipping sauce? **[MENU_QUESTION]**
- 3 business: They come plain, no dipping sauce included. We do have ketchup and mustard if you want them on the side.
- 4 customer: Ok perfect, thanks. Just the 2 onion rings then. **[SMALL_TALK]**

  - L1: 2 × onion_rings
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0425: correction, deepseek-flash@none, morning-crumb
Card: First asks for 3 × Muffin (Blueberry) (plus anything else below), then changes the quantity to 2. Final order: 2 × Muffin (Blueberry). Will pick it up. Pays by card. Gives their name: June.
Card check: agrees

- 0 customer: hey! first time trying this place 😊 can I get 3 blueberry muffins? **[PLACE_ORDER]**
- 1 business: Hi! Welcome in 😊 Just to confirm — 3 blueberry muffins?
- 2 customer: actually make it 2 please! 🙏 name's June, I'll pick them up and pay by card **[MODIFY_ORDER]**

  - L1: 2 × muffin blueberry
  - fulfillment pickup, address not_applicable, payment card, name June, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0454: unclear_message, claude-haiku-5-5@off-low, morning-crumb
Card: Sends a message too unclear to tell what they want (a fragment, a garbled word, a message meant for someone else). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: ok one sec 🎮 gg almost got him.. get me two of the uh bag- ppl hd tur zz 😂 **[PLACE_ORDER]**

  - L1: 2 × bagel
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_variant/missing, fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0458: combo, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Orders: 1 × Coffee & Pastry, drink: Latte, pastry: Croissant. Picks every combo choice. Will pick it up. Pays cash. Gives their name: Luis. Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: hey u guys open rn? wanna order a coffee & pastry combo, can i get a latte w the croissant? name is luis **[PLACE_ORDER + DELIVERY_QUESTION]**
- 1 business: Hi Luis! Yes we are open. I have your order down for a Coffee & Pastry combo with a Latte and a Croissant. Did you have a preference for the type of croissant?
- 2 customer: oh shoot my bad i meant the plain croissant pls thx **[PLACE_ORDER]**

  - L1: 1 × coffee_pastry_combo   drink=latte, pastry=croissant
  - fulfillment unknown, address not_mentioned, payment unknown, name luis, decision pending
  - missing: combo_choice/missing, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0460: missing_info, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 1 × BBQ Chicken Pizza (Medium 12-inch), no House cheese blend, add Thick crust; 1 × Meat Lovers Pizza (Personal 8-inch), add Onions; 2 × Coke (Can 12 oz). Chooses delivery but never gives an address. Never says whether it's pickup or delivery. Pays cash. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: hey! looking to get some food for the team. **[PLACE_ORDER]**
- 1 business: Hi there! What can I get for you today?
- 2 customer: okay so **[UNKNOWN]**
- 3 customer: a medium bbq chicken pizza **[PLACE_ORDER]**
- 4 customer: no house cheese blend though **[MODIFY_ORDER]**
- 5 customer: and add thick crust **[MODIFY_ORDER]**
- 6 customer: plus a personal meat lovers pizza **[PLACE_ORDER]**
- 7 customer: with onions **[MODIFY_ORDER]**
- 8 customer: and 2 cans of coke **[PLACE_ORDER]**
- 9 business: Got it. So that is one medium BBQ chicken pizza with no house cheese blend and thick crust, one personal meat lovers pizza with onions, and two 12 oz cans of Coke. Is that everything?
- 10 customer: yep! for delivery **[CONFIRM_ORDER + PLACE_ORDER]**
- 11 customer: paying cash **[PLACE_ORDER]**
- 12 customer: need it by 6:30 please **[PLACE_ORDER]**

  - L1: 1 × bbq_chicken_pizza medium remove cheese, add crust_thick
  - L2: 1 × meat_lovers_pizza personal add onions
  - L3: 2 × coke can
  - fulfillment delivery, address not_mentioned, payment cash, name –, decision pending
  - missing: address/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0490: delivery_question, deepseek-flash@none, corner-patty
Card: Only asks about delivery or pickup (delivery area, fee, how long it takes, opening hours). Does not order.
Card check: agrees

- 0 customer: hey, rough morning lol 🥴 do u guys deliver? **[DELIVERY_QUESTION + SMALL_TALK]**
- 1 business: Hey! 😄 We do deliver — what area are you in?
- 2 customer: im near the park on 5th ave. whats the fee and how long does it take? also what time do u close? **[DELIVERY_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

