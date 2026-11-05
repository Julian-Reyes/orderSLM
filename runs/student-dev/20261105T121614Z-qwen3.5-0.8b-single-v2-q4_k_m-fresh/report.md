# `qwen3.5-0.8b-single-v2-q4_k_m` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.4`, finalize `finalize@0.2`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 86/90 | ?/? |
| Valid answers, earlier messages | 182/188 | n/a (one call per chat) |
| Intent, all customer messages | 252/278 (90.6%, 95% CI 0.866–0.935) | ? |
| Intent, last message | 79/90 (87.8%, 95% CI 0.794–0.930) | |
| Intent, earlier messages (mid-chat) | 173/188 (92.0%, 95% CI 0.873–0.951) | |
| Items (F1) | 130 found / 18 extra / 26 missed (F1 0.8552631578947368) | ? |
| Fully correct orders | 66/90 (95% CI (0.6337996218328292, 0.8137630795703863)) | ? |
| Same action (bot sends/asks the same; wording aside) | 67/90 (95% CI (0.645621572349918, 0.823253638643927)) | |

Field accuracy: {'method': 1.0, 'time': 0.9848484848484849, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8484848484848485}

Hit the token limit: 0; latency p50/p95 {'p50': 2422, 'p95': 3970} ms (T4, fp16, greedy); output tokens p50 325.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 5, '2 validation errors for StudentOutput': 5}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 148 | 151 |
| SMALL_TALK | 43 | 43 | 53 |
| MODIFY_ORDER | 18 | 15 | 16 |
| MENU_QUESTION | 14 | 12 | 12 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 4 | 4 |
| ORDER_PROBLEM | 5 | 4 | 4 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 8
- PLACE_ORDER → SMALL_TALK: 6
- UNKNOWN → SMALL_TALK: 2
- MODIFY_ORDER → None: 2
- MENU_QUESTION → SMALL_TALK: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → PLACE_ORDER: 1
