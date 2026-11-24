# `qwen3.5-0.8b-single-v4` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/90 | ?/? |
| Valid answers, earlier messages | 185/185 | n/a (one call per chat) |
| Intent, all customer messages | 259/275 (94.2%, 95% CI 0.908–0.964) | ? |
| Intent, last message | 84/90 (93.3%, 95% CI 0.862–0.969) | |
| Intent, earlier messages (mid-chat) | 175/185 (94.6%, 95% CI 0.903–0.970) | |
| Items (F1) | 151 found / 18 extra / 20 missed (F1 0.888235294117647) | ? |
| Fully correct orders | 71/90 (95% CI (0.6936500878323096, 0.8604751615240526)) | ? |
| Same action (bot sends/asks the same; wording aside) | 72/90 (95% CI (0.7058607285729566, 0.8695770303740351)) | |

Field accuracy: {'method': 1.0, 'time': 0.9852941176470589, 'address': 1.0, 'payment': 0.9852941176470589, 'name': 1.0, 'decision': 1.0, 'missing': 0.9117647058823529}

Hit the token limit: 0; latency p50/p95 {'p50': 14476, 'p95': 21264} ms (T4, fp16, greedy); output tokens p50 335.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 170 | 173 |
| SMALL_TALK | 25 | 23 | 25 |
| MODIFY_ORDER | 18 | 18 | 20 |
| MENU_QUESTION | 12 | 11 | 13 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 4 | 5 |
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
- PAYMENT_CLAIM → PLACE_ORDER: 1
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
- UNKNOWN → SMALL_TALK: 1
