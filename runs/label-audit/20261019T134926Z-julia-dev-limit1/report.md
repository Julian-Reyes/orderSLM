# Label audit `dev` (label-audit@0.3, plant@0.1)

Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged matching, planted copies not.

| | julia-1 |
|---|---|
| intent = gold (primary) | 0/2 (0.0) |
| intent 95% CI | (0.0, 0.6576280471103807) |
| intent = gold primary or secondary | 0 |
| correct orders judged NOT matching | 0/1 (0.0) |
| planted mistakes caught | None |
| errors | 0 |
| input tokens | 977 |
| cost (USD) | $0.0000 |
| latency p50 / p95 ms | 1494 / 1494 |

Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.

Top intent disagreements, julia-1: OUT_OF_SCOPE→PLACE_ORDER ×1; OUT_OF_SCOPE→UNKNOWN ×1
