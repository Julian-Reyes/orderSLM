# Label prompt on dev: `teacher-label@0.6`, openai/gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 91 (64 with a gold order)
- Valid label (contract): 91/91
- Items: 146 found / 0 extra / 0 missed of 146 (F1 1.0)
- Fully correct orders: 91/91 (95% CI (0.959494567784601, 1.0))
- Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 1.0}
- Labels the synthetic pipeline would drop: none

## Intents (per customer message, against reviewed gold)

- Primary label correct: 265/268 (98.9%, 95% CI (0.9676106407461019, 0.9961859231352174))
- Primary + secondary exactly right: 261/268 (97.4%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 158 | 158 |
| SMALL_TALK | 28 | 28 | 30 |
| MENU_QUESTION | 16 | 16 | 16 |
| MODIFY_ORDER | 14 | 14 | 15 |
| CONFIRM_ORDER | 8 | 8 | 8 |
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

- PLACE_ORDER → SMALL_TALK: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- UNKNOWN → SMALL_TALK: 1

Cost: $0.0581
