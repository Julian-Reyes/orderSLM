# `qwen3.5-0.8b-single-v6` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 91/91 | 90/91 |
| Valid answers, earlier messages | 176/177 | n/a (one call per chat) |
| Intent, all customer messages | 251/268 (93.7%, 95% CI 0.901–0.960) | 257/268 |
| Intent, last message | 85/91 (93.4%, 95% CI 0.864–0.969) | |
| Intent, earlier messages (mid-chat) | 166/177 (93.8%, 95% CI 0.892–0.965) | |
| Items (F1) | 137 found / 6 extra / 9 missed (F1 0.9480968858131488) | F1 0.993103448275862 |
| Fully correct orders | 82/91 (95% CI (0.8226124740847462, 0.9470919594127909)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 82/91 (95% CI (0.8226124740847462, 0.9470919594127909)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 0.984375, 'name': 1.0, 'decision': 1.0, 'missing': 0.9375}

Hit the token limit: 0; latency p50/p95 {'p50': 13471, 'p95': 19994} ms (T4, fp16, greedy); output tokens p50 321.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 160 | 165 |
| SMALL_TALK | 26 | 25 | 27 |
| MENU_QUESTION | 16 | 14 | 14 |
| MODIFY_ORDER | 14 | 11 | 13 |
| CONFIRM_ORDER | 8 | 8 | 9 |
| ORDER_PROBLEM | 8 | 7 | 9 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 5 |
| HUMAN_REQUEST | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 3 | 3 |
| UNKNOWN | 4 | 2 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- MODIFY_ORDER → PLACE_ORDER: 3
- UNKNOWN → SMALL_TALK: 1
- PLACE_ORDER → None: 1
- MENU_QUESTION → UNKNOWN: 1
- SMALL_TALK → MODIFY_ORDER: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- UNKNOWN → CONFIRM_ORDER: 1
- REFUND_REQUEST → ORDER_PROBLEM: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- ORDER_PROBLEM → DELIVERY_QUESTION: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
