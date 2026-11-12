# `qwen3.5-0.8b-single-v2` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.5`, finalize `finalize@0.3`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 87/90 | ?/? |
| Valid answers, earlier messages | 184/185 | n/a (one call per chat) |
| Intent, all customer messages | 249/275 (90.5%, 95% CI 0.865–0.935) | ? |
| Intent, last message | 79/90 (87.8%, 95% CI 0.794–0.930) | |
| Intent, earlier messages (mid-chat) | 170/185 (91.9%, 95% CI 0.871–0.950) | |
| Items (F1) | 138 found / 21 extra / 33 missed (F1 0.8363636363636363) | ? |
| Fully correct orders | 62/90 (95% CI (0.5871698145125097, 0.7751428485281886)) | ? |
| Same action (bot sends/asks the same; wording aside) | 63/90 (95% CI (0.598732953143893, 0.7848922194874346)) | |

Field accuracy: {'method': 1.0, 'time': 0.9846153846153847, 'address': 1.0, 'payment': 0.9846153846153847, 'name': 1.0, 'decision': 1.0, 'missing': 0.8615384615384616}

Hit the token limit: 0; latency p50/p95 {'p50': 14112, 'p95': 20946} ms (T4, fp16, greedy); output tokens p50 335.
Invalid answers by reason: {'1 validation error for StudentOutput': 4}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 161 | 165 |
| SMALL_TALK | 25 | 23 | 33 |
| MODIFY_ORDER | 18 | 14 | 16 |
| MENU_QUESTION | 12 | 11 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 3 | 3 |
| OUT_OF_SCOPE | 6 | 6 | 8 |
| ORDER_STATUS | 5 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 3 | 5 |
| ORDER_PROBLEM | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 1 |
| PAYMENT_QUESTION | 2 | 2 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → SMALL_TALK: 7
- UNKNOWN → SMALL_TALK: 3
- MODIFY_ORDER → PLACE_ORDER: 2
- MODIFY_ORDER → None: 2
- PLACE_ORDER → None: 2
- PLACE_ORDER → MODIFY_ORDER: 2
- PAYMENT_CLAIM → PLACE_ORDER: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → DELIVERY_QUESTION: 1
- UNKNOWN → MENU_QUESTION: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- PLACE_ORDER → MENU_QUESTION: 1
- ORDER_STATUS → DELIVERY_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
