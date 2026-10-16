# Label audit `dev` (label-audit@0.2, plant@0.1)

Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged matching, planted copies not.

| | jev | openai-decisions |
|---|---|---|
| intent = gold (primary) | 256/268 (0.9552) | 258/268 (0.9627) |
| intent 95% CI | (0.9233778264856487, 0.9742037062893203) | (0.9326877732096551, 0.9796082109222807) |
| intent = gold primary or secondary | 256 | 259 |
| correct orders judged NOT matching | 11/91 (0.1209) | 2/91 (0.022) |
| planted mistakes caught | 0.8879 | 0.8224 |
| … added_modification | 54/60 | 37/60 |
| … dropped_modification | 8/23 | 5/23 |
| … extra_item | 64/64 | 57/64 |
| … fulfillment_flip | 48/49 | 47/49 |
| … missing_item | 43/54 | 50/54 |
| … swapped_item | 52/54 | 45/54 |
| … wrong_payment | 51/53 | 51/53 |
| … wrong_quantity | 56/64 | 57/64 |
| … wrong_size | 44/52 | 40/52 |
| errors | 0 | 0 |
| input tokens | 395,085 | 310,379 |
| cost (USD) | $0.0169 | $0.0313 |
| latency p50 / p95 ms | 253 / 349 | 276 / 640 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×6; SMALL_TALK→PLACE_ORDER ×2; OUT_OF_SCOPE→PLACE_ORDER ×1; SMALL_TALK→CANCEL_ORDER ×1; SMALL_TALK→OUT_OF_SCOPE ×1; ORDER_PROBLEM→PAYMENT_CLAIM ×1
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×3; SMALL_TALK→PLACE_ORDER ×2; SMALL_TALK→UNKNOWN ×1; MODIFY_ORDER→PLACE_ORDER ×1; REFUND_REQUEST→PAYMENT_CLAIM ×1; PAYMENT_CLAIM→PLACE_ORDER ×1; PLACE_ORDER→MENU_QUESTION ×1
