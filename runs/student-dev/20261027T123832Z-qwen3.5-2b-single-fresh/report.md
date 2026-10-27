# `qwen3.5-2b-single` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.2`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 85/90 | ?/? |
| Valid answers, earlier messages | 183/188 | n/a (one call per chat) |
| Intent, all customer messages | 237/278 (85.2%, 95% CI 0.806–0.889) | ? |
| Intent, last message | 69/90 (76.7%, 95% CI 0.669–0.842) | |
| Intent, earlier messages (mid-chat) | 168/188 (89.4%, 95% CI 0.841–0.930) | |
| Items (F1) | 109 found / 25 extra / 47 missed (F1 0.7517241379310344) | ? |
| Fully correct orders | 51/90 (95% CI (0.4636391101764269, 0.664235947367349)) | ? |

Field accuracy: {'method': 0.9841269841269841, 'time': 0.9523809523809523, 'address': 0.9841269841269841, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.746031746031746}

Hit the token limit: 0; latency p50/p95 {'p50': 14919, 'p95': 24444} ms (T4, fp16, greedy); output tokens p50 319.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 9, '2 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 150 | 138 | 153 |
| SMALL_TALK | 56 | 44 | 54 |
| MODIFY_ORDER | 18 | 14 | 16 |
| MENU_QUESTION | 14 | 13 | 15 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 1 | 2 |
| ORDER_PROBLEM | 5 | 5 | 6 |
| OUT_OF_SCOPE | 5 | 1 | 1 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 3 | 3 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → PLACE_ORDER: 12
- PLACE_ORDER → None: 8
- UNKNOWN → SMALL_TALK: 5
- OUT_OF_SCOPE → SMALL_TALK: 4
- MODIFY_ORDER → PLACE_ORDER: 2
- MODIFY_ORDER → None: 2
- PLACE_ORDER → MODIFY_ORDER: 2
- MENU_QUESTION → SMALL_TALK: 1
- PLACE_ORDER → MENU_QUESTION: 1
- UNKNOWN → MENU_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- ORDER_STATUS → ORDER_PROBLEM: 1
- PLACE_ORDER → UNKNOWN: 1
