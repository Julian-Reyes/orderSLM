# `qwen3.5-2b-mixed-v2` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.2`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/91 | 90/91 |
| Valid answers, earlier messages | 174/177 | n/a (one call per chat) |
| Intent, all customer messages | 251/268 (93.7%, 95% CI 0.901–0.960) | 259/268 |
| Intent, last message | 85/91 (93.4%, 95% CI 0.864–0.969) | |
| Intent, earlier messages (mid-chat) | 166/177 (93.8%, 95% CI 0.892–0.965) | |
| Items (F1) | 126 found / 11 extra / 20 missed (F1 0.8904593639575972) | F1 0.993103448275862 |
| Fully correct orders | 73/91 (95% CI (0.7088578689746323, 0.8710564302358408)) | 90/91 |

Field accuracy: {'method': 0.9838709677419355, 'time': 1.0, 'address': 1.0, 'payment': 0.967741935483871, 'name': 1.0, 'decision': 1.0, 'missing': 0.9032258064516129}

Hit the token limit: 0; latency p50/p95 {'p50': 14729, 'p95': 21665} ms (T4, fp16, greedy); output tokens p50 322.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 5}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 157 | 163 |
| SMALL_TALK | 28 | 27 | 30 |
| MENU_QUESTION | 16 | 15 | 15 |
| MODIFY_ORDER | 14 | 9 | 9 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 2 | 2 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 2 | 2 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- MODIFY_ORDER → PLACE_ORDER: 4
- PLACE_ORDER → None: 3
- UNKNOWN → SMALL_TALK: 2
- MODIFY_ORDER → None: 1
- HUMAN_REQUEST → None: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- PAYMENT_CLAIM → ORDER_PROBLEM: 1
- SMALL_TALK → PLACE_ORDER: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
