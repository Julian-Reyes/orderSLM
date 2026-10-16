# Label audit `dev` (label-audit@0.3, plant@0.1)

Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged matching, planted copies not.

| | jev | openai-decisions |
|---|---|---|
| intent = gold (primary) | 257/268 (0.959) | 258/268 (0.9627) |
| intent 95% CI | (0.9280093369841262, 0.9769294214693263) | (0.9326877732096551, 0.9796082109222807) |
| intent = gold primary or secondary | 257 | 259 |
| correct orders judged NOT matching | 5/91 (0.0549) | 0/91 (0.0) |
| planted mistakes caught | 0.8879 | 0.7822 |
| … added_modification | 54/60 | 27/60 |
| … dropped_modification | 6/23 | 4/23 |
| … extra_item | 64/64 | 53/64 |
| … fulfillment_flip | 48/49 | 48/49 |
| … missing_item | 46/54 | 50/54 |
| … swapped_item | 52/54 | 44/54 |
| … wrong_payment | 51/53 | 52/53 |
| … wrong_quantity | 56/64 | 55/64 |
| … wrong_size | 43/52 | 37/52 |
| errors | 0 | 0 |
| input tokens | 402,582 | 317,876 |
| cost (USD) | $0.0172 | $0.0320 |
| latency p50 / p95 ms | 261 / 358 | 238 / 615 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×6; SMALL_TALK→PLACE_ORDER ×2; SMALL_TALK→CANCEL_ORDER ×1; SMALL_TALK→OUT_OF_SCOPE ×1; ORDER_PROBLEM→PAYMENT_CLAIM ×1
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×3; SMALL_TALK→PLACE_ORDER ×2; SMALL_TALK→UNKNOWN ×1; HUMAN_REQUEST→SMALL_TALK ×1; MODIFY_ORDER→PLACE_ORDER ×1; REFUND_REQUEST→PAYMENT_CLAIM ×1; PLACE_ORDER→MENU_QUESTION ×1
