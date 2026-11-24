# M6 error review on fresh

Every chat or customer message a model got wrong, from saved outputs. Fresh is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v5 |
|---|---|
| chats not fully right (of 90) | 9 |
| · fields only | 1 |
| · item mistakes | 7 |
| · items where there is no order | 1 |
| item: missing_item | 3 |
| item: wrong_quantity | 2 |
| item: extra_item | 1 |
| item: wrong_modifications | 1 |
| item: wrong_variant | 1 |
| field: missing | 7 |
| intents wrong (of 278) | 11 |

Overlap: {'chats_all_students_wrong': 9, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 9, 'messages_all_students_wrong': 11, 'messages_one_student_only': 11}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v5': 2}
- missing_info: {'qwen3.5-0.8b-single-v5': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v5': 1}
- off_menu: {'qwen3.5-0.8b-single-v5': 1}
- refund_request: {'qwen3.5-0.8b-single-v5': 1}
- simple_order: {'qwen3.5-0.8b-single-v5': 1}
- small_talk: {'qwen3.5-0.8b-single-v5': 1}
- unclear_message: {'qwen3.5-0.8b-single-v5': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v5:** UNKNOWN → SMALL_TALK ×3; SMALL_TALK → PLACE_ORDER ×2; PLACE_ORDER → None ×2; SMALL_TALK → UNKNOWN ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; ORDER_PROBLEM → REFUND_REQUEST ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh-004#1 | party at my place tonight | SMALL_TALK | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh-008#1 | 47 | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh-012#0 | ] | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh-023#1 | random q | SMALL_TALK | qwen3.5-0.8b-single-v5: UNKNOWN |
| a-fresh-032#1 | ? | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh-043#0 | hi do u guys have spicy stuff | MENU_QUESTION | qwen3.5-0.8b-single-v5: OUT_OF_SCOPE |
| a-fresh-046#1 | party tmrw | SMALL_TALK | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh-047#2 | CAN U DELIVER IT | DELIVERY_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh-057#2 | ok 2 bacon burgers n one of them pls, pickup | PLACE_ORDER | qwen3.5-0.8b-single-v5: None |
| a-fresh-057#3 | card | PLACE_ORDER | qwen3.5-0.8b-single-v5: None |
| a-fresh-069#0 | Hello, my delivery came but the onion rings I paid for never arrived. Could I get a refund for them? | ORDER_PROBLEM | qwen3.5-0.8b-single-v5: REFUND_REQUEST |

## Order mistakes, chat by chat

### a-fresh-009 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v5:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-037 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× americano, large | pred 1× americano, large, substitute whole_milk; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'ambiguous'), 1), (('payment_method', 'missing'), 1))

### a-fresh-049 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× off-menu 'a red bull'; extra 1× drip_coffee, medium; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ()

### a-fresh-057 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× off-menu 'one of them'; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ()

### a-fresh-059 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity: gold None× breadsticks | pred 1× breadsticks; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-fresh-063 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-065 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity: gold 1× dr_pepper, two_liter | pred 2× dr_pepper, two_liter

### a-fresh-068 (refund_request) — **all students**
- **qwen3.5-0.8b-single-v5:** items with no gold order: ['2× pepperoni_pizza', '2× veggie_pizza']

### a-fresh-087 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 1× off-menu 'the usual'; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

