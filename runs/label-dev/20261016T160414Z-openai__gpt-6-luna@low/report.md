# Label prompt on dev: `teacher-label@0.4`, openai/gpt-6-luna@low

Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.

## Orders (M3 scorer, after finalize)

- Conversations: 91 (64 with a gold order)
- Valid label (contract): 91/91
- Items: 145 found / 1 extra / 1 missed of 146 (F1 0.9931506849315068)
- Fully correct orders: 90/91 (95% CI (0.9403491964093862, 0.9980575786766521))
- Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 1.0}
- Labels the synthetic pipeline would drop: none

## Intents (per customer message, against reviewed gold)

- Primary label correct: 264/268 (98.5%, 95% CI (0.9622583365416947, 0.9941810016611411))
- Primary + secondary exactly right: 260/268 (97.0%)

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 161 | 160 | 161 |
| SMALL_TALK | 27 | 26 | 27 |
| MENU_QUESTION | 16 | 16 | 16 |
| MODIFY_ORDER | 14 | 14 | 15 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 8 | 9 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| CANCEL_ORDER | 4 | 4 | 4 |
| UNKNOWN | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 3 | 3 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 4 | 4 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 2 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → MODIFY_ORDER: 1
- UNKNOWN → SMALL_TALK: 1
- SMALL_TALK → PLACE_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1

Cost: $0.0578
