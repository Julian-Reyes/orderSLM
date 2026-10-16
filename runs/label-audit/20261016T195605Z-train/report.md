# Label audit `train` (label-audit@0.3, plant@0.1)

Training labels from the teacher. Agreement = provider's intent equals the teacher's primary. Flags: `flags.jsonl` (for review, not deletion).

| | jev | openai-decisions |
|---|---|---|
| intent = teacher (primary) | 7355/8310 (0.8851) | 7402/8310 (0.8907) |
| intent 95% CI | (0.8780423488493636, 0.8917582208415478) | (0.883844952874229, 0.8972620626840176) |
| intent = teacher primary or secondary | 7473 | 7547 |
| teacher orders judged NOT matching | 45/2356 (0.0191) | 24/2356 (0.0102) |
| errors | 0 | 0 |
| input tokens | 4,745,335 | 4,047,412 |
| cost (USD) | $0.2004 | $0.4057 |
| latency p50 / p95 ms | 271 / 386 | 327 / 1378 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, jev: PLACE_ORDER→MODIFY_ORDER ×228; PLACE_ORDER→CONFIRM_ORDER ×134; SMALL_TALK→PLACE_ORDER ×126; SMALL_TALK→CONFIRM_ORDER ×98; CONFIRM_ORDER→PLACE_ORDER ×29; PLACE_ORDER→MENU_QUESTION ×25; PLACE_ORDER→PAYMENT_QUESTION ×24; SMALL_TALK→OUT_OF_SCOPE ×24
Top intent disagreements, openai-decisions: PLACE_ORDER→MODIFY_ORDER ×170; SMALL_TALK→PLACE_ORDER ×135; CONFIRM_ORDER→PLACE_ORDER ×74; DELIVERY_QUESTION→SMALL_TALK ×55; CONFIRM_ORDER→SMALL_TALK ×38; PLACE_ORDER→CONFIRM_ORDER ×38; SMALL_TALK→UNKNOWN ×37; PLACE_ORDER→SMALL_TALK ×34
