# `qwen3.5-0.8b-single` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.2`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/91 | 90/91 |
| Valid answers, earlier messages | 176/177 | n/a (one call per chat) |
| Intent, all customer messages | 244/268 (91.0%, 95% CI 0.870–0.939) | 259/268 |
| Intent, last message | 83/91 (91.2%, 95% CI 0.836–0.955) | |
| Intent, earlier messages (mid-chat) | 161/177 (91.0%, 95% CI 0.858–0.944) | |
| Items (F1) | 114 found / 21 extra / 32 missed (F1 0.8113879003558719) | F1 0.993103448275862 |
| Fully correct orders | 64/91 (95% CI (0.6027577176380822, 0.7873664472853271)) | 90/91 |

Field accuracy: {'method': 0.9841269841269841, 'time': 0.9365079365079365, 'address': 0.9841269841269841, 'payment': 0.8888888888888888, 'name': 1.0, 'decision': 0.9841269841269841, 'missing': 0.8412698412698413}

Hit the token limit: 0; latency p50/p95 {'p50': 13141, 'p95': 19045} ms (T4, fp16, greedy); output tokens p50 316.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 157 | 164 |
| SMALL_TALK | 28 | 25 | 31 |
| MENU_QUESTION | 16 | 16 | 21 |
| MODIFY_ORDER | 14 | 9 | 10 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 1 | 1 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 2 | 3 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 0 | 0 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- UNKNOWN → SMALL_TALK: 4
- OUT_OF_SCOPE → MENU_QUESTION: 3
- MODIFY_ORDER → PLACE_ORDER: 3
- PAYMENT_CLAIM → PLACE_ORDER: 2
- SMALL_TALK → MODIFY_ORDER: 1
- PLACE_ORDER → SMALL_TALK: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- MODIFY_ORDER → SMALL_TALK: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
- PLACE_ORDER → None: 1
- MODIFY_ORDER → None: 1
- SMALL_TALK → MENU_QUESTION: 1
- SMALL_TALK → PLACE_ORDER: 1
- PLACE_ORDER → MENU_QUESTION: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
