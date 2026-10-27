# `qwen3.5-2b-mixed` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.2`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 89/90 | ?/? |
| Valid answers, earlier messages | 184/188 | n/a (one call per chat) |
| Intent, all customer messages | 248/278 (89.2%, 95% CI 0.850–0.923) | ? |
| Intent, last message | 77/90 (85.6%, 95% CI 0.768–0.914) | |
| Intent, earlier messages (mid-chat) | 171/188 (91.0%, 95% CI 0.860–0.943) | |
| Items (F1) | 115 found / 30 extra / 41 missed (F1 0.7641196013289037) | ? |
| Fully correct orders | 52/90 (95% CI (0.4746099802268749, 0.6745775869075303)) | ? |

Field accuracy: {'method': 0.9701492537313433, 'time': 0.9701492537313433, 'address': 0.9701492537313433, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.7014925373134329}

Hit the token limit: 0; latency p50/p95 {'p50': 15018, 'p95': 26062} ms (T4, fp16, greedy); output tokens p50 323.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 5}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 150 | 143 | 154 |
| SMALL_TALK | 56 | 46 | 51 |
| MODIFY_ORDER | 18 | 14 | 15 |
| MENU_QUESTION | 14 | 12 | 15 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 5 | 7 |
| ORDER_PROBLEM | 5 | 3 | 4 |
| OUT_OF_SCOPE | 5 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 3 | 3 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 2 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → PLACE_ORDER: 7
- PLACE_ORDER → MENU_QUESTION: 3
- MODIFY_ORDER → PLACE_ORDER: 3
- SMALL_TALK → None: 3
- UNKNOWN → SMALL_TALK: 2
- MENU_QUESTION → SMALL_TALK: 1
- OUT_OF_SCOPE → SMALL_TALK: 1
- MODIFY_ORDER → None: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- ORDER_STATUS → ORDER_PROBLEM: 1
- PLACE_ORDER → UNKNOWN: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- MENU_QUESTION → UNKNOWN: 1
- PLACE_ORDER → PAYMENT_QUESTION: 1
- ORDER_PROBLEM → SMALL_TALK: 1
- PLACE_ORDER → None: 1
