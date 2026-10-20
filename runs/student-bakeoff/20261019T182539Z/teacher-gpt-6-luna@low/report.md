# Label prompt on dev: `teacher-label@0.7`, teacher-gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 20 (14 with a gold order)
- Valid label (contract): 20/20
- Items: 29 found / 0 extra / 0 missed of 29 (F1 1.0)
- Fully correct orders: 20/20 (95% CI (0.8388698745050667, 1.0))
- Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 1.0}
- Labels the synthetic pipeline would drop: none

## Intents (per customer message, against reviewed gold)

- Primary label correct: 54/54 (100.0%, 95% CI (0.9335841332189981, 1.0))
- Primary + secondary exactly right: 54/54 (100.0%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 31 | 31 | 31 |
| MENU_QUESTION | 5 | 5 | 5 |
| SMALL_TALK | 4 | 4 | 4 |
| MODIFY_ORDER | 3 | 3 | 3 |
| OUT_OF_SCOPE | 2 | 2 | 2 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| DELIVERY_QUESTION | 2 | 2 | 2 |
| CANCEL_ORDER | 1 | 1 | 1 |
| CONFIRM_ORDER | 1 | 1 | 1 |
| ORDER_PROBLEM | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |
| HUMAN_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):


Cost: $0.0000
