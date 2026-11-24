# `qwen3.5-0.8b-single-v4` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 109/110 | ?/? |
| Valid answers, earlier messages | 211/211 | n/a (one call per chat) |
| Intent, all customer messages | 303/321 (94.4%, 95% CI 0.913–0.964) | ? |
| Intent, last message | 103/110 (93.6%, 95% CI 0.874–0.969) | |
| Intent, earlier messages (mid-chat) | 200/211 (94.8%, 95% CI 0.909–0.971) | |
| Items (F1) | 174 found / 11 extra / 12 missed (F1 0.9380053908355795) | ? |
| Fully correct orders | 93/110 (95% CI (0.7663799761205109, 0.9012142952179102)) | ? |
| Same action (bot sends/asks the same; wording aside) | 95/110 (95% CI (0.787141630195824, 0.9155891817393563)) | |

Field accuracy: {'method': 1.0, 'time': 0.9545454545454546, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9431818181818182}

Hit the token limit: 0; latency p50/p95 {'p50': 13429, 'p95': 18311} ms (T4, fp16, greedy); output tokens p50 324.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 199 | 206 |
| SMALL_TALK | 35 | 31 | 33 |
| MODIFY_ORDER | 21 | 20 | 23 |
| MENU_QUESTION | 18 | 18 | 18 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 9 | 6 | 8 |
| OUT_OF_SCOPE | 6 | 4 | 4 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| ORDER_STATUS | 5 | 5 | 6 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 2 |
| PAYMENT_CLAIM | 1 | 0 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- DELIVERY_QUESTION → PLACE_ORDER: 3
- PLACE_ORDER → MODIFY_ORDER: 2
- UNKNOWN → SMALL_TALK: 2
- SMALL_TALK → PLACE_ORDER: 2
- MODIFY_ORDER → None: 1
- UNKNOWN → PLACE_ORDER: 1
- SMALL_TALK → PAYMENT_CLAIM: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- ORDER_PROBLEM → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- SMALL_TALK → UNKNOWN: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
