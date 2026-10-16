# Label audit `train` (label-audit@0.2, plant@0.1)

Training labels from the teacher. Agreement = provider's intent equals the teacher's primary. Flags: `flags.jsonl` (for review, not deletion).

| | jev | openai-decisions |
|---|---|---|
| intent = teacher (primary) | 7309/8310 (0.8795) | 7341/8310 (0.8834) |
| intent 95% CI | (0.8723683338448738, 0.8863663526567309) | (0.8763149523470503, 0.8901177398514636) |
| intent = teacher primary or secondary | 7426 | 7488 |
| teacher orders judged NOT matching | 155/2356 (0.0658) | 40/2356 (0.017) |
| errors | 0 | 0 |
| input tokens | 4,696,961 | 3,999,038 |
| cost (USD) | $0.1984 | $0.4009 |
| latency p50 / p95 ms | 260 / 354 | 348 / 1014 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×223; PLACE_ORDER→CONFIRM_ORDER ×134; SMALL_TALK→PLACE_ORDER ×128; SMALL_TALK→CONFIRM_ORDER ×124; CONFIRM_ORDER→PLACE_ORDER ×29; PLACE_ORDER→MENU_QUESTION ×25; PLACE_ORDER→PAYMENT_QUESTION ×23; SMALL_TALK→OUT_OF_SCOPE ×23
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×170; SMALL_TALK→PLACE_ORDER ×138; CONFIRM_ORDER→PLACE_ORDER ×74; DELIVERY_QUESTION→SMALL_TALK ×49; PLACE_ORDER→CONFIRM_ORDER ×38; CONFIRM_ORDER→SMALL_TALK ×37; SMALL_TALK→CONFIRM_ORDER ×36; PLACE_ORDER→SMALL_TALK ×35
