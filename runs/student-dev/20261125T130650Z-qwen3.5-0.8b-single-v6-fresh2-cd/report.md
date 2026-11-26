# `qwen3.5-0.8b-single-v6` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/90 | ?/? |
| Valid answers, earlier messages | 185/185 | n/a (one call per chat) |
| Intent, all customer messages | 257/275 (93.5%, 95% CI 0.899–0.958) | ? |
| Intent, last message | 84/90 (93.3%, 95% CI 0.862–0.969) | |
| Intent, earlier messages (mid-chat) | 173/185 (93.5%, 95% CI 0.890–0.963) | |
| Items (F1) | 158 found / 12 extra / 13 missed (F1 0.9266862170087976) | ? |
| Fully correct orders | 75/90 (95% CI (0.7430592627681392, 0.8963160249507403)) | ? |
| Same action (bot sends/asks the same; wording aside) | 77/90 (95% CI (0.7683993769120605, 0.9136009299880774)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 0.9852941176470589, 'name': 1.0, 'decision': 1.0, 'missing': 0.9117647058823529}

Hit the token limit: 0; latency p50/p95 {'p50': 14339, 'p95': 21061} ms (T4, fp16, greedy); output tokens p50 338.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 168 | 172 |
| SMALL_TALK | 25 | 22 | 25 |
| MODIFY_ORDER | 18 | 18 | 21 |
| MENU_QUESTION | 12 | 12 | 14 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 4 | 6 |
| OUT_OF_SCOPE | 6 | 5 | 5 |
| ORDER_STATUS | 5 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 3 | 5 |
| ORDER_PROBLEM | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 3 | 3 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 3 |
| PAYMENT_CLAIM | 2 | 1 | 2 |
| PAYMENT_QUESTION | 2 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → MODIFY_ORDER: 3
- SMALL_TALK → UNKNOWN: 2
- PAYMENT_CLAIM → PLACE_ORDER: 1
- PLACE_ORDER → SMALL_TALK: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → DELIVERY_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → MENU_QUESTION: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
- PLACE_ORDER → MENU_QUESTION: 1
- ORDER_STATUS → DELIVERY_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PAYMENT_QUESTION → PLACE_ORDER: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
- UNKNOWN → SMALL_TALK: 1
