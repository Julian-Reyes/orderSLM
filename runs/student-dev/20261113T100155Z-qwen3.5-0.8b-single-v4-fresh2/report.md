# `qwen3.5-0.8b-single-v4` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/90 | ?/? |
| Valid answers, earlier messages | 185/185 | n/a (one call per chat) |
| Intent, all customer messages | 257/275 (93.5%, 95% CI 0.899–0.958) | ? |
| Intent, last message | 82/90 (91.1%, 95% CI 0.834–0.954) | |
| Intent, earlier messages (mid-chat) | 175/185 (94.6%, 95% CI 0.903–0.970) | |
| Items (F1) | 149 found / 17 extra / 22 missed (F1 0.884272997032641) | ? |
| Fully correct orders | 70/90 (95% CI (0.6815249725824009, 0.8512877671833321)) | ? |
| Same action (bot sends/asks the same; wording aside) | 71/90 (95% CI (0.6936500878323096, 0.8604751615240526)) | |

Field accuracy: {'method': 1.0, 'time': 0.9850746268656716, 'address': 1.0, 'payment': 0.9850746268656716, 'name': 1.0, 'decision': 1.0, 'missing': 0.9253731343283582}

Hit the token limit: 0; latency p50/p95 {'p50': 14896, 'p95': 22258} ms (T4, fp16, greedy); output tokens p50 337.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 169 | 172 |
| SMALL_TALK | 25 | 23 | 26 |
| MODIFY_ORDER | 18 | 18 | 20 |
| MENU_QUESTION | 12 | 11 | 13 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 3 | 4 |
| OUT_OF_SCOPE | 6 | 3 | 5 |
| ORDER_STATUS | 5 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 3 | 5 |
| ORDER_PROBLEM | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 4 |
| PAYMENT_CLAIM | 2 | 1 | 1 |
| PAYMENT_QUESTION | 2 | 2 | 2 |

Mistakes (gold → predicted):

- OUT_OF_SCOPE → HUMAN_REQUEST: 2
- PLACE_ORDER → MODIFY_ORDER: 2
- UNKNOWN → SMALL_TALK: 2
- PAYMENT_CLAIM → PLACE_ORDER: 1
- PLACE_ORDER → None: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → DELIVERY_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → MENU_QUESTION: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- PLACE_ORDER → MENU_QUESTION: 1
- ORDER_STATUS → DELIVERY_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
