# `qwen3.5-0.8b-single-v2-q8_0` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.4`, finalize `finalize@0.2`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/91 | 90/91 |
| Valid answers, earlier messages | 175/177 | n/a (one call per chat) |
| Intent, all customer messages | 248/268 (92.5%, 95% CI 0.888–0.951) | 257/268 |
| Intent, last message | 84/91 (92.3%, 95% CI 0.850–0.962) | |
| Intent, earlier messages (mid-chat) | 164/177 (92.7%, 95% CI 0.878–0.957) | |
| Items (F1) | 125 found / 16 extra / 21 missed (F1 0.8710801393728222) | F1 0.993103448275862 |
| Fully correct orders | 69/91 (95% CI (0.6609799811910234, 0.8345831472251989)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 71/91 (95% CI (0.6847588519917921, 0.8529798618215557)) | |

Field accuracy: {'method': 1.0, 'time': 0.9838709677419355, 'address': 0.9838709677419355, 'payment': 0.967741935483871, 'name': 1.0, 'decision': 0.9838709677419355, 'missing': 0.8709677419354839}

Hit the token limit: 0; latency p50/p95 {'p50': 112088, 'p95': 204741} ms (T4, fp16, greedy); output tokens p50 319.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 4}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 157 | 162 |
| SMALL_TALK | 26 | 25 | 29 |
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

- PLACE_ORDER → None: 3
- MODIFY_ORDER → PLACE_ORDER: 3
- PLACE_ORDER → SMALL_TALK: 2
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
