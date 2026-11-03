# `qwen3.5-0.8b-single` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.1`, scorer `scorer@0.3`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 181/188 | n/a (one call per chat) |
| Intent, all customer messages | 248/278 (89.2%, 95% CI 0.850–0.923) | ? |
| Intent, last message | 72/90 (80.0%, 95% CI 0.706–0.870) | |
| Intent, earlier messages (mid-chat) | 176/188 (93.6%, 95% CI 0.892–0.963) | |
| Items (F1) | 117 found / 28 extra / 39 missed (F1 0.7774086378737541) | ? |
| Fully correct orders | 54/90 (95% CI (0.4967011780834921, 0.6951114082321718)) | ? |
| Same action (bot sends/asks the same; wording aside) | 55/90 (95% CI (0.5078226845453937, 0.7053024113608994)) | |

Field accuracy: {'method': 1.0, 'time': 0.9705882352941176, 'address': 1.0, 'payment': 1.0, 'name': 0.9852941176470589, 'decision': 0.9852941176470589, 'missing': 0.7941176470588235}

Hit the token limit: 0; latency p50/p95 {'p50': 13518, 'p95': 23156} ms (T4, fp16, greedy); output tokens p50 320.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 6, '2 validation errors for StudentOutput': 3}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 147 | 149 |
| SMALL_TALK | 43 | 43 | 51 |
| MODIFY_ORDER | 18 | 15 | 17 |
| MENU_QUESTION | 14 | 14 | 20 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 3 | 3 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| OUT_OF_SCOPE | 5 | 1 | 1 |
| DELIVERY_QUESTION | 4 | 4 | 4 |
| ORDER_STATUS | 4 | 4 | 5 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 0 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 8
- UNKNOWN → SMALL_TALK: 4
- PLACE_ORDER → MENU_QUESTION: 3
- OUT_OF_SCOPE → MENU_QUESTION: 2
- MODIFY_ORDER → PLACE_ORDER: 2
- PLACE_ORDER → SMALL_TALK: 2
- PLACE_ORDER → MODIFY_ORDER: 2
- OUT_OF_SCOPE → SMALL_TALK: 1
- HUMAN_REQUEST → MENU_QUESTION: 1
- PLACE_ORDER → ORDER_STATUS: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
- MODIFY_ORDER → None: 1
- ORDER_PROBLEM → SMALL_TALK: 1
