# M6 error review on fresh3

Every chat or customer message a model got wrong, from saved outputs. Fresh3 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v3 | qwen3.5-0.8b-single-v4 |
|---|---|---|
| chats not fully right (of 110) | 40 | 19 |
| · fields only | 23 | 4 |
| · invalid answer | 2 | 3 |
| · item mistakes | 14 | 11 |
| · items where there is no order | 1 | 1 |
| item: missing_item | 7 | 3 |
| item: wrong_modifications | 4 | 5 |
| item: extra_item | 5 | 3 |
| item: wrong_quantity | 2 | 2 |
| item: wrong_variant | 0 | 1 |
| field: address | 1 | 0 |
| field: method | 2 | 0 |
| field: missing | 11 | 5 |
| field: time | 23 | 3 |
| intents wrong (of 321) | 35 | 21 |

Overlap: {'chats_all_students_wrong': 17, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 25, 'messages_all_students_wrong': 15, 'messages_one_student_only': 26}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v3': 1}
- combo: {'qwen3.5-0.8b-single-v3': 1}
- correction: {'qwen3.5-0.8b-single-v3': 4, 'qwen3.5-0.8b-single-v4': 4}
- future_day: {'qwen3.5-0.8b-single-v3': 20, 'qwen3.5-0.8b-single-v4': 2}
- human_request: {'qwen3.5-0.8b-single-v3': 1, 'qwen3.5-0.8b-single-v4': 1}
- implicit_category: {'qwen3.5-0.8b-single-v3': 1, 'qwen3.5-0.8b-single-v4': 1}
- missing_info: {'qwen3.5-0.8b-single-v3': 3, 'qwen3.5-0.8b-single-v4': 3}
- multi_message_order: {'qwen3.5-0.8b-single-v3': 3, 'qwen3.5-0.8b-single-v4': 2}
- off_menu: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 2}
- simple_order: {'qwen3.5-0.8b-single-v3': 3, 'qwen3.5-0.8b-single-v4': 2}
- small_talk: {'qwen3.5-0.8b-single-v3': 3, 'qwen3.5-0.8b-single-v4': 3}
- two_requests: {'qwen3.5-0.8b-single-v4': 1}
- unclear_message: {'qwen3.5-0.8b-single-v3': 1, 'qwen3.5-0.8b-single-v4': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v3:** SMALL_TALK → UNKNOWN ×15; PLACE_ORDER → None ×4; PLACE_ORDER → MODIFY_ORDER ×3; SMALL_TALK → PLACE_ORDER ×2; DELIVERY_QUESTION → PLACE_ORDER ×2; ORDER_PROBLEM → ORDER_STATUS ×2; DELIVERY_QUESTION → SMALL_TALK ×1; UNKNOWN → SMALL_TALK ×1; PLACE_ORDER → ORDER_PROBLEM ×1; UNKNOWN → PLACE_ORDER ×1; MODIFY_ORDER → PLACE_ORDER ×1; OUT_OF_SCOPE → UNKNOWN ×1; PAYMENT_CLAIM → PLACE_ORDER ×1
- **qwen3.5-0.8b-single-v4:** DELIVERY_QUESTION → PLACE_ORDER ×3; PLACE_ORDER → None ×3; PLACE_ORDER → MODIFY_ORDER ×2; UNKNOWN → SMALL_TALK ×2; SMALL_TALK → PLACE_ORDER ×2; MODIFY_ORDER → None ×1; UNKNOWN → PLACE_ORDER ×1; SMALL_TALK → PAYMENT_CLAIM ×1; OUT_OF_SCOPE → UNKNOWN ×1; ORDER_PROBLEM → ORDER_STATUS ×1; ORDER_PROBLEM → MODIFY_ORDER ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; SMALL_TALK → UNKNOWN ×1; OUT_OF_SCOPE → HUMAN_REQUEST ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh3-001#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-001#5 | card | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER |
| a-fresh3-002#0 | hey do u guys take orders for tmrw | DELIVERY_QUESTION | qwen3.5-0.8b-single-v3: SMALL_TALK, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-003#2 | Yes please. For a little party: 2 large lattes, a medium hot chocolate, 3 chocolate croissants warmed, 2 blueberry muffi | PLACE_ORDER | qwen3.5-0.8b-single-v3: None, qwen3.5-0.8b-single-v4: None |
| a-fresh3-008#0 | hey quick q | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-010#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-014#0 | hiya | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-026#1 | but please leave the olives off two of them | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER, qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-030#2 | 🤔 | UNKNOWN | qwen3.5-0.8b-single-v3: SMALL_TALK, qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh3-033#1 | n that one u had on special last week | PLACE_ORDER | qwen3.5-0.8b-single-v3: ORDER_PROBLEM |
| a-fresh3-033#3 | deliver to 55 ivanhoe st | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER |
| a-fresh3-044#0 | HI! PARTY TOMORROW | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-045#0 | Hi there! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-051#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-051#3 | ok nvm the other one | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh3-053#0 | can i order now for friday? | DELIVERY_QUESTION | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-057#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-057#4 | ok add it | PLACE_ORDER | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-061#0 | hi | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-064#3 | actually make it 1:15 instead, meeting got pushed | MODIFY_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-067#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-069#0 | YO | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-075#1 | can i get a medium lat | UNKNOWN | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-076#3 | wait not tonight, sat at 7 | MODIFY_ORDER | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh3-079#0 | SETTLE A BET | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN, qwen3.5-0.8b-single-v4: PAYMENT_CLAIM |
| a-fresh3-079#1 | IS A HOT DOG A SANDWICH??? | OUT_OF_SCOPE | qwen3.5-0.8b-single-v3: UNKNOWN, qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh3-083#0 | WE JUST GOT OUR ORDER | ORDER_PROBLEM | qwen3.5-0.8b-single-v3: ORDER_STATUS, qwen3.5-0.8b-single-v4: ORDER_STATUS |
| a-fresh3-083#2 | HE'S ALLERGIC TO MUSTARD, I SAID NO MUSTARD | ORDER_PROBLEM | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-087#1 | w a drip coffee but large pls ☕ | PLACE_ORDER | qwen3.5-0.8b-single-v3: None, qwen3.5-0.8b-single-v4: None |
| a-fresh3-087#2 | n an almond croissant 🥐 | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh3-087#3 | pickup for sam | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh3-089#1 | i already paid thru the app 🙏 | PAYMENT_CLAIM | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-090#0 | hi 👋 we're arriving thursday nov 19, could we get 2 bacon burgers n 2 cokes delivered to the harbor inn, 400 front st, r | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-096#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-099#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-099#1 | just picked up my order n its a pepperoni, i ordered a veggie | ORDER_PROBLEM | qwen3.5-0.8b-single-v3: ORDER_STATUS |
| a-fresh3-100#0 | can i preorder for sunday? 🍕 | DELIVERY_QUESTION | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-101#0 | HI, FIRST TIME ORDERING | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-103#0 | hi | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh3-105#0 | random q | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN, qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh3-107#0 | Hi, are you hiring? I'd like to apply for a cashier job. | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: HUMAN_REQUEST |

## Order mistakes, chat by chat

### a-fresh3-002 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '19:00', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '19:00', None)

### a-fresh3-003 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** invalid: order.items.2.modifications.0.kind: Input should be 'remove', 'add' or 'substitute'
- **qwen3.5-0.8b-single-v4:** invalid: order.items.2.modifications.0.kind: Input should be 'remove', 'add' or 'substitute'

### a-fresh3-005 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'asap', None, None) | pred ('not_mentioned', None, None, None)
- **qwen3.5-0.8b-single-v4:** time: gold ('provided', 'asap', None, None) | pred ('not_mentioned', None, None, None)

### a-fresh3-009 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold 1× milkshake, chocolate | pred 2× milkshake, chocolate; missing 1× milkshake, strawberry
- **qwen3.5-0.8b-single-v4:** quantity: gold 1× milkshake, chocolate | pred 2× milkshake, chocolate

### a-fresh3-010 (simple_order)
- **qwen3.5-0.8b-single-v3:** missing 2× latte, small

### a-fresh3-019 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '08:15', ('weekday', 'mon', None, None)) | pred ('provided', 'clock_time', '08:15', None)

### a-fresh3-024 (ambiguous_reference)
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'the same as last time'; extra 1× latte, large; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-032 (human_request) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('ambiguous', None, None, ('weekday', 'fri', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-0.8b-single-v4:** time: gold ('ambiguous', None, None, ('weekday', 'fri', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-036 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('ambiguous', None, None, ('weekday', 'sat', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('fulfillment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-fresh3-037 (future_day) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '12:30', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '12:30', None)
- **qwen3.5-0.8b-single-v4:** time: gold ('provided', 'clock_time', '12:30', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '12:30', None)

### a-fresh3-039 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'the big one'; method: gold delivery | pred unknown; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-0.8b-single-v4:** missing 1× off-menu 'the big one'; extra 1× cheeseburger, single; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh3-041 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '18:00', ('weekday', 'thu', None, None)) | pred ('provided', 'clock_time', '18:00', None)

### a-fresh3-044 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '09:30', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '09:30', None)

### a-fresh3-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-0.8b-single-v4:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-047 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('ambiguous', None, None, ('weekday', 'wed', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('requested_time', 'ambiguous'), 1),) | pred ()

### a-fresh3-048 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× meat_lovers_pizza, medium, add w pesto drizzle | pred 1× meat_lovers_pizza, medium, add pesto, add drizzle
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× meat_lovers_pizza, medium, add w pesto drizzle | pred 1× meat_lovers_pizza, medium, add w pesto, add drizzle

### a-fresh3-052 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '17:30', ('date', None, None, 21)) | pred ('provided', 'clock_time', '17:30', None)

### a-fresh3-053 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '18:30', ('weekday', 'fri', None, None)) | pred ('provided', 'clock_time', '18:30', None)

### a-fresh3-057 (two_requests)
- **qwen3.5-0.8b-single-v4:** missing 1× bbq_chicken_pizza, medium

### a-fresh3-058 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold 5× latte, medium | pred 4× latte, medium
- **qwen3.5-0.8b-single-v4:** quantity: gold 5× latte, medium | pred 4× latte, medium

### a-fresh3-059 (correction)
- **qwen3.5-0.8b-single-v4:** modifications: gold 6× cheeseburger, single, add bacon | pred 6× cheeseburger, single; extra 6× bacon_burger, add bacon

### a-fresh3-060 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '20:00', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '20:00', None)

### a-fresh3-062 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '12:15', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '12:15', None)

### a-fresh3-064 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '13:15', None) | pred ('provided', 'clock_time', '12:30', None)
- **qwen3.5-0.8b-single-v4:** invalid: order.fulfillment.requested_time.day.kind: Input should be 'tomorrow', 'weekday' or 'date'

### a-fresh3-066 (multi_message_order)
- **qwen3.5-0.8b-single-v3:** extra 4× muffin; missing: gold ((('payment_method', 'missing'), 1),) | pred ((('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-068 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '12:15', ('weekday', 'thu', None, None)) | pred ('provided', 'clock_time', '12:15', None)

### a-fresh3-074 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× bagel, plain, add cream_cheese | pred 1× bagel, plain
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× bagel, plain, add cream_cheese | pred 1× bagel, plain

### a-fresh3-075 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v3:** items with no gold order: ['1× latte, medium']
- **qwen3.5-0.8b-single-v4:** items with no gold order: ['1× latte, medium']

### a-fresh3-076 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '19:00', ('weekday', 'sat', None, None)) | pred ('provided', 'clock_time', '19:00', None)

### a-fresh3-080 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '15:00', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '15:00', None)

### a-fresh3-081 (correction)
- **qwen3.5-0.8b-single-v3:** extra 1× garlic_knots

### a-fresh3-082 (future_day)
- **qwen3.5-0.8b-single-v3:** missing 3× breakfast_sandwich, bagel; extra 3× bagel, everything; time: gold ('ambiguous', None, None, ('weekday', 'sat', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-087 (combo)
- **qwen3.5-0.8b-single-v3:** invalid: order.items.0.combo_selections.0.unmatched_variant_text: Extra inputs are not permitted

### a-fresh3-090 (future_day) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '20:00', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '20:00', None)
- **qwen3.5-0.8b-single-v4:** invalid: order.fulfillment.requested_time.day.month: Input should be a valid integer, unable to parse string as an integer

### a-fresh3-091 (implicit_category) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× breadsticks; extra 1× off-menu 'cheesy'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1),)
- **qwen3.5-0.8b-single-v4:** missing 1× breadsticks; extra 1× garlic_knots

### a-fresh3-093 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× latte, small, substitute whole_milk | pred 1× latte, small, add almond_milk
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× latte, small, substitute whole_milk | pred 1× latte, small, add almond_milk

### a-fresh3-094 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '07:40', ('weekday', 'mon', None, None)) | pred ('provided', 'clock_time', '07:40', None)

### a-fresh3-098 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× bagel, everything, add w lox, add cream_cheese | pred 1× bagel, everything, add lox, add cream_cheese; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1))
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× bagel, everything, add w lox, add cream_cheese | pred 1× bagel, everything, add lox, add cream_cheese; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1))

### a-fresh3-100 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '17:00', ('weekday', 'sun', None, None)) | pred ('provided', 'clock_time', '17:00', None)

### a-fresh3-104 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '17:30', ('weekday', 'wed', None, None)) | pred ('provided', 'clock_time', '17:30', None)

### a-fresh3-106 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× latte; method: gold pickup | pred unknown; address: gold ('not_applicable', ()) | pred ('not_mentioned', ()); missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-0.8b-single-v4:** variant: gold 1× latte | pred 1× latte, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh3-109 (future_day)
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '11:45', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '11:45', None)

