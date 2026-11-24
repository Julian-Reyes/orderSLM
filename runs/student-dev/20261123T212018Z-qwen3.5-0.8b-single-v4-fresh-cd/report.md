# `qwen3.5-0.8b-single-v4` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 188/188 | n/a (one call per chat) |
| Intent, all customer messages | 264/278 (95.0%, 95% CI 0.917–0.970) | ? |
| Intent, last message | 82/90 (91.1%, 95% CI 0.834–0.954) | |
| Intent, earlier messages (mid-chat) | 182/188 (96.8%, 95% CI 0.932–0.985) | |
| Items (F1) | 147 found / 5 extra / 9 missed (F1 0.9545454545454546) | ? |
| Fully correct orders | 82/90 (95% CI (0.8342928001780631, 0.9542700546752215)) | ? |
| Same action (bot sends/asks the same; wording aside) | 83/90 (95% CI (0.8480596940416417, 0.9618156704022723)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9264705882352942}

Hit the token limit: 0; latency p50/p95 {'p50': 14105, 'p95': 23752} ms (T4, fp16, greedy); output tokens p50 325.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 160 | 165 |
| SMALL_TALK | 43 | 38 | 40 |
| MODIFY_ORDER | 18 | 17 | 17 |
| MENU_QUESTION | 14 | 14 | 16 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 4 | 6 |
| ORDER_PROBLEM | 5 | 4 | 4 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → PLACE_ORDER: 2
- UNKNOWN → PLACE_ORDER: 2
- SMALL_TALK → UNKNOWN: 2
- PLACE_ORDER → MENU_QUESTION: 1
- UNKNOWN → SMALL_TALK: 1
- PLACE_ORDER → SMALL_TALK: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- MODIFY_ORDER → None: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- SMALL_TALK → MENU_QUESTION: 1
- PLACE_ORDER → None: 1
