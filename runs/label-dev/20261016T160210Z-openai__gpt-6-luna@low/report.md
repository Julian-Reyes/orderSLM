# Label prompt on dev: `teacher-label@0.3`, openai/gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 91 (64 with a gold order)
- Valid label (contract): 91/91
- Items: 146 found / 0 extra / 0 missed of 146 (F1 1.0)
- Fully correct orders: 91/91 (95% CI (0.959494567784601, 1.0))
- Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 1.0}
- Labels the synthetic pipeline would drop: none

## Intents (per customer message, against reviewed gold)

- Primary label correct: 263/268 (98.1%, 95% CI (0.9570767030396662, 0.9920054094846863))
- Primary + secondary exactly right: 259/268 (96.6%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 161 | 160 | 161 |
| SMALL_TALK | 27 | 27 | 28 |
| MENU_QUESTION | 16 | 16 | 16 |
| MODIFY_ORDER | 14 | 13 | 13 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 6 | 6 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| CANCEL_ORDER | 4 | 4 | 4 |
| UNKNOWN | 4 | 4 | 4 |
| ORDER_STATUS | 4 | 4 | 7 |
| HUMAN_REQUEST | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 3 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 2 | 2 |

Mistakes (gold → predicted):

- ORDER_PROBLEM → ORDER_STATUS: 2
- REFUND_REQUEST → ORDER_STATUS: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- PLACE_ORDER → SMALL_TALK: 1

Cost: $0.0577
