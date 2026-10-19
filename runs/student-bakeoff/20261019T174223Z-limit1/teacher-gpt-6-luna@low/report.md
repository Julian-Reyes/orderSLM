# Label prompt on dev: `teacher-label@0.7`, teacher-gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 1 (0 with a gold order)
- Valid label (contract): 1/1
- Items: 0 found / 0 extra / 0 missed of 0 (F1 None)
- Fully correct orders: 1/1 (95% CI (0.20654329147389294, 1.0))
- Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}
- Labels the synthetic pipeline would drop: none

## Intents (per customer message, against reviewed gold)

- Primary label correct: 2/2 (100.0%, 95% CI (0.34237195288961925, 1.0))
- Primary + secondary exactly right: 2/2 (100.0%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| OUT_OF_SCOPE | 2 | 2 | 2 |

Mistakes (gold → predicted):


Cost: $0.0000
