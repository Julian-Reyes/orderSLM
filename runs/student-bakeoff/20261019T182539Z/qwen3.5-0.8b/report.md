# Label prompt on dev: `teacher-label@0.7`, qwen3.5-0.8b

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 20 (14 with a gold order)
- Valid label (contract): 0/20
- Items: 0 found / 0 extra / 29 missed of 29 (F1 0.0)
- Fully correct orders: 0/20 (95% CI (0.0, 0.16113012549493322))
- Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}
- Labels the synthetic pipeline would drop: {'invalid_contract': 20}

## Intents (per customer message, against reviewed gold)

- Primary label correct: 0/54 (0.0%, 95% CI (6.938893903907228e-18, 0.06641586678100189))
- Primary + secondary exactly right: 0/54 (0.0%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 31 | 0 | 0 |
| MENU_QUESTION | 5 | 0 | 0 |
| SMALL_TALK | 4 | 0 | 0 |
| MODIFY_ORDER | 3 | 0 | 0 |
| OUT_OF_SCOPE | 2 | 0 | 0 |
| PAYMENT_QUESTION | 2 | 0 | 0 |
| DELIVERY_QUESTION | 2 | 0 | 0 |
| CANCEL_ORDER | 1 | 0 | 0 |
| CONFIRM_ORDER | 1 | 0 | 0 |
| ORDER_PROBLEM | 1 | 0 | 0 |
| REFUND_REQUEST | 1 | 0 | 0 |
| HUMAN_REQUEST | 1 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 31
- MENU_QUESTION → None: 5
- SMALL_TALK → None: 4
- MODIFY_ORDER → None: 3
- OUT_OF_SCOPE → None: 2
- PAYMENT_QUESTION → None: 2
- DELIVERY_QUESTION → None: 2
- CANCEL_ORDER → None: 1
- CONFIRM_ORDER → None: 1
- ORDER_PROBLEM → None: 1
- REFUND_REQUEST → None: 1
- HUMAN_REQUEST → None: 1

Cost: $0.0000
