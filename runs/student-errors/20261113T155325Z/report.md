# M6 error review on fresh

Every chat or customer message a model got wrong, from saved outputs. Fresh is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v4 |
|---|---|
| chats not fully right (of 90) | 8 |
| · fields only | 1 |
| · invalid answer | 2 |
| · item mistakes | 5 |
| item: extra_item | 2 |
| item: missing_item | 2 |
| item: wrong_modifications | 1 |
| item: wrong_variant | 1 |
| item: wrong_quantity | 1 |
| field: missing | 5 |
| intents wrong (of 278) | 14 |

Overlap: {'chats_all_students_wrong': 8, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 8, 'messages_all_students_wrong': 14, 'messages_one_student_only': 14}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v4': 1}
- correction: {'qwen3.5-0.8b-single-v4': 1}
- missing_info: {'qwen3.5-0.8b-single-v4': 2}
- off_menu: {'qwen3.5-0.8b-single-v4': 1}
- simple_order: {'qwen3.5-0.8b-single-v4': 2}
- small_talk: {'qwen3.5-0.8b-single-v4': 1}
- unclear_message: {'qwen3.5-0.8b-single-v4': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v4:** SMALL_TALK → PLACE_ORDER ×2; UNKNOWN → PLACE_ORDER ×2; SMALL_TALK → UNKNOWN ×2; PLACE_ORDER → MENU_QUESTION ×1; UNKNOWN → SMALL_TALK ×1; PLACE_ORDER → SMALL_TALK ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; MODIFY_ORDER → None ×1; ORDER_PROBLEM → REFUND_REQUEST ×1; SMALL_TALK → MENU_QUESTION ×1; PLACE_ORDER → None ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh-004#1 | party at my place tonight | SMALL_TALK | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh-008#1 | 47 | UNKNOWN | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh-009#0 | good afternoon, id like to order one of the big margheritas pls, and could u tell me if the margherita has fresh mozzare | PLACE_ORDER | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-fresh-012#0 | ] | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh-023#1 | random q | SMALL_TALK | qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh-029#0 | Hi! | SMALL_TALK | qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh-037#0 | hey! 🚗 grabbing stuff for the office on my way in | PLACE_ORDER | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh-046#1 | party tmrw | SMALL_TALK | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh-047#2 | CAN U DELIVER IT | DELIVERY_QUESTION | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh-057#4 | actualy make it 3 bacon burgers | MODIFY_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh-069#0 | Hello, my delivery came but the onion rings I paid for never arrived. Could I get a refund for them? | ORDER_PROBLEM | qwen3.5-0.8b-single-v4: REFUND_REQUEST |
| a-fresh-080#0 | HI! I'M VEGAN | SMALL_TALK | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-fresh-084#8 | cash pls | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh-087#3 | oh right its the bac | UNKNOWN | qwen3.5-0.8b-single-v4: PLACE_ORDER |

## Order mistakes, chat by chat

### a-fresh-009 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v4:** missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-031 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity: gold 3× supreme_pizza, large | pred 2× supreme_pizza, large

### a-fresh-057 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order.items.1: Value error, L2: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4)

### a-fresh-063 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, large; missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-066 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× breakfast_sandwich, croissant; extra 1× croissant; missing: gold () | pred ((('item_variant', 'missing'), 1),)

### a-fresh-080 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× veggie_pizza, large, remove cheese, add VEGAN CHEESE | pred 1× veggie_pizza, large, remove cheese, add feta_cheese; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1)) | pred ((('fulfillment_method', 'missing'), 1),)

### a-fresh-084 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order: Value error, address must be not_applicable for pickup

### a-fresh-087 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× off-menu 'the usual'; extra 1× bacon_burger; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

