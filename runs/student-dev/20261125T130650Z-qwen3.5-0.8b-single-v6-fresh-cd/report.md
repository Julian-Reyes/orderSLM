# `qwen3.5-0.8b-single-v6` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 186/188 | n/a (one call per chat) |
| Intent, all customer messages | 262/278 (94.2%, 95% CI 0.909–0.964) | ? |
| Intent, last message | 84/90 (93.3%, 95% CI 0.862–0.969) | |
| Intent, earlier messages (mid-chat) | 178/188 (94.7%, 95% CI 0.905–0.971) | |
| Items (F1) | 144 found / 5 extra / 12 missed (F1 0.9442622950819672) | ? |
| Fully correct orders | 79/90 (95% CI (0.7942607696004786, 0.930364556480918)) | ? |
| Same action (bot sends/asks the same; wording aside) | 81/90 (95% CI (0.8207564910060137, 0.9464938542566417)) | |

Field accuracy: {'method': 1.0, 'time': 0.9852941176470589, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8970588235294118}

Hit the token limit: 0; latency p50/p95 {'p50': 13964, 'p95': 23564} ms (T4, fp16, greedy); output tokens p50 325.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 4}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 154 | 157 |
| SMALL_TALK | 43 | 38 | 39 |
| MODIFY_ORDER | 18 | 18 | 18 |
| MENU_QUESTION | 14 | 14 | 18 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 7 | 9 |
| ORDER_PROBLEM | 5 | 4 | 5 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 4
- PLACE_ORDER → MENU_QUESTION: 3
- SMALL_TALK → PLACE_ORDER: 2
- SMALL_TALK → UNKNOWN: 2
- PLACE_ORDER → SMALL_TALK: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PLACE_ORDER → ORDER_PROBLEM: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
- SMALL_TALK → MENU_QUESTION: 1
