# M6 error review on fresh3

Every chat or customer message a model got wrong, from saved outputs. Fresh3 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v4 |
|---|---|
| chats not fully right (of 110) | 18 |
| · fields only | 4 |
| · invalid answer | 3 |
| · item mistakes | 10 |
| · items where there is no order | 1 |
| item: wrong_modifications | 4 |
| item: extra_item | 3 |
| item: missing_item | 3 |
| item: wrong_quantity | 2 |
| item: wrong_variant | 1 |
| field: missing | 5 |
| field: time | 3 |
| intents wrong (of 321) | 21 |

Overlap: {'chats_all_students_wrong': 18, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 18, 'messages_all_students_wrong': 21, 'messages_one_student_only': 21}

Chats wrong by scenario (a chat can have several):

- correction: {'qwen3.5-0.8b-single-v4': 3}
- future_day: {'qwen3.5-0.8b-single-v4': 2}
- human_request: {'qwen3.5-0.8b-single-v4': 1}
- implicit_category: {'qwen3.5-0.8b-single-v4': 1}
- missing_info: {'qwen3.5-0.8b-single-v4': 3}
- multi_message_order: {'qwen3.5-0.8b-single-v4': 2}
- off_menu: {'qwen3.5-0.8b-single-v4': 2}
- simple_order: {'qwen3.5-0.8b-single-v4': 2}
- small_talk: {'qwen3.5-0.8b-single-v4': 3}
- two_requests: {'qwen3.5-0.8b-single-v4': 1}
- unclear_message: {'qwen3.5-0.8b-single-v4': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v4:** DELIVERY_QUESTION → PLACE_ORDER ×3; PLACE_ORDER → None ×3; PLACE_ORDER → MODIFY_ORDER ×2; UNKNOWN → SMALL_TALK ×2; SMALL_TALK → PLACE_ORDER ×2; MODIFY_ORDER → None ×1; UNKNOWN → PLACE_ORDER ×1; SMALL_TALK → PAYMENT_CLAIM ×1; OUT_OF_SCOPE → UNKNOWN ×1; ORDER_PROBLEM → ORDER_STATUS ×1; ORDER_PROBLEM → MODIFY_ORDER ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; SMALL_TALK → UNKNOWN ×1; OUT_OF_SCOPE → HUMAN_REQUEST ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh3-002#0 | hey do u guys take orders for tmrw | DELIVERY_QUESTION | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-003#2 | Yes please. For a little party: 2 large lattes, a medium hot chocolate, 3 chocolate croissants warmed, 2 blueberry muffi | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-026#1 | but please leave the olives off two of them | PLACE_ORDER | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-030#2 | 🤔 | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh3-044#0 | HI! PARTY TOMORROW | SMALL_TALK | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-051#3 | ok nvm the other one | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh3-053#0 | can i order now for friday? | DELIVERY_QUESTION | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-057#4 | ok add it | PLACE_ORDER | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-064#3 | actually make it 1:15 instead, meeting got pushed | MODIFY_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-075#1 | can i get a medium lat | UNKNOWN | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-079#0 | SETTLE A BET | SMALL_TALK | qwen3.5-0.8b-single-v4: PAYMENT_CLAIM |
| a-fresh3-079#1 | IS A HOT DOG A SANDWICH??? | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh3-083#0 | WE JUST GOT OUR ORDER | ORDER_PROBLEM | qwen3.5-0.8b-single-v4: ORDER_STATUS |
| a-fresh3-083#2 | HE'S ALLERGIC TO MUSTARD, I SAID NO MUSTARD | ORDER_PROBLEM | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh3-087#1 | w a drip coffee but large pls ☕ | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-089#1 | i already paid thru the app 🙏 | PAYMENT_CLAIM | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-090#0 | hi 👋 we're arriving thursday nov 19, could we get 2 bacon burgers n 2 cokes delivered to the harbor inn, 400 front st, r | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh3-100#0 | can i preorder for sunday? 🍕 | DELIVERY_QUESTION | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-101#0 | HI, FIRST TIME ORDERING | SMALL_TALK | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh3-105#0 | random q | SMALL_TALK | qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh3-107#0 | Hi, are you hiring? I'd like to apply for a cashier job. | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: HUMAN_REQUEST |

## Order mistakes, chat by chat

### a-fresh3-003 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order.items.2.modifications.0.kind: Input should be 'remove', 'add' or 'substitute'

### a-fresh3-005 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v4:** time: gold ('provided', 'asap', None, None) | pred ('not_mentioned', None, None, None)

### a-fresh3-009 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity: gold 1× milkshake, chocolate | pred 2× milkshake, chocolate

### a-fresh3-032 (human_request) — **all students**
- **qwen3.5-0.8b-single-v4:** time: gold ('ambiguous', None, None, ('weekday', 'fri', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-037 (future_day) — **all students**
- **qwen3.5-0.8b-single-v4:** time: gold ('provided', 'clock_time', '12:30', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '12:30', None)

### a-fresh3-039 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× off-menu 'the big one'; extra 1× cheeseburger, single; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh3-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-048 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× meat_lovers_pizza, medium, add w pesto drizzle | pred 1× meat_lovers_pizza, medium, add w pesto, add drizzle

### a-fresh3-057 (two_requests) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× bbq_chicken_pizza, medium

### a-fresh3-058 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity: gold 5× latte, medium | pred 4× latte, medium

### a-fresh3-059 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 6× cheeseburger, single, add bacon | pred 6× cheeseburger, single; extra 6× bacon_burger, add bacon

### a-fresh3-064 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order.fulfillment.requested_time.day.kind: Input should be 'tomorrow', 'weekday' or 'date'

### a-fresh3-074 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× bagel, plain, add cream_cheese | pred 1× bagel, plain

### a-fresh3-075 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v4:** items with no gold order: ['1× latte, medium']

### a-fresh3-090 (future_day) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order.fulfillment.requested_time.day.month: Input should be a valid integer, unable to parse string as an integer

### a-fresh3-091 (implicit_category) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× breadsticks; extra 1× garlic_knots

### a-fresh3-098 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× bagel, everything, add w lox, add cream_cheese | pred 1× bagel, everything, add lox, add cream_cheese; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1))

### a-fresh3-106 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v4:** variant: gold 1× latte | pred 1× latte, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

