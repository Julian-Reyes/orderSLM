# M6 error review on fresh2

Every chat or customer message a model got wrong, from saved outputs. Fresh2 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v4 |
|---|---|
| chats not fully right (of 90) | 20 |
| · fields only | 2 |
| · invalid answer | 1 |
| · item mistakes | 17 |
| item: missing_item | 7 |
| item: wrong_modifications | 5 |
| item: extra_item | 4 |
| item: wrong_quantity | 3 |
| item: wrong_variant | 3 |
| item: wrong_quantity+modifications | 1 |
| item: wrong_modifications+combo_picks | 1 |
| field: missing | 5 |
| field: payment | 1 |
| field: time | 1 |
| intents wrong (of 275) | 18 |

Overlap: {'chats_all_students_wrong': 20, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 20, 'messages_all_students_wrong': 18, 'messages_one_student_only': 18}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v4': 1}
- combo: {'qwen3.5-0.8b-single-v4': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v4': 1}
- correction: {'qwen3.5-0.8b-single-v4': 3}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v4': 1}
- human_request: {'qwen3.5-0.8b-single-v4': 1}
- implicit_category: {'qwen3.5-0.8b-single-v4': 1}
- missing_info: {'qwen3.5-0.8b-single-v4': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v4': 5}
- off_menu: {'qwen3.5-0.8b-single-v4': 2}
- payment_claim: {'qwen3.5-0.8b-single-v4': 1}
- simple_order: {'qwen3.5-0.8b-single-v4': 2}
- small_talk: {'qwen3.5-0.8b-single-v4': 4}

## Intent mistakes

- **qwen3.5-0.8b-single-v4:** OUT_OF_SCOPE → HUMAN_REQUEST ×2; PLACE_ORDER → MODIFY_ORDER ×2; UNKNOWN → SMALL_TALK ×2; PAYMENT_CLAIM → PLACE_ORDER ×1; PLACE_ORDER → None ×1; UNKNOWN → PLACE_ORDER ×1; SMALL_TALK → OUT_OF_SCOPE ×1; SMALL_TALK → DELIVERY_QUESTION ×1; CONFIRM_ORDER → SMALL_TALK ×1; UNKNOWN → MENU_QUESTION ×1; OUT_OF_SCOPE → UNKNOWN ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; PLACE_ORDER → MENU_QUESTION ×1; ORDER_STATUS → DELIVERY_QUESTION ×1; DELIVERY_QUESTION → PLACE_ORDER ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh2-003#3 | AND I ALREADY PAID, I HAVE THE SCREENSHOT | PAYMENT_CLAIM | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh2-015#0 | Good morning. I would like a medium latte and a plain bagel, toasted, with a side of strawberry jam please. | PLACE_ORDER | qwen3.5-0.8b-single-v4: None |
| a-fresh2-018#2 | ok 14 | UNKNOWN | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh2-020#0 | Hey, random question for a school thing. | SMALL_TALK | qwen3.5-0.8b-single-v4: OUT_OF_SCOPE |
| a-fresh2-021#0 | omg ur still open 🙏🍕 | SMALL_TALK | qwen3.5-0.8b-single-v4: DELIVERY_QUESTION |
| a-fresh2-035#2 | ya | CONFIRM_ORDER | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh2-048#0 | HI DO ANY OF YOUR PASTRIES HAVE NU | UNKNOWN | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-fresh2-050#0 | hi!! 👋 are u guys hiring? 😊 | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: HUMAN_REQUEST |
| a-fresh2-050#1 | i'd love to apply for a barista job ☕ where do i send my resume? 📄 | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: HUMAN_REQUEST |
| a-fresh2-056#0 | ok settle a bet for us 😂☕ is a tomato a fruit or a vegetable?? 🍅 | OUT_OF_SCOPE | qwen3.5-0.8b-single-v4: UNKNOWN |
| a-fresh2-058#0 | hey whats popular there | MENU_QUESTION | qwen3.5-0.8b-single-v4: OUT_OF_SCOPE |
| a-fresh2-063#3 | Pickup please, the name is Mei. | PLACE_ORDER | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh2-064#2 | ? | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |
| a-fresh2-069#1 | make 2 of em double | PLACE_ORDER | qwen3.5-0.8b-single-v4: MODIFY_ORDER |
| a-fresh2-076#0 | Hi, coud I get a large drip coffe? | PLACE_ORDER | qwen3.5-0.8b-single-v4: MENU_QUESTION |
| a-fresh2-080#0 | hi! just checking on my delivery | ORDER_STATUS | qwen3.5-0.8b-single-v4: DELIVERY_QUESTION |
| a-fresh2-082#1 | can i pick up an order there | DELIVERY_QUESTION | qwen3.5-0.8b-single-v4: PLACE_ORDER |
| a-fresh2-090#2 | ok can u save me a bluebe | UNKNOWN | qwen3.5-0.8b-single-v4: SMALL_TALK |

## Order mistakes, chat by chat

### a-fresh2-003 (payment_claim) — **all students**
- **qwen3.5-0.8b-single-v4:** payment: gold ('unknown', None, True) | pred ('cash', None, True)

### a-fresh2-004 (implicit_category) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 2× pepperoni_pizza, large

### a-fresh2-005 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 1× latte, large; variant: gold 1× americano, small | pred 1× americano; variant: gold 3× muffin, blueberry | pred 3× muffin; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 2), (('payment_method', 'missing'), 1))

### a-fresh2-014 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× cheese_pizza, medium, add crust_gluten_free | pred 1× cheese_pizza, medium, add mushrooms, add crust_gluten_free; quantity: gold 2× cheese_pizza, medium, add mushrooms, add crust_gluten_free | pred 1× cheese_pizza, medium, add mushrooms, add crust_gluten_free

### a-fresh2-015 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v4:** invalid: order.items.1.modifications.0.kind: Input should be 'remove', 'add' or 'substitute'

### a-fresh2-019 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× cappuccino, medium, substitute whole_milk | pred 1× cappuccino, medium, substitute whole_milk

### a-fresh2-022 (multi_message_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity: gold 3× cheeseburger, single | pred 2× cheeseburger, single

### a-fresh2-023 (combo) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications+combo_picks: gold 1× cheeseburger_combo, remove cheese, side=onion_rings, drink=sprite | pred 1× cheeseburger_combo, side=onion_rings, drink=sprite, drink=lemonade; missing 1× lemonade

### a-fresh2-024 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 2× sprite, can; extra 1× breadsticks

### a-fresh2-031 (simple_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity: gold 2× milkshake, vanilla | pred 3× milkshake, vanilla

### a-fresh2-033 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v4:** extra 1× latte, large

### a-fresh2-042 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 2× pepperoni_pizza, personal, add w ricotta | pred 2× pepperoni_pizza, personal, add w ricotta; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh2-049 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 3× off-menu 'the big burgers'; extra 3× bacon_burger; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh2-061 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× latte, medium, substitute whole_milk | pred 1× latte, medium, substitute whole_milk

### a-fresh2-067 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v4:** extra 2× milkshake, chocolate

### a-fresh2-069 (correction) — **all students**
- **qwen3.5-0.8b-single-v4:** missing 2× cheeseburger, single

### a-fresh2-072 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v4:** variant: gold 1× latte, small, substitute whole_milk | pred 1× latte, substitute whole_milk; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-079 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v4:** quantity+modifications: gold 1× hawaiian_pizza, large | pred 2× hawaiian_pizza, large, add pineapple; missing 1× hawaiian_pizza, large, add pineapple

### a-fresh2-086 (multi_message_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v4:** modifications: gold 1× breakfast_sandwich, bagel | pred 1× breakfast_sandwich, bagel, add bacon, add cheddar

### a-fresh2-089 (human_request) — **all students**
- **qwen3.5-0.8b-single-v4:** time: gold ('ambiguous', None, None, ('tomorrow', None, None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

