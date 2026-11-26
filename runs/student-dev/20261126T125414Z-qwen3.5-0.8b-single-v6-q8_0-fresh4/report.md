# `qwen3.5-0.8b-single-v6-q8_0` on fresh4 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh4 split: written after the v5 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 108/110 | ?/? |
| Valid answers, earlier messages | 233/233 | n/a (one call per chat) |
| Intent, all customer messages | 321/343 (93.6%, 95% CI 0.905–0.957) | ? |
| Intent, last message | 101/110 (91.8%, 95% CI 0.852–0.956) | |
| Intent, earlier messages (mid-chat) | 220/233 (94.4%, 95% CI 0.907–0.967) | |
| Items (F1) | 181 found / 12 extra / 14 missed (F1 0.9329896907216495) | ? |
| Fully correct orders | 97/110 (95% CI (0.8082479662756031, 0.9296193862563361)) | ? |
| Same action (bot sends/asks the same; wording aside) | 97/110 (95% CI (0.8082479662756031, 0.9296193862563361)) | |

Field accuracy: {'method': 1.0, 'time': 0.9880952380952381, 'address': 1.0, 'payment': 1.0, 'name': 0.9880952380952381, 'decision': 1.0, 'missing': 0.9523809523809523}

Hit the token limit: 0; latency p50/p95 {'p50': 2822, 'p95': 3919} ms (T4, fp16, greedy); output tokens p50 340.
Invalid answers by reason: {'1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 215 | 212 | 214 |
| SMALL_TALK | 49 | 41 | 46 |
| MODIFY_ORDER | 20 | 18 | 19 |
| MENU_QUESTION | 16 | 16 | 19 |
| CONFIRM_ORDER | 8 | 6 | 6 |
| OUT_OF_SCOPE | 7 | 6 | 7 |
| UNKNOWN | 7 | 4 | 10 |
| DELIVERY_QUESTION | 5 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 6 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| ORDER_PROBLEM | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 1 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 6
- UNKNOWN → SMALL_TALK: 3
- DELIVERY_QUESTION → PLACE_ORDER: 2
- PLACE_ORDER → MENU_QUESTION: 2
- MODIFY_ORDER → None: 2
- CONFIRM_ORDER → SMALL_TALK: 2
- OUT_OF_SCOPE → MENU_QUESTION: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → ORDER_STATUS: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
