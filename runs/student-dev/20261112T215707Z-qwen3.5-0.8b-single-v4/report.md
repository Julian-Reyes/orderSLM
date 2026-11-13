# `qwen3.5-0.8b-single-v4` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/91 | 90/91 |
| Valid answers, earlier messages | 177/177 | n/a (one call per chat) |
| Intent, all customer messages | 251/268 (93.7%, 95% CI 0.901–0.960) | 257/268 |
| Intent, last message | 85/91 (93.4%, 95% CI 0.864–0.969) | |
| Intent, earlier messages (mid-chat) | 166/177 (93.8%, 95% CI 0.892–0.965) | |
| Items (F1) | 134 found / 8 extra / 12 missed (F1 0.9305555555555556) | F1 0.993103448275862 |
| Fully correct orders | 79/91 (95% CI (0.7835113710706528, 0.9229296843311962)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 79/91 (95% CI (0.7835113710706528, 0.9229296843311962)) | |

Field accuracy: {'method': 1.0, 'time': 0.9841269841269841, 'address': 1.0, 'payment': 0.9841269841269841, 'name': 1.0, 'decision': 1.0, 'missing': 0.9365079365079365}

Hit the token limit: 0; latency p50/p95 {'p50': 14579, 'p95': 21539} ms (T4, fp16, greedy); output tokens p50 324.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 159 | 163 |
| SMALL_TALK | 26 | 24 | 26 |
| MENU_QUESTION | 16 | 15 | 19 |
| MODIFY_ORDER | 14 | 13 | 15 |
| CONFIRM_ORDER | 8 | 8 | 9 |
| ORDER_PROBLEM | 8 | 8 | 9 |
| OUT_OF_SCOPE | 5 | 2 | 2 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 1 | 2 |
| ORDER_STATUS | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 2 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- OUT_OF_SCOPE → MENU_QUESTION: 2
- PAYMENT_CLAIM → PLACE_ORDER: 2
- UNKNOWN → SMALL_TALK: 1
- MENU_QUESTION → UNKNOWN: 1
- PLACE_ORDER → None: 1
- SMALL_TALK → MODIFY_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
- UNKNOWN → CONFIRM_ORDER: 1
- PLACE_ORDER → MENU_QUESTION: 1
- SMALL_TALK → MENU_QUESTION: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
