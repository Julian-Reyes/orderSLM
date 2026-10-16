# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-p3-0003: payment_claim, deepseek-flash@none, corner-patty
Card: Says they already paid for an earlier order (on the phone, online or in the app) and asks whether it went through. Does not order anything new.
Card check: labels (expected labels not found: PAYMENT_CLAIM)

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: i ordered like 20 min ago over the phone **[ORDER_STATUS]**
- 2 customer: did it go thru? **[ORDER_STATUS]**
- 3 business: Hey! What name was the order under?
- 4 customer: sam **[ORDER_STATUS]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0008: off_menu, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Orders: 1 × Muffin (Banana nut); 1 × a smoothie (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Will pick it up. Never says how they'll pay. Gives their name: Tara.
Card check: items

- 0 customer: Hey **[SMALL_TALK]**
- 1 customer: Need a few things for my team **[SMALL_TALK]**
- 2 customer: Can I get 1 banana nut muffin **[PLACE_ORDER]**
- 3 customer: And 1 smoothie? **[PLACE_ORDER]**
- 4 business: Hi! We have the banana nut muffin ready for you, Tara. Sorry, but we don't have smoothies on the menu.
- 5 customer: Oh really? Okay just the muffin then please **[MODIFY_ORDER]**

  - L1: 1 × muffin banana_nut
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0035: ambiguous_reference, deepseek-flash@none, morning-crumb
Card: Refers to the first item vaguely at first ('that thing from before'); the business asks which one, and the customer names it. Final order: 1 × Latte (Medium 12 oz), add Hazelnut syrup; 1 × Drip Coffee (no size mentioned by anyone: the regular one); 1 × Croissant (no size mentioned by anyone: the regular one). Will pick it up. Pays by card. Gives their name: Maya. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: heyyy can i get that thing from before 😅 **[PLACE_ORDER]**
- 1 business: Hi! Which item was that? 😊
- 2 customer: the latte! medium, w hazelnut syrup pls. also a drip coffee and a croissant 🙏 **[PLACE_ORDER]**
- 3 business: Got it: 1 medium latte with hazelnut syrup, 1 drip coffee, 1 croissant. Pickup today?
- 4 customer: yess, name's Maya, i'll pick it up at 6:30, payin by card 💳 **[PLACE_ORDER]**

  - L1: 1 × latte medium add hazelnut_syrup
  - L2: 1 × drip_coffee medium
  - L3: 1 × croissant plain
  - fulfillment pickup, address not_applicable, payment card, name Maya, decision pending
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

## syn-p3-0105: unclear_message, deepseek-flash@none, halfmoon-pizza
Card: Sends a message too unclear to tell what they want (a fragment, a garbled word, a message meant for someone else). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: u guys still open **[DELIVERY_QUESTION]**
- 1 business: yep open til 11! what can i get u?
- 2 customer: ok cool lemme chekc the menue rn **[SMALL_TALK]**
- 3 customer: wait nvm wrong chat lol that was 4 jess **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0113: payment_question, claude-haiku-5-5@off-low, corner-patty
Card: Only asks how they can pay (cash, card, an app). Does not order.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: lemme ask rn **[SMALL_TALK]**
- 2 customer: can i pay w cash or u only take card? or an app? **[PAYMENT_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0118: correction_after_confirmation, deepseek-flash@none, halfmoon-pizza
Card: First orders 1 × Cheese Pizza (Personal 8-inch), no House cheese blend, add Tomatoes (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 × Supreme Pizza (Small 10-inch), add Fresh mozzarella. Final order: 1 × Supreme Pizza (Small 10-inch), add Fresh mozzarella; 1 × Meat Lovers Pizza (Medium 12-inch), no Pepperoni, add Tomatoes. Will pick it up. Pays by card. Says when they want it: asap.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey first time ordering from u guys **[SMALL_TALK]**
- 1 customer: can i get 1 personal cheese pizza, no house cheese blend, add tomatoes pls **[PLACE_ORDER]**
- 2 business: hey welcome! just to read that back: 1 personal 8-inch cheese pizza, no house cheese blend, add tomatoes. that right?
- 3 customer: yep thats it... actually wait can u swap that for a small supreme instead, add fresh mozzarella **[MODIFY_ORDER]**
- 4 business: got it! so 1 small 10-inch supreme pizza with fresh mozzarella added. anything else?
- 5 customer: ya add 1 medium meat lovers, no pepperoni, add tomatoes **[PLACE_ORDER]**
- 6 business: perfect. thats 1 small supreme with fresh mozzarella and 1 medium meat lovers, no pepperoni, add tomatoes. how would u like that?
- 7 customer: gonna pick it up, payin by card, need it asap pls thx **[PLACE_ORDER]**

  - L1: 1 × supreme_pizza small add mozzarella
  - L2: 1 × meat_lovers_pizza medium remove pepperoni, add tomatoes
  - fulfillment pickup, address not_applicable, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0123: off_menu, deepseek-flash@none, corner-patty
Card: Orders: 1 × Cheeseburger (Single patty); 1 × Lemonade; 1 × chicken nuggets (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Never says whether it's pickup or delivery. Pays by card. Asks a menu question partway through.
Card check: items

- 0 customer: hey do u guys have chicken nuggets **[MENU_QUESTION]**
- 1 business: hey! not sure yet, let me check on that for u. anything else i can get started on?
- 2 customer: k lemme get a single cheeseburger and a lemonade pls **[PLACE_ORDER]**
- 3 business: got it! one single patty cheeseburger and a lemonade. just to make sure, is that everything so far?
- 4 customer: yea thats it thx **[CONFIRM_ORDER]**

  - L1: 1 × cheeseburger single
  - L2: 1 × lemonade
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0148: correction_after_confirmation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. First orders 4 × Diet Coke (Can 12 oz) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 3. Final order: 3 × Diet Coke (Can 12 oz). Will pick it up. Pays by card. Gives their name: Dev. Says when they want it: a relative time (like 'in 20 min').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey **[SMALL_TALK]**
- 1 business: Hi there! Welcome to Halfmoon Pizza, what can I get you?
- 2 customer: lemme get four diet coke cans pls **[PLACE_ORDER]**
- 3 business: Got it. Let me confirm: 4 x Diet Coke (Can 12 oz). Is that right?
- 4 customer: yea but wait make that three thx **[MODIFY_ORDER]**
- 5 business: No problem, 3 x Diet Coke (Can 12 oz). Anything else?
- 6 customer: nah thats it. im gonna pick it up, its dev, ready in like 20 min **[PLACE_ORDER + SMALL_TALK]**
- 7 business: Sounds good Dev, see you in about 20 min!
- 8 customer: k thx. paying w card when i get there **[PLACE_ORDER]**

  - L1: 3 × diet_coke can
  - fulfillment pickup, address not_applicable, payment card, name Dev, decision pending
  - missing: nothing

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

## syn-p3-0236: menu_question, gemini-3.1-flash-lite@minimal, corner-patty
Card: Only asks one or two questions about the menu (what comes on something, sizes, what's good, whether they have something). Does not order.
Card check: items

- 0 business: Hi there! Welcome to Corner Patty. How can we help you today?
- 1 customer: hey **[SMALL_TALK]**
- 2 customer: my head is pounding **[SMALL_TALK]**
- 3 customer: do you guys have milkshakes? **[MENU_QUESTION]**
- 4 business: We sure do! We have vanilla, chocolate, and strawberry.
- 5 customer: cool **[SMALL_TALK]**
- 6 customer: and the veggie burger **[PLACE_ORDER]**
- 7 customer: what comes on that? **[MENU_QUESTION]**

  - L1: 1 × veggie_burger
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

## syn-p3-0292: correction_after_confirmation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. First orders 2 × Hawaiian Pizza (Medium 12-inch) (plus anything else below). The business reads the order back (no prices); the customer confirms, then changes the quantity to 1. Final order: 1 × Hawaiian Pizza (Medium 12-inch); 1 × Sprite (Can 12 oz). Wants delivery to 57 Hawthorne Rd (written the way the customer would type it). Pays cash.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey hows it going **[SMALL_TALK]**
- 1 business: Hi there! Welcome to Halfmoon Pizza. What can I get started for you?
- 2 customer: lemme get 2 hawaiian pizzas medium 12 inch pls **[PLACE_ORDER]**
- 3 business: Got it: 2 Hawaiian Pizza, Medium 12-inch. Is that everything?
- 4 customer: wait actually just 1 hawaiian. and a sprite can pls **[MODIFY_ORDER]**
- 5 business: No problem. So that's 1 Hawaiian Pizza, Medium 12-inch, and 1 Sprite, 12 oz can. Anything else?
- 6 customer: nah thats it thx. delivery to 57 hawthorne rd. paying cash **[PLACE_ORDER]**

  - L1: 1 × hawaiian_pizza medium
  - L2: 1 × sprite can
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0309: combo, gemini-3.1-flash-lite@minimal, corner-patty
Card: Orders: 1 × Cheeseburger Combo, side: Onion Rings, drink: Coke; 2 × Cheeseburger (Double patty). Picks every combo choice. Wants delivery to 5107 Orchard St (written the way the customer would type it). Pays cash. Asks a menu question partway through.
Card check: agrees

- 0 customer: yo, tryin u guys out for the first time. can i get a cheeseburger combo w onion rings and a coke? also what kind of burgers u have? **[PLACE_ORDER + MENU_QUESTION]**
- 1 business: hey there! welcome. we have cheeseburgers, bacon burgers, and veggie burgers.
- 2 customer: k cool, add two double patty cheeseburgers to that order too pls. delivering to 5107 orchard st and paying cash thx **[PLACE_ORDER]**

  - L1: 1 × cheeseburger_combo   side=onion_rings, drink=coke
  - L2: 2 × cheeseburger double
  - fulfillment delivery, address provided, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0313: cancellation, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 4 × Lemonade; 1 × Veggie Burger. Then cancels the whole order before it is placed (the last customer message is the cancellation). Wants delivery to 612 Magnolia Blvd, # 23 (written the way the customer would type it). Never says how they'll pay.
Card check: agrees

- 0 customer: hi **[SMALL_TALK]**
- 1 customer: can i get **[PLACE_ORDER]**
- 2 customer: four lemonades **[PLACE_ORDER]**
- 3 business: Hi! Sure, 4 lemonades. Anything else?
- 4 customer: and a veggie burger **[PLACE_ORDER]**
- 5 customer: one **[PLACE_ORDER]**
- 6 business: Got it: 4 Lemonade and 1 Veggie Burger. Would you like delivery or pickup?
- 7 customer: delivery **[PLACE_ORDER]**
- 8 customer: 612 magnolia blvd # 23 **[PLACE_ORDER]**
- 9 business: Thanks! Let me know when you're ready to confirm.
- 10 customer: actually nvm cancel the whole thing **[CANCEL_ORDER]**
- 11 customer: sorry **[SMALL_TALK]**

  - L1: 4 × lemonade
  - L2: 1 × veggie_burger
  - fulfillment delivery, address provided, payment unknown, name –, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0402: cancellation, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Cappuccino (Large 16 oz), Almond milk instead of Whole milk; 1 × Breakfast Sandwich (On a bagel), add Avocado. Then cancels the whole order before it is placed (the last customer message is the cancellation). Will pick it up. Pays by card. Gives their name: Ana.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: usual-ish **[PLACE_ORDER]**
- 2 customer: a large cappuccino **[PLACE_ORDER]**
- 3 customer: almond milk not whole **[PLACE_ORDER]**
- 4 business: Hi! Got it, large cappuccino with almond milk. Anything else?
- 5 customer: yes **[SMALL_TALK]**
- 6 customer: one breakfast sandwich **[PLACE_ORDER]**
- 7 customer: on a bagel **[PLACE_ORDER]**
- 8 customer: add avocado pls **[PLACE_ORDER]**
- 9 business: Sure, breakfast sandwich on a bagel with avocado. Want me to read back the whole order?
- 10 customer: nah wait **[SMALL_TALK]**
- 11 customer: cancel it all **[CANCEL_ORDER]**
- 12 customer: sorry, ana btw **[PLACE_ORDER]**

  - L1: 1 × cappuccino large substitute whole_milk→almond_milk
  - L2: 1 × breakfast_sandwich bagel add avocado
  - fulfillment unknown, address not_mentioned, payment unknown, name Ana, decision cancelled
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0420: off_menu, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 1 order of Breadsticks (4 pieces each); 1 × cannoli (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Wants delivery to 63 Lakeview Ln (written the way the customer would type it). Pays cash. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey can i get some breadsticks and a cannoli pls? to 63 lakeview ln in like 20 mins **[PLACE_ORDER]**

  - L1: 1 × breadsticks
  - L2: 1 × off-menu 'cannoli'
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, payment_method/missing

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

## syn-p3-0427: multi_message_order, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 2 × Drip Coffee (no size mentioned by anyone: the regular one). Will pick it up. Pays cash. Gives their name: Ben.
Card check: agrees

- 0 customer: hey good moring **[SMALL_TALK]**
- 1 business: hey there! what can i get started for you?
- 2 customer: lemme get two drip coffees pls **[PLACE_ORDER]**
- 3 business: got it, two drip coffees! anything else?
- 4 customer: nope thats it thx **[SMALL_TALK]**
- 5 business: sounds good! will that be for pickup?
- 6 customer: ya ill come pick it up rn **[PLACE_ORDER]**
- 7 business: perfect, paying when you get here i assume?
- 8 customer: yea cash pls **[PLACE_ORDER]**
- 9 business: you got it! what name should i put on the order?
- 10 customer: its ben **[PLACE_ORDER]**

  - L1: 2 × drip_coffee medium
  - fulfillment pickup, address not_applicable, payment cash, name Ben, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0434: off_menu, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 2 × Dr Pepper (Bottle 20 oz); 1 × Meat Lovers Pizza (Large 14-inch), no Ground beef, add Olive oil; 1 × a calzone (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Wants delivery to 12 Prospect St (written the way the customer would type it). Pays by card. Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: hey! 😊 hope ur having a good day **[SMALL_TALK]**
- 1 business: Hi there! Thanks for reaching out 🍕 What can I get started for you?
- 2 customer: ok so lemme get 2 dr peppers, the 20 oz bottles pls 🥤🥤 and a large meat lovers, but no ground beef on it, and can u add olive oil to the pizza? thx!! **[PLACE_ORDER]**
- 3 business: Got it: 2 Dr Pepper (20 oz bottles) and a Large 14-inch Meat Lovers with no ground beef and olive oil added. Anything else?
- 4 customer: yes!! also can i get a calzone rn 🙏 i always get the calzone w my pizza lol **[PLACE_ORDER]**

  - L1: 2 × dr_pepper bottle_20oz
  - L2: 1 × meat_lovers_pizza large remove beef, add olive_oil
  - L3: 1 × off-menu 'calzone'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/off_menu, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0436: payment_claim, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Says they already paid for an earlier order (on the phone, online or in the app) and asks whether it went through. Does not order anything new.
Card check: labels (expected labels not found: PAYMENT_CLAIM)

- 0 customer: hey i just put in an order for a coffee and sandwich online earlier, just wanted to check if u guys got it and if it went through ok? **[ORDER_STATUS]**
- 1 business: Hi there! Yes, we have received your order for the coffee and breakfast sandwich. We are working on it now!
- 2 customer: sweet thx sm, just finished an exam so i rly need that coffee rn **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0438: multi_message_order, deepseek-flash@none, corner-patty
Card: Builds the order over several messages, a thing or two at a time: 1 × Cheeseburger (no size mentioned by anyone: the regular one). Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: yo can i get a cheeseburger rn **[PLACE_ORDER]**
- 1 business: Hey! Sure thing, one Cheeseburger. Anything else?
- 2 customer: nah just the burger **[PLACE_ORDER]**
- 3 business: Got it — one Cheeseburger. Pickup or delivery?
- 4 customer: ill come grab it **[PLACE_ORDER]**
- 5 business: Perfect. When do you want it ready?
- 6 customer: in like 20 min pls **[PLACE_ORDER]**
- 7 business: Cool, we'll have it ready. Paying by card or cash?
- 8 customer: cash and can u break a 50? need change **[PLACE_ORDER]**
- 9 business: Yep, no problem. See you in 20!
- 10 customer: thx **[SMALL_TALK]**

  - L1: 1 × cheeseburger single
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0446: contextual_yes, deepseek-flash@none, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 1 order of Breadsticks (4 pieces each). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Wants delivery to 1104 Magnolia Blvd (side entrance) (written the way the customer would type it). Pays by card. Says when they want it: a clock time (like 'at 6:30').
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: yo **[SMALL_TALK]**
- 1 customer: u guys open rn? **[DELIVERY_QUESTION]**
- 2 business: Hey! Yep, we're open till 11 👍 What can we get you?
- 3 customer: sweet **[SMALL_TALK]**
- 4 customer: lemme get an order of breadsticks pls **[PLACE_ORDER]**
- 5 customer: delivery to 1104 Magnolia Blvd, side entrance **[PLACE_ORDER]**
- 6 customer: gonna pay by card **[PLACE_ORDER]**
- 7 business: Got it — 1 order of Breadsticks (4 pieces each), delivery to 1104 Magnolia Blvd, side entrance, paying by card. Is that right?
- 8 customer: at 6:30 btw **[MODIFY_ORDER]**
- 9 business: 👍 Anything else?
- 10 customer: yep thats it **[SMALL_TALK]**

  - L1: 1 × breadsticks
  - fulfillment delivery, address provided, payment card, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0452: refund_request, deepseek-flash@none, corner-patty
Card: Got an earlier order (not in this chat) where the onion rings was missing, and asks for their money back.
Card check: agrees

- 0 customer: hey so i got an order from u guys earlier and the onion rings were missing **[ORDER_PROBLEM]**
- 1 business: Oh no, sorry about that! Can you tell me what name the order was under?
- 2 customer: it was under dana and yeah we kinda need that money back pls **[REFUND_REQUEST]**
- 3 business: Got it, Dana. I'll let the manager know about the missing onion rings and the refund.
- 4 customer: thx appreciate it **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0464: unclear_message, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Sends a message too unclear to tell what they want (a fragment, a garbled word, a message meant for someone else). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: u still open? **[DELIVERY_QUESTION]**
- 2 business: Hi! Yes, we are open until 3pm. How can I help you?
- 3 customer: wait **[SMALL_TALK]**
- 4 customer: nvm **[SMALL_TALK]**
- 5 customer: did u get the invite? pls send asap **[OUT_OF_SCOPE]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0467: multi_message_order, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Builds the order over several messages, a thing or two at a time: 3 × Supreme Pizza (Small 10-inch); 1 × Pepperoni Pizza (Medium 12-inch), no House cheese blend. Will pick it up. Pays by card. Gives their name: Maya. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: HEY WE NEED FOOD!! CAN WE GET 3 SMALL SUPREME PIZZAS PLEASE??? **[PLACE_ORDER]**
- 1 business: Hi! We can definitely get those 3 Small Supreme pizzas ready for you. Anything else?
- 2 customer: YES ADD A MEDIUM PEPPERONI PIZZA TO THAT!! BUT PLEASE NO HOUSE CHEESE BLEND ON THE PEPPERONI ONE!! **[PLACE_ORDER]**
- 3 business: Got it. So that is 3 Small Supreme pizzas and 1 Medium Pepperoni pizza without the house cheese blend. Is that right?
- 4 customer: YES THATS PERFECT!! WE WILL PICK IT UP AT 6:30!! WE ARE PAYING BY CARD!! MY NAME IS MAYA!! **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 3 × supreme_pizza small
  - L2: 1 × pepperoni_pizza medium remove cheese
  - fulfillment pickup, address not_applicable, payment card, name Maya, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0470: contextual_yes, gemini-3.1-flash-lite@minimal, corner-patty
Card: Orders: 2 × Sprite; 1 × Coke. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Wants delivery to 58 Willow Creek Rd (across from the park) (written the way the customer would type it). Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey! can i get 2 sprites and a coke? **[PLACE_ORDER]**
- 1 customer: need that delivered **[PLACE_ORDER]**
- 2 customer: to 58 willow creek rd, right across from the park **[PLACE_ORDER]**
- 3 customer: think you can get it here in like 20 min? **[PLACE_ORDER]**
- 4 business: Hey there! We can get that over to you. Just to confirm: 2 Sprites and 1 Coke for delivery to 58 Willow Creek Rd in 20 minutes. Does that look right?
- 5 customer: yep **[CONFIRM_ORDER]**

  - L1: 2 × sprite
  - L2: 1 × coke
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0483: menu_question, gemini-3.1-flash-lite@minimal, corner-patty
Card: Only asks one or two questions about the menu (what comes on something, sizes, what's good, whether they have something). Does not order.
Card check: agrees

- 0 business: Hi! Welcome to Corner Patty, how can we help you?
- 1 customer: hey! my friend is feeling super sick rn so i'm trying to grab them some food. what comes on the veggie burger by default? **[MENU_QUESTION]**
- 2 business: Hey there! The veggie burger comes with lettuce, tomato, onions, pickles, and mayo.
- 3 customer: gotcha, thanks so much! also do you guys have any milkshakes? just wondering what flavors u have 🥤 **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p3-0487: multi_message_order, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Builds the order over several messages, a thing or two at a time: 1 order of Breadsticks (4 pieces each). Wants delivery to 80 Franklin Way (written the way the customer would type it). Pays cash. Asks a menu question partway through.
Card check: agrees

- 0 customer: hi **[SMALL_TALK]**
- 1 business: Hi! Welcome to Halfmoon Pizza, what can I get started for you?
- 2 customer: lemme see **[SMALL_TALK]**
- 3 customer: u guys have breadsticks rn? **[MENU_QUESTION]**
- 4 business: Yes we do! Breadsticks are a side. Want one order?
- 5 customer: yea one order pls **[PLACE_ORDER]**
- 6 customer: how many pieces r in it **[MENU_QUESTION]**
- 7 business: Each order comes with 4 pieces.
- 8 customer: ok perfect **[SMALL_TALK]**
- 9 customer: delivery to 80 franklin way **[PLACE_ORDER]**
- 10 business: Got it, 80 Franklin Way. So 1 order of breadsticks, 4 pieces, delivered. Is that right?
- 11 customer: yep thx **[CONFIRM_ORDER]**
- 12 customer: paying cash **[PLACE_ORDER]**

  - L1: 1 × breadsticks
  - fulfillment delivery, address provided, payment cash, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

