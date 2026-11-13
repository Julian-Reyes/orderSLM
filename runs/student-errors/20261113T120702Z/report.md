# M6 error review on dev

Every chat or customer message a model got wrong, from saved outputs. Dev is tuning / "used for fixes" data, not held-out. The teacher (`teacher-label@0.7`, the labels the students learned from) is shown as a reference.

| | qwen3.5-0.8b-single-v3 | qwen3.5-0.8b-single-v4 | teacher |
|---|---|---|---|
| chats not fully right (of 91) | 15 | 12 | 1 |
| · fields only | 2 | 1 | 0 |
| · invalid answer | 2 | 1 | 1 |
| · item mistakes | 11 | 10 | 0 |
| item: missing_item | 7 | 5 | 0 |
| item: wrong_quantity | 3 | 3 | 0 |
| item: extra_item | 2 | 2 | 0 |
| item: wrong_variant | 2 | 2 | 0 |
| item: wrong_modifications | 1 | 1 | 0 |
| field: address | 1 | 0 | 0 |
| field: missing | 4 | 4 | 0 |
| field: payment | 1 | 1 | 0 |
| field: time | 1 | 1 | 0 |
| intents wrong (of 268) | 21 | 17 | 11 |

Overlap: {'chats_all_students_wrong': 11, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 5, 'messages_all_students_wrong': 12, 'messages_one_student_only': 14}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 2}
- combo: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v3': 2, 'teacher': 1}
- correction: {'qwen3.5-0.8b-single-v3': 3, 'qwen3.5-0.8b-single-v4': 3}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v3': 2, 'teacher': 1}
- half_and_half: {'qwen3.5-0.8b-single-v3': 1, 'qwen3.5-0.8b-single-v4': 1}
- implicit_category: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 2}
- menu_question: {'qwen3.5-0.8b-single-v3': 4, 'qwen3.5-0.8b-single-v4': 5}
- missing_info: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v3': 4, 'qwen3.5-0.8b-single-v4': 4}
- simple_order: {'qwen3.5-0.8b-single-v4': 1, 'qwen3.5-0.8b-single-v3': 1}
- small_talk: {'qwen3.5-0.8b-single-v3': 4, 'qwen3.5-0.8b-single-v4': 3}
- two_requests: {'qwen3.5-0.8b-single-v3': 2, 'qwen3.5-0.8b-single-v4': 2}

## Intent mistakes

- **qwen3.5-0.8b-single-v3:** PLACE_ORDER → None ×5; MODIFY_ORDER → PLACE_ORDER ×2; MENU_QUESTION → UNKNOWN ×1; SMALL_TALK → MODIFY_ORDER ×1; PLACE_ORDER → SMALL_TALK ×1; HUMAN_REQUEST → PLACE_ORDER ×1; HUMAN_REQUEST → SMALL_TALK ×1; UNKNOWN → CONFIRM_ORDER ×1; PLACE_ORDER → MENU_QUESTION ×1; PAYMENT_CLAIM → ORDER_STATUS ×1; PLACE_ORDER → MODIFY_ORDER ×1; SMALL_TALK → UNKNOWN ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; ORDER_PROBLEM → ORDER_STATUS ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; HUMAN_REQUEST → ORDER_PROBLEM ×1
- **qwen3.5-0.8b-single-v4:** OUT_OF_SCOPE → MENU_QUESTION ×2; PAYMENT_CLAIM → PLACE_ORDER ×2; UNKNOWN → SMALL_TALK ×1; MENU_QUESTION → UNKNOWN ×1; PLACE_ORDER → None ×1; SMALL_TALK → MODIFY_ORDER ×1; MODIFY_ORDER → PLACE_ORDER ×1; HUMAN_REQUEST → PLACE_ORDER ×1; HUMAN_REQUEST → SMALL_TALK ×1; OUT_OF_SCOPE → HUMAN_REQUEST ×1; UNKNOWN → CONFIRM_ORDER ×1; PLACE_ORDER → MENU_QUESTION ×1; SMALL_TALK → MENU_QUESTION ×1; PLACE_ORDER → MODIFY_ORDER ×1; HUMAN_REQUEST → ORDER_PROBLEM ×1
- **teacher:** PLACE_ORDER → SMALL_TALK ×4; PLACE_ORDER → None ×4; CONFIRM_ORDER → None ×1; MODIFY_ORDER → None ×1; UNKNOWN → SMALL_TALK ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-dev-001#0 | hey is this the bakery on 5th that does the custom bday cakes? need one for sat | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-dev-003#2 | can I get the coffee & pastry deal w a large latte and a chocolate croissant 🥐 | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-dev-003#3 | pickup in 10 min, name's Marcus 🙏 paying card | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-dev-005#0 | . | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-dev-007#3 | ok add one of those no mayo 👍 delivery to 25 Cedar Ln, card 💳 | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-dev-010#1 | or still just s m l | MENU_QUESTION | qwen3.5-0.8b-single-v3: UNKNOWN, qwen3.5-0.8b-single-v4: UNKNOWN |
| a-dev-011#0 | lemme get a numbr 1 combo w fries, payin cash | PLACE_ORDER | qwen3.5-0.8b-single-v3: None, qwen3.5-0.8b-single-v4: None |
| a-dev-014#2 | oof thats more than i thoght | SMALL_TALK | qwen3.5-0.8b-single-v3: MODIFY_ORDER, qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-dev-016#3 | OK I'LL TAKE THAT ONE | PLACE_ORDER | qwen3.5-0.8b-single-v3: SMALL_TALK |
| a-dev-016#4 | AND MAKE THE LATTE OAT MILK PLEASE | MODIFY_ORDER | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-dev-020#0 | hey need lunch for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-021#0 | Hi, I'm organizing a dorm event next Friday and need about 30 large pizzas. Can I talk to a manager about a catering ord | HUMAN_REQUEST | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-dev-021#2 | Yes, please have them message me here. Thanks! | HUMAN_REQUEST | qwen3.5-0.8b-single-v3: SMALL_TALK, qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-dev-023#0 | hi need 2 large cheese pizzas | PLACE_ORDER | teacher: None |
| a-dev-023#1 | n a 2 liter coke | PLACE_ORDER | teacher: None |
| a-dev-023#2 | delivery to 140 river rd | PLACE_ORDER | teacher: None |
| a-dev-023#3 | card | PLACE_ORDER | teacher: None |
| a-dev-023#5 | yep | CONFIRM_ORDER | teacher: None |
| a-dev-023#6 | wait sry its 104 river rd not 140 | MODIFY_ORDER | teacher: None |
| a-dev-031#0 | hey r u guys hiring? just moved here n lookin for weekend shifts | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: HUMAN_REQUEST |
| a-dev-032#4 | 👍 SOUNDS GOOD | UNKNOWN | qwen3.5-0.8b-single-v3: CONFIRM_ORDER, qwen3.5-0.8b-single-v4: CONFIRM_ORDER, teacher: SMALL_TALK |
| a-dev-038#3 | actually make it a medium. pickup, card | MODIFY_ORDER | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-dev-050#0 | Hi! Can I get a medium latte with caramel? Also, do you have any vegan pastries? | PLACE_ORDER | qwen3.5-0.8b-single-v3: MENU_QUESTION, qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-dev-056#0 | hi! I ordered a latte + croissant for pickup a few min ago, name's Priya 😊 already paid when I called it in 💳✅ | PAYMENT_CLAIM | qwen3.5-0.8b-single-v3: ORDER_STATUS, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-dev-060#0 | just wanted to say thx for making my latte w oat milk perfectly today 🥰 so hard to find dairy free spots | SMALL_TALK | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-dev-062#3 | I WILL PAY CASH, THANK YOU | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER, qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-dev-071#0 | hi! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-dev-074#0 | hey ordering for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-074#3 | ya warm pls | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-dev-075#0 | ok party order incoming | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-076#0 | hi do ur pastries have tree nuts or r they made near them? coworker has a severe allergy | MENU_QUESTION | qwen3.5-0.8b-single-v3: OUT_OF_SCOPE |
| a-dev-082#0 | Random question, but who invented the cheeseburger? | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-dev-088#2 | It was under Whitfield, a large Hawaiian 🍍 | ORDER_PROBLEM | qwen3.5-0.8b-single-v3: ORDER_STATUS |
| a-dev-089#0 | hey big ordr for pickup | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-089#3 | already sent the payment, i have a screenshot if u need it | PAYMENT_CLAIM | qwen3.5-0.8b-single-v3: PLACE_ORDER, qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-dev-090#0 | this bot keeps getting my order wrong, i said NO cheese like 3 times. let me talk to a real person pls | HUMAN_REQUEST | qwen3.5-0.8b-single-v3: ORDER_PROBLEM, qwen3.5-0.8b-single-v4: ORDER_PROBLEM |

## Order mistakes, chat by chat

### a-dev-003 (combo, small_talk)
- **qwen3.5-0.8b-single-v3:** invalid: order.items.0.combo_selections.0.customer_selection: Extra inputs are not permitted

### a-dev-011 (combo, missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** invalid: order.items.0.combo_selections.1.menu_item_id: Input should be a valid string
- **qwen3.5-0.8b-single-v4:** invalid: order.items.0.combo_selections.1.menu_item_id: Input should be a valid string

### a-dev-016 (ambiguous_reference, menu_question) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'THAT ONE'; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)
- **qwen3.5-0.8b-single-v4:** missing 1× off-menu 'THAT ONE'; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-dev-017 (half_and_half) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× off-menu 'xl pizza half mushroom n olives, half sausage n jalapenos'; missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1))
- **qwen3.5-0.8b-single-v4:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× off-menu 'xl pizza half mushroom n olives, half sausage n jalapenos'; missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1))

### a-dev-020 (correction, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold 2× cheeseburger, single | pred 4× cheeseburger, single
- **qwen3.5-0.8b-single-v4:** quantity: gold 2× cheeseburger, single | pred 3× cheeseburger, single

### a-dev-023 (correction_after_confirmation, contextual_yes)
- **qwen3.5-0.8b-single-v3:** address: gold ('provided', ('104',)) | pred ('provided', ('140',))
- **teacher:** invalid: 1 validation error for TeacherLabel
order.customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pending', 'agr...x': 5, 'quote': 'yep'}]}, input_type=dict]
    For further informati

### a-dev-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()
- **qwen3.5-0.8b-single-v4:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-dev-048 (simple_order, menu_question)
- **qwen3.5-0.8b-single-v4:** variant: gold 1× breakfast_sandwich, croissant | pred 1× breakfast_sandwich, english_muffin

### a-dev-049 (ambiguous_reference, menu_question, correction) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 1× milkshake | pred 1× milkshake, chocolate; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)
- **qwen3.5-0.8b-single-v4:** variant: gold 1× milkshake | pred 1× milkshake, chocolate; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-063 (simple_order)
- **qwen3.5-0.8b-single-v3:** missing 2× cheeseburger, single

### a-dev-067 (correction_after_confirmation, contextual_yes)
- **qwen3.5-0.8b-single-v3:** variant: gold 1× cheeseburger, double | pred 1× cheeseburger, single

### a-dev-073 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('provided', 'clock_time', '22:30', None) | pred ('provided', 'clock_time', '10:30', None)
- **qwen3.5-0.8b-single-v4:** time: gold ('provided', 'clock_time', '22:30', None) | pred ('provided', 'clock_time', '10:30', None)

### a-dev-074 (two_requests, menu_question, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; extra 3× bagel, everything
- **qwen3.5-0.8b-single-v4:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; extra 3× bagel, everything

### a-dev-075 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold 6× cheeseburger, single | pred 3× cheeseburger, single; payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)
- **qwen3.5-0.8b-single-v4:** quantity: gold 6× cheeseburger, single | pred 3× cheeseburger, single; payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)

### a-dev-083 (implicit_category, small_talk, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× muffin, blueberry; missing 1× bagel, everything, add cream_cheese
- **qwen3.5-0.8b-single-v4:** missing 1× bagel, everything, add cream_cheese

### a-dev-085 (implicit_category, two_requests, menu_question) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× pepperoni_pizza, large
- **qwen3.5-0.8b-single-v4:** missing 1× pepperoni_pizza, large

