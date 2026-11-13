# `qwen3.5-0.8b-single-v4` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 107/110 | ?/? |
| Valid answers, earlier messages | 210/211 | n/a (one call per chat) |
| Intent, all customer messages | 300/321 (93.5%, 95% CI 0.902–0.957) | ? |
| Intent, last message | 101/110 (91.8%, 95% CI 0.852–0.956) | |
| Intent, earlier messages (mid-chat) | 199/211 (94.3%, 95% CI 0.903–0.967) | |
| Items (F1) | 167 found / 11 extra / 19 missed (F1 0.9175824175824175) | ? |
| Fully correct orders | 92/110 (95% CI (0.7561132241492788, 0.8939127768907628)) | ? |
| Same action (bot sends/asks the same; wording aside) | 94/110 (95% CI (0.7767209782912426, 0.9084415633455579)) | |

Field accuracy: {'method': 1.0, 'time': 0.9651162790697675, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9418604651162791}

Hit the token limit: 0; latency p50/p95 {'p50': 13730, 'p95': 18612} ms (T4, fp16, greedy); output tokens p50 326.
Invalid answers by reason: {'1 validation error for StudentOutput': 3, '3 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 196 | 203 |
| SMALL_TALK | 35 | 31 | 33 |
| MODIFY_ORDER | 21 | 20 | 23 |
| MENU_QUESTION | 18 | 18 | 18 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 9 | 6 | 8 |
| OUT_OF_SCOPE | 6 | 4 | 4 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| ORDER_STATUS | 5 | 5 | 6 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 2 |
| PAYMENT_CLAIM | 1 | 0 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- DELIVERY_QUESTION → PLACE_ORDER: 3
- PLACE_ORDER → None: 3
- PLACE_ORDER → MODIFY_ORDER: 2
- UNKNOWN → SMALL_TALK: 2
- SMALL_TALK → PLACE_ORDER: 2
- MODIFY_ORDER → None: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → PAYMENT_CLAIM: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- ORDER_PROBLEM → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- SMALL_TALK → UNKNOWN: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
