# `qwen3.5-0.8b-single-v3` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.3`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 108/110 | ?/? |
| Valid answers, earlier messages | 209/211 | n/a (one call per chat) |
| Intent, all customer messages | 286/321 (89.1%, 95% CI 0.852–0.921) | ? |
| Intent, last message | 101/110 (91.8%, 95% CI 0.852–0.956) | |
| Intent, earlier messages (mid-chat) | 185/211 (87.7%, 95% CI 0.826–0.915) | |
| Items (F1) | 168 found / 11 extra / 18 missed (F1 0.9205479452054794) | ? |
| Fully correct orders | 71/110 (95% CI (0.5525323623689828, 0.7285599624050894)) | ? |
| Same action (bot sends/asks the same; wording aside) | 73/110 (95% CI (0.5711478504963664, 0.7450810148744648)) | |

Field accuracy: {'method': 0.9770114942528736, 'time': 0.735632183908046, 'address': 0.9885057471264368, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8735632183908046}

Hit the token limit: 0; latency p50/p95 {'p50': 13867, 'p95': 19337} ms (T4, fp16, greedy); output tokens p50 321.
Invalid answers by reason: {'2 validation errors for StudentOutput': 2, '1 validation error for StudentOutput': 1, '6 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 193 | 200 |
| SMALL_TALK | 35 | 18 | 20 |
| MODIFY_ORDER | 21 | 20 | 23 |
| MENU_QUESTION | 18 | 18 | 18 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 9 | 7 | 23 |
| OUT_OF_SCOPE | 6 | 5 | 5 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 4 |
| ORDER_STATUS | 5 | 5 | 7 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 15
- PLACE_ORDER → None: 4
- PLACE_ORDER → MODIFY_ORDER: 3
- SMALL_TALK → PLACE_ORDER: 2
- DELIVERY_QUESTION → PLACE_ORDER: 2
- ORDER_PROBLEM → ORDER_STATUS: 2
- DELIVERY_QUESTION → SMALL_TALK: 1
- UNKNOWN → SMALL_TALK: 1
- PLACE_ORDER → ORDER_PROBLEM: 1
- UNKNOWN → PLACE_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
