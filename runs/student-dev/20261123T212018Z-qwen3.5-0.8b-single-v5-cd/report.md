# `qwen3.5-0.8b-single-v5` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 91/91 | 90/91 |
| Valid answers, earlier messages | 176/177 | n/a (one call per chat) |
| Intent, all customer messages | 252/268 (94.0%, 95% CI 0.905–0.963) | 257/268 |
| Intent, last message | 87/91 (95.6%, 95% CI 0.892–0.983) | |
| Intent, earlier messages (mid-chat) | 165/177 (93.2%, 95% CI 0.885–0.961) | |
| Items (F1) | 132 found / 13 extra / 14 missed (F1 0.9072164948453608) | F1 0.993103448275862 |
| Fully correct orders | 75/91 (95% CI (0.7333142298436154, 0.888775654763983)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 75/91 (95% CI (0.7333142298436154, 0.888775654763983)) | |

Field accuracy: {'method': 0.984375, 'time': 1.0, 'address': 0.984375, 'payment': 0.984375, 'name': 1.0, 'decision': 1.0, 'missing': 0.859375}

Hit the token limit: 0; latency p50/p95 {'p50': 13622, 'p95': 19842} ms (T4, fp16, greedy); output tokens p50 323.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 161 | 166 |
| SMALL_TALK | 26 | 25 | 27 |
| MENU_QUESTION | 16 | 14 | 15 |
| MODIFY_ORDER | 14 | 12 | 13 |
| CONFIRM_ORDER | 8 | 8 | 9 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 4 | 5 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 3 | 3 |
| UNKNOWN | 4 | 2 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 1 |

Mistakes (gold → predicted):

- MODIFY_ORDER → PLACE_ORDER: 2
- PAYMENT_CLAIM → PLACE_ORDER: 2
- UNKNOWN → SMALL_TALK: 1
- PLACE_ORDER → None: 1
- MENU_QUESTION → UNKNOWN: 1
- SMALL_TALK → MODIFY_ORDER: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- UNKNOWN → CONFIRM_ORDER: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- OUT_OF_SCOPE → MENU_QUESTION: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
