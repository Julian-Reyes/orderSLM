# M6 error review on dev

Every chat or customer message a model got wrong, from saved outputs. Dev (tuning), not held-out. The teacher (`teacher-label@0.7`, the labels the students learned from) is shown as a reference.

| | qwen3.5-0.8b-single-v2 | teacher |
|---|---|---|
| chats not fully right (of 91) | 22 | 1 |
| · fields only | 6 | 0 |
| · invalid answer | 1 | 1 |
| · item mistakes | 15 | 0 |
| item: missing_item | 9 | 0 |
| item: extra_item | 7 | 0 |
| item: wrong_modifications | 3 | 0 |
| item: wrong_variant | 3 | 0 |
| item: wrong_quantity+modifications | 2 | 0 |
| item: wrong_combo_picks | 1 | 0 |
| item: wrong_quantity | 1 | 0 |
| field: address | 1 | 0 |
| field: decision | 1 | 0 |
| field: missing | 9 | 0 |
| field: payment | 2 | 0 |
| field: time | 1 | 0 |
| intents wrong (of 268) | 19 | 11 |

Overlap: {'chats_all_students_wrong': 22, 'chats_all_students_and_teacher_wrong': 1, 'chats_one_student_only': 22, 'messages_all_students_wrong': 19, 'messages_one_student_only': 19}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v2': 3}
- combo: {'qwen3.5-0.8b-single-v2': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v2': 3, 'teacher': 1}
- correction: {'qwen3.5-0.8b-single-v2': 4}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v2': 2, 'teacher': 1}
- half_and_half: {'qwen3.5-0.8b-single-v2': 1}
- implicit_category: {'qwen3.5-0.8b-single-v2': 2}
- menu_question: {'qwen3.5-0.8b-single-v2': 6}
- missing_info: {'qwen3.5-0.8b-single-v2': 3}
- multi_message_order: {'qwen3.5-0.8b-single-v2': 5}
- off_menu: {'qwen3.5-0.8b-single-v2': 2}
- payment_claim: {'qwen3.5-0.8b-single-v2': 1}
- simple_order: {'qwen3.5-0.8b-single-v2': 2}
- small_talk: {'qwen3.5-0.8b-single-v2': 3}
- two_requests: {'qwen3.5-0.8b-single-v2': 2}

## Intent mistakes

- **qwen3.5-0.8b-single-v2:** MODIFY_ORDER → PLACE_ORDER ×3; PLACE_ORDER → None ×2; PLACE_ORDER → SMALL_TALK ×2; UNKNOWN → SMALL_TALK ×1; MENU_QUESTION → UNKNOWN ×1; SMALL_TALK → MODIFY_ORDER ×1; HUMAN_REQUEST → PLACE_ORDER ×1; HUMAN_REQUEST → SMALL_TALK ×1; UNKNOWN → CONFIRM_ORDER ×1; PAYMENT_CLAIM → ORDER_STATUS ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; MENU_QUESTION → None ×1; ORDER_PROBLEM → ORDER_STATUS ×1; PAYMENT_CLAIM → PLACE_ORDER ×1; HUMAN_REQUEST → ORDER_PROBLEM ×1
- **teacher:** PLACE_ORDER → SMALL_TALK ×4; PLACE_ORDER → None ×4; CONFIRM_ORDER → None ×1; MODIFY_ORDER → None ×1; UNKNOWN → SMALL_TALK ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-dev-005#0 | . | UNKNOWN | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-dev-010#1 | or still just s m l | MENU_QUESTION | qwen3.5-0.8b-single-v2: UNKNOWN |
| a-dev-012#0 | 2 large cheese pizzas for delivery please 🍕🍕 paying card 💳 | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-dev-014#2 | oof thats more than i thoght | SMALL_TALK | qwen3.5-0.8b-single-v2: MODIFY_ORDER |
| a-dev-016#4 | AND MAKE THE LATTE OAT MILK PLEASE | MODIFY_ORDER | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-dev-020#0 | hey need lunch for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-021#0 | Hi, I'm organizing a dorm event next Friday and need about 30 large pizzas. Can I talk to a manager about a catering ord | HUMAN_REQUEST | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-dev-021#2 | Yes, please have them message me here. Thanks! | HUMAN_REQUEST | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-dev-023#0 | hi need 2 large cheese pizzas | PLACE_ORDER | teacher: None |
| a-dev-023#1 | n a 2 liter coke | PLACE_ORDER | teacher: None |
| a-dev-023#2 | delivery to 140 river rd | PLACE_ORDER | teacher: None |
| a-dev-023#3 | card | PLACE_ORDER | teacher: None |
| a-dev-023#5 | yep | CONFIRM_ORDER | teacher: None |
| a-dev-023#6 | wait sry its 104 river rd not 140 | MODIFY_ORDER | teacher: None |
| a-dev-032#4 | 👍 SOUNDS GOOD | UNKNOWN | qwen3.5-0.8b-single-v2: CONFIRM_ORDER, teacher: SMALL_TALK |
| a-dev-035#2 | make the fries large | MODIFY_ORDER | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-dev-040#4 | oh and make the fries large 🍟 | MODIFY_ORDER | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-dev-056#0 | hi! I ordered a latte + croissant for pickup a few min ago, name's Priya 😊 already paid when I called it in 💳✅ | PAYMENT_CLAIM | qwen3.5-0.8b-single-v2: ORDER_STATUS |
| a-dev-074#0 | hey ordering for the office | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK, teacher: SMALL_TALK |
| a-dev-075#0 | ok party order incoming | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK, teacher: SMALL_TALK |
| a-dev-076#0 | hi do ur pastries have tree nuts or r they made near them? coworker has a severe allergy | MENU_QUESTION | qwen3.5-0.8b-single-v2: OUT_OF_SCOPE |
| a-dev-079#0 | CAN I GET 2 PARTY SIZE PEPPERONI PIZZAS AND 2 XL CHEESE FOR DELIVERY | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-dev-079#1 | WAIT HOW BIG IS THE XL | MENU_QUESTION | qwen3.5-0.8b-single-v2: None |
| a-dev-088#2 | It was under Whitfield, a large Hawaiian 🍍 | ORDER_PROBLEM | qwen3.5-0.8b-single-v2: ORDER_STATUS |
| a-dev-089#0 | hey big ordr for pickup | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-089#3 | already sent the payment, i have a screenshot if u need it | PAYMENT_CLAIM | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-dev-090#0 | this bot keeps getting my order wrong, i said NO cheese like 3 times. let me talk to a real person pls | HUMAN_REQUEST | qwen3.5-0.8b-single-v2: ORDER_PROBLEM |

## Order mistakes, chat by chat

### a-dev-011 (combo, missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** combo_picks: gold 1× cheeseburger_combo, side=fries | pred 1× cheeseburger_combo, side=fries, drink=coke; missing: gold ((('combo_choice', 'missing'), 1), (('fulfillment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-012 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** invalid: order: Value error, address is only not_applicable for pickup

### a-dev-016 (ambiguous_reference, menu_question) — **all students**
- **qwen3.5-0.8b-single-v2:** missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))

### a-dev-017 (half_and_half) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× off-menu 'xl pizza half mushroom n olives, half sausage n jalapenos'; missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1))

### a-dev-019 (correction) — **all students**
- **qwen3.5-0.8b-single-v2:** extra 1× muffin, chocolate_chip

### a-dev-020 (correction, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove pickle; missing 2× cheeseburger, single, remove pickle

### a-dev-023 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v2:** address: gold ('provided', ('104',)) | pred ('provided', ('140',))
- **teacher:** invalid: 1 validation error for TeacherLabel
order.customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pending', 'agr...x': 5, 'quote': 'yep'}]}, input_type=dict]
    For further informati

### a-dev-038 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v2:** missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ((('item_menu_match', 'off_menu'), 1),)

### a-dev-039 (contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v2:** modifications: gold 1× americano, medium, add almond_milk | pred 1× americano, medium, substitute whole_milk

### a-dev-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-dev-048 (simple_order, menu_question) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× breakfast_sandwich, croissant; extra 1× croissant, plain

### a-dev-049 (ambiguous_reference, menu_question, correction) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 1× milkshake | pred 1× milkshake, chocolate; extra 1× milkshake, strawberry; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-061 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× off-menu 'Mountain Dew'; extra 1× dr_pepper, can; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ()

### a-dev-063 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove onion; missing 2× cheeseburger, single, remove onion

### a-dev-067 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 1× cheeseburger, double | pred 1× cheeseburger, single; decision: gold ('pending', False) | pred ('confirmed', False)

### a-dev-073 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v2:** time: gold ('provided', 'clock_time', '22:30') | pred ('provided', 'clock_time', '10:30')

### a-dev-074 (two_requests, menu_question, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; missing 2× latte, medium, substitute whole_milk; extra 3× bagel; extra 2× off-menu '2 medium oat lattes'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1), (('item_variant', 'missing'), 1))

### a-dev-075 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)

### a-dev-079 (off_menu, menu_question) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, personal; missing: gold ((('item_variant', 'missing'), 1),) | pred ()

### a-dev-083 (implicit_category, small_talk, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× bagel, everything, add cream_cheese; modifications: gold 1× croissant, chocolate | pred 1× croissant, chocolate, add butter

### a-dev-085 (implicit_category, two_requests, menu_question) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× pepperoni_pizza, large

### a-dev-089 (payment_claim, multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** payment: gold ('unknown', None, True) | pred ('cash', None, True)

