# `qwen3.5-2b-single-v2` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.3`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/91 | 90/91 |
| Valid answers, earlier messages | 170/177 | n/a (one call per chat) |
| Intent, all customer messages | 245/268 (91.4%, 95% CI 0.875–0.942) | 259/268 |
| Intent, last message | 85/91 (93.4%, 95% CI 0.864–0.969) | |
| Intent, earlier messages (mid-chat) | 160/177 (90.4%, 95% CI 0.852–0.939) | |
| Items (F1) | 121 found / 14 extra / 25 missed (F1 0.8612099644128114) | F1 0.993103448275862 |
| Fully correct orders | 69/91 (95% CI (0.6609799811910234, 0.8345831472251989)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 69/91 (95% CI (0.6609799811910234, 0.8345831472251989)) | |

Field accuracy: {'method': 1.0, 'time': 0.967741935483871, 'address': 1.0, 'payment': 0.9838709677419355, 'name': 1.0, 'decision': 1.0, 'missing': 0.9032258064516129}

Hit the token limit: 0; latency p50/p95 {'p50': 13977, 'p95': 21010} ms (T4, fp16, greedy); output tokens p50 320.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 8, '2 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 152 | 158 |
| SMALL_TALK | 26 | 26 | 30 |
| MENU_QUESTION | 16 | 15 | 15 |
| MODIFY_ORDER | 14 | 9 | 9 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 2 | 2 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 2 | 4 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 7
- MODIFY_ORDER → PLACE_ORDER: 4
- UNKNOWN → SMALL_TALK: 2
- PLACE_ORDER → UNKNOWN: 2
- MODIFY_ORDER → None: 1
- HUMAN_REQUEST → None: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- PAYMENT_CLAIM → ORDER_PROBLEM: 1
- PLACE_ORDER → SMALL_TALK: 1
- MENU_QUESTION → PLACE_ORDER: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
