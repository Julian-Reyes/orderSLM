# `qwen3.5-0.8b-single-v6` on fresh5 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh5 split: written after the v6 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 110/110 | ?/? |
| Valid answers, earlier messages | 248/248 | n/a (one call per chat) |
| Intent, all customer messages | 331/358 (92.5%, 95% CI 0.892–0.948) | ? |
| Intent, last message | 105/110 (95.5%, 95% CI 0.898–0.980) | |
| Intent, earlier messages (mid-chat) | 226/248 (91.1%, 95% CI 0.869–0.941) | |
| Items (F1) | 176 found / 10 extra / 16 missed (F1 0.9312169312169312) | ? |
| Fully correct orders | 95/110 (95% CI (0.787141630195824, 0.9155891817393563)) | ? |
| Same action (bot sends/asks the same; wording aside) | 95/110 (95% CI (0.787141630195824, 0.9155891817393563)) | |

Field accuracy: {'method': 1.0, 'time': 0.9770114942528736, 'address': 1.0, 'payment': 1.0, 'name': 0.9770114942528736, 'decision': 1.0, 'missing': 0.896551724137931}

Hit the token limit: 0; latency p50/p95 {'p50': 14203, 'p95': 20824} ms (T4, fp16, greedy); output tokens p50 326.0.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 234 | 230 | 234 |
| SMALL_TALK | 37 | 28 | 35 |
| MODIFY_ORDER | 21 | 20 | 21 |
| UNKNOWN | 16 | 12 | 20 |
| MENU_QUESTION | 11 | 11 | 14 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| OUT_OF_SCOPE | 7 | 7 | 8 |
| DELIVERY_QUESTION | 6 | 3 | 3 |
| PAYMENT_CLAIM | 4 | 1 | 2 |
| HUMAN_REQUEST | 3 | 1 | 1 |
| ORDER_STATUS | 3 | 3 | 5 |
| REFUND_REQUEST | 3 | 2 | 2 |
| CANCEL_ORDER | 2 | 2 | 2 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| ORDER_PROBLEM | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 8
- UNKNOWN → SMALL_TALK: 4
- DELIVERY_QUESTION → PLACE_ORDER: 3
- PAYMENT_CLAIM → ORDER_STATUS: 2
- PLACE_ORDER → MENU_QUESTION: 2
- SMALL_TALK → MENU_QUESTION: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- HUMAN_REQUEST → OUT_OF_SCOPE: 1
- PLACE_ORDER → SMALL_TALK: 1
- PAYMENT_CLAIM → SMALL_TALK: 1
