# M6 error review on fresh3

Every chat or customer message a model got wrong, from saved outputs. Fresh3 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v6 |
|---|---|
| chats not fully right (of 110) | 17 |
| · fields only | 4 |
| · invalid answer | 4 |
| · item mistakes | 8 |
| · items where there is no order | 1 |
| item: missing_item | 5 |
| item: wrong_quantity | 2 |
| item: wrong_variant | 1 |
| item: wrong_modifications | 1 |
| field: address | 1 |
| field: method | 1 |
| field: missing | 7 |
| field: time | 3 |
| intents wrong (of 321) | 32 |

Overlap: {'chats_all_students_wrong': 17, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 17, 'messages_all_students_wrong': 32, 'messages_one_student_only': 32}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v6': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v6': 1}
- correction: {'qwen3.5-0.8b-single-v6': 2}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v6': 1}
- future_day: {'qwen3.5-0.8b-single-v6': 2}
- human_request: {'qwen3.5-0.8b-single-v6': 1}
- missing_info: {'qwen3.5-0.8b-single-v6': 3}
- multi_message_order: {'qwen3.5-0.8b-single-v6': 2}
- off_menu: {'qwen3.5-0.8b-single-v6': 1}
- simple_order: {'qwen3.5-0.8b-single-v6': 3}
- small_talk: {'qwen3.5-0.8b-single-v6': 4}
- unclear_message: {'qwen3.5-0.8b-single-v6': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v6:** SMALL_TALK → UNKNOWN ×4; UNKNOWN → SMALL_TALK ×3; PLACE_ORDER → MODIFY_ORDER ×3; PLACE_ORDER → None ×3; SMALL_TALK → PLACE_ORDER ×3; PLACE_ORDER → MENU_QUESTION ×3; MODIFY_ORDER → None ×2; DELIVERY_QUESTION → PLACE_ORDER ×2; DELIVERY_QUESTION → ORDER_STATUS ×1; UNKNOWN → MENU_QUESTION ×1; CONFIRM_ORDER → SMALL_TALK ×1; UNKNOWN → PLACE_ORDER ×1; OUT_OF_SCOPE → UNKNOWN ×1; ORDER_PROBLEM → ORDER_STATUS ×1; ORDER_PROBLEM → MODIFY_ORDER ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; OUT_OF_SCOPE → HUMAN_REQUEST ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh3-002#0 | hey do u guys take orders for tmrw | DELIVERY_QUESTION | qwen3.5-0.8b-single-v6: ORDER_STATUS |
| a-fresh3-007#0 | k | UNKNOWN | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-fresh3-008#1 | is the bacon burger ok for someone who cant ea | UNKNOWN | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh3-020#3 | Actually, could the supreme be a large? | MODIFY_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh3-026#1 | but please leave the olives off two of them | PLACE_ORDER | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-fresh3-030#2 | 🤔 | UNKNOWN | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-fresh3-033#3 | deliver to 55 ivanhoe st | PLACE_ORDER | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-fresh3-039#3 | ok the big one then, delivered to 14 alder ct | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh3-042#2 | ya | CONFIRM_ORDER | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-fresh3-044#0 | HI! PARTY TOMORROW | SMALL_TALK | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-045#1 | Could I get one of your larger pepperoni pizzas? Not sure which size. | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh3-051#3 | ok nvm the other one | UNKNOWN | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-fresh3-053#0 | can i order now for friday? | DELIVERY_QUESTION | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-057#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh3-057#2 | n is the bbq chicken spicy, if not add a medium one | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh3-057#4 | ok add it | PLACE_ORDER | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-fresh3-064#3 | actually make it 1:15 instead, meeting got pushed | MODIFY_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh3-069#0 | YO | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh3-075#1 | can i get a medium lat | UNKNOWN | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-079#0 | SETTLE A BET | SMALL_TALK | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-079#1 | IS A HOT DOG A SANDWICH??? | OUT_OF_SCOPE | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh3-083#0 | WE JUST GOT OUR ORDER | ORDER_PROBLEM | qwen3.5-0.8b-single-v6: ORDER_STATUS |
| a-fresh3-083#2 | HE'S ALLERGIC TO MUSTARD, I SAID NO MUSTARD | ORDER_PROBLEM | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-fresh3-087#0 | hi 🌙 can i get the coffee n pastry deal | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh3-088#2 | one of them on thin crust | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh3-088#3 | delivered to 412 dover st, card | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh3-089#1 | i already paid thru the app 🙏 | PAYMENT_CLAIM | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-099#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh3-100#0 | can i preorder for sunday? 🍕 | DELIVERY_QUESTION | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-101#0 | HI, FIRST TIME ORDERING | SMALL_TALK | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh3-105#0 | random q | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh3-107#0 | Hi, are you hiring? I'd like to apply for a cashier job. | OUT_OF_SCOPE | qwen3.5-0.8b-single-v6: HUMAN_REQUEST |

## Order mistakes, chat by chat

### a-fresh3-003 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v6:** modifications: gold 3× croissant, chocolate, add warmed | pred 3× croissant, chocolate, add with cream cheese; missing: gold () | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh3-009 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v6:** quantity: gold 1× milkshake, chocolate | pred 2× milkshake, chocolate

### a-fresh3-010 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 2× latte, small, add vanilla_syrup

### a-fresh3-014 (off_menu, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** missing: gold ((('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-020 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order: Value error, L2: item_variant flag only on a menu line with no variant_id

### a-fresh3-024 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× off-menu 'the same as last time'; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-032 (human_request) — **all students**
- **qwen3.5-0.8b-single-v6:** time: gold ('ambiguous', None, None, ('weekday', 'fri', None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-037 (future_day) — **all students**
- **qwen3.5-0.8b-single-v6:** time: gold ('provided', 'clock_time', '12:30', ('date', None, 11, 19)) | pred ('provided', 'clock_time', '12:30', None)

### a-fresh3-039 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order.items.0: Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4)

### a-fresh3-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× pepperoni_pizza; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh3-058 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** quantity: gold 5× latte, medium | pred 4× latte, medium

### a-fresh3-064 (correction) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order.fulfillment.requested_time.day: Value error, requested_time.day: day_of_month is set exactly for kind 'date'

### a-fresh3-074 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v6:** variant: gold 1× bagel, plain, add cream_cheese | pred 1× bagel, add cream_cheese; missing 1× bagel, everything, add cream_cheese; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1))

### a-fresh3-075 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v6:** items with no gold order: ['1× latte, medium']

### a-fresh3-080 (future_day) — **all students**
- **qwen3.5-0.8b-single-v6:** time: gold ('provided', 'clock_time', '15:00', ('tomorrow', None, None, None)) | pred ('provided', 'clock_time', '15:00', None)

### a-fresh3-088 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order: Value error, L2: item_variant flag only on a menu line with no variant_id

### a-fresh3-106 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× latte; method: gold pickup | pred unknown; address: gold ('not_applicable', ()) | pred ('not_mentioned', ()); missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

