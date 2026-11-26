# `qwen3.5-0.8b-single-v6-q8_0` on fresh5 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh5 split: written after the v6 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 108/110 | ?/? |
| Valid answers, earlier messages | 247/248 | n/a (one call per chat) |
| Intent, all customer messages | 328/358 (91.6%, 95% CI 0.883–0.941) | ? |
| Intent, last message | 103/110 (93.6%, 95% CI 0.874–0.969) | |
| Intent, earlier messages (mid-chat) | 225/248 (90.7%, 95% CI 0.865–0.937) | |
| Items (F1) | 173 found / 11 extra / 19 missed (F1 0.9202127659574468) | ? |
| Fully correct orders | 93/110 (95% CI (0.7663799761205109, 0.9012142952179102)) | ? |
| Same action (bot sends/asks the same; wording aside) | 93/110 (95% CI (0.7663799761205109, 0.9012142952179102)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 0.9647058823529412, 'decision': 1.0, 'missing': 0.9176470588235294}

Hit the token limit: 0; latency p50/p95 {'p50': 2788, 'p95': 4114} ms (T4, fp16, greedy); output tokens p50 326.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 234 | 227 | 231 |
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
- PLACE_ORDER → None: 3
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
