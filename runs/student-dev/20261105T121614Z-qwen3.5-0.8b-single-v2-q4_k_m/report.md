# `qwen3.5-0.8b-single-v2-q4_k_m` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.4`, finalize `finalize@0.2`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/91 | 90/91 |
| Valid answers, earlier messages | 174/177 | n/a (one call per chat) |
| Intent, all customer messages | 244/268 (91.0%, 95% CI 0.870–0.939) | 257/268 |
| Intent, last message | 83/91 (91.2%, 95% CI 0.836–0.955) | |
| Intent, earlier messages (mid-chat) | 161/177 (91.0%, 95% CI 0.858–0.944) | |
| Items (F1) | 119 found / 16 extra / 27 missed (F1 0.8469750889679716) | F1 0.993103448275862 |
| Fully correct orders | 66/91 (95% CI (0.6258502470283998, 0.8064495032921346)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 67/91 (95% CI (0.6374922768443272, 0.81589526617477)) | |

Field accuracy: {'method': 1.0, 'time': 0.9836065573770492, 'address': 0.9836065573770492, 'payment': 0.9836065573770492, 'name': 1.0, 'decision': 1.0, 'missing': 0.8032786885245902}

Hit the token limit: 0; latency p50/p95 {'p50': 2378, 'p95': 3395} ms (T4, fp16, greedy); output tokens p50 318.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 6}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 156 | 161 |
| SMALL_TALK | 26 | 25 | 30 |
| MENU_QUESTION | 16 | 12 | 12 |
| MODIFY_ORDER | 14 | 10 | 11 |
| CONFIRM_ORDER | 8 | 7 | 8 |
| ORDER_PROBLEM | 8 | 7 | 9 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| HUMAN_REQUEST | 4 | 1 | 1 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 2 | 3 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 0 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 3
- MODIFY_ORDER → PLACE_ORDER: 3
- PLACE_ORDER → SMALL_TALK: 3
- UNKNOWN → SMALL_TALK: 1
- MENU_QUESTION → UNKNOWN: 1
- SMALL_TALK → MODIFY_ORDER: 1
- MODIFY_ORDER → None: 1
- HUMAN_REQUEST → PLACE_ORDER: 1
- HUMAN_REQUEST → SMALL_TALK: 1
- MENU_QUESTION → ORDER_PROBLEM: 1
- UNKNOWN → CONFIRM_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- CONFIRM_ORDER → None: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- MENU_QUESTION → None: 1
- ORDER_PROBLEM → PAYMENT_CLAIM: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- HUMAN_REQUEST → ORDER_PROBLEM: 1
