# `qwen3.5-0.8b-single-v2` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.2`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/91 | 90/91 |
| Valid answers, earlier messages | 175/177 | n/a (one call per chat) |
| Intent, all customer messages | 251/268 (93.7%, 95% CI 0.901–0.960) | 259/268 |
| Intent, last message | 85/91 (93.4%, 95% CI 0.864–0.969) | |
| Intent, earlier messages (mid-chat) | 166/177 (93.8%, 95% CI 0.892–0.965) | |
| Items (F1) | 126 found / 17 extra / 20 missed (F1 0.8719723183391004) | F1 0.993103448275862 |
| Fully correct orders | 70/91 (95% CI (0.672831372058367, 0.8438195490564182)) | 90/91 |

Field accuracy: {'method': 1.0, 'time': 0.9841269841269841, 'address': 1.0, 'payment': 0.9682539682539683, 'name': 1.0, 'decision': 0.9841269841269841, 'missing': 0.873015873015873}

Hit the token limit: 0; latency p50/p95 {'p50': 13542, 'p95': 19839} ms (T4, fp16, greedy); output tokens p50 321.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 158 | 163 |
| SMALL_TALK | 28 | 27 | 29 |
| MENU_QUESTION | 16 | 13 | 13 |
| MODIFY_ORDER | 14 | 11 | 12 |
| CONFIRM_ORDER | 8 | 8 | 9 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 6 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 2 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- MODIFY_ORDER → PLACE_ORDER: 3
- PLACE_ORDER → None: 2
- UNKNOWN → SMALL_TALK: 1
- MENU_QUESTION → UNKNOWN: 1
- SMALL_TALK → MODIFY_ORDER: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- UNKNOWN → CONFIRM_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- MENU_QUESTION → None: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
