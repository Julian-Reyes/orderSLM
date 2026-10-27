# `qwen3.5-0.8b-single-v2` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.2`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 87/90 | ?/? |
| Valid answers, earlier messages | 184/188 | n/a (one call per chat) |
| Intent, all customer messages | 253/278 (91.0%, 95% CI 0.871–0.938) | ? |
| Intent, last message | 81/90 (90.0%, 95% CI 0.821–0.946) | |
| Intent, earlier messages (mid-chat) | 172/188 (91.5%, 95% CI 0.866–0.947) | |
| Items (F1) | 130 found / 23 extra / 26 missed (F1 0.8414239482200647) | ? |
| Fully correct orders | 67/90 (95% CI (0.645621572349918, 0.823253638643927)) | ? |

Field accuracy: {'method': 1.0, 'time': 0.9846153846153847, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8615384615384616}

Hit the token limit: 0; latency p50/p95 {'p50': 13849, 'p95': 23225} ms (T4, fp16, greedy); output tokens p50 327.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 4, '6 validation errors for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 150 | 143 | 154 |
| SMALL_TALK | 56 | 47 | 48 |
| MODIFY_ORDER | 18 | 16 | 16 |
| MENU_QUESTION | 14 | 13 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 5 | 6 |
| ORDER_PROBLEM | 5 | 4 | 4 |
| OUT_OF_SCOPE | 5 | 5 | 8 |
| DELIVERY_QUESTION | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 5 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → PLACE_ORDER: 8
- PLACE_ORDER → None: 6
- DELIVERY_QUESTION → OUT_OF_SCOPE: 2
- UNKNOWN → SMALL_TALK: 1
- SMALL_TALK → UNKNOWN: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- PLACE_ORDER → ORDER_STATUS: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- MODIFY_ORDER → None: 1
- UNKNOWN → PLACE_ORDER: 1
