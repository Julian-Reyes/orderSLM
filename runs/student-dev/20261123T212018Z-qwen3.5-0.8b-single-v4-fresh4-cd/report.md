# `qwen3.5-0.8b-single-v4` on fresh4 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh4 split: written after the v5 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 110/110 | ?/? |
| Valid answers, earlier messages | 233/233 | n/a (one call per chat) |
| Intent, all customer messages | 326/343 (95.0%, 95% CI 0.922–0.969) | ? |
| Intent, last message | 102/110 (92.7%, 95% CI 0.863–0.963) | |
| Intent, earlier messages (mid-chat) | 224/233 (96.1%, 95% CI 0.928–0.980) | |
| Items (F1) | 172 found / 24 extra / 23 missed (F1 0.8797953964194374) | ? |
| Fully correct orders | 89/110 (95% CI (0.7257143161698456, 0.8716068739750575)) | ? |
| Same action (bot sends/asks the same; wording aside) | 90/110 (95% CI (0.7357842649287114, 0.8791051955145714)) | |

Field accuracy: {'method': 1.0, 'time': 0.9883720930232558, 'address': 1.0, 'payment': 1.0, 'name': 0.9883720930232558, 'decision': 1.0, 'missing': 0.8953488372093024}

Hit the token limit: 0; latency p50/p95 {'p50': 14536, 'p95': 19589} ms (T4, fp16, greedy); output tokens p50 341.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 215 | 213 | 217 |
| SMALL_TALK | 49 | 44 | 47 |
| MODIFY_ORDER | 20 | 20 | 21 |
| MENU_QUESTION | 16 | 16 | 18 |
| CONFIRM_ORDER | 8 | 7 | 7 |
| OUT_OF_SCOPE | 7 | 5 | 6 |
| UNKNOWN | 7 | 4 | 6 |
| DELIVERY_QUESTION | 5 | 3 | 4 |
| ORDER_STATUS | 4 | 4 | 6 |
| CANCEL_ORDER | 2 | 2 | 3 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| ORDER_PROBLEM | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 0 | 0 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 2
- UNKNOWN → SMALL_TALK: 2
- DELIVERY_QUESTION → PLACE_ORDER: 2
- OUT_OF_SCOPE → MENU_QUESTION: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → ORDER_STATUS: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- PLACE_ORDER → MENU_QUESTION: 1
- OUT_OF_SCOPE → DELIVERY_QUESTION: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → CANCEL_ORDER: 1
