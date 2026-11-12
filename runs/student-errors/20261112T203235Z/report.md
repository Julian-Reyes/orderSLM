# M6 error review on fresh

Every chat or customer message a model got wrong, from saved outputs. Fresh is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v3 |
|---|---|
| chats not fully right (of 90) | 14 |
| · invalid answer | 2 |
| · item mistakes | 12 |
| item: wrong_modifications | 3 |
| item: missing_item | 3 |
| item: wrong_quantity | 3 |
| item: wrong_variant | 2 |
| item: extra_item | 1 |
| item: wrong_variant+modifications | 1 |
| field: address | 1 |
| field: missing | 10 |
| intents wrong (of 278) | 27 |

Overlap: {'chats_all_students_wrong': 14, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 14, 'messages_all_students_wrong': 27, 'messages_one_student_only': 27}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v3': 2}
- combo: {'qwen3.5-0.8b-single-v3': 1}
- correction: {'qwen3.5-0.8b-single-v3': 1}
- missing_info: {'qwen3.5-0.8b-single-v3': 4}
- multi_message_order: {'qwen3.5-0.8b-single-v3': 1}
- off_menu: {'qwen3.5-0.8b-single-v3': 3}
- simple_order: {'qwen3.5-0.8b-single-v3': 1}
- small_talk: {'qwen3.5-0.8b-single-v3': 2}
- unclear_message: {'qwen3.5-0.8b-single-v3': 1}

## Intent mistakes

- **qwen3.5-0.8b-single-v3:** SMALL_TALK → UNKNOWN ×13; PLACE_ORDER → None ×6; SMALL_TALK → PLACE_ORDER ×4; MENU_QUESTION → SMALL_TALK ×1; UNKNOWN → SMALL_TALK ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; PLACE_ORDER → ORDER_PROBLEM ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh-001#0 | hi! 👋 first time ordering from u guys | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh-001#2 | ok so im kinda unsure 😅 whats good | MENU_QUESTION | qwen3.5-0.8b-single-v3: SMALL_TALK |
| a-fresh-002#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-003#0 | hey quick q | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-004#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-004#1 | party at my place tonight | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh-008#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-013#0 | hey! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-016#0 | hi | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-023#1 | random q | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-029#0 | Hi! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-031#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-032#1 | ? | UNKNOWN | qwen3.5-0.8b-single-v3: SMALL_TALK |
| a-fresh-034#0 | Hi! Can I get a cheeseburger combo with large fries and a lemonade? | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-034#1 | No onions on the burger, please. | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-034#2 | Delivery to 415 Carver St. | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-034#3 | I'll pay by card. | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-046#1 | party tmrw | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh-047#2 | CAN U DELIVER IT | DELIVERY_QUESTION | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh-051#0 | hi | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-053#1 | first time ordering | SMALL_TALK | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh-059#2 | Right, it was a large Hawaiian and some breadsticks. | PLACE_ORDER | qwen3.5-0.8b-single-v3: ORDER_PROBLEM |
| a-fresh-073#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-079#0 | hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh-080#2 | AND A BOTTLED WATER | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-080#3 | PAYING CASH! | PLACE_ORDER | qwen3.5-0.8b-single-v3: None |
| a-fresh-088#0 | Hi there! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |

## Order mistakes, chat by chat

### a-fresh-006 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× hawaiian_pizza, medium | pred 1× hawaiian_pizza, medium, add as is; missing: gold () | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh-009 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 1× margherita_pizza | pred 1× margherita_pizza, large; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh-013 (correction, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** variant+modifications: gold 1× milkshake, chocolate | pred 1× milkshake, vanilla, substitute chocolate; missing: gold ((('payment_method', 'missing'), 1),) | pred ((('item_modification', 'ambiguous'), 1), (('payment_method', 'missing'), 1))

### a-fresh-034 (combo) — **all students**
- **qwen3.5-0.8b-single-v3:** invalid: order.items.0.combo_selections.0.unmatched_variant_text: Extra inputs are not permitted

### a-fresh-044 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× drip_coffee, medium, add almond_milk | pred 1× drip_coffee, medium, substitute whole_milk

### a-fresh-049 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'a red bull'; extra 1× bagel; missing: gold ((('item_menu_match', 'off_menu'), 1),) | pred ((('item_variant', 'missing'), 1),)

### a-fresh-056 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold None× onion_rings | pred 1× onion_rings; missing: gold ((('item_quantity', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-057 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'one of them'; missing: gold ((('item_menu_match', 'ambiguous'), 1),) | pred ()

### a-fresh-059 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold None× breadsticks | pred 1× breadsticks; missing: gold ((('item_quantity', 'ambiguous'), 1),) | pred ()

### a-fresh-063 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 2× pepperoni_pizza | pred 2× pepperoni_pizza, large; address: gold ('provided', ('400', '5')) | pred ('provided', ('400',)); missing: gold ((('item_variant', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh-065 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity: gold 1× dr_pepper, two_liter | pred 2× dr_pepper, two_liter

### a-fresh-074 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 3× bacon_burger, add BBQ SAUCE | pred 3× bacon_burger, add bacon; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ()

### a-fresh-080 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** invalid: order.items.0.modifications.1: Value error, not_on_menu/kitchen_note only for a request with no catalog id

### a-fresh-087 (unclear_message) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× off-menu 'the usual'; missing: gold ((('fulfillment_method', 'missing'), 1), (('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

