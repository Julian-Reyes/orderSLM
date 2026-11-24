# `qwen3.5-0.8b-single-v5` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 110/110 | ?/? |
| Valid answers, earlier messages | 211/211 | n/a (one call per chat) |
| Intent, all customer messages | 303/321 (94.4%, 95% CI 0.913–0.964) | ? |
| Intent, last message | 102/110 (92.7%, 95% CI 0.863–0.963) | |
| Intent, earlier messages (mid-chat) | 201/211 (95.3%, 95% CI 0.915–0.974) | |
| Items (F1) | 174 found / 11 extra / 12 missed (F1 0.9380053908355795) | ? |
| Fully correct orders | 90/110 (95% CI (0.7357842649287114, 0.8791051955145714)) | ? |
| Same action (bot sends/asks the same; wording aside) | 92/110 (95% CI (0.7561132241492788, 0.8939127768907628)) | |

Field accuracy: {'method': 1.0, 'time': 0.9213483146067416, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9213483146067416}

Hit the token limit: 0; latency p50/p95 {'p50': 13633, 'p95': 18322} ms (T4, fp16, greedy); output tokens p50 324.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 199 | 205 |
| SMALL_TALK | 35 | 33 | 37 |
| MODIFY_ORDER | 21 | 21 | 24 |
| MENU_QUESTION | 18 | 17 | 18 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 9 | 4 | 6 |
| OUT_OF_SCOPE | 6 | 5 | 5 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| ORDER_STATUS | 5 | 5 | 7 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- UNKNOWN → SMALL_TALK: 3
- PLACE_ORDER → MODIFY_ORDER: 2
- DELIVERY_QUESTION → PLACE_ORDER: 2
- DELIVERY_QUESTION → ORDER_STATUS: 1
- UNKNOWN → MENU_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- MENU_QUESTION → PLACE_ORDER: 1
- UNKNOWN → PLACE_ORDER: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- ORDER_PROBLEM → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- SMALL_TALK → PLACE_ORDER: 1
- SMALL_TALK → UNKNOWN: 1
