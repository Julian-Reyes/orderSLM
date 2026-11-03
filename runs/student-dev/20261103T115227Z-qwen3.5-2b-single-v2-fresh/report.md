# `qwen3.5-2b-single-v2` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.2`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 187/188 | n/a (one call per chat) |
| Intent, all customer messages | 254/278 (91.4%, 95% CI 0.875–0.941) | ? |
| Intent, last message | 82/90 (91.1%, 95% CI 0.834–0.954) | |
| Intent, earlier messages (mid-chat) | 172/188 (91.5%, 95% CI 0.866–0.947) | |
| Items (F1) | 131 found / 19 extra / 25 missed (F1 0.8562091503267973) | ? |
| Fully correct orders | 69/90 (95% CI (0.6694810141144782, 0.8420192160606255)) | ? |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8333333333333334}

Hit the token limit: 0; latency p50/p95 {'p50': 14142, 'p95': 24037} ms (T4, fp16, greedy); output tokens p50 327.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 150 | 145 | 159 |
| SMALL_TALK | 56 | 45 | 47 |
| MODIFY_ORDER | 18 | 14 | 15 |
| MENU_QUESTION | 14 | 12 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 6 | 9 |
| ORDER_PROBLEM | 5 | 5 | 5 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → PLACE_ORDER: 11
- MODIFY_ORDER → PLACE_ORDER: 2
- MODIFY_ORDER → None: 2
- PLACE_ORDER → UNKNOWN: 2
- MENU_QUESTION → SMALL_TALK: 1
- PLACE_ORDER → MENU_QUESTION: 1
- UNKNOWN → SMALL_TALK: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- MENU_QUESTION → UNKNOWN: 1
- PLACE_ORDER → None: 1
