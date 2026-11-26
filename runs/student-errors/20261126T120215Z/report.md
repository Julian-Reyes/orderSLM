# M6 error review on dev

Every chat or customer message a model got wrong, from saved outputs. Dev is tuning / "used for fixes" data, not held-out. The teacher (`teacher-label@0.7`, the labels the students learned from) is shown as a reference.

| | qwen3.5-0.8b-single-v6 | teacher |
|---|---|---|
| chats not fully right (of 91) | 9 | 1 |
| · invalid answer | 0 | 1 |
| · item mistakes | 9 | 0 |
| item: missing_item | 4 | 0 |
| item: wrong_quantity | 2 | 0 |
| item: wrong_modifications | 2 | 0 |
| item: extra_item | 1 | 0 |
| item: wrong_combo_picks | 1 | 0 |
| field: missing | 4 | 0 |
| field: payment | 1 | 0 |
| intents wrong (of 268) | 17 | 11 |

Overlap: {'chats_all_students_wrong': 9, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 9, 'messages_all_students_wrong': 17, 'messages_one_student_only': 17}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v6': 1}
- combo: {'qwen3.5-0.8b-single-v6': 2}
- contextual_yes: {'teacher': 1}
- correction: {'qwen3.5-0.8b-single-v6': 1}
- correction_after_confirmation: {'teacher': 1}
- half_and_half: {'qwen3.5-0.8b-single-v6': 1}
- implicit_category: {'qwen3.5-0.8b-single-v6': 2}
- menu_question: {'qwen3.5-0.8b-single-v6': 3}
- missing_info: {'qwen3.5-0.8b-single-v6': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v6': 3}
- small_talk: {'qwen3.5-0.8b-single-v6': 2}
- two_requests: {'qwen3.5-0.8b-single-v6': 2}

## Intent mistakes

- **qwen3.5-0.8b-single-v6:** MODIFY_ORDER → PLACE_ORDER ×3; UNKNOWN → SMALL_TALK ×1; PLACE_ORDER → None ×1; MENU_QUESTION → UNKNOWN ×1; SMALL_TALK → MODIFY_ORDER ×1; HUMAN_REQUEST → PLACE_ORDER ×1; HUMAN_REQUEST → SMALL_TALK ×1; UNKNOWN → CONFIRM_ORDER ×1; REFUND_REQUEST → ORDER_PROBLEM ×1; PAYMENT_CLAIM → ORDER_STATUS ×1; PLACE_ORDER → MODIFY_ORDER ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; ORDER_PROBLEM → DELIVERY_QUESTION ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; HUMAN_REQUEST → ORDER_PROBLEM ×1
- **teacher:** PLACE_ORDER → SMALL_TALK ×4; PLACE_ORDER → None ×4; CONFIRM_ORDER → None ×1; MODIFY_ORDER → None ×1; UNKNOWN → SMALL_TALK ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-dev-005#0 | . | UNKNOWN | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-dev-007#3 | ok add one of those no mayo 👍 delivery to 25 Cedar Ln, card 💳 | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-dev-010#1 | or still just s m l | MENU_QUESTION | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-dev-014#2 | oof thats more than i thoght | SMALL_TALK | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-dev-016#4 | AND MAKE THE LATTE OAT MILK PLEASE | MODIFY_ORDER | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-dev-020#0 | hey need lunch for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-021#0 | Hi, I'm organizing a dorm event next Friday and need about 30 large pizzas. Can I talk to a manager about a catering ord | HUMAN_REQUEST | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-dev-021#2 | Yes, please have them message me here. Thanks! | HUMAN_REQUEST | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-dev-023#0 | hi need 2 large cheese pizzas | PLACE_ORDER | teacher: None |
| a-dev-023#1 | n a 2 liter coke | PLACE_ORDER | teacher: None |
| a-dev-023#2 | delivery to 140 river rd | PLACE_ORDER | teacher: None |
| a-dev-023#3 | card | PLACE_ORDER | teacher: None |
| a-dev-023#5 | yep | CONFIRM_ORDER | teacher: None |
| a-dev-023#6 | wait sry its 104 river rd not 140 | MODIFY_ORDER | teacher: None |
| a-dev-032#4 | 👍 SOUNDS GOOD | UNKNOWN | qwen3.5-0.8b-single-v6: CONFIRM_ORDER, teacher: SMALL_TALK |
| a-dev-035#2 | make the fries large | MODIFY_ORDER | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-dev-040#4 | oh and make the fries large 🍟 | MODIFY_ORDER | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-dev-053#2 | Kim. it was the veggie burger + fries, $13.48 both times | REFUND_REQUEST | qwen3.5-0.8b-single-v6: ORDER_PROBLEM |
| a-dev-056#0 | hi! I ordered a latte + croissant for pickup a few min ago, name's Priya 😊 already paid when I called it in 💳✅ | PAYMENT_CLAIM | qwen3.5-0.8b-single-v6: ORDER_STATUS |
| a-dev-062#3 | I WILL PAY CASH, THANK YOU | PLACE_ORDER | qwen3.5-0.8b-single-v6: MODIFY_ORDER |
| a-dev-074#0 | hey ordering for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-075#0 | ok party order incoming | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-076#0 | hi do ur pastries have tree nuts or r they made near them? coworker has a severe allergy | MENU_QUESTION | qwen3.5-0.8b-single-v6: OUT_OF_SCOPE |
| a-dev-088#0 | Hello 🙂 Our delivery last night never arrived, even though the card was charged. | ORDER_PROBLEM | qwen3.5-0.8b-single-v6: DELIVERY_QUESTION |
| a-dev-089#0 | hey big ordr for pickup | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-089#3 | already sent the payment, i have a screenshot if u need it | PAYMENT_CLAIM | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-dev-090#0 | this bot keeps getting my order wrong, i said NO cheese like 3 times. let me talk to a real person pls | HUMAN_REQUEST | qwen3.5-0.8b-single-v6: ORDER_PROBLEM |

## Order mistakes, chat by chat

### a-dev-002 (combo) — **all students**
- **qwen3.5-0.8b-single-v6:** modifications: gold 1× cheeseburger_combo, remove cheese, side=onion_rings, drink=lemonade | pred 1× cheeseburger_combo, add onion, remove cheese, side=onion_rings, drink=lemonade

### a-dev-011 (combo, missing_info) — **all students**
- **qwen3.5-0.8b-single-v6:** combo_picks: gold 1× cheeseburger_combo, side=fries | pred 1× cheeseburger_combo, side=fries, drink=coke; missing: gold ((('combo_choice', 'missing'), 1), (('fulfillment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-017 (half_and_half) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× off-menu 'an xl pizza half mushroom n olives, half sausage n jalapenos'; missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1))

### a-dev-023 (correction_after_confirmation, contextual_yes)
- **teacher:** invalid: 1 validation error for TeacherLabel
order.customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pending', 'agr...x': 5, 'quote': 'yep'}]}, input_type=dict]
    For further informati

### a-dev-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-dev-049 (ambiguous_reference, menu_question, correction) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× milkshake; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-074 (two_requests, menu_question, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v6:** modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain

### a-dev-075 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v6:** quantity: gold 6× cheeseburger, single | pred 3× cheeseburger, single; payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)

### a-dev-083 (implicit_category, small_talk, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× bagel, everything, add cream_cheese

### a-dev-085 (implicit_category, two_requests, menu_question) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× pepperoni_pizza, large

