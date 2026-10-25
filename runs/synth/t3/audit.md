# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-t3-0062: simple_order, deepseek-flash@none, halfmoon-pizza
Card: Orders: 2 × Dr Pepper (the customer doesn't mention a size); 1 × Iced Tea (Bottle 20 oz); 1 × Bottled Water; 2 × Supreme Pizza (Personal 8-inch). Never says whether it's pickup or delivery. Pays by card. Says when they want it: asap. Asks for arugula on the Supreme Pizza, as if the place has it (it isn't on the menu).
Card check: agrees

- 0 customer: yo **[SMALL_TALK]**
- 1 business: Hey! What can I get for you?
- 2 customer: 2 dr peppers **[PLACE_ORDER]**
- 3 customer: and an iced tea **[PLACE_ORDER]**
- 4 business: Got it. What size on the iced tea?
- 5 customer: 20 oz bottle pls. and a water **[PLACE_ORDER]**
- 6 business: Okay! Anything to eat?
- 7 customer: 2 personal supremes **[PLACE_ORDER]**
- 8 customer: can u add arugula on those? **[PLACE_ORDER]**
- 9 business: We don't have arugula, sorry! Want anything else on them?
- 10 customer: nah thats it. payin by card **[PLACE_ORDER]**
- 11 business: Sounds good! So that's 2 Dr Peppers, a 20 oz iced tea, a water, and 2 personal Supremes. When do you want it?
- 12 customer: asap thx **[PLACE_ORDER]**

  - L1: 2 × dr_pepper can
  - L2: 1 × iced_tea bottle_20oz
  - L3: 1 × water
  - L4: 2 × supreme_pizza personal add arugula
  - fulfillment unknown, address not_mentioned, payment card, name –, decision pending
  - missing: item_modification/off_menu, fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0107: correction_after_confirmation, deepseek-flash@none, halfmoon-pizza
Card: First orders the items below, but with the earlier version of the changed one. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, changes the size of the Dr Pepper from Bottle 20 oz to Can 12 oz (like 'make it a can'). Their other details come before that change; nothing comes after it. Final order: 1 × Dr Pepper (Can 12 oz); 3 × Margherita Pizza (Small 10-inch), no Basil; 1 order of Breadsticks (4 pieces each). Will pick it up. Never says how they'll pay. Asks a menu question partway through.
Card check: agrees

- 0 customer: HEY! QUICK QUESTION BEFORE I ORDER **[SMALL_TALK]**
- 1 business: Hey! Go ahead, ask away
- 2 customer: DO THE BREADSTICKS COME WITH ANY DIP OR SAUCE?? **[MENU_QUESTION]**
- 3 business: They come on their own, no dip included. You can add sauces from the menu though
- 4 customer: OK COOL. SO I WANT 3 SMALL MARGHERITA PIZZAS, BUT NO BASIL ON ANY OF THEM! NONE!! **[PLACE_ORDER]**
- 5 business: Got it, 3 small Margheritas with no basil. Anything else?
- 6 customer: YES! ONE ORDER OF BREADSTICKS AND A 20 OZ BOTTLE OF DR PEPPER! PICKING IT UP MYSELF **[PLACE_ORDER]**
- 7 business: So that's 3 small Margherita pizzas with no basil, 1 order of breadsticks, and a 20 oz bottle of Dr Pepper, for pickup. Sound right?
- 8 customer: YEP THATS IT! **[CONFIRM_ORDER]**
- 9 customer: ACTUALLY MAKE THE DR PEPPER A CAN, NOT THE BOTTLE! **[MODIFY_ORDER]**

  - L1: 3 × margherita_pizza small remove basil
  - L2: 1 × breadsticks
  - L3: 1 × dr_pepper can
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0187: unclear_message, deepseek-flash@none, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: hey r u still open rn **[DELIVERY_QUESTION]**
- 1 business: Yep, open till 10! What can I get you?
- 2 customer: ok so im starving lol i forgot to eat all day and **[SMALL_TALK]**
- 3 business: Been there. Take your time, no rush.
- 4 customer: the burger with the thing and the not the other one pls thx **[PLACE_ORDER]**

  - L1: 1 × off-menu 'the burger'
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: item_menu_match/ambiguous, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0270: correction_after_confirmation, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. First orders the items below except the one added at the end. The business reads the order back (no prices) and the customer confirms. Then, in the very last customer message, adds 1 × Drip Coffee (the customer doesn't mention a size), add Hazelnut syrup (not asked for before). Their other details come before that change; nothing comes after it. Final order: 1 × Latte (Large 16 oz); 1 × Americano (Medium 12 oz), add Caramel syrup; 1 × Drip Coffee (the customer doesn't mention a size), add Hazelnut syrup. Will pick it up. Pays by card. Gives their name: Tom.
Card check: agrees

- 0 customer: hey good morning **[SMALL_TALK]**
- 1 business: morning! what can we get started for ya?
- 2 customer: ok so lemme get a large latte and a medium americano w caramel syrup pls **[PLACE_ORDER]**
- 3 business: got it: 1 large latte and 1 medium americano with caramel syrup. anything else?
- 4 customer: nope thats it for now thx. oh and name's tom, ill pick it up, paying by card **[PLACE_ORDER + SMALL_TALK]**
- 5 business: sounds good tom. so just to read it back: 1 large latte, 1 medium americano with caramel syrup, pickup, pay by card. look right?
- 6 customer: yep thats right **[CONFIRM_ORDER]**
- 7 customer: actually one more thing add a drip coffee w hazelnut syrup too pls **[MODIFY_ORDER]**

  - L1: 1 × latte large
  - L2: 1 × americano medium add caramel_syrup
  - L3: 1 × drip_coffee medium add hazelnut_syrup
  - fulfillment pickup, address not_applicable, payment card, name Tom, decision pending
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0333: unclear_message, deepseek-flash@none, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: labels (expected labels not found: UNKNOWN)

- 0 customer: heyy r u still open rn **[DELIVERY_QUESTION]**
- 1 business: yep, we're open til 10! what can i get u
- 2 customer: ok so like 2 burgrs one no onin n the other... wait lol my pocket typed that. hold on lemme lk at the menu n figre out **[SMALL_TALK]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0364: simple_order, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Orders: 2 × Hot Chocolate (Small 8 oz). Will pick it up. Pays cash. Gives their name: Luis. Says when they want it as a bare clock time with no am/pm: 'at 2' (meaning 14:00 today).
Card check: agrees

- 0 customer: hey good morning **[SMALL_TALK]**
- 1 business: morning! what can i get ya
- 2 customer: could u do 2 small hot chocolates pls **[PLACE_ORDER]**
- 3 business: 2 small hot chocolates got it. anything else?
- 4 customer: nope thats it thx. name's luis and im gonna pay cash at 2 **[CONFIRM_ORDER]**

  - L1: 2 × hot_chocolate small
  - fulfillment unknown, address not_mentioned, payment cash, name luis, decision pending
  - missing: fulfillment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0439: multi_message_order, deepseek-flash@none, morning-crumb
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 3 × Latte (Medium 12 oz); 3 × Hot Chocolate (the customer doesn't mention a size); 2 × Breakfast Sandwich (On a bagel); 1 × Americano (Large 16 oz), add Hazelnut syrup; 3 × Muffin (Banana nut). Will pick it up. Never says how they'll pay. Gives their name: Nico.
Card check: agrees

- 0 customer: Hello, good morning. **[SMALL_TALK]**
- 1 business: Good morning! What can I get started for you?
- 2 customer: I'm ordering for a few players after practice. Could I get three medium lattes to start? **[PLACE_ORDER]**
- 3 business: Three medium lattes, got it. Anything else?
- 4 customer: Yes, three hot chocolates as well. **[PLACE_ORDER]**
- 5 customer: And two breakfast sandwiches on bagels. **[PLACE_ORDER]**
- 6 business: Three hot chocolates and two breakfast sandwiches on bagels. Go on.
- 7 customer: One large americano with hazelnut syrup. **[PLACE_ORDER]**
- 8 customer: Lastly, three banana nut muffins. That should be everything. **[PLACE_ORDER]**
- 9 business: So that's three medium lattes, three hot chocolates, two breakfast sandwiches on bagels, one large americano with hazelnut, and three banana nut muffins. Can I get a name for the order?
- 10 customer: Nico. I'll pick it up. **[PLACE_ORDER]**

  - L1: 3 × latte medium
  - L2: 3 × hot_chocolate medium
  - L3: 2 × breakfast_sandwich bagel
  - L4: 1 × americano large add hazelnut_syrup
  - L5: 3 × muffin banana_nut
  - fulfillment pickup, address not_applicable, payment unknown, name Nico, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0441: simple_order, deepseek-flash@none, morning-crumb
Card: Orders: 4 × Cappuccino (Small 8 oz); 1 × Cappuccino (Small 8 oz), add Hazelnut syrup; 2 × Breakfast Sandwich (the customer doesn't mention a size); 1 × Americano (Medium 12 oz), add Caramel syrup, add Almond milk. Will pick it up. Never says how they'll pay. Gives their name: Priya. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: item_details

- 0 customer: hey can i get 5 small cappuccinos, 1 of em with hazelnut syrup **[PLACE_ORDER]**
- 1 business: hi! got it - 5 small cappuccinos, one with hazelnut syrup. anything else?
- 2 customer: yeah also 2 breakfast sandwiches and a medium americano w caramel and almond milk pls **[PLACE_ORDER]**
- 3 business: ok so that's 5 small cappuccinos (1 hazelnut), 2 breakfast sandwiches, and 1 medium americano with caramel and almond milk. can i get a name for the order?
- 4 customer: priya, and ill pick it up thx **[PLACE_ORDER]**

  - L1: 4 × cappuccino small
  - L2: 1 × cappuccino small add hazelnut_syrup
  - L3: 2 × breakfast_sandwich english_muffin
  - L4: 1 × americano medium add caramel_syrup, substitute whole_milk→almond_milk
  - fulfillment pickup, address not_applicable, payment unknown, name Priya, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0552: simple_order, deepseek-flash@none, corner-patty
Card: Orders: 1 × Veggie Burger; 5 × Veggie Burger, add American cheese; 1 × Cheeseburger (Single patty), no Pickles, add Avocado; 1 × Bacon Burger, no Bacon; 2 orders of Fries (the customer doesn't mention a size). Wants delivery to 30 Kensington Ln (written the way the customer would type it). Never says how they'll pay. The first two lines are the same item: says them as one request with a count and how many get the change (like '4 burgers, 2 of them no onions').
Card check: item_details

- 0 customer: yo need a big lunch order for the crew pls 🙏 **[SMALL_TALK]**
- 1 business: Hey! Happy to help — what can we get started for you?
- 2 customer: ok so six veggie burgers, five of em with american cheese and one plain. then a single cheeseburger no pickles add avocado, a bacon burger but no bacon lol, and two fries. deliver to 30 kensington ln thx!! 🍔🍟 **[PLACE_ORDER]**
- 3 business: Got it! Quick read-back: 6 Veggie Burgers — 5 with American cheese, 1 plain; 1 single Cheeseburger no pickles, add avocado; 1 Bacon Burger no bacon; 2 Fries. Delivering to 30 Kensington Ln. Sound right?
- 4 customer: yep thats it, thx! 👍 **[CONFIRM_ORDER]**

  - L1: 5 × veggie_burger  add cheese
  - L2: 1 × veggie_burger  remove lettuce, remove tomato, remove onion, remove pickle, remove mayo
  - L3: 1 × cheeseburger single remove pickle, add avocado
  - L4: 1 × bacon_burger  remove bacon
  - L5: 2 × fries regular
  - fulfillment delivery, address provided, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-t3-0578: unclear_message, deepseek-flash@none, corner-patty
Card: Sends one or two messages that can't be understood: a cut-off fragment, garbled words or a pocket-text. Not a clear 'wrong chat' or 'never mind' (those are understandable). Does not order.
Card check: items, labels (expected labels not found: UNKNOWN)

- 0 customer: hii sorry my kid grabbed the phone 😅 2 cheeseburg **[PLACE_ORDER]**

  - L1: 2 × cheeseburger single
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

