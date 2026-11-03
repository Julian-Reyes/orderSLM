# Label prompt on dev: `teacher-label@0.7`, openai/gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 91 (64 with a gold order)
- Valid label (contract): 90/91
- Items: 144 found / 0 extra / 2 missed of 146 (F1 0.993103448275862)
- Fully correct orders: 90/91 (95% CI (0.9403491964093862, 0.9980575786766521))
- Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 1.0}
- Labels the synthetic pipeline would drop: {'invalid_contract': 1}

## Intents (per customer message, against reviewed gold)

- Primary label correct: 257/268 (95.9%, 95% CI (0.9280093369841262, 0.9769294214693263))
- Primary + secondary exactly right: 256/268 (95.5%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 154 | 154 |
| SMALL_TALK | 26 | 26 | 31 |
| MENU_QUESTION | 16 | 16 | 16 |
| MODIFY_ORDER | 14 | 13 | 13 |
| CONFIRM_ORDER | 8 | 7 | 7 |
| ORDER_PROBLEM | 8 | 8 | 8 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| CANCEL_ORDER | 4 | 4 | 4 |
| UNKNOWN | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 4 | 4 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 2 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → SMALL_TALK: 4
- PLACE_ORDER → None: 4
- CONFIRM_ORDER → None: 1
- MODIFY_ORDER → None: 1
- UNKNOWN → SMALL_TALK: 1

Cost: $0.0577
