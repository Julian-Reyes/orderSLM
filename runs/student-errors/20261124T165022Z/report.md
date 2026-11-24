# M6 error review on fresh3

Every chat or customer message a model got wrong, from saved outputs. Fresh3 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v5 |
|---|---|
| chats not fully right (of 110) | 20 |
| · fields only | 7 |
| · item mistakes | 12 |
| · items where there is no order | 1 |
| item: missing_item | 5 |
| item: wrong_modifications | 4 |
| item: extra_item | 3 |
| item: wrong_quantity | 3 |
| field: missing | 7 |
| field: time | 7 |
| intents wrong (of 321) | 18 |

Overlap: {'chats_all_students_wrong': 20, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 20, 'messages_all_students_wrong': 18, 'messages_one_student_only': 18}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v5': 1}
- combo: {'qwen3.5-0.8b-single-v5': 1}
- correction: {'qwen3.5-0.8b-single-v5': 3}
- future_day: {'qwen3.5-0.8b-single-v5': 4}
- human_request: {'qwen3.5-0.8b-single-v5': 1}
- missing_info: {'qwen3.5-0.8b-single-v5': 3}
- multi_message_order: {'qwen3.5-0.8b-single-v5': 2}
- off_menu: {'qwen3.5-0.8b-single-v5': 2}
- simple_order: {'qwen3.5-0.8b-single-v5': 2}
- small_talk: {'qwen3.5-0.8b-single-v5': 3}
- unclear_message: {'qwen3.5-0.8b-single-v5': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v5:** UNKNOWN → SMALL_TALK ×3; PLACE_ORDER → MODIFY_ORDER ×2; DELIVERY_QUESTION → PLACE_ORDER ×2; DELIVERY_QUESTION → ORDER_STATUS ×1; UNKNOWN → MENU_QUESTION ×1; CONFIRM_ORDER → SMALL_TALK ×1; MENU_QUESTION → PLACE_ORDER ×1; UNKNOWN → PLACE_ORDER ×1; OUT_OF_SCOPE → UNKNOWN ×1; ORDER_PROBLEM → ORDER_STATUS ×1; ORDER_PROBLEM → MODIFY_ORDER ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; SMALL_TALK → PLACE_ORDER ×1; SMALL_TALK → UNKNOWN ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh3-002#0 | hey do u guys take orders for tmrw | DELIVERY_QUESTION | qwen3.5-0.8b-single-v5: ORDER_STATUS |
| a-fresh3-007#0 | k | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh3-008#1 | is the bacon burger ok for someone who cant ea | UNKNOWN | qwen3.5-0.8b-single-v5: MENU_QUESTION |
| a-fresh3-026#1 | but please leave the olives off two of them | PLACE_ORDER | qwen3.5-0.8b-single-v5: MODIFY_ORDER |
| a-fresh3-030#2 | 🤔 | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh3-033#3 | deliver to 55 ivanhoe st | PLACE_ORDER | qwen3.5-0.8b-single-v5: MODIFY_ORDER |
| a-fresh3-042#2 | ya | CONFIRM_ORDER | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh3-051#3 | ok nvm the other one | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh3-053#0 | can i order now for friday? | DELIVERY_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-061#2 | do they come w cheese | MENU_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-075#1 | can i get a medium lat | UNKNOWN | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-079#1 | IS A HOT DOG A SANDWICH??? | OUT_OF_SCOPE | qwen3.5-0.8b-single-v5: UNKNOWN |
| a-fresh3-083#0 | WE JUST GOT OUR ORDER | ORDER_PROBLEM | qwen3.5-0.8b-single-v5: ORDER_STATUS |
| a-fresh3-083#2 | HE'S ALLERGIC TO MUSTARD, I SAID NO MUSTARD | ORDER_PROBLEM | qwen3.5-0.8b-single-v5: MODIFY_ORDER |
| a-fresh3-089#1 | i already paid thru the app 🙏 | PAYMENT_CLAIM | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-100#0 | can i preorder for sunday? 🍕 | DELIVERY_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-101#0 | HI, FIRST TIME ORDERING | SMALL_TALK | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh3-105#0 | random q | SMALL_TALK | qwen3.5-0.8b-single-v5: UNKNOWN |

## Order mistakes, chat by chat

### a-fresh3-003 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 3× croissant, chocolate, add warmed | pred 3× croissant, chocolate, add with cream cheese; missing: gold () | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh3-005 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('provided', 'asap', None, None) | pred ('not_mentioned', None, None, None)

### a-fresh3-009 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity: gold 1× milkshake, chocolate | pred 2× milkshake, chocolate; missing 1× milkshake, strawberry

### a-fresh3-024 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× off-menu 'the same as last time'; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-032 (human_request) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('ambiguous', None, None, ('weekday', 'fri', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-037 (future_day) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('provided', 'clock_time', '12:30', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '12:30', None)

### a-fresh3-039 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× off-menu 'the big one'; extra 1× cheeseburger, double; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh3-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-048 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× meat_lovers_pizza, medium, add w pesto drizzle | pred 1× meat_lovers_pizza, medium, add w pesto, add drizzle

### a-fresh3-058 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity: gold 5× latte, medium | pred 4× latte, medium

### a-fresh3-064 (correction) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity: gold 4× veggie_burger | pred 1× veggie_burger; time: gold ('provided', 'clock_time', '13:15', None) | pred ('provided', 'clock_time', '12:30', None)

### a-fresh3-068 (future_day) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('provided', 'clock_time', '12:15', ('weekday', 'thu', None, None)) | pred ('provided', 'clock_time', '12:15', None)

### a-fresh3-074 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× bagel, plain, add cream_cheese | pred 1× bagel, plain

### a-fresh3-075 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v5:** items with no gold order: ['1× latte, medium']

### a-fresh3-080 (future_day) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('provided', 'clock_time', '15:00', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '15:00', None)

### a-fresh3-084 (correction) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× sprite, can

### a-fresh3-087 (combo) — **all students**
- **qwen3.5-0.8b-single-v5:** extra 1× croissant, almond

### a-fresh3-090 (future_day) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('provided', 'clock_time', '20:00', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '20:00', ('weekday', 'thu', None, None))

### a-fresh3-098 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× bagel, everything, add w lox, add cream_cheese | pred 1× bagel, everything, add w lox, add cream_cheese; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1))

### a-fresh3-106 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× latte; extra 1× off-menu 'one of the bigger ones'; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1))

