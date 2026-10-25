# `qwen3.5-2b-mixed` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.2`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/91 | 90/91 |
| Valid answers, earlier messages | 170/177 | n/a (one call per chat) |
| Intent, all customer messages | 241/268 (89.9%, 95% CI 0.857–0.930) | 259/268 |
| Intent, last message | 84/91 (92.3%, 95% CI 0.850–0.962) | |
| Intent, earlier messages (mid-chat) | 157/177 (88.7%, 95% CI 0.832–0.926) | |
| Items (F1) | 115 found / 20 extra / 31 missed (F1 0.8185053380782918) | F1 0.993103448275862 |
| Fully correct orders | 65/91 (95% CI (0.6142727836093079, 0.796939174012664)) | 90/91 |

Field accuracy: {'method': 0.9838709677419355, 'time': 0.9838709677419355, 'address': 1.0, 'payment': 0.9838709677419355, 'name': 1.0, 'decision': 1.0, 'missing': 0.8709677419354839}

Hit the token limit: 0; latency p50/p95 {'p50': 14304, 'p95': 21523} ms (T4, fp16, greedy); output tokens p50 319.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 8, '2 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 147 | 153 |
| SMALL_TALK | 28 | 27 | 32 |
| MENU_QUESTION | 16 | 16 | 19 |
| MODIFY_ORDER | 14 | 9 | 9 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 4 | 4 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 2 | 2 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 1 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 8
- MODIFY_ORDER → PLACE_ORDER: 5
- UNKNOWN → SMALL_TALK: 3
- PLACE_ORDER → UNKNOWN: 2
- PLACE_ORDER → MENU_QUESTION: 2
- HUMAN_REQUEST → None: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- PLACE_ORDER → SMALL_TALK: 1
- PAYMENT_CLAIM → ORDER_PROBLEM: 1
- SMALL_TALK → PLACE_ORDER: 1
- OUT_OF_SCOPE → MENU_QUESTION: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
