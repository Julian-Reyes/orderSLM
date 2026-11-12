# M6 error review on fresh2

Every chat or customer message a model got wrong, from saved outputs. Fresh2 is tuning / "used for fixes" data, not held-out.

| | qwen3.5-0.8b-single-v3 |
|---|---|
| chats not fully right (of 90) | 23 |
| · fields only | 1 |
| · item mistakes | 22 |
| item: missing_item | 12 |
| item: extra_item | 9 |
| item: wrong_modifications | 7 |
| item: wrong_variant | 4 |
| item: wrong_combo_picks | 1 |
| item: wrong_quantity+modifications | 1 |
| field: missing | 10 |
| field: time | 1 |
| intents wrong (of 275) | 20 |

Overlap: {'chats_all_students_wrong': 23, 'chats_all_students_and_teacher_wrong': 0, 'chats_one_student_only': 23, 'messages_all_students_wrong': 20, 'messages_one_student_only': 20}

Chats wrong by scenario (a chat can have several):

- ambiguous_reference: {'qwen3.5-0.8b-single-v3': 2}
- combo: {'qwen3.5-0.8b-single-v3': 1}
- contextual_yes: {'qwen3.5-0.8b-single-v3': 2}
- correction: {'qwen3.5-0.8b-single-v3': 4}
- correction_after_confirmation: {'qwen3.5-0.8b-single-v3': 1}
- human_request: {'qwen3.5-0.8b-single-v3': 1}
- implicit_category: {'qwen3.5-0.8b-single-v3': 2}
- missing_info: {'qwen3.5-0.8b-single-v3': 2}
- multi_message_order: {'qwen3.5-0.8b-single-v3': 4}
- off_menu: {'qwen3.5-0.8b-single-v3': 3}
- simple_order: {'qwen3.5-0.8b-single-v3': 2}
- small_talk: {'qwen3.5-0.8b-single-v3': 2}

## Intent mistakes

- **qwen3.5-0.8b-single-v3:** SMALL_TALK → UNKNOWN ×5; UNKNOWN → SMALL_TALK ×3; PLACE_ORDER → MODIFY_ORDER ×2; PAYMENT_CLAIM → PLACE_ORDER ×1; MODIFY_ORDER → PLACE_ORDER ×1; SMALL_TALK → OUT_OF_SCOPE ×1; SMALL_TALK → DELIVERY_QUESTION ×1; MENU_QUESTION → OUT_OF_SCOPE ×1; PLACE_ORDER → UNKNOWN ×1; PLACE_ORDER → MENU_QUESTION ×1; DELIVERY_QUESTION → PLACE_ORDER ×1; PAYMENT_QUESTION → PLACE_ORDER ×1; REFUND_REQUEST → PAYMENT_CLAIM ×1

| chat#msg | customer message | gold | wrong answers |
|---|---|---|---|
| a-fresh2-003#3 | AND I ALREADY PAID, I HAVE THE SCREENSHOT | PAYMENT_CLAIM | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh2-006#0 | hey! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-012#2 | OK MAKE ALL THE FRIES LARGE THEN | MODIFY_ORDER | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh2-013#0 | yo | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-017#0 | Hi there! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-018#2 | ok 14 | UNKNOWN | qwen3.5-0.8b-single-v3: SMALL_TALK |
| a-fresh2-020#0 | Hey, random question for a school thing. | SMALL_TALK | qwen3.5-0.8b-single-v3: OUT_OF_SCOPE |
| a-fresh2-021#0 | omg ur still open 🙏🍕 | SMALL_TALK | qwen3.5-0.8b-single-v3: DELIVERY_QUESTION |
| a-fresh2-022#0 | hey hey | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-031#0 | hi! | SMALL_TALK | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-058#0 | hey whats popular there | MENU_QUESTION | qwen3.5-0.8b-single-v3: OUT_OF_SCOPE |
| a-fresh2-063#3 | Pickup please, the name is Mei. | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER |
| a-fresh2-064#2 | ? | UNKNOWN | qwen3.5-0.8b-single-v3: SMALL_TALK |
| a-fresh2-069#1 | make 2 of em double | PLACE_ORDER | qwen3.5-0.8b-single-v3: MODIFY_ORDER |
| a-fresh2-072#0 | hiii can i order | PLACE_ORDER | qwen3.5-0.8b-single-v3: UNKNOWN |
| a-fresh2-076#0 | Hi, coud I get a large drip coffe? | PLACE_ORDER | qwen3.5-0.8b-single-v3: MENU_QUESTION |
| a-fresh2-082#1 | can i pick up an order there | DELIVERY_QUESTION | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh2-083#0 | hey if i order delivery can i pay w card at the door | PAYMENT_QUESTION | qwen3.5-0.8b-single-v3: PLACE_ORDER |
| a-fresh2-085#3 | both charges r on my card rn | REFUND_REQUEST | qwen3.5-0.8b-single-v3: PAYMENT_CLAIM |
| a-fresh2-090#2 | ok can u save me a bluebe | UNKNOWN | qwen3.5-0.8b-single-v3: SMALL_TALK |

## Order mistakes, chat by chat

### a-fresh2-004 (implicit_category) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 2× garlic_knots; extra 1× off-menu 'smth to snack on'; missing: gold () | pred ((('item_menu_match', 'off_menu'), 1),)

### a-fresh2-005 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× latte, large; variant: gold 3× muffin, blueberry | pred 3× muffin; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-013 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× onion_rings; extra 1× fries; missing: gold () | pred ((('item_variant', 'missing'), 1),)

### a-fresh2-014 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× cheese_pizza, medium, add crust_gluten_free | pred 1× cheese_pizza, medium

### a-fresh2-015 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× bagel, plain, add toasted, add strawberry jam | pred 1× bagel, plain, add toasted, add side of strawberry jam

### a-fresh2-019 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× cappuccino, medium, substitute whole_milk | pred 1× cappuccino, medium, substitute oat_milk

### a-fresh2-023 (combo) — **all students**
- **qwen3.5-0.8b-single-v3:** combo_picks: gold 1× cheeseburger_combo, remove cheese, side=onion_rings, drink=sprite | pred 1× cheeseburger_combo, remove cheese, side=onion_rings, drink=sprite, drink=lemonade; missing 1× lemonade

### a-fresh2-024 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 2× sprite, can; extra 1× breadsticks

### a-fresh2-033 (missing_info) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 2× latte | pred 2× latte, large; missing: gold ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('customer_name', 'missing'), 1), (('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-037 (contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× cappuccino, small, substitute whole_milk | pred 1× cappuccino, small, add skim_milk

### a-fresh2-042 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 2× pepperoni_pizza, personal, add w ricotta | pred 2× pepperoni_pizza, personal, add w ricotta; missing: gold ((('item_modification', 'off_menu'), 1),) | pred ((('item_modification', 'ambiguous'), 1),)

### a-fresh2-044 (simple_order) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 2× drip_coffee, medium, add oat_milk | pred 2× drip_coffee, medium, substitute whole_milk

### a-fresh2-049 (missing_info, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 3× off-menu 'the big burgers'; extra 3× bacon_burger; missing: gold ((('item_menu_match', 'ambiguous'), 1), (('payment_method', 'missing'), 1)) | pred ((('payment_method', 'missing'), 1),)

### a-fresh2-059 (off_menu) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 1× pepperoni_pizza | pred 1× pepperoni_pizza, personal; missing: gold ((('item_variant', 'missing'), 1),) | pred ()

### a-fresh2-061 (ambiguous_reference) — **all students**
- **qwen3.5-0.8b-single-v3:** modifications: gold 1× latte, medium, substitute whole_milk | pred 1× latte, medium, substitute whole_milk

### a-fresh2-063 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× bagel, everything, add avocado, add tomato; extra 1× breakfast_sandwich, croissant

### a-fresh2-067 (correction_after_confirmation, contextual_yes) — **all students**
- **qwen3.5-0.8b-single-v3:** extra 2× milkshake, chocolate

### a-fresh2-068 (implicit_category) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× milkshake, strawberry; extra 1× sprite

### a-fresh2-069 (correction) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 2× cheeseburger, single; missing 4× lemonade; extra 2× coke

### a-fresh2-072 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** variant: gold 1× latte, small, substitute whole_milk | pred 1× latte, substitute whole_milk; missing: gold ((('fulfillment_method', 'missing'), 1), (('payment_method', 'missing'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('item_variant', 'missing'), 1), (('payment_method', 'missing'), 1))

### a-fresh2-079 (multi_message_order) — **all students**
- **qwen3.5-0.8b-single-v3:** quantity+modifications: gold 1× hawaiian_pizza, large | pred 2× hawaiian_pizza, large, add pineapple; missing 1× hawaiian_pizza, large, add pineapple

### a-fresh2-086 (multi_message_order, small_talk) — **all students**
- **qwen3.5-0.8b-single-v3:** missing 1× breakfast_sandwich, bagel; extra 1× bagel, add a bacon, add n cheese; missing: gold () | pred ((('item_modification', 'ambiguous'), 1), (('item_variant', 'missing'), 1))

### a-fresh2-089 (human_request) — **all students**
- **qwen3.5-0.8b-single-v3:** time: gold ('ambiguous', None, None, ('tomorrow', None, None, None)) | pred ('not_mentioned', None, None, None); missing: gold ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1), (('requested_time', 'ambiguous'), 1)) | pred ((('fulfillment_method', 'missing'), 1), (('items', 'missing'), 1), (('payment_method', 'missing'), 1))

