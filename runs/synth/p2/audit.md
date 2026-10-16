# Audit sample

For each chat: the card, the chat, the teacher's finalized label, and the card check.

## syn-p2-0001: missing_info, gemini-3.1-flash-lite@minimal, corner-patty
Card: Orders: 1 × Coke; 3 orders of Onion Rings; 2 orders of Fries (Large). Will pick it up. Never says how they'll pay. Gives their name: Marcus.
Card check: agrees

- 0 customer: Hi, I just finished my exam and am looking to grab some food. Can I get one Coke, three orders of onion rings, and two large fries, please? My name is Marcus. **[PLACE_ORDER]**
- 1 business: Hey Marcus, congrats on finishing your exam! I have that down as one Coke, three orders of onion rings, and two large fries. Will you be picking that up?
- 2 customer: Yes, I will be picking that up. **[PLACE_ORDER]**

  - L1: 1 × coke
  - L2: 3 × onion_rings
  - L3: 2 × fries large
  - fulfillment pickup, address not_applicable, payment unknown, name Marcus, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0002: contextual_yes, deepseek-flash@none, halfmoon-pizza
Card: Orders: 2 × BBQ Chicken Pizza (Personal 8-inch). The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Wants delivery to 4722 Vine Blvd, unit 27B (written the way the customer would type it). Pays cash, and asks for change for a bill (a 20 or a 50). Asks a menu question partway through.
Card check: agrees

- 0 customer: hey! my buddy's sick rn and I wanna get him some pizza 🍕 can u help me out **[PLACE_ORDER]**
- 1 business: Hey! Of course, happy to help. What can I get for you?
- 2 customer: does the bbq chicken come in a personal size? he's not gonna eat a whole big one lol **[MENU_QUESTION]**
- 3 business: Yep, it does! Personal 8-inch.
- 4 customer: perfect, lemme get 2 of those pls. deliver to 4722 Vine Blvd unit 27B. payin cash and can u make change for a 20? **[PLACE_ORDER]**
- 5 business: Got it: 2 BBQ Chicken Pizzas, Personal 8-inch, delivered to 4722 Vine Blvd unit 27B, cash with change for a 20. Is that right?
- 6 customer: yep 👍 **[CONFIRM_ORDER]**

  - L1: 2 × bbq_chicken_pizza personal
  - fulfillment delivery, address provided, payment cash, name –, decision confirmed
  - missing: nothing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0003: order_problem, deepseek-flash@none, halfmoon-pizza
Card: Got an earlier order (not in this chat) with a problem: the iced tea was missing. Complains. Does not order anything new.
Card check: agrees

- 0 customer: yo my last order was missing the iced tea **[ORDER_PROBLEM]**
- 1 business: Oh no, sorry about that! Let me check on it for you.
- 2 customer: can u pls look it up rn **[ORDER_STATUS]**
- 3 customer: kind of in a hurry over here **[SMALL_TALK]**
- 4 business: Sure, what was the name on the order?
- 5 customer: it was the same name as always **[ORDER_STATUS]**
- 6 customer: thx, lemme know what u find **[ORDER_STATUS]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0004: two_requests, gemini-3.1-flash-lite@minimal, corner-patty
Card: Opens with a greeting before ordering. Orders: 2 × Sprite; 1 × Veggie Burger, add Mustard. In the same message as the first item, also asks a question about the menu. Will pick it up. Pays by card. Says when they want it: asap.
Card check: labels (expected labels not found: SMALL_TALK)

- 0 customer: hey! quick q before we order - do u guys have shakes? **[MENU_QUESTION]**
- 1 business: hi! yes we do, we have vanilla, chocolate, and strawberry milkshakes
- 2 customer: k cool thx! lemme get two sprites and one veggie burger with mustard pls. we want it asap! **[PLACE_ORDER]**

  - L1: 2 × sprite
  - L2: 1 × veggie_burger  add mustard
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0005: menu_question, deepseek-flash@none, corner-patty
Card: Only asks one or two questions about the menu (what comes on something, sizes, what's good, whether they have something). Does not order.
Card check: agrees

- 0 customer: hey do u guys have anything veggie rn **[MENU_QUESTION]**
- 1 business: we do! veggie burger, comes with lettuce tomato onions pickles and mayo
- 2 customer: oh nice whats good on it tho any add ons **[MENU_QUESTION]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0006: simple_order, deepseek-flash@none, halfmoon-pizza
Card: Orders: 1 × Meat Lovers Pizza (Personal 8-inch), no Bacon. Will pick it up. Never says how they'll pay.
Card check: agrees

- 0 customer: hey! 👋 my buddy is home sick and i wanna grab him something comforting **[SMALL_TALK]**
- 1 business: Hey! 😊 Happy to help. What can we get for him?
- 2 customer: one personal meat lovers please, but no bacon 🙏 **[PLACE_ORDER]**
- 3 business: Got it — one personal 8-inch Meat Lovers, no bacon. Anything else?
- 4 customer: that's it! i'll come pick it up 👍 **[PLACE_ORDER]**

  - L1: 1 × meat_lovers_pizza personal remove bacon
  - fulfillment pickup, address not_applicable, payment unknown, name –, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0007: contextual_yes, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Orders: 2 × Breakfast Sandwich (On an English muffin), no Cheddar; 1 × Hot Chocolate, no Whipped cream, add Vanilla syrup; 2 × Americano (Large 16 oz), add Caramel syrup, add Almond milk. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Will pick it up. Pays by card. Gives their name: Maya.
Card check: agrees

- 0 customer: Hey Morning Crumb! Maya here. Need to grab some fuel before my shift. Can I get 2 breakfast sandwiches on English muffins but please no cheddar? Also 1 hot chocolate with no whipped cream but add vanilla syrup. And 2 large Americanos with caramel syrup and almond milk pls! ☕️🥪 **[PLACE_ORDER]**
- 1 business: Hi Maya! Got that: 2 breakfast sandwiches on English muffins (no cheddar), 1 hot chocolate (no whipped cream, add vanilla), and 2 large Americanos (add caramel and almond milk). Does that look right?
- 2 customer: yep, that's it 👍 **[CONFIRM_ORDER]**

  - L1: 2 × breakfast_sandwich english_muffin remove cheddar
  - L2: 1 × hot_chocolate medium remove whipped_cream, add vanilla_syrup
  - L3: 2 × americano large add caramel_syrup, add almond_milk
  - fulfillment unknown, address not_mentioned, payment unknown, name Maya, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0008: human_request, deepseek-flash@none, morning-crumb
Card: Asks to talk to a person or the manager, with a short reason. Does not order.
Card check: agrees

- 0 customer: hey **[SMALL_TALK]**
- 1 customer: u guys got a manager around rn? **[HUMAN_REQUEST]**
- 2 business: Hey! Yes, our manager's in — what's going on?
- 3 customer: k lemme talk to them pls, order got messed up last time **[HUMAN_REQUEST]**

  - no order

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0009: correction_after_confirmation, claude-haiku-5-5@off-low, morning-crumb
Card: First orders 4 × Americano (Small 8 oz) (plus anything else below). The business reads the order back (no prices); the customer confirms, then swaps it for 1 × Americano (Small 8 oz), add Caramel syrup. Final order: 1 × Americano (Small 8 oz), add Caramel syrup; 1 × Latte (Small 8 oz), add Whipped cream; 1 × Hot Chocolate, no Whipped cream. Never says whether it's pickup or delivery. Never says how they'll pay.
Card check: labels (expected labels not found: CONFIRM_ORDER)

- 0 customer: hey!! lemme get 4 americanos small pls ☕️ **[PLACE_ORDER]**
- 1 business: Hi! Sure, 4 Americanos in small (8 oz). Is that everything?
- 2 customer: wait actually lol just kidding, changing that. just gonna do two americano smalls w caramel syrup **[MODIFY_ORDER]**
- 3 business: No problem! Let me read that back: 1 Americano small with caramel syrup. Is that right?
- 4 customer: omg no I meant ONE americano small w caramel syrup 😭 thx for checking **[MODIFY_ORDER]**
- 5 business: Got it, 1 Americano small with caramel syrup. Anything else?
- 6 customer: yes!! a latte small w whipped cream pls 🥹 **[PLACE_ORDER]**
- 7 customer: and a hot chocolate, no whipped cream on that one. u can skip the cream 🙏 **[PLACE_ORDER]**

  - L1: 1 × americano small add caramel_syrup
  - L2: 1 × latte small add whipped_cream
  - L3: 1 × hot_chocolate medium remove whipped_cream
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0010: multi_message_order, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. Builds the order over several messages, a thing or two at a time: 1 × Breakfast Sandwich, no Bacon, add Avocado. Will pick it up. Never says how they'll pay. Gives their name: Tara. Says when they want it: a relative time (like 'in 20 min').
Card check: item_details

- 0 customer: HEY THERE!!! MORNING CRUMB!!! **[SMALL_TALK]**
- 1 business: Hi! Welcome to Morning Crumb, what can I get for you today?
- 2 customer: I NEED A BREAKFAST SANDWICH PLEASE **[PLACE_ORDER]**
- 3 business: Sure thing! Would you like that on an English muffin, croissant, or bagel?
- 4 customer: ON A BAGEL PLS **[PLACE_ORDER]**
- 5 business: Got it. That comes with egg, cheddar, and bacon. Anything else?
- 6 customer: WAIT ACTUALLY NO BACON!! ADD AVOCADO TO IT THO **[MODIFY_ORDER]**
- 7 business: No problem, one bagel breakfast sandwich with egg, cheddar, and avocado, no bacon. Is that all?
- 8 customer: YES THATS IT!! ILL BE THERE IN 20 MIN. NAME IS TARA **[CONFIRM_ORDER + PLACE_ORDER]**

  - L1: 1 × breakfast_sandwich bagel remove bacon, add avocado
  - fulfillment pickup, address not_applicable, payment unknown, name TARA, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0013: off_menu, gemini-3.1-flash-lite@minimal, morning-crumb
Card: Opens with a greeting before ordering. Orders: 1 × Drip Coffee (Medium 12 oz), add Vanilla syrup; 1 × a fruit cup (not on the menu). The item marked 'not on the menu' is asked for as if the customer thinks they have it; the chat ends before the business answers about it. Will pick it up. Pays by card. Gives their name: Tara.
Card check: labels (expected labels not found: SMALL_TALK)

- 0 customer: hey morning crumb its tara ordering for a meeting today **[PLACE_ORDER]**
- 1 business: Hi Tara! What can I get started for you?
- 2 customer: can i get 1 medium drip coffee w vanilla syrup and also a fruit cup pls **[PLACE_ORDER]**

  - L1: 1 × drip_coffee medium add vanilla_syrup
  - L2: 1 × off-menu 'fruit cup'
  - fulfillment unknown, address not_mentioned, payment unknown, name Tara, decision pending
  - missing: item_menu_match/off_menu, fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0017: implicit_category, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 2 × Hot Chocolate; 1 × Cappuccino (Small 8 oz). Never uses category words: names items casually ('a coke', 'some fries') or with a synonym ('pop' for a soda), never 'a drink' or 'a side' alone. Never says whether it's pickup or delivery. Pays by card.
Card check: item_details

- 0 customer: hey lemme get two hot chocolate and a cappuccino small rn pls **[PLACE_ORDER]**
- 1 business: Sure! Hot chocolate in small, medium or large? And should the cappuccino be small too, or a different size?
- 2 customer: oh the cappuccino is small, and the hot chocolates r small too thx **[PLACE_ORDER]**

  - L1: 2 × hot_chocolate small
  - L2: 1 × cappuccino small
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing, customer_name/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0020: two_requests, claude-haiku-5-5@off-low, morning-crumb
Card: Orders: 1 × Drip Coffee (Large 16 oz), add Caramel syrup, add Almond milk; 1 × Cappuccino (Medium 12 oz); 1 × Hot Chocolate (Medium 12 oz), add Vanilla syrup, Oat milk instead of Whole milk. In the same message as the first item, also asks a question about the menu. Will pick it up. Pays by card. Gives their name: Leah.
Card check: agrees

- 0 customer: Hi there. I'd like one large drip coffee with caramel syrup and almond milk, please. Quick question first: does the cappuccino come with whole milk by default, or can I get it with skim? **[PLACE_ORDER + MENU_QUESTION]**
- 1 business: Hi! Yes, the cappuccino comes with whole milk, but you can swap in skim, oat, or almond for no extra fuss. Want a medium?
- 2 customer: Yes, a medium cappuccino, please. Then a couple of other things: one medium hot chocolate with vanilla syrup, and I'd like oat milk in it instead of whole milk. **[PLACE_ORDER]**
- 3 business: Got it. So: 1 large drip coffee with caramel syrup and almond milk, 1 medium cappuccino, and 1 medium hot chocolate with vanilla syrup and oat milk instead of whole milk. Is that everything?
- 4 customer: That's everything. I'll pick it up. My name is Leah. **[PLACE_ORDER]**

  - L1: 1 × drip_coffee large add caramel_syrup, add almond_milk
  - L2: 1 × cappuccino medium
  - L3: 1 × hot_chocolate medium add vanilla_syrup, substitute whole_milk→oat_milk
  - fulfillment pickup, address not_applicable, payment unknown, name Leah, decision pending
  - missing: payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0021: contextual_yes, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 1 × Veggie Burger, no Tomato. The business reads the order back (no prices) and asks if it's right; the customer's last message is only a short yes ('yep', 'that's it', a thumbs up). Never says whether it's pickup or delivery. Never says how they'll pay. Says when they want it: a relative time (like 'in 20 min').
Card check: agrees

- 0 customer: hey, do you guys take orders over text? **[UNKNOWN]**
- 1 business: Hi! Yes we do. What can I get you?
- 2 customer: I'd like a Veggie Burger, but can you please leave off the tomato. I'm mid match so I can't really step away lol **[PLACE_ORDER]**
- 3 business: No problem! So that's 1 Veggie Burger with no tomato. Is that right?
- 4 customer: yep that's it **[CONFIRM_ORDER]**

  - L1: 1 × veggie_burger  remove tomato
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

## syn-p2-0023: simple_order, claude-haiku-5-5@off-low, corner-patty
Card: Orders: 3 × Milkshake (Chocolate); 1 × Bacon Burger, no American cheese. Will pick it up. Never says how they'll pay. Asks a menu question partway through.
Card check: agrees

- 0 customer: hey u open rn **[DELIVERY_QUESTION]**
- 1 business: Hi! Yes, we're open till 10pm. What can I get you?
- 2 customer: lemme get 3 chocolate milkshakes pls **[PLACE_ORDER]**
- 3 business: Got it, 3 chocolate milkshakes. Anything else?
- 4 customer: wait does the bacon burger come w cheese **[MENU_QUESTION]**
- 5 business: It does, American cheese is included. We can take it off if you'd like.
- 6 customer: yea lemme get one bacon burger no cheese thx **[PLACE_ORDER]**
- 7 business: Okay so that's 3 chocolate milkshakes and 1 Bacon Burger with no American cheese. Sound right?
- 8 customer: yep thats it **[CONFIRM_ORDER]**

  - L1: 3 × milkshake chocolate
  - L2: 1 × bacon_burger  remove cheese
  - fulfillment unknown, address not_mentioned, payment unknown, name –, decision pending
  - missing: fulfillment_method/missing, payment_method/missing

Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:

