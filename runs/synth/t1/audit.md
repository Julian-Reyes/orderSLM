# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t1-0001: ambiguous_reference, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Refers to the first item vaguely at first ('the one I always get'); the business asks which one, and the customer names it. Final order: 1 × Americano (Medium 12 oz), add Vanilla syrup; 2 × Croissant (the customer doesn't mention a size), add Butter; 4 × Hot Chocolate (the customer doesn't mention a size), add Vanilla syrup, Oat milk instead of Whole milk; 2 × Cappuccino (Large 16 oz). Will pick it up. Never says how they'll pay. Gives their name: Grace. Says when they want it: asap.
Card check: agrees

- 0 customer: hey morning! **[SMALL_TALK]**
- 1 business: Morning! What can we get started for you?
- 2 customer: lemme get the one I always get **[PLACE_ORDER]**
- 3 business: Which one is that? We've got a few regulars :)
- 4 customer: the americano! medium w vanilla syrup **[PLACE_ORDER]**
- 5 customer: also 2 croissants w butter pls **[PLACE_ORDER]**
- 6 customer: 4 hot chocolates, vanilla + oat milk instead of whole **[PLACE_ORDER]**
- 7 customer: and 2 lg cappuccinos **[PLACE_ORDER]**
- 8 business: Got it — 1 medium Americano with vanilla, 2 croissants with butter, 4 hot chocolates with vanilla and oat milk, 2 large cappuccinos. Name for the order?
- 9 customer: grace. gonna pick it up, need it asap pls thx **[PLACE_ORDER]**

  - L1: 1 × americano medium add vanilla_syrup
  - L2: 2 × croissant plain add butter
  - L3: 4 × hot_chocolate medium add vanilla_syrup, substitute whole_milk→oat_milk
  - L4: 2 × cappuccino large
  - fulfillment pickup, address not_applicable, payment unknown, name grace, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0002: unclear_message, deepseek-flash@none, morning-crumb
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items

- 0 customer: heyyy 😊 quick q — for the mtg tmrw can we do **[UNKNOWN]**
- 1 business: Hey! Happy to help 😊 What are you thinking of getting?
- 2 customer: sry pocket txt 😅 two lg lattes w oat n a cpl crsnts pls **[PLACE_ORDER]**

  - L1: 2 × latte large substitute whole_milk→oat_milk
  - L2: 2 × croissant plain
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0003: correction_after_confirmation, claude-haiku-5-5@off-low, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, adds 1 × Supreme Pizza (Personal 8-inch) (not asked for before). Anything they say about pickup or delivery, payment or their name comes before that change; nothing comes after it. Final order: 1 order of Breadsticks (4 pieces each); 1 × Supreme Pizza (Personal 8-inch). Never says whether it's pickup or delivery. Pays by card.
Card check: items

- 0 customer: HEY I JUST FINISHED MY EXAM AND I AM STARVING!!! **[SMALL_TALK]**
- 1 business: Congrats on finishing! What can we get started for you?
- 2 customer: I WANT ONE ORDER OF BREADSTICKS AND A PEPPERONI PIZZA, PERSONAL SIZE!!! **[PLACE_ORDER]**
- 3 business: Got it. Sure you want the personal 8-inch pepperoni? Anything else?
- 4 customer: YES THATS IT!!! OH WAIT NO I MEAN THAT'S GOOD!!! **[SMALL_TALK]**
- 5 business: Ok so that's one order of breadsticks (4 pieces each) and one personal 8-inch Pepperoni Pizza. Does that look right?
- 6 customer: YES PERFECT!!! CONFIRMED!!! **[CONFIRM_ORDER]**
- 7 customer: OH AND ADD ONE MORE PIZZA, A SUPREME, PERSONAL SIZE TOO!!! **[MODIFY_ORDER]**

  - L1: 1 × breadsticks
  - L2: 1 × pepperoni_pizza personal
  - L3: 1 × supreme_pizza personal
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0004: simple_order, deepseek-flash@none, corner-patty
Card: Orders: 1 × Coke. Wants delivery to 3306 Birch Ln (written the way the customer would type it). Pays by card. Says when they want it as a bare clock time with no am/pm: 'at 9' (meaning 21:00 today).
Card check: agrees

- 0 customer: hey! 😊 quick one — can u deliver a coke to 3306 birch ln pls? payin by card **[PLACE_ORDER]**
- 1 business: Hey! Sure thing — one Coke, delivery to 3306 Birch Ln, card on arrival. When would u like it?
- 2 customer: at 9 pls 🙏 thx so much! **[PLACE_ORDER]**
- 3 business: Got it — 1 Coke, delivery to 3306 Birch Ln, card, at 9. See u then! 😊
- 4 customer: perfect thx!! 😄 **[CONFIRM_ORDER]**

  - L1: 1 × coke
  - fulfillment delivery, address provided, payment card, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0005: correction, deepseek-flash@none, corner-patty
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, adds 1 × Milkshake (Vanilla) (not asked for before). Anything they say about pickup or delivery, payment or their name comes before that change; nothing comes after it. Final order: 1 × Veggie Burger; 1 order of Fries (the customer doesn't mention a size); 1 × Milkshake (Vanilla). Never says whether it's pickup or delivery. Pays by card. Says when they want it: a clock time (like 'at 6:30').
Card check: labels (expected labels not found: MODIFY_ORDER)

- 0 customer: yo u guys open rn **[DELIVERY_QUESTION]**
- 1 business: yep we're open till 10!
- 2 customer: cool lemme get a veggie burger and an order of fries pls **[PLACE_ORDER]**
- 3 business: got it - one veggie burger and one fries. anything else?
- 4 customer: nah thats it for now im payin by card and can i get it at 6:30 **[PLACE_ORDER + SMALL_TALK]**
- 5 business: sounds good, card at 6:30 it is. see ya then!
- 6 customer: oh wait also add a vanilla milkshake pls thx **[PLACE_ORDER]**

  - L1: 1 × veggie_burger
  - L2: 1 × fries regular
  - L3: 1 × milkshake vanilla
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0006: multi_message_order, deepseek-flash@none, morning-crumb
Card: Builds the order over several messages, a thing or two at a time: 2 × Americano (Large 16 oz); 1 × Muffin (Banana nut); 1 × Hot Chocolate (the customer doesn't mention a size). Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Marcus. Says when they want it as a bare clock time with no am/pm: 'at 1' (meaning 13:00 today).
Card check: agrees

- 0 customer: yo 👋 can I get 2 large americanos? **[PLACE_ORDER]**
- 1 business: Hey! Two large americanos, got it 😊 Anything else?
- 2 customer: yeah a banana nut muffin and a hot chocolate too 🙏 **[PLACE_ORDER]**
- 3 business: Got it — 2 large americanos, 1 banana nut muffin, 1 hot chocolate. What name for the order?
- 4 customer: Marcus! also I'll pay cash, can you break a 20? and I'll grab it at 1 🕐 **[PLACE_ORDER]**

  - L1: 2 × americano large
  - L2: 1 × muffin banana_nut
  - L3: 1 × hot_chocolate medium
  - fulfillment pickup, address not_applicable, payment cash, name Marcus, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0009: simple_order, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Latte (Small 8 oz). Will pick it up. Pays cash, and asks for change for a bill (a 20 or a 50). Gives their name: Keisha. Asks for honey on the Latte, as if the place has it (it isn't on the menu).
Card check: agrees

- 0 customer: hi can i get a latte pls **[PLACE_ORDER]**
- 1 business: Hi! Sure, what size would you like? We have small, medium, or large.
- 2 customer: small. also can u put honey in it? thx **[PLACE_ORDER]**
- 3 business: Sorry, we don't have honey. We do have vanilla, caramel, or hazelnut syrup if you'd like one of those.
- 4 customer: ok no worries. ill pick it up rn. i'll pay cash, do u have change for a 20 or a 50 lol **[PLACE_ORDER + PAYMENT_QUESTION]**

  - L1: 1 × latte small add honey
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: item_modification/off_menu, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0013: ambiguous_reference, gemini-3.1-flash-lite@minimal, corner-patty
Card: Refers to the first item vaguely at first ('same as last time'); the business asks which one, and the customer names it. Final order: 2 × Sprite; 1 × Lemonade; 2 × Bacon Burger, add Mustard; 2 × Veggie Burger, no Lettuce. Will pick it up. Pays cash. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey its me again can i get the usual pls **[PLACE_ORDER]**
- 1 business: hey! could you remind me what that was again?
- 2 customer: oops sorry yeah can i get two bacon burgers add mustard and two veggie burgers no lettuce also two sprite and one lemonade **[PLACE_ORDER]**
- 3 business: got it two bacon burgers with mustard two veggie burgers no lettuce two sprite and one lemonade. anything else?
- 4 customer: nah thats it gonna pick it up in 20 min and pay cash thx **[PLACE_ORDER + SMALL_TALK]**

  - L1: 2 × bacon_burger  add mustard
  - L2: 2 × veggie_burger  remove lettuce
  - L3: 2 × sprite
  - L4: 1 × lemonade
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0015: ambiguous_reference, claude-haiku-5-5@off-low, corner-patty
Card: Refers to the first item vaguely at first ('the one I always get'); the business asks which one, and the customer names it. Final order: 1 × Bacon Burger; 2 × Sprite; 1 order of Onion Rings; 1 × Coke; 2 × Milkshake (Vanilla). Wants delivery to 3643 Spruce Dr, # 2A (written the way the customer would type it). Never says how they'll pay.
Card check: agrees

- 0 customer: HEY!! I NEED FOOD FOR MY 2 KIDS AND ME!!! THE ONE I ALWAYS GET!! **[PLACE_ORDER]**
- 1 business: Hi there! Which one is your usual? We have a few burgers on the menu.
- 2 customer: THE BACON ONE!!! 1 BACON BURGER!!! AND THEN 2 SPRITE, 1 ORDER OF ONION RINGS, 1 COKE, AND 2 VANILLA MILKSHAKES!!! **[PLACE_ORDER]**
- 3 customer: DELIVER TO 3643 SPRUCE DR, # 2A PLEASE!!! **[PLACE_ORDER]**

  - L1: 1 × bacon_burger
  - L2: 2 × sprite
  - L3: 1 × onion_rings
  - L4: 1 × coke
  - L5: 2 × milkshake vanilla
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0017: correction, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, changes the Hawaiian Pizza from 2 to 1. Anything they say about pickup or delivery, payment or their name comes before that change; nothing comes after it. Final order: 1 × Hawaiian Pizza (Extra large 16-inch), add Mushrooms. Wants delivery to 84 Easton Dr, apt 4A (written the way the customer would type it). Pays by card.
Card check: agrees

- 0 customer: hey its mark the delivery driver can i get two extra large hawaiian pizzas with mushrooms for delivery to 84 easton dr apt 4a ill pay with card **[PLACE_ORDER]**
- 1 business: hey mark sure thing so that is two extra large hawaiian pizzas with mushrooms going to 84 easton dr apt 4a and you will be paying with card right
- 2 customer: yeah that sounds right actually sorry can you just make it one hawaiian pizza instead of two pls **[MODIFY_ORDER]**

  - L1: 1 × hawaiian_pizza extra_large add mushrooms
  - fulfillment delivery, address provided, payment card, name Mark, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0018: unclear_message, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: agrees

- 0 customer: HEY ARE U OPEN RN?!?!?! 11111111111111111111111111111111 **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes, we are open until 11pm. How can we help you?
- 2 customer: AGGGHHHHH KKKKKKKKKKKKKKKKKKKKKKKK XXXXXXXXXXXXXX999999999999999999 **[UNKNOWN]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0020: correction, claude-haiku-5-5@off-low, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. Then, in the very last customer message, changes the Hawaiian Pizza from 3 to 2. Anything they say about pickup or delivery, payment or their name comes before that change; nothing comes after it. Final order: 2 × Hawaiian Pizza (Medium 12-inch), no House cheese blend, add Jalapeños. Will pick it up. Pays cash.
Card check: agrees

- 0 customer: Hi, it's pretty late but are you still taking orders? **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes, we're open until 11. What can I get you?
- 2 customer: I'd like 3 Hawaiian Pizzas, Medium 12-inch, with no House cheese blend and add jalapeños. I'll pick it up. I'm paying cash. **[PLACE_ORDER]**
- 3 business: Got it. 3 Hawaiian Pizzas, Medium 12-inch, no House cheese blend, jalapeños added, pickup, cash. Anything else?
- 4 customer: Actually, make that 2 Hawaiian Pizzas, same everything else. Thanks! **[MODIFY_ORDER]**

  - L1: 2 × hawaiian_pizza medium remove cheese, add jalapenos
  - fulfillment pickup, address not_applicable, payment cash, name –, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0027: simple_order, gemini-3.1-flash-lite@minimal, halfmoon-pizza
Card: Orders: 3 × Hawaiian Pizza (Medium 12-inch); 1 × Hawaiian Pizza (Medium 12-inch), no Ham; 3 × Coke (the customer doesn't mention a size). Wants delivery to 7076 Cedar Hill Terrace (written the way the customer would type it). Pays by card. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: agrees

- 0 customer: hey! just finished my last exam **[SMALL_TALK]**
- 1 customer: can i get 4 medium hawaiian pizzas **[PLACE_ORDER]**
- 2 customer: but one of them with no ham pls **[PLACE_ORDER]**
- 3 customer: and 3 cokes **[PLACE_ORDER]**
- 4 business: Hey there! Congrats on finishing your exam. Just to confirm: 3 medium Hawaiian pizzas, 1 medium Hawaiian pizza with no ham, and 3 Cokes. Is that all?
- 5 customer: yep thats it! sending to 7076 cedar hill terrace. paying w card thx **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 3 × hawaiian_pizza medium
  - L2: 1 × hawaiian_pizza medium remove ham
  - L3: 3 × coke can
  - fulfillment delivery, address provided, payment card, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t1-0028: unclear_message, claude-haiku-5-5@off-low, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 business: Hi there! Welcome to Corner Patty. What can I get started for you?
- 2 customer: ok so the **[UNKNOWN]**
- 3 customer: tkn bgr w/ jal **[UNKNOWN]**
- 4 customer: lol sorry thumbs **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

