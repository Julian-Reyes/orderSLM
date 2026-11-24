# `qwen3.5-0.8b-single-v5` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/90 | ?/? |
| Valid answers, earlier messages | 185/185 | n/a (one call per chat) |
| Intent, all customer messages | 261/275 (94.9%, 95% CI 0.916–0.969) | ? |
| Intent, last message | 85/90 (94.4%, 95% CI 0.876–0.976) | |
| Intent, earlier messages (mid-chat) | 176/185 (95.1%, 95% CI 0.910–0.974) | |
| Items (F1) | 158 found / 12 extra / 13 missed (F1 0.9266862170087976) | ? |
| Fully correct orders | 75/90 (95% CI (0.7430592627681392, 0.8963160249507403)) | ? |
| Same action (bot sends/asks the same; wording aside) | 75/90 (95% CI (0.7430592627681392, 0.8963160249507403)) | |

Field accuracy: {'method': 1.0, 'time': 0.9852941176470589, 'address': 1.0, 'payment': 0.9852941176470589, 'name': 1.0, 'decision': 1.0, 'missing': 0.9117647058823529}

Hit the token limit: 0; latency p50/p95 {'p50': 14445, 'p95': 20040} ms (T4, fp16, greedy); output tokens p50 337.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 170 | 174 |
| SMALL_TALK | 25 | 24 | 27 |
| MODIFY_ORDER | 18 | 18 | 20 |
| MENU_QUESTION | 12 | 11 | 13 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 3 | 3 |
| OUT_OF_SCOPE | 6 | 6 | 7 |
| ORDER_STATUS | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 4 |
| ORDER_PROBLEM | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 3 | 3 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 2 |
| PAYMENT_QUESTION | 2 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → MODIFY_ORDER: 2
- UNKNOWN → SMALL_TALK: 2
- PAYMENT_CLAIM → PLACE_ORDER: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → DELIVERY_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → MENU_QUESTION: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- PLACE_ORDER → MENU_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PAYMENT_QUESTION → PLACE_ORDER: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
