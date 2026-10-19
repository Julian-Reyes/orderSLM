# Label audit `dev` (label-audit@0.3, plant@0.1)

Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged matching, planted copies not.

| | julia-1 |
|---|---|
| intent = gold (primary) | 146/268 (0.5448) |
| intent 95% CI | (0.4849402512239235, 0.6033464569178767) |
| intent = gold primary or secondary | 151 |
| correct orders judged NOT matching | 41/91 (0.4505) |
| planted mistakes caught | 0.4947 |
| … added_modification | 29/60 |
| … dropped_modification | 12/23 |
| … extra_item | 38/64 |
| … fulfillment_flip | 24/49 |
| … missing_item | 28/54 |
| … swapped_item | 27/54 |
| … wrong_payment | 20/53 |
| … wrong_quantity | 32/64 |
| … wrong_size | 24/52 |
| errors | 0 |
| input tokens | 243,749 |
| cost (USD) | $0.0000 |
| latency p50 / p95 ms | 270 / 1421 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, julia-1: SMALL_TALK→PLACE_ORDER ×20; MODIFY_ORDER→PLACE_ORDER ×13; MENU_QUESTION→PLACE_ORDER ×12; PLACE_ORDER→CANCEL_ORDER ×9; PLACE_ORDER→UNKNOWN ×8; PLACE_ORDER→MENU_QUESTION ×7; CONFIRM_ORDER→PLACE_ORDER ×7; SMALL_TALK→CANCEL_ORDER ×4
