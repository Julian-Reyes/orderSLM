# M6 error review on fresh2

Every chat or customer message a model got wrong, from saved outputs. Fresh2 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v5 |
|---|---|
| chats not fully right (of 90) | 15 |
| · fields only | 2 |
| · item mistakes | 13 |
| item: wrong_modifications | 4 |
| item: wrong_variant | 4 |
| item: missing_item | 4 |
| item: extra_item | 3 |
| item: wrong_quantity+modifications | 1 |
| field: missing | 6 |
| field: payment | 1 |
| field: time | 1 |
| intents wrong (of 275) | 14 |

Overlap: {'chats_all_students_wrong': 15, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 15, 'messages_all_students_wrong': 14, 'messages_one_student_only': 14}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v5': 1}
- combo: {'qwen3.5-0.8b-single-v5': 1}
- correction: {'qwen3.5-0.8b-single-v5': 1}
- human_request: {'qwen3.5-0.8b-single-v5': 1}
- missing_info: {'qwen3.5-0.8b-single-v5': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v5': 3}
- off_menu: {'qwen3.5-0.8b-single-v5': 2}
- payment_claim: {'qwen3.5-0.8b-single-v5': 1}
- simple_order: {'qwen3.5-0.8b-single-v5': 3}
- small_talk: {'qwen3.5-0.8b-single-v5': 2}

## Intent mistakes

- **qwen3.5-0.8b-single-v5:** PLACE_ORDER → MODIFY_ORDER ×2; UNKNOWN → SMALL_TALK ×2; PAYMENT_CLAIM → PLACE_ORDER ×1; UNKNOWN → PLACE_ORDER ×1; SMALL_TALK → DELIVERY_QUESTION ×1; CONFIRM_ORDER → SMALL_TALK ×1; UNKNOWN → MENU_QUESTION ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; PLACE_ORDER → MENU_QUESTION ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; PAYMENT_QUESTION → PLACE_ORDER ×1; REFUND_REQUEST → PAYMENT_CLAIM ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh2-003#3 | AND I ALREADY PAID, I HAVE THE SCREENSHOT | PAYMENT_CLAIM | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh2-018#2 | ok 14 | UNKNOWN | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh2-021#0 | omg ur still open 🙏🍕 | SMALL_TALK | qwen3.5-0.8b-single-v5: DELIVERY_QUESTION |
| a-fresh2-035#2 | ya | CONFIRM_ORDER | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh2-048#0 | HI DO ANY OF YOUR PASTRIES HAVE NU | UNKNOWN | qwen3.5-0.8b-single-v5: MENU_QUESTION |
| a-fresh2-058#0 | hey whats popular there | MENU_QUESTION | qwen3.5-0.8b-single-v5: OUT_OF_SCOPE |
| a-fresh2-063#3 | Pickup please, the name is Mei. | PLACE_ORDER | qwen3.5-0.8b-single-v5: MODIFY_ORDER |
| a-fresh2-064#2 | ? | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |
| a-fresh2-069#1 | make 2 of em double | PLACE_ORDER | qwen3.5-0.8b-single-v5: MODIFY_ORDER |
| a-fresh2-076#0 | Hi, coud I get a large drip coffe? | PLACE_ORDER | qwen3.5-0.8b-single-v5: MENU_QUESTION |
| a-fresh2-082#1 | can i pick up an order there | DELIVERY_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh2-083#0 | hey if i order delivery can i pay w card at the door | PAYMENT_QUESTION | qwen3.5-0.8b-single-v5: PLACE_ORDER |
| a-fresh2-085#3 | both charges r on my card rn | REFUND_REQUEST | qwen3.5-0.8b-single-v5: PAYMENT_CLAIM |
| a-fresh2-090#2 | ok can u save me a bluebe | UNKNOWN | qwen3.5-0.8b-single-v5: SMALL_TALK |

## Order mistakes, chat by chat

### a-fresh2-003 (payment_claim) — **all students**
- **qwen3.5-0.8b-single-v5:** payment: gold ('unknown', None, True) | pred ('cash', None, True)

### a-fresh2-005 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** variant: gold 3× muffin, blueberry | pred 3× muffin; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-014 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× cheese_pizza, medium, add crust_gluten_free | pred 1× cheese_pizza, medium

### a-fresh2-015 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× bagel, plain, add toasted, add strawberry jam | pred 1× bagel, plain, add toasted; extra 1× off-menu 'strawberry jam'; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_modification', 'off_menu'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_menu_match', 'off_menu'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-023 (combo) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× cheeseburger_combo, remove cheese, side=onion_rings, drink=sprite | pred 1× cheeseburger_combo, side=onion_rings, drink=sprite

### a-fresh2-031 (simple_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** variant: gold 2× milkshake, chocolate | pred 2× milkshake, vanilla

### a-fresh2-033 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v5:** extra 1× latte, large

### a-fresh2-044 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 2× drip_coffee, medium

### a-fresh2-049 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 3× off-menu 'the big burgers'; extra 3× cheeseburger; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-059 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v5:** variant: gold 1× pepperoni_pizza | pred 1× pepperoni_pizza, personal; missing: gold ((('item_variant', 'missing'), 1),) | pred ()

### a-fresh2-061 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v5:** modifications: gold 1× latte, medium, substitute whole_milk | pred 1× latte, medium, substitute whole_milk

### a-fresh2-069 (correction) — **all students**
- **qwen3.5-0.8b-single-v5:** missing 2× cheeseburger, single

### a-fresh2-072 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** variant: gold 1× latte, small, substitute whole_milk | pred 1× latte, substitute whole_milk; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-079 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v5:** quantity+modifications: gold 1× hawaiian_pizza, large | pred 2× hawaiian_pizza, large, add pineapple; missing 1× hawaiian_pizza, large, add pineapple

### a-fresh2-089 (human_request) — **all students**
- **qwen3.5-0.8b-single-v5:** time: gold ('ambiguous', None, None, ('tomorrow', None, None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

