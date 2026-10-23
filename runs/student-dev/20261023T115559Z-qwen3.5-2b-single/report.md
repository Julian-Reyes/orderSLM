# `qwen3.5-2b-single` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.2`, finalize `finalize@0.1`. Dev numbers (tuning), not held-out results.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 86/91 | 90/91 |
| Valid answers, earlier messages | 169/177 | n/a (one call per chat) |
| Intent, all customer messages | 236/268 (88.1%, 95% CI 0.836–0.914) | 259/268 |
| Intent, last message | 80/91 (87.9%, 95% CI 0.796–0.931) | |
| Intent, earlier messages (mid-chat) | 156/177 (88.1%, 95% CI 0.825–0.921) | |
| Items (F1) | 103 found / 21 extra / 43 missed (F1 0.762962962962963) | F1 0.993103448275862 |
| Fully correct orders | 59/91 (95% CI (0.5460564927584927, 0.7386287086721032)) | 90/91 |

Field accuracy: {'method': 0.9661016949152542, 'time': 0.9322033898305084, 'address': 0.9830508474576272, 'payment': 0.9322033898305084, 'name': 1.0, 'decision': 1.0, 'missing': 0.8135593220338984}

Hit the token limit: 0; latency p50/p95 {'p50': 15164, 'p95': 23918} ms (T4, fp16, greedy); output tokens p50 310.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 12, '2 validation errors for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 160 | 147 | 152 |
| SMALL_TALK | 28 | 27 | 32 |
| MENU_QUESTION | 16 | 14 | 16 |
| MODIFY_ORDER | 14 | 8 | 8 |
| CONFIRM_ORDER | 8 | 8 | 8 |
| ORDER_PROBLEM | 8 | 7 | 8 |
| OUT_OF_SCOPE | 5 | 1 | 1 |
| CANCEL_ORDER | 4 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 4 | 6 |
| HUMAN_REQUEST | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 5 |
| REFUND_REQUEST | 4 | 4 | 4 |
| UNKNOWN | 4 | 1 | 4 |
| PAYMENT_QUESTION | 3 | 3 | 3 |
| PAYMENT_CLAIM | 2 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 9
- MODIFY_ORDER → PLACE_ORDER: 4
- UNKNOWN → SMALL_TALK: 3
- OUT_OF_SCOPE → DELIVERY_QUESTION: 2
- PLACE_ORDER → UNKNOWN: 2
- MODIFY_ORDER → None: 2
- MENU_QUESTION → UNKNOWN: 1
- HUMAN_REQUEST → None: 1
- PLACE_ORDER → SMALL_TALK: 1
- PAYMENT_CLAIM → ORDER_PROBLEM: 1
- SMALL_TALK → PLACE_ORDER: 1
- MENU_QUESTION → None: 1
- OUT_OF_SCOPE → MENU_QUESTION: 1
- OUT_OF_SCOPE → SMALL_TALK: 1
- PLACE_ORDER → MENU_QUESTION: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
