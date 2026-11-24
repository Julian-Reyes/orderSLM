# `qwen3.5-0.8b-single-v5` on fresh4 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh4 split: written after the v5 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 108/110 | ?/? |
| Valid answers, earlier messages | 232/233 | n/a (one call per chat) |
| Intent, all customer messages | 324/343 (94.5%, 95% CI 0.915–0.964) | ? |
| Intent, last message | 101/110 (91.8%, 95% CI 0.852–0.956) | |
| Intent, earlier messages (mid-chat) | 223/233 (95.7%, 95% CI 0.923–0.977) | |
| Items (F1) | 177 found / 16 extra / 18 missed (F1 0.9123711340206185) | ? |
| Fully correct orders | 94/110 (95% CI (0.7767209782912426, 0.9084415633455579)) | ? |
| Same action (bot sends/asks the same; wording aside) | 94/110 (95% CI (0.7767209782912426, 0.9084415633455579)) | |

Field accuracy: {'method': 1.0, 'time': 0.9882352941176471, 'address': 1.0, 'payment': 1.0, 'name': 0.9882352941176471, 'decision': 1.0, 'missing': 0.9529411764705882}

Hit the token limit: 0; latency p50/p95 {'p50': 14391, 'p95': 19588} ms (T4, fp16, greedy); output tokens p50 341.
Invalid answers by reason: {'1 validation error for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 215 | 212 | 214 |
| SMALL_TALK | 49 | 44 | 49 |
| MODIFY_ORDER | 20 | 19 | 20 |
| MENU_QUESTION | 16 | 16 | 17 |
| CONFIRM_ORDER | 8 | 7 | 8 |
| OUT_OF_SCOPE | 7 | 6 | 7 |
| UNKNOWN | 7 | 3 | 5 |
| DELIVERY_QUESTION | 5 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 5 |
| CANCEL_ORDER | 2 | 2 | 3 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| ORDER_PROBLEM | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 1 |
| PAYMENT_QUESTION | 2 | 1 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |

Mistakes (gold → predicted):

- UNKNOWN → SMALL_TALK: 4
- SMALL_TALK → UNKNOWN: 2
- PLACE_ORDER → None: 2
- OUT_OF_SCOPE → MENU_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → ORDER_STATUS: 1
- PAYMENT_QUESTION → None: 1
- DELIVERY_QUESTION → PAYMENT_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- PAYMENT_CLAIM → CONFIRM_ORDER: 1
- SMALL_TALK → CANCEL_ORDER: 1
