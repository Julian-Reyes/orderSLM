# M6 error review on fresh

Every chat or customer message a model got wrong, from saved outputs. Fresh is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v2 |
|---|---|
| chats not fully right (of 90) | 21 |
| · fields only | 1 |
| · invalid answer | 3 |
| · item mistakes | 17 |
| item: wrong_quantity | 7 |
| item: extra_item | 6 |
| item: wrong_modifications | 4 |
| item: missing_item | 4 |
| item: wrong_variant | 3 |
| field: missing | 10 |
| field: time | 1 |
| intents wrong (of 278) | 22 |

Overlap: {'chats_all_students_wrong': 21, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 21, 'messages_all_students_wrong': 22, 'messages_one_student_only': 22}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v2': 1}
- combo: {'qwen3.5-0.8b-single-v2': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v2': 1}
- correction: {'qwen3.5-0.8b-single-v2': 4}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v2': 1}
- missing_info: {'qwen3.5-0.8b-single-v2': 5}
- multi_message_order: {'qwen3.5-0.8b-single-v2': 1}
- off_menu: {'qwen3.5-0.8b-single-v2': 2}
- simple_order: {'qwen3.5-0.8b-single-v2': 5}
- small_talk: {'qwen3.5-0.8b-single-v2': 3}
- unclear_message: {'qwen3.5-0.8b-single-v2': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v2:** PLACE_ORDER → None ×6; PLACE_ORDER → SMALL_TALK ×5; DELIVERY_QUESTION → OUT_OF_SCOPE ×2; UNKNOWN → SMALL_TALK ×1; SMALL_TALK → UNKNOWN ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; MODIFY_ORDER → PLACE_ORDER ×1; PLACE_ORDER → ORDER_STATUS ×1; ORDER_PROBLEM → REFUND_REQUEST ×1; MODIFY_ORDER → None ×1; UNKNOWN → PLACE_ORDER ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh-006#0 | hey 🌙 just got off my shift, ordering for the crew | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-012#0 | ] | UNKNOWN | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-023#1 | random q | SMALL_TALK | qwen3.5-0.8b-single-v2: UNKNOWN |
| a-fresh-025#0 | GOOD AFTERNOON! I WOULD LIKE TO ORDER FOR MY GRANDCHILDREN | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-032#0 | Hello, I'm putting together a lunch order for my team. | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-034#1 | No onions on the burger, please. | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-034#2 | Delivery to 415 Carver St. | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-034#3 | I'll pay by card. | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-037#0 | hey! 🚗 grabbing stuff for the office on my way in | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-043#0 | hi do u guys have spicy stuff | MENU_QUESTION | qwen3.5-0.8b-single-v2: OUT_OF_SCOPE |
| a-fresh-047#2 | CAN U DELIVER IT | DELIVERY_QUESTION | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-fresh-048#0 | HEY DO YOU GUYS DELIVER TO THE DORMS ON CAMPUS?? | DELIVERY_QUESTION | qwen3.5-0.8b-single-v2: OUT_OF_SCOPE |
| a-fresh-048#1 | LIKE WESTFIELD HALL | DELIVERY_QUESTION | qwen3.5-0.8b-single-v2: OUT_OF_SCOPE |
| a-fresh-053#5 | oh can i add garlic knots too | MODIFY_ORDER | qwen3.5-0.8b-single-v2: PLACE_ORDER |
| a-fresh-059#2 | Right, it was a large Hawaiian and some breadsticks. | PLACE_ORDER | qwen3.5-0.8b-single-v2: ORDER_STATUS |
| a-fresh-061#0 | hi ordering for my study group | PLACE_ORDER | qwen3.5-0.8b-single-v2: SMALL_TALK |
| a-fresh-069#0 | Hello, my delivery came but the onion rings I paid for never arrived. Could I get a refund for them? | ORDER_PROBLEM | qwen3.5-0.8b-single-v2: REFUND_REQUEST |
| a-fresh-074#1 | 3 BACON BURGERS WITH BBQ SAUCE AND 3 LEMONADES | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-074#2 | PICKUP AT 12:45, PAYING BY CARD!! | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-084#7 | actually could u deliver it instead, to 18 primrose ln | MODIFY_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-084#8 | cash pls | PLACE_ORDER | qwen3.5-0.8b-single-v2: None |
| a-fresh-087#3 | oh right its the bac | UNKNOWN | qwen3.5-0.8b-single-v2: PLACE_ORDER |

## Order mistakes, chat by chat

### a-fresh-007 (simple_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold 1× hot_chocolate, large | pred 3× hot_chocolate, large

### a-fresh-009 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 1× margherita_pizza | pred 1× margherita_pizza, large; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-016 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 1× muffin, banana_nut | pred 1× muffin, chocolate_chip; missing 1× latte, large, substitute whole_milk

### a-fresh-024 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v2:** time: gold ('provided', 'clock_time', '11:30') | pred ('provided', 'clock_time', '11:00')

### a-fresh-034 (combo) — **all students**
- **qwen3.5-0.8b-single-v2:** invalid: order.items.0.combo_selections.0.raw_text: Extra inputs are not permitted

### a-fresh-037 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v2:** modifications: gold 1× americano, large | pred 1× americano, large, add black; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1), (('payment_method', 'missing'), 1))

### a-fresh-039 (correction) — **all students**
- **qwen3.5-0.8b-single-v2:** extra 1× coke

### a-fresh-043 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold 2× veggie_burger | pred 4× veggie_burger

### a-fresh-044 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold None× muffin, blueberry | pred 2× muffin, blueberry; modifications: gold 1× drip_coffee, medium, add almond_milk | pred 1× drip_coffee, medium, substitute whole_milk; missing: gold ((('item_quantity', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-051 (correction) — **all students**
- **qwen3.5-0.8b-single-v2:** extra 1× muffin, chocolate_chip

### a-fresh-056 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold None× onion_rings | pred 1× onion_rings; missing: gold ((('item_quantity', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-057 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold 3× bacon_burger | pred 2× bacon_burger; missing 1× off-menu 'one of them'; extra 1× bacon_burger; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ()

### a-fresh-063 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v2:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-065 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold 1× dr_pepper, two_liter | pred 2× dr_pepper, two_liter

### a-fresh-066 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× breakfast_sandwich, croissant; modifications: gold 1× americano, large, add oat_milk | pred 1× americano, large, substitute whole_milk; extra 1× croissant; missing: gold () | pred ((('item_variant', 'missing'), 1),)

### a-fresh-073 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v2:** extra 1× milkshake, vanilla

### a-fresh-074 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v2:** invalid: order.items.0.modifications.0: Value error, not_on_menu/kitchen_note only for a request with no catalog id

### a-fresh-080 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v2:** modifications: gold 1× veggie_pizza, large, remove cheese, add VEGAN CHEESE | pred 1× veggie_pizza, large, remove cheese, substitute cheese; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-fresh-084 (correction) — **all students**
- **qwen3.5-0.8b-single-v2:** invalid: order: Value error, address must be not_applicable for pickup

### a-fresh-087 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v2:** missing 1× off-menu 'the usual'; extra 1× bacon_burger; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-089 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v2:** quantity: gold None× muffin, chocolate_chip | pred 2× muffin, chocolate_chip; missing: gold ((('item_quantity', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

