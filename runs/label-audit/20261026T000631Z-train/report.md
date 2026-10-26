# Label audit `train` (label-audit@0.3, plant@0.1)

Training labels from the teacher. Agreement = provider's intent equals the teacher's primary. Flags: `flags.jsonl` (for review, not deletion).

| | jev |
|---|---|
| intent = teacher (primary) | 332/416 (0.7981) |
| intent 95% CI | (0.7568529684664661, 0.833845999906368) |
| intent = teacher primary or secondary | 333 |
| teacher orders judged NOT matching | 6/122 (0.0492) |
| errors | 0 |
| input tokens | 234,330 |
| cost (USD) | $0.0099 |
| latency p50 / p95 ms | 351 / 2511 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×54; UNKNOWN→SMALL_TALK ×8; UNKNOWN→PLACE_ORDER ×6; SMALL_TALK→UNKNOWN ×6; SMALL_TALK→PLACE_ORDER ×5; UNKNOWN→MODIFY_ORDER ×2; PLACE_ORDER→PAYMENT_QUESTION ×1; DELIVERY_QUESTION→SMALL_TALK ×1
