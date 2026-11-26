# M6 error review on fresh

Every chat or customer message a model got wrong, from saved outputs. Fresh is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v6 |
|---|---|
| chats not fully right (of 90) | 11 |
| · fields only | 1 |
| · invalid answer | 2 |
| · item mistakes | 8 |
| item: missing_item | 4 |
| item: wrong_variant | 2 |
| item: wrong_quantity | 1 |
| item: wrong_modifications | 1 |
| item: extra_item | 1 |
| field: missing | 7 |
| field: time | 1 |
| intents wrong (of 278) | 16 |

Overlap: {'chats_all_students_wrong': 11, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 11, 'messages_all_students_wrong': 16, 'messages_one_student_only': 16}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v6': 2}
- correction: {'qwen3.5-0.8b-single-v6': 1}
- missing_info: {'qwen3.5-0.8b-single-v6': 2}
- off_menu: {'qwen3.5-0.8b-single-v6': 3}
- simple_order: {'qwen3.5-0.8b-single-v6': 2}
- small_talk: {'qwen3.5-0.8b-single-v6': 1}
- unclear_message: {'qwen3.5-0.8b-single-v6': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v6:** PLACE_ORDER → None ×4; PLACE_ORDER → MENU_QUESTION ×3; SMALL_TALK → PLACE_ORDER ×2; SMALL_TALK → UNKNOWN ×2; PLACE_ORDER → SMALL_TALK ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; PLACE_ORDER → ORDER_PROBLEM ×1; ORDER_PROBLEM → REFUND_REQUEST ×1; SMALL_TALK → MENU_QUESTION ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh-004#1 | party at my place tonight | SMALL_TALK | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh-009#0 | good afternoon, id like to order one of the big margheritas pls, and could u tell me if the margherita has fresh mozzare | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh-013#0 | hey! | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh-017#3 | and garlic knots, do u take apple pay? | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh-023#1 | random q | SMALL_TALK | qwen3.5-0.8b-single-v6: UNKNOWN |
| a-fresh-037#0 | hey! 🚗 grabbing stuff for the office on my way in | PLACE_ORDER | qwen3.5-0.8b-single-v6: SMALL_TALK |
| a-fresh-046#1 | party tmrw | SMALL_TALK | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh-047#2 | CAN U DELIVER IT | DELIVERY_QUESTION | qwen3.5-0.8b-single-v6: PLACE_ORDER |
| a-fresh-056#0 | hi! 😊 are the onion rings homemade? either way can i get some onion rings and a veggie burger delivered to 92 kent ave 🙏 | PLACE_ORDER | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh-059#2 | Right, it was a large Hawaiian and some breadsticks. | PLACE_ORDER | qwen3.5-0.8b-single-v6: ORDER_PROBLEM |
| a-fresh-069#0 | Hello, my delivery came but the onion rings I paid for never arrived. Could I get a refund for them? | ORDER_PROBLEM | qwen3.5-0.8b-single-v6: REFUND_REQUEST |
| a-fresh-080#0 | HI! I'M VEGAN | SMALL_TALK | qwen3.5-0.8b-single-v6: MENU_QUESTION |
| a-fresh-080#1 | CAN I GET A LARGE VEGGIE PIZZA WITH NO CHEESE AND VEGAN CHEESE INSTEAD? | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh-080#2 | AND A BOTTLED WATER | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh-080#3 | PAYING CASH! | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |
| a-fresh-084#8 | cash pls | PLACE_ORDER | qwen3.5-0.8b-single-v6: None |

## Order mistakes, chat by chat

### a-fresh-009 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× margherita_pizza; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-025 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v6:** variant: gold 2× cheeseburger, single | pred 2× cheeseburger, double

### a-fresh-049 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× off-menu 'a red bull'; extra 1× drip_coffee, medium; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ()

### a-fresh-054 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v6:** time: gold ('provided', 'clock_time', '21:30', None) | pred ('provided', 'clock_time', '21:30', ('tomorrow', None, None, None))

### a-fresh-057 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× off-menu 'one of them'; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ()

### a-fresh-059 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v6:** quantity: gold None× breadsticks | pred 1× breadsticks; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-fresh-063 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v6:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-074 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v6:** modifications: gold 3× bacon_burger, add BBQ SAUCE | pred 3× bacon_burger, add WITH BBQ SAUCE; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh-080 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order.items.0.modifications.1: Value error, not_on_menu/kitchen_note only for a request with no catalog id

### a-fresh-084 (correction) — **all students**
- **qwen3.5-0.8b-single-v6:** invalid: order: Value error, address must be not_applicable for pickup

### a-fresh-087 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v6:** missing 1× off-menu 'the usual'; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

