# `qwen3.5-0.8b-single-v3` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.3`, scorer `scorer@0.4`, finalize `finalize@0.2`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/91 | 90/91 |
| Valid answers, earlier messages | 174/177 | n/a (one call per chat) |
| Intent, all customer messages | 247/268 (92.2%, 95% CI 0.883–0.948) | 257/268 |
| Intent, last message | 84/91 (92.3%, 95% CI 0.850–0.962) | |
| Intent, earlier messages (mid-chat) | 163/177 (92.1%, 95% CI 0.872–0.952) | |
| Items (F1) | 130 found / 9 extra / 16 missed (F1 0.9122807017543859) | F1 0.993103448275862 |
| Fully correct orders | 75/91 (95% CI (0.7333142298436154, 0.888775654763983)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 75/91 (95% CI (0.7333142298436154, 0.888775654763983)) | |

Field accuracy: {'method': 1.0, 'time': 0.9838709677419355, 'address': 0.9838709677419355, 'payment': 0.9838709677419355, 'name': 1.0, 'decision': 1.0, 'missing': 0.9354838709677419}

Hit the token limit: 0; latency p50/p95 {'p50': 13179, 'p95': 19401} ms (T4, fp16, greedy); output tokens p50 324.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 3, '4 validation errors for StudentOutput': 1, '2 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 154 | 158 |
| SMALL_TALK | 26 | 24 | 26 |
| MENU_QUESTION | 16 | 14 | 15 |
| MODIFY_ORDER | 14 | 12 | 14 |
| CONFIRM_ORDER | 8 | 8 | 9 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 6 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 3 | 5 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 5
- MODIFY_ORDER → PLACE_ORDER: 2
- MENU_QUESTION → UNKNOWN: 1
- SMALL_TALK → MODIFY_ORDER: 1
- PLACE_ORDER → SMALL_TALK: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- UNKNOWN → CONFIRM_ORDER: 1
- PLACE_ORDER → MENU_QUESTION: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- SMALL_TALK → UNKNOWN: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
