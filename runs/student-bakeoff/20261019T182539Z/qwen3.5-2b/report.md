# Label prompt on dev: `teacher-label@0.7`, qwen3.5-2b

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 20 (14 with a gold order)
- Valid label (contract): 3/20
- Items: 0 found / 0 extra / 29 missed of 29 (F1 0.0)
- Fully correct orders: 3/20 (95% CI (0.05236779195949584, 0.36042329588695743))
- Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}
- Labels the synthetic pipeline would drop: {'invalid_contract': 17, 'intents_mismatch': 2}

## Intents (per customer message, against reviewed gold)

- Primary label correct: 5/54 (9.3%, 95% CI (0.040200542070567336, 0.1991012753065453))
- Primary + secondary exactly right: 5/54 (9.3%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 31 | 0 | 0 |
| MENU_QUESTION | 5 | 3 | 4 |
| SMALL_TALK | 4 | 0 | 0 |
| MODIFY_ORDER | 3 | 0 | 0 |
| OUT_OF_SCOPE | 2 | 0 | 0 |
| PAYMENT_QUESTION | 2 | 1 | 1 |
| DELIVERY_QUESTION | 2 | 0 | 0 |
| CANCEL_ORDER | 1 | 0 | 0 |
| CONFIRM_ORDER | 1 | 0 | 0 |
| ORDER_PROBLEM | 1 | 0 | 0 |
| REFUND_REQUEST | 1 | 0 | 0 |
| HUMAN_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 31
- SMALL_TALK → None: 4
- MODIFY_ORDER → None: 3
- OUT_OF_SCOPE → None: 2
- MENU_QUESTION → None: 2
- DELIVERY_QUESTION → None: 2
- CANCEL_ORDER → None: 1
- PAYMENT_QUESTION → MENU_QUESTION: 1
- CONFIRM_ORDER → None: 1
- ORDER_PROBLEM → None: 1
- REFUND_REQUEST → None: 1

Cost: $0.0000
