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

## syn-b1-0099: small_talk, deepseek-flash@none, halfmoon-pizza
Card: Only greets, thanks the business or chats briefly. No request.
Card check: agrees

- 0 customer: hey! **[SMALL_TALK]**
- 1 business: Hi there! How can we help you today?
- 2 customer: just wanted to say we love ur spot **[SMALL_TALK]**
- 3 customer: ordering for the shop next week for sure **[SMALL_TALK]**
- 4 customer: thx! **[SMALL_TALK]**

  - no order

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

## syn-b1-0279: missing_info, deepseek-flash@none, morning-crumb
Card: Orders: 1 × Bagel (Everything), add Tomato; 1 × Croissant (Almond). Never says whether it's pickup or delivery. Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: u got bagels rn **[MENU_QUESTION]**
- 2 business: hey! yes we do — plain, everything, sesame, cinnamon raisin
- 3 customer: cool lemme get one everything bagel w tomato pls **[PLACE_ORDER]**
- 4 customer: and a almond croissant **[PLACE_ORDER]**
- 5 customer: gonna swing by in 20 min thx **[PLACE_ORDER]**

  - L1: 1 × bagel everything add tomato
  - L2: 1 × croissant almond
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing, customer_name/missing

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

## syn-b1-0334: unclear_message, deepseek-flash@none, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: hey r u open rn **[DELIVERY_QUESTION]**
- 1 business: we are! open till 10 tonight. what can i get started for you?
- 2 customer: yea can i get a chzburger no oninon and a lrg fryy pls thx **[PLACE_ORDER]**

  - L1: 1 × cheeseburger single remove onion
  - L2: 1 × fries large
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0356: correction_after_confirmation, deepseek-flash@none, morning-crumb
Card: First orders 2 × Cappuccino (Medium 12 oz), Almond milk instead of Whole milk (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 2 × Latte (Small 8 oz), add Whipped cream. Final order: 2 × Latte (Small 8 oz), add Whipped cream; 2 × Americano (Medium 12 oz). Will pick it up. Never says how they'll pay. Gives their name: Leah.
Card check: items

- 0 customer: HEY! NEED COFFEE FOR MY SICK FRIEND ASAP!! **[PLACE_ORDER]**
- 1 business: Hey! Happy to help — what can we get started for you?
- 2 customer: 2 MEDIUM CAPPUCCINOS!!! ALMOND MILK INSTEAD OF WHOLE!! **[PLACE_ORDER]**
- 3 business: Got it: 2 Medium 12 oz Cappuccinos with almond milk instead of whole milk. Did I get that right?
- 4 customer: YES PERFECT!! **[CONFIRM_ORDER]**
- 5 customer: WAIT NO!! CHANGE THAT TO 2 SMALL LATTES WITH WHIPPED CREAM!! **[MODIFY_ORDER]**
- 6 business: No problem — 2 Small 8 oz Lattes with whipped cream. Anything else?
- 7 customer: YES 2 MEDIUM AMERICANOS TOO!! AND ITS PICKUP!! **[PLACE_ORDER]**
- 8 business: You got it! So that's 2 Small Lattes with whipped cream and 2 Medium Americanos, for pickup. Can I get a name for the order?
- 9 customer: LEAH!! THANK YOU SO MUCH!!! **[PLACE_ORDER]**

  - L1: 1 × drip_coffee medium
  - L2: 2 × latte small add whipped_cream
  - L3: 2 × americano medium
  - fulfillment pickup, address not_applicable, payment unknown, name Leah, decision pending
  - missing: payment_method/missing

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

## syn-b1-0461: combo, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Coffee & Pastry, drink: Drip Coffee, pastry: Croissant. Picks every combo choice. Never says whether it's pickup or delivery. Pays by card.
Card check: agrees

- 0 customer: hey lemme get a coffee and pastry combo pls **[PLACE_ORDER]**
- 1 business: Hi! Sure, which drink would you like with it? Drip Coffee, Latte, or Americano?
- 2 customer: drip coffee thx and the croissant **[PLACE_ORDER]**
- 3 business: Got it: Coffee & Pastry combo with Drip Coffee and a Croissant. Would you like plain, chocolate, or almond croissant?
- 4 customer: plain pls **[PLACE_ORDER]**

  - L1: 1 × coffee_pastry_combo   drink=drip_coffee, pastry=croissant
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

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

## syn-b1-0700: refund_request, claude-haiku-5-5@off-low, morning-crumb
Card: Got an earlier order (not in this chat) where the americano was missing, and asks for their money back.
Card check: agrees

- 0 customer: hey 👋 small biz owner here, ordering for my shop. got an order earlier today and the americano was missing 😩 can i get a refund for it pls? 🙏 **[ORDER_PROBLEM + REFUND_REQUEST]**
- 1 business: Hi there! Sorry about that 😕 Can you tell me the name the order was under, or the time you picked it up?
- 2 customer: order was under Lin, around 10am 👍 thanks so much! 😊 **[REFUND_REQUEST]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0801: unclear_message, deepseek-flash@none, morning-crumb
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: yo my usual pls i cant even rn **[PLACE_ORDER]**
- 1 customer: wait wut **[SMALL_TALK]**

  - L1: 1 × off-menu 'my usual'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0892: unclear_message, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: Hey there! 👋 Need to grab some stuff for the kiddos. **[SMALL_TALK]**
- 1 business: Hi! We're ready when you are. What can we get for you today?
- 2 customer: Oh geez, so srry my pocket went crazy there for a sec! 😅😅 I think I hit like 8000 buttons. **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-0900: contextual_yes, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 2 × Breakfast Sandwich (On a bagel). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Jordan.
Card check: agrees

- 0 customer: hey u guys still doing breakfast sandwiches rn **[MENU_QUESTION]**
- 1 business: Hi! Yes we are, until 3pm. What can I get started for you?
- 2 customer: lemme get 2 breakfast sandwiches on a bagel pls **[PLACE_ORDER]**
- 3 business: Got it, 2 Breakfast Sandwiches on a bagel. Is that right?
- 4 customer: yep thx **[CONFIRM_ORDER]**

  - L1: 2 × breakfast_sandwich bagel
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

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

## syn-b1-1059: correction_after_confirmation, claude-haiku-5-5@off-low, morning-crumb
Card: Opens with a greeting before ordering. First orders 3 × Drip Coffee (Medium 12 oz), add Skim milk (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 × Muffin (Banana nut). Final order: 1 × Muffin (Banana nut); 1 × Cappuccino (Medium 12 oz). Will pick it up. Never says how they'll pay. Gives their name: Ivy. Asks a menu question partway through.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hiii good morning 😊 **[SMALL_TALK]**
- 1 business: Good morning! Welcome to Morning Crumb Café. What can I get started for you?
- 2 customer: can i get three drip coffees, medium pls ☕ **[PLACE_ORDER]**
- 3 business: Sure! Three medium drip coffees. Would you like any milk or syrup in them?
- 4 customer: yes skim milk in all of them thx **[PLACE_ORDER]**
- 5 business: Got it: 3 medium drip coffees with skim milk. Does that sound right?
- 6 customer: wait actually lemme change that. can u do a cappuccino medium instead of the coffees? and a banana nut muffin 🙏 **[MODIFY_ORDER + PLACE_ORDER]**
- 7 business: Of course! So that's 1 medium cappuccino and 1 banana nut muffin. Anything else?
- 8 customer: hmm do u guys have oat milk for the cappuccino? i'm lactose free rn **[MENU_QUESTION]**
- 9 business: Yes, we have oat milk. Want me to swap it in for the cappuccino?
- 10 customer: no its fine, the whole milk is ok 😅 just the cappuccino and the muffin thx **[PLACE_ORDER]**
- 11 business: No problem! 1 medium cappuccino and 1 banana nut muffin. Can I get a name for the order?
- 12 customer: ivy! im gonna pick it up in like 10 min 🏃‍♀️💨 **[PLACE_ORDER]**

  - L1: 1 × cappuccino medium
  - L2: 1 × muffin banana_nut
  - fulfillment pickup, address not_applicable, payment unknown, name Ivy, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1061: unclear_message, deepseek-flash@none, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: two kids starvin **[SMALL_TALK]**
- 2 customer: cn i get a burgr for the uhh **[PLACE_ORDER]**

  - L1: 1 × off-menu 'a burger'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1072: simple_order, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 2 × Bottled Water. Wants delivery to 1880 Franklin Ct (side entrance) (written the way the customer would type it). Pays by card. Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: Hi there! 😊 hope ur having a good day **[SMALL_TALK]**
- 1 business: Hi! Thanks for reaching out 🙂 What can I get started for you?
- 2 customer: lemme get 2 bottled water pls 💧 do u guys do delivery? also do u take card rn?? thx so much 🙏 1880 franklin ct, come to the side entrance pls **[PLACE_ORDER + DELIVERY_QUESTION]**

  - L1: 2 × water
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

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

## syn-b1-1209: unclear_message, claude-haiku-5-5@off-low, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items

- 0 customer: I would like the Cheeseburger with no onions and extra pickles, if that is possible, and also swap the **[PLACE_ORDER]**
- 1 customer: jalap bu the wrt **[UNKNOWN]**

  - L1: 1 × cheeseburger single remove onion, add pickle
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1217: contextual_yes, deepseek-flash@none, corner-patty
Card: Orders: 1 × Bacon Burger. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Never says how they'll pay. Says when they want it: a clock time (like 'at 6:30').
Card check: agrees

- 0 customer: hey u guys still open **[DELIVERY_QUESTION]**
- 1 business: yep we're open till 10! what can i get u
- 2 customer: can i get 1 bacon burger pls. pickin it up at 6:30 **[PLACE_ORDER]**
- 3 business: got it! so that's 1 Bacon Burger, pickup at 6:30. sound right?
- 4 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × bacon_burger
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1278: contextual_yes, deepseek-flash@none, corner-patty
Card: Orders: 1 × Veggie Burger, no Lettuce; 2 orders of Fries (Regular). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Never says whether it's pickup or delivery. Pays by card. Says when they want it: asap.
Card check: agrees

- 0 customer: hey are you guys open **[DELIVERY_QUESTION]**
- 1 business: we are! open till 10 tonight. what can we get started for you?
- 2 customer: one veggie burger **[PLACE_ORDER]**
- 3 customer: no lettuce tho **[PLACE_ORDER]**
- 4 customer: and two fries, regular **[PLACE_ORDER]**
- 5 customer: asap pls, got a baby in one arm lol **[PLACE_ORDER]**
- 6 business: got it — 1 Veggie Burger with no lettuce, and 2 regular Fries. is that right?
- 7 customer: yep **[CONFIRM_ORDER]**

  - L1: 1 × veggie_burger  remove lettuce
  - L2: 2 × fries regular
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1288: unclear_message, deepseek-flash@none, halfmoon-pizza
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: hey r u guys open rn i need like a couple of **[DELIVERY_QUESTION]**
- 1 customer: sry pocket txt lol **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1355: payment_claim, deepseek-flash@none, halfmoon-pizza
Card: Says outright that they already paid for an earlier order (e.g. 'I paid online', 'I sent the money on the app') and asks whether the payment went through. Does not order anything new.
Card check: agrees

- 0 customer: yo did my payment go thru? i paid online like 10 min ago for my earlier order **[PAYMENT_CLAIM]**
- 1 business: hey! can u send me the name on the order so i can check?
- 2 customer: its under samir k, pls lemme kno soon im in the middle of a match rn thx **[PAYMENT_CLAIM]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-b1-1419: half_and_half, claude-haiku-5-5@off-low, halfmoon-pizza
Card: Opens with a greeting before ordering. Orders: 1 × half-and-half pizza (Medium 12-inch): half Margherita Pizza, half Hawaiian Pizza. Wants delivery to 75 Harbor Rd, # 4 (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50). Asks a menu question partway through.
Card check: labels (expected labels not found: MENU_QUESTION)

- 0 customer: hey! 😊 hope ur having a good day **[SMALL_TALK]**
- 1 business: Hi there! Thanks for reaching out to Halfmoon Pizza. What can I get started for you?
- 2 customer: can i get a medium 12 inch half margherita half hawaiian 🍕🍍 my roommate & i are splitting it lol **[PLACE_ORDER]**
- 3 business: Got it, one medium 12-inch half Margherita, half Hawaiian. Is that for delivery or pickup?
- 4 customer: delivery pls 🛵 75 harbor rd # 4 **[PLACE_ORDER]**
- 5 customer: also do u guys take cash? 💵 we'd need change for a 20 or a 50 if so 😅 **[PAYMENT_QUESTION + PLACE_ORDER]**

  - L1: 1 × half margherita_pizza / half hawaiian_pizza medium
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

