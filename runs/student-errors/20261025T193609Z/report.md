# M6 error review on dev

Every chat or customer message a model got wrong, from saved outputs. Dev (tuning), not held-out. The teacher (`teacher-label@0.7`, the labels the students learned from) is shown as a reference.

| | qwen3.5-0.8b-single | qwen3.5-2b-single | qwen3.5-2b-mixed | teacher |
|---|---|---|---|---|
| chats not fully right (of 91) | 27 | 32 | 26 | 1 |
| · fields only | 7 | 5 | 3 | 0 |
| · invalid answer | 1 | 5 | 2 | 1 |
| · item mistakes | 19 | 22 | 21 | 0 |
| item: missing_item | 14 | 14 | 14 | 0 |
| item: extra_item | 7 | 6 | 6 | 0 |
| item: wrong_modifications | 6 | 7 | 6 | 0 |
| item: wrong_variant | 4 | 3 | 4 | 0 |
| item: wrong_quantity+modifications | 2 | 1 | 2 | 0 |
| item: wrong_quantity | 1 | 1 | 1 | 0 |
| item: wrong_variant+modifications | 0 | 2 | 0 | 0 |
| item: wrong_quantity+variant | 0 | 1 | 1 | 0 |
| item: wrong_combo_picks | 1 | 0 | 0 | 0 |
| field: address | 1 | 1 | 0 | 0 |
| field: decision | 1 | 0 | 0 | 0 |
| field: method | 1 | 2 | 1 | 0 |
| field: missing | 10 | 11 | 8 | 0 |
| field: payment | 7 | 4 | 1 | 0 |
| field: time | 4 | 4 | 1 | 0 |
| intents wrong (of 268) | 24 | 32 | 27 | 9 |

Overlap: {'chats_all_students_wrong': 19, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 10, 'messages_all_students_wrong': 12, 'messages_one_student_only': 23}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single': 3, 'qwen3.5-2b-single': 3, 'qwen3.5-2b-mixed': 3}
- cancellation: {'qwen3.5-2b-single': 1}
- combo: {'qwen3.5-0.8b-single': 1, 'qwen3.5-2b-single': 1, 'qwen3.5-2b-mixed': 1}
- contextual_yes: {'teacher': 1, 'qwen3.5-0.8b-single': 4, 'qwen3.5-2b-single': 4, 'qwen3.5-2b-mixed': 3}
- correction: {'qwen3.5-0.8b-single': 4, 'qwen3.5-2b-single': 5, 'qwen3.5-2b-mixed': 5}
- correction_after_confirmation: {'teacher': 1, 'qwen3.5-0.8b-single': 3, 'qwen3.5-2b-single': 3, 'qwen3.5-2b-mixed': 2}
- half_and_half: {'qwen3.5-0.8b-single': 1, 'qwen3.5-2b-single': 1, 'qwen3.5-2b-mixed': 1}
- implicit_category: {'qwen3.5-0.8b-single': 3, 'qwen3.5-2b-single': 2, 'qwen3.5-2b-mixed': 3}
- menu_question: {'qwen3.5-0.8b-single': 7, 'qwen3.5-2b-single': 6, 'qwen3.5-2b-mixed': 7}
- missing_info: {'qwen3.5-0.8b-single': 2, 'qwen3.5-2b-single': 3, 'qwen3.5-2b-mixed': 2}
- multi_message_order: {'qwen3.5-2b-single': 8, 'qwen3.5-0.8b-single': 7, 'qwen3.5-2b-mixed': 5}
- off_menu: {'qwen3.5-2b-single': 4, 'qwen3.5-0.8b-single': 1, 'qwen3.5-2b-mixed': 3}
- payment_claim: {'qwen3.5-0.8b-single': 2, 'qwen3.5-2b-single': 1, 'qwen3.5-2b-mixed': 1}
- simple_order: {'qwen3.5-2b-single': 3, 'qwen3.5-2b-mixed': 3, 'qwen3.5-0.8b-single': 4}
- small_talk: {'qwen3.5-2b-single': 6, 'qwen3.5-0.8b-single': 6, 'qwen3.5-2b-mixed': 4}
- two_requests: {'qwen3.5-0.8b-single': 3, 'qwen3.5-2b-mixed': 4, 'qwen3.5-2b-single': 3}

## Intent mistakes

- **qwen3.5-0.8b-single:** UNKNOWN → SMALL_TALK ×4; OUT_OF_SCOPE → MENU_QUESTION ×3; MODIFY_ORDER → PLACE_ORDER ×3; PAYMENT_CLAIM → PLACE_ORDER ×2; SMALL_TALK → MODIFY_ORDER ×1; PLACE_ORDER → SMALL_TALK ×1; HUMAN_REQUEST → PLACE_ORDER ×1; MODIFY_ORDER → SMALL_TALK ×1; OUT_OF_SCOPE → HUMAN_REQUEST ×1; PLACE_ORDER → None ×1; MODIFY_ORDER → None ×1; SMALL_TALK → MENU_QUESTION ×1; SMALL_TALK → PLACE_ORDER ×1; PLACE_ORDER → MENU_QUESTION ×1; ORDER_PROBLEM → ORDER_STATUS ×1; HUMAN_REQUEST → ORDER_PROBLEM ×1
- **qwen3.5-2b-single:** PLACE_ORDER → None ×9; MODIFY_ORDER → PLACE_ORDER ×4; UNKNOWN → SMALL_TALK ×3; OUT_OF_SCOPE → DELIVERY_QUESTION ×2; PLACE_ORDER → UNKNOWN ×2; MODIFY_ORDER → None ×2; MENU_QUESTION → UNKNOWN ×1; HUMAN_REQUEST → None ×1; PLACE_ORDER → SMALL_TALK ×1; PAYMENT_CLAIM → ORDER_PROBLEM ×1; SMALL_TALK → PLACE_ORDER ×1; MENU_QUESTION → None ×1; OUT_OF_SCOPE → MENU_QUESTION ×1; OUT_OF_SCOPE → SMALL_TALK ×1; PLACE_ORDER → MENU_QUESTION ×1; ORDER_PROBLEM → ORDER_STATUS ×1
- **qwen3.5-2b-mixed:** PLACE_ORDER → None ×8; MODIFY_ORDER → PLACE_ORDER ×5; UNKNOWN → SMALL_TALK ×3; PLACE_ORDER → UNKNOWN ×2; PLACE_ORDER → MENU_QUESTION ×2; HUMAN_REQUEST → None ×1; HUMAN_REQUEST → SMALL_TALK ×1; PLACE_ORDER → SMALL_TALK ×1; PAYMENT_CLAIM → ORDER_PROBLEM ×1; SMALL_TALK → PLACE_ORDER ×1; OUT_OF_SCOPE → MENU_QUESTION ×1; ORDER_PROBLEM → ORDER_STATUS ×1
- **teacher:** PLACE_ORDER → None ×4; PLACE_ORDER → SMALL_TALK ×2; CONFIRM_ORDER → None ×1; MODIFY_ORDER → None ×1; UNKNOWN → SMALL_TALK ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-dev-001#0 | hey is this the bakery on 5th that does the custom bday cakes? need one for sat | OUT_OF_SCOPE | qwen3.5-0.8b-single: MENU_QUESTION, qwen3.5-2b-single: DELIVERY_QUESTION |
| a-dev-001#2 | oh my bad wrong numbr lol do u kno their # by any chance | OUT_OF_SCOPE | qwen3.5-2b-single: DELIVERY_QUESTION |
| a-dev-005#0 | . | UNKNOWN | qwen3.5-0.8b-single: SMALL_TALK, qwen3.5-2b-single: SMALL_TALK, qwen3.5-2b-mixed: SMALL_TALK |
| a-dev-006#1 | n a chicken tikka masala | PLACE_ORDER | qwen3.5-2b-single: UNKNOWN, qwen3.5-2b-mixed: UNKNOWN |
| a-dev-006#2 | and breadstiks | PLACE_ORDER | qwen3.5-2b-single: None |
| a-dev-006#3 | deliver to 9 oak ct pls | PLACE_ORDER | qwen3.5-2b-single: None |
| a-dev-007#3 | ok add one of those no mayo 👍 delivery to 25 Cedar Ln, card 💳 | PLACE_ORDER | qwen3.5-2b-mixed: None |
| a-dev-010#1 | or still just s m l | MENU_QUESTION | qwen3.5-2b-single: UNKNOWN |
| a-dev-011#0 | lemme get a numbr 1 combo w fries, payin cash | PLACE_ORDER | qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |
| a-dev-014#2 | oof thats more than i thoght | SMALL_TALK | qwen3.5-0.8b-single: MODIFY_ORDER |
| a-dev-016#3 | OK I'LL TAKE THAT ONE | PLACE_ORDER | qwen3.5-0.8b-single: SMALL_TALK |
| a-dev-016#4 | AND MAKE THE LATTE OAT MILK PLEASE | MODIFY_ORDER | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: PLACE_ORDER, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-020#0 | hey need lunch for the office | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-020#2 | 2 no pickles | PLACE_ORDER | qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |
| a-dev-020#3 | 3 lg fries n 4 cokes | PLACE_ORDER | qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |
| a-dev-020#4 | pickup at 12:30 | PLACE_ORDER | qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |
| a-dev-020#5 | wait actually can u deliver instead to 200 park ave 5th fl, card | MODIFY_ORDER | qwen3.5-2b-single: None |
| a-dev-021#0 | Hi, I'm organizing a dorm event next Friday and need about 30 large pizzas. Can I talk to a manager about a catering ord | HUMAN_REQUEST | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |
| a-dev-021#2 | Yes, please have them message me here. Thanks! | HUMAN_REQUEST | qwen3.5-2b-mixed: SMALL_TALK |
| a-dev-023#0 | hi need 2 large cheese pizzas | PLACE_ORDER | teacher: None |
| a-dev-023#1 | n a 2 liter coke | PLACE_ORDER | teacher: None |
| a-dev-023#2 | delivery to 140 river rd | PLACE_ORDER | teacher: None |
| a-dev-023#3 | card | PLACE_ORDER | teacher: None |
| a-dev-023#5 | yep | CONFIRM_ORDER | teacher: None |
| a-dev-023#6 | wait sry its 104 river rd not 140 | MODIFY_ORDER | qwen3.5-0.8b-single: SMALL_TALK, teacher: None |
| a-dev-031#0 | hey r u guys hiring? just moved here n lookin for weekend shifts | OUT_OF_SCOPE | qwen3.5-0.8b-single: HUMAN_REQUEST |
| a-dev-032#4 | 👍 SOUNDS GOOD | UNKNOWN | qwen3.5-0.8b-single: SMALL_TALK, qwen3.5-2b-single: SMALL_TALK, qwen3.5-2b-mixed: SMALL_TALK, teacher: SMALL_TALK |
| a-dev-035#2 | make the fries large | MODIFY_ORDER | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: PLACE_ORDER, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-037#0 | ok so the uhh 🤔 w tht | UNKNOWN | qwen3.5-0.8b-single: SMALL_TALK, qwen3.5-2b-single: SMALL_TALK, qwen3.5-2b-mixed: SMALL_TALK |
| a-dev-038#0 | hey can i get the same as last time | PLACE_ORDER | qwen3.5-2b-single: UNKNOWN, qwen3.5-2b-mixed: UNKNOWN |
| a-dev-040#1 | can I get the usual 😎 | PLACE_ORDER | qwen3.5-2b-single: SMALL_TALK, qwen3.5-2b-mixed: SMALL_TALK |
| a-dev-040#4 | oh and make the fries large 🍟 | MODIFY_ORDER | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: PLACE_ORDER, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-046#1 | n a hawaiian | PLACE_ORDER | qwen3.5-2b-single: None |
| a-dev-046#2 | pickup, card | PLACE_ORDER | qwen3.5-2b-single: None |
| a-dev-049#2 | OK ONE CHOCOLATE AND ONE OF THE OTHER ONE | PLACE_ORDER | qwen3.5-2b-mixed: MENU_QUESTION |
| a-dev-049#3 | ACTUALLY SWAP THE CHOCOLATE FOR A LEMONADE. AND 2 CHEESEBURGERS. CASH | MODIFY_ORDER | qwen3.5-2b-single: PLACE_ORDER, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-056#0 | hi! I ordered a latte + croissant for pickup a few min ago, name's Priya 😊 already paid when I called it in 💳✅ | PAYMENT_CLAIM | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: ORDER_PROBLEM, qwen3.5-2b-mixed: ORDER_PROBLEM |
| a-dev-057#1 | deliver to 31 college ave dorm b rm 210, cash 💵 | PLACE_ORDER | qwen3.5-0.8b-single: None |
| a-dev-059#4 | oh wait can u add a strawberry shake for my daughter 🍓 | MODIFY_ORDER | qwen3.5-0.8b-single: None, qwen3.5-2b-single: None, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-060#0 | just wanted to say thx for making my latte w oat milk perfectly today 🥰 so hard to find dairy free spots | SMALL_TALK | qwen3.5-0.8b-single: MENU_QUESTION |
| a-dev-074#0 | hey ordering for the office | SMALL_TALK | qwen3.5-0.8b-single: PLACE_ORDER, qwen3.5-2b-single: PLACE_ORDER, qwen3.5-2b-mixed: PLACE_ORDER |
| a-dev-074#1 | 3 bec on bagels n 2 plain croissants, do the croissants come warm? | PLACE_ORDER | qwen3.5-0.8b-single: MENU_QUESTION |
| a-dev-079#1 | WAIT HOW BIG IS THE XL | MENU_QUESTION | qwen3.5-2b-single: None |
| a-dev-079#3 | OK DELIVER TO 5 ASPEN DR, CARD | PLACE_ORDER | qwen3.5-2b-mixed: None |
| a-dev-082#0 | Random question, but who invented the cheeseburger? | OUT_OF_SCOPE | qwen3.5-0.8b-single: MENU_QUESTION, qwen3.5-2b-single: MENU_QUESTION, qwen3.5-2b-mixed: MENU_QUESTION |
| a-dev-082#2 | Lol fair. Also what's the capital of Australia? It's for a bet. | OUT_OF_SCOPE | qwen3.5-0.8b-single: MENU_QUESTION, qwen3.5-2b-single: SMALL_TALK |
| a-dev-085#0 | lg pepperoni to 300 university dr, n do u have anything sweet? | PLACE_ORDER | qwen3.5-2b-single: MENU_QUESTION, qwen3.5-2b-mixed: None |
| a-dev-085#2 | ok a 2 liter dr pepper then. n smth to snack on, wat do u recommend | PLACE_ORDER | qwen3.5-2b-mixed: MENU_QUESTION |
| a-dev-086#0 | 4417 PLEASE | UNKNOWN | qwen3.5-0.8b-single: SMALL_TALK |
| a-dev-088#2 | It was under Whitfield, a large Hawaiian 🍍 | ORDER_PROBLEM | qwen3.5-0.8b-single: ORDER_STATUS, qwen3.5-2b-single: ORDER_STATUS, qwen3.5-2b-mixed: ORDER_STATUS |
| a-dev-089#0 | hey big ordr for pickup | PLACE_ORDER | teacher: SMALL_TALK |
| a-dev-089#3 | already sent the payment, i have a screenshot if u need it | PAYMENT_CLAIM | qwen3.5-0.8b-single: PLACE_ORDER |
| a-dev-090#0 | this bot keeps getting my order wrong, i said NO cheese like 3 times. let me talk to a real person pls | HUMAN_REQUEST | qwen3.5-0.8b-single: ORDER_PROBLEM |
| a-dev-091#0 | can i get something warm to drink 🥶 nothing w coffee tho | PLACE_ORDER | qwen3.5-2b-single: None, qwen3.5-2b-mixed: None |

## Order mistakes, chat by chat

### a-dev-006 (off_menu)
- **qwen3.5-2b-single:** invalid: order.items.0: Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4)

### a-dev-008 (multi_message_order, small_talk)
- **qwen3.5-2b-single:** modifications: gold 1× cappuccino, medium, substitute whole_milk | pred 1× cappuccino, medium, add almond_milk

### a-dev-011 (combo, missing_info) — **all students**
- **qwen3.5-0.8b-single:** combo_picks: gold 1× cheeseburger_combo, side=fries | pred 1× cheeseburger_combo, side=fries, drink=coke; missing: gold ((('combo_choice', 'missing'), 1), (('fulfillment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)
- **qwen3.5-2b-single:** invalid: order.items.0.combo_selections.1.menu_item_id: Input should be a valid string
- **qwen3.5-2b-mixed:** invalid: order.items.0.combo_selections.1.menu_item_id: Input should be a valid string

### a-dev-014 (cancellation)
- **qwen3.5-2b-single:** method: gold pickup | pred unknown; address: gold not_applicable | pred not_mentioned

### a-dev-016 (ambiguous_reference, menu_question) — **all students**
- **qwen3.5-0.8b-single:** modifications: gold 1× latte, large, add vanilla_syrup, substitute whole_milk | pred 1× latte, large, add oat_milk; missing 1× off-menu 'THAT ONE'; time: gold ('provided', 'clock_time', '08:00') | pred ('provided', 'clock_time', None); missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)
- **qwen3.5-2b-single:** modifications: gold 1× latte, large, add vanilla_syrup, substitute whole_milk | pred 1× latte, large, substitute whole_milk; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-2b-mixed:** missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))

### a-dev-017 (half_and_half) — **all students**
- **qwen3.5-0.8b-single:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× half mushroom_pizza / sausage_pizza, extra_large; payment: gold ('card', None, False) | pred ('unknown', None, False); missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-2b-single:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× half mushroom / olives, extra_large; payment: gold ('card', None, False) | pred ('unknown', None, False); missing: gold ((('fulfillment_method', 'missing'), 1),) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-2b-mixed:** missing 1× half cheese_pizza / cheese_pizza, extra_large; extra 1× half mushroom / olives, extra_large

### a-dev-019 (correction) — **all students**
- **qwen3.5-0.8b-single:** extra 1× muffin, chocolate_chip
- **qwen3.5-2b-single:** extra 1× muffin, chocolate_chip, remove remove the muffin; time: gold ('provided', 'clock_time', '10:30') | pred ('provided', 'clock_time', None); missing: gold () | pred ((('item_modification', 'ambiguous'), 1),)
- **qwen3.5-2b-mixed:** extra 1× muffin, chocolate_chip, remove muffin

### a-dev-020 (correction, multi_message_order) — **all students**
- **qwen3.5-0.8b-single:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove pickle; missing 2× cheeseburger, single, remove pickle
- **qwen3.5-2b-single:** invalid: order.items.1: Value error, L2: an off-menu item can't have variant, modifications or combo picks
- **qwen3.5-2b-mixed:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove pickle; missing 2× cheeseburger, single, remove pickle

### a-dev-022 (simple_order)
- **qwen3.5-2b-single:** quantity+variant: gold 1× cheeseburger, double, remove onion | pred 2× cheeseburger, single, remove onion; missing 1× fries, large
- **qwen3.5-2b-mixed:** quantity+variant: gold 1× cheeseburger, double, remove onion | pred 2× cheeseburger, single, remove onion

### a-dev-023 (correction_after_confirmation, contextual_yes)
- **teacher:** invalid: 1 validation error for TeacherLabel
order.customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pending', 'agr...x': 5, 'quote': 'yep'}]}, input_type=dict]
    For further informati

### a-dev-028 (simple_order)
- **qwen3.5-0.8b-single:** modifications: gold 1× latte, large, substitute whole_milk | pred 1× latte, large, add oat_milk; time: gold ('provided', 'clock_time', '09:30') | pred ('provided', 'clock_time', None)

### a-dev-034 (off_menu) — **all students**
- **qwen3.5-0.8b-single:** modifications: gold 1× supreme_pizza, large, add with artichoke hearts | pred 1× supreme_pizza, large, add artichoke_hearts; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ()
- **qwen3.5-2b-single:** modifications: gold 1× supreme_pizza, large, add with artichoke hearts | pred 1× supreme_pizza, large, add unknown; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ()
- **qwen3.5-2b-mixed:** modifications: gold 1× supreme_pizza, large, add with artichoke hearts | pred 1× supreme_pizza, large, add anchovies; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ()

### a-dev-038 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single:** variant: gold 1× pepperoni_pizza, medium | pred 1× pepperoni_pizza, large; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ((('item_menu_match', 'off_menu'), 1),)
- **qwen3.5-2b-single:** variant: gold 1× pepperoni_pizza, medium | pred 1× pepperoni_pizza, large; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ((('item_menu_match', 'off_menu'), 1),)
- **qwen3.5-2b-mixed:** variant: gold 1× pepperoni_pizza, medium | pred 1× pepperoni_pizza, large; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ((('item_menu_match', 'off_menu'), 1),)

### a-dev-039 (contextual_yes) — **all students**
- **qwen3.5-0.8b-single:** payment: gold ('card', None, False) | pred ('unknown', None, False); decision: gold ('confirmed', False) | pred ('pending', True); missing: gold () | pred ((('payment_method', 'missing'), 1),)
- **qwen3.5-2b-single:** modifications: gold 1× americano, medium, add almond_milk | pred 1× americano, medium, substitute whole_milk
- **qwen3.5-2b-mixed:** modifications: gold 1× americano, medium, add almond_milk | pred 1× americano, medium, substitute whole_milk

### a-dev-042 (simple_order, two_requests, menu_question)
- **qwen3.5-0.8b-single:** variant: gold 1× diet_coke, bottle_20oz | pred 1× diet_coke, can
- **qwen3.5-2b-mixed:** variant: gold 1× diet_coke, bottle_20oz | pred 1× diet_coke, can

### a-dev-045 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()
- **qwen3.5-2b-single:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()
- **qwen3.5-2b-mixed:** quantity: gold None× garlic_knots | pred 1× garlic_knots; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-dev-046 (missing_info)
- **qwen3.5-2b-single:** invalid: order.items.0: Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4)

### a-dev-048 (simple_order, menu_question)
- **qwen3.5-0.8b-single:** missing 1× breakfast_sandwich, croissant; extra 1× croissant, plain, add began

### a-dev-049 (ambiguous_reference, menu_question, correction) — **all students**
- **qwen3.5-0.8b-single:** missing 1× milkshake; variant: gold 1× lemonade | pred 1× lemonade, chocolate; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)
- **qwen3.5-2b-single:** missing 1× milkshake; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)
- **qwen3.5-2b-mixed:** missing 1× milkshake; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-050 (two_requests)
- **qwen3.5-2b-single:** missing 1× latte, medium, add caramel_syrup
- **qwen3.5-2b-mixed:** missing 1× latte, medium, add caramel_syrup

### a-dev-059 (correction_after_confirmation, contextual_yes, small_talk)
- **qwen3.5-0.8b-single:** invalid: order.items.3: Value error, L4: an off-menu item can't have variant, modifications or combo picks
- **qwen3.5-2b-single:** invalid: order.items.3: Value error, L4: an off-menu item can't have variant, modifications or combo picks

### a-dev-061 (off_menu)
- **qwen3.5-2b-single:** missing 1× off-menu 'Mountain Dew'; extra 1× dr_pepper, can; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ()
- **qwen3.5-2b-mixed:** missing 1× off-menu 'Mountain Dew'; extra 1× sprite, can; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ()

### a-dev-062 (correction)
- **qwen3.5-2b-mixed:** missing 1× muffin, chocolate_chip; extra 1× croissant, plain

### a-dev-063 (simple_order) — **all students**
- **qwen3.5-0.8b-single:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove onion; missing 2× cheeseburger, single, remove onion
- **qwen3.5-2b-single:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove onion; missing 2× cheeseburger, single, remove onion
- **qwen3.5-2b-mixed:** quantity+modifications: gold 2× cheeseburger, single | pred 4× cheeseburger, single, remove onion; missing 2× cheeseburger, single, remove onion

### a-dev-064 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single:** payment: gold ('card', None, False) | pred ('cash', None, False)
- **qwen3.5-2b-single:** payment: gold ('card', None, False) | pred ('cash', None, False)
- **qwen3.5-2b-mixed:** payment: gold ('card', None, False) | pred ('cash', None, False)

### a-dev-065 (correction)
- **qwen3.5-2b-single:** missing 1× drip_coffee, medium; extra 1× off-menu 'Drip Coffee'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1),)

### a-dev-066 (multi_message_order)
- **qwen3.5-0.8b-single:** time: gold ('provided', 'clock_time', '21:45') | pred ('provided', 'clock_time', '09:45')
- **qwen3.5-2b-single:** time: gold ('provided', 'clock_time', '21:45') | pred ('provided', 'clock_time', '09:45')

### a-dev-067 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single:** variant: gold 1× cheeseburger, double | pred 1× cheeseburger, single
- **qwen3.5-2b-single:** variant+modifications: gold 1× cheeseburger, double | pred 1× cheeseburger, single, add cheese
- **qwen3.5-2b-mixed:** variant: gold 1× cheeseburger, double | pred 1× cheeseburger, single

### a-dev-068 (simple_order, menu_question)
- **qwen3.5-2b-single:** variant+modifications: gold 1× meat_lovers_pizza, large, add crust_stuffed | pred 1× meat_lovers_pizza, extra_large

### a-dev-071 (multi_message_order, small_talk) — **all students**
- **qwen3.5-0.8b-single:** modifications: gold 1× margherita_pizza, medium | pred 1× margherita_pizza, medium, add cheese; modifications: gold 1× pepperoni_pizza, personal, add cheese | pred 1× pepperoni_pizza, personal
- **qwen3.5-2b-single:** modifications: gold 1× pepperoni_pizza, personal, add cheese | pred 1× pepperoni_pizza, personal, add cheese
- **qwen3.5-2b-mixed:** modifications: gold 1× margherita_pizza, medium | pred 1× margherita_pizza, medium, add cheese; modifications: gold 1× pepperoni_pizza, personal, add cheese | pred 1× pepperoni_pizza, personal

### a-dev-072 (payment_claim, small_talk)
- **qwen3.5-0.8b-single:** payment: gold ('unknown', None, True) | pred ('cash', None, True)

### a-dev-073 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single:** time: gold ('provided', 'clock_time', '22:30') | pred ('provided', 'clock_time', '10:30')
- **qwen3.5-2b-single:** time: gold ('provided', 'clock_time', '22:30') | pred ('provided', 'clock_time', '10:00')
- **qwen3.5-2b-mixed:** time: gold ('provided', 'clock_time', '22:30') | pred ('provided', 'clock_time', '10:30')

### a-dev-074 (two_requests, menu_question, multi_message_order) — **all students**
- **qwen3.5-0.8b-single:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; missing 2× latte, medium, substitute whole_milk; extra 3× bagel, everything; extra 2× oat_milk_latte, medium
- **qwen3.5-2b-single:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; modifications: gold 2× latte, medium, substitute whole_milk | pred 2× latte, medium; extra 3× bagel, bagel
- **qwen3.5-2b-mixed:** missing 3× breakfast_sandwich, bagel; modifications: gold 2× croissant, plain, add warm | pred 2× croissant, plain; modifications: gold 2× latte, medium, substitute whole_milk | pred 2× latte, medium; extra 3× bagel, bagel

### a-dev-075 (multi_message_order)
- **qwen3.5-0.8b-single:** payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)
- **qwen3.5-2b-single:** payment: gold ('cash', 20000, False) | pred ('cash', 2000, False)

### a-dev-079 (off_menu, menu_question)
- **qwen3.5-2b-single:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, extra_large; missing 2× cheese_pizza, extra_large; extra 2× off-menu 'CHEESE'; payment: gold ('card', None, False) | pred ('unknown', None, False); missing: gold ((('item_variant', 'missing'), 1),) | pred ((('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-2b-mixed:** invalid: order.items.1: Value error, L2: an off-menu item can't have variant, modifications or combo picks

### a-dev-083 (implicit_category, small_talk, multi_message_order) — **all students**
- **qwen3.5-0.8b-single:** missing 1× cappuccino, large; missing 1× muffin, blueberry; missing 1× bagel, everything, add cream_cheese
- **qwen3.5-2b-single:** missing 1× cappuccino, large; missing 1× muffin, blueberry; missing 1× bagel, everything, add cream_cheese; variant: gold 1× croissant, chocolate | pred 1× croissant, plain
- **qwen3.5-2b-mixed:** missing 1× cappuccino, large; missing 1× muffin, blueberry; missing 1× bagel, everything, add cream_cheese; variant: gold 1× croissant, chocolate | pred 1× croissant, plain

### a-dev-084 (implicit_category, menu_question)
- **qwen3.5-0.8b-single:** missing 1× coke; extra 1× off-menu 'pop'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1),)
- **qwen3.5-2b-mixed:** missing 1× coke; extra 1× off-menu 'pop'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1),)

### a-dev-085 (implicit_category, two_requests, menu_question) — **all students**
- **qwen3.5-0.8b-single:** missing 1× pepperoni_pizza, large; missing 1× garlic_knots; extra 1× off-menu 'garlic knots'; method: gold delivery | pred unknown; address: gold provided | pred not_mentioned; payment: gold ('card', None, False) | pred ('unknown', None, False); missing: gold () | pred ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))
- **qwen3.5-2b-single:** missing 1× pepperoni_pizza, large; method: gold delivery | pred unknown; missing: gold () | pred ((('fulfillment_method', 'missing'), 1),)
- **qwen3.5-2b-mixed:** missing 1× pepperoni_pizza, large; method: gold delivery | pred unknown; missing: gold () | pred ((('fulfillment_method', 'missing'), 1),)

### a-dev-089 (payment_claim, multi_message_order) — **all students**
- **qwen3.5-0.8b-single:** payment: gold ('unknown', None, True) | pred ('cash', None, True)
- **qwen3.5-2b-single:** missing 2× cheese_pizza, extra_large; time: gold ('provided', 'clock_time', '17:00') | pred ('provided', 'clock_time', '17:05')
- **qwen3.5-2b-mixed:** missing 2× cheese_pizza, extra_large

