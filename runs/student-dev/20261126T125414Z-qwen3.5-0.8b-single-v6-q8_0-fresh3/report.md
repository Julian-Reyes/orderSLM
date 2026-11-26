# `qwen3.5-0.8b-single-v6-q8_0` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 104/110 | ?/? |
| Valid answers, earlier messages | 210/211 | n/a (one call per chat) |
| Intent, all customer messages | 288/321 (89.7%, 95% CI 0.859–0.926) | ? |
| Intent, last message | 95/110 (86.4%, 95% CI 0.787–0.916) | |
| Intent, earlier messages (mid-chat) | 193/211 (91.5%, 95% CI 0.869–0.945) | |
| Items (F1) | 164 found / 4 extra / 22 missed (F1 0.9265536723163842) | ? |
| Fully correct orders | 90/110 (95% CI (0.7357842649287114, 0.8791051955145714)) | ? |
| Same action (bot sends/asks the same; wording aside) | 91/110 (95% CI (0.7459160253006629, 0.8865417054409992)) | |

Field accuracy: {'method': 0.9879518072289156, 'time': 0.9518072289156626, 'address': 0.9879518072289156, 'payment': 0.9879518072289156, 'name': 1.0, 'decision': 1.0, 'missing': 0.927710843373494}

Hit the token limit: 0; latency p50/p95 {'p50': 2734, 'p95': 3777} ms (T4, fp16, greedy); output tokens p50 324.
Invalid answers by reason: {'1 validation error for StudentOutput': 7}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 190 | 197 |
| SMALL_TALK | 35 | 28 | 31 |
| MODIFY_ORDER | 21 | 19 | 23 |
| MENU_QUESTION | 18 | 18 | 22 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 9 | 5 | 10 |
| OUT_OF_SCOPE | 6 | 4 | 4 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| ORDER_STATUS | 5 | 5 | 7 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 2 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 5
- SMALL_TALK → UNKNOWN: 4
- PLACE_ORDER → MODIFY_ORDER: 3
- SMALL_TALK → PLACE_ORDER: 3
- PLACE_ORDER → MENU_QUESTION: 3
- MODIFY_ORDER → None: 2
- UNKNOWN → SMALL_TALK: 2
- DELIVERY_QUESTION → PLACE_ORDER: 2
- DELIVERY_QUESTION → ORDER_STATUS: 1
- UNKNOWN → MENU_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → PLACE_ORDER: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- ORDER_PROBLEM → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
