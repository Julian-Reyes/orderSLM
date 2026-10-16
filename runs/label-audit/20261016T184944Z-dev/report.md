# Label audit `dev` (label-audit@0.1, plant@0.1)

Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged matching, planted copies not.

| | jev | openai-decisions |
|---|---|---|
| intent = gold (primary) | 256/268 (0.9552) | 258/268 (0.9627) |
| intent 95% CI | (0.9233778264856487, 0.9742037062893203) | (0.9326877732096551, 0.9796082109222807) |
| intent = gold primary or secondary | 256 | 259 |
| correct orders judged NOT matching | 38/91 (0.4176) | 30/91 (0.3297) |
| planted mistakes caught | 0.945 | 0.8879 |
| … added_modification | 59/60 | 42/60 |
| … dropped_modification | 12/23 | 9/23 |
| … extra_item | 64/64 | 60/64 |
| … fulfillment_flip | 48/49 | 49/49 |
| … missing_item | 48/54 | 54/54 |
| … swapped_item | 52/54 | 49/54 |
| … wrong_payment | 53/53 | 51/53 |
| … wrong_quantity | 61/64 | 61/64 |
| … wrong_size | 50/52 | 45/52 |
| errors | 0 | 0 |
| input tokens | 368,163 | 283,513 |
| cost (USD) | $0.0000 | $0.0000 |
| latency p50 / p95 ms | 251 / 342 | 282 / 614 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×6; SMALL_TALK→PLACE_ORDER ×2; OUT_OF_SCOPE→PLACE_ORDER ×1; SMALL_TALK→UNKNOWN ×1; SMALL_TALK→OUT_OF_SCOPE ×1; ORDER_PROBLEM→PAYMENT_CLAIM ×1
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×4; SMALL_TALK→PLACE_ORDER ×2; HUMAN_REQUEST→SMALL_TALK ×1; REFUND_REQUEST→PAYMENT_CLAIM ×1; PLACE_ORDER→PAYMENT_CLAIM ×1; ORDER_PROBLEM→UNKNOWN ×1
