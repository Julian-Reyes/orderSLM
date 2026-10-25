# Label audit `train` (label-audit@0.3, plant@0.1)

Training labels from the teacher. Agreement = provider's intent equals the teacher's primary. Flags: `flags.jsonl` (for review, not deletion).

| | jev | openai-decisions |
|---|---|---|
| intent = teacher (primary) | 2152/2420 (0.8893) | 2145/2420 (0.8864) |
| intent 95% CI | (0.8761307355367806, 0.9011477796929276) | (0.8731016434976725, 0.8984009167356365) |
| intent = teacher primary or secondary | 2189 | 2198 |
| teacher orders judged NOT matching | 54/568 (0.0951) | 21/568 (0.037) |
| errors | 0 | 0 |
| input tokens | 1,343,207 | 1,152,824 |
| cost (USD) | $0.0566 | $0.1154 |
| latency p50 / p95 ms | 269 / 696 | 295 / 649 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×57; SMALL_TALK→PLACE_ORDER ×46; PLACE_ORDER→CONFIRM_ORDER ×41; SMALL_TALK→CONFIRM_ORDER ×18; CONFIRM_ORDER→PLACE_ORDER ×17; PLACE_ORDER→MENU_QUESTION ×13; PLACE_ORDER→PAYMENT_QUESTION ×11; UNKNOWN→PLACE_ORDER ×11
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×46; SMALL_TALK→PLACE_ORDER ×41; CONFIRM_ORDER→PLACE_ORDER ×38; CONFIRM_ORDER→SMALL_TALK ×15; PLACE_ORDER→SMALL_TALK ×15; DELIVERY_QUESTION→SMALL_TALK ×14; MODIFY_ORDER→PLACE_ORDER ×13; SMALL_TALK→UNKNOWN ×12
