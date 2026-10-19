# Label prompt on dev: `teacher-label@0.7`, gemma-4-e2b-it

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 1 (0 with a gold order)
- Valid label (contract): 0/1
- Items: 0 found / 0 extra / 0 missed of 0 (F1 None)
- Fully correct orders: 0/1 (95% CI (0.0, 0.7934567085261071))
- Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}
- Labels the synthetic pipeline would drop: {'invalid_contract': 1}

## Intents (per customer message, against reviewed gold)

- Primary label correct: 0/2 (0.0%, 95% CI (0.0, 0.6576280471103807))
- Primary + secondary exactly right: 0/2 (0.0%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| OUT_OF_SCOPE | 2 | 0 | 0 |

Mistakes (gold → predicted):

- OUT_OF_SCOPE → None: 2

Cost: $0.0000
