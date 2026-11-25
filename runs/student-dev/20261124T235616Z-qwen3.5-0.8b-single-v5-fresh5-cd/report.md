# `qwen3.5-0.8b-single-v5` on fresh5 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh5 split: written after the v6 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 106/110 | ?/? |
| Valid answers, earlier messages | 247/248 | n/a (one call per chat) |
| Intent, all customer messages | 334/358 (93.3%, 95% CI 0.902–0.955) | ? |
| Intent, last message | 101/110 (91.8%, 95% CI 0.852–0.956) | |
| Intent, earlier messages (mid-chat) | 233/248 (94.0%, 95% CI 0.903–0.963) | |
| Items (F1) | 167 found / 14 extra / 25 missed (F1 0.8954423592493298) | ? |
| Fully correct orders | 89/110 (95% CI (0.7257143161698456, 0.8716068739750575)) | ? |
| Same action (bot sends/asks the same; wording aside) | 89/110 (95% CI (0.7257143161698456, 0.8716068739750575)) | |

Field accuracy: {'method': 1.0, 'time': 0.9759036144578314, 'address': 1.0, 'payment': 1.0, 'name': 0.9759036144578314, 'decision': 1.0, 'missing': 0.927710843373494}

Hit the token limit: 0; latency p50/p95 {'p50': 13696, 'p95': 20273} ms (T4, fp16, greedy); output tokens p50 327.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 5}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 234 | 227 | 232 |
| SMALL_TALK | 37 | 36 | 42 |
| MODIFY_ORDER | 21 | 19 | 19 |
| UNKNOWN | 16 | 12 | 12 |
| MENU_QUESTION | 11 | 11 | 15 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| OUT_OF_SCOPE | 7 | 7 | 9 |
| DELIVERY_QUESTION | 6 | 2 | 2 |
| PAYMENT_CLAIM | 4 | 1 | 2 |
| HUMAN_REQUEST | 3 | 1 | 1 |
| ORDER_STATUS | 3 | 3 | 4 |
| REFUND_REQUEST | 3 | 2 | 2 |
| CANCEL_ORDER | 2 | 2 | 2 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| ORDER_PROBLEM | 1 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 4
- UNKNOWN → SMALL_TALK: 4
- DELIVERY_QUESTION → PLACE_ORDER: 3
- PLACE_ORDER → MENU_QUESTION: 2
- HUMAN_REQUEST → OUT_OF_SCOPE: 2
- MODIFY_ORDER → None: 1
- SMALL_TALK → MENU_QUESTION: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- DELIVERY_QUESTION → MENU_QUESTION: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
- PLACE_ORDER → SMALL_TALK: 1
- PAYMENT_CLAIM → SMALL_TALK: 1
