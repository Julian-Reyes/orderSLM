# `qwen3.5-0.8b-single-v5` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.5`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/90 | ?/? |
| Valid answers, earlier messages | 186/188 | n/a (one call per chat) |
| Intent, all customer messages | 267/278 (96.0%, 95% CI 0.931–0.978) | ? |
| Intent, last message | 85/90 (94.4%, 95% CI 0.876–0.976) | |
| Intent, earlier messages (mid-chat) | 182/188 (96.8%, 95% CI 0.932–0.985) | |
| Items (F1) | 149 found / 7 extra / 7 missed (F1 0.9551282051282052) | ? |
| Fully correct orders | 81/90 (95% CI (0.8207564910060137, 0.9464938542566417)) | ? |
| Same action (bot sends/asks the same; wording aside) | 83/90 (95% CI (0.8480596940416417, 0.9618156704022723)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9}

Hit the token limit: 0; latency p50/p95 {'p50': 13938, 'p95': 23628} ms (T4, fp16, greedy); output tokens p50 325.5.
Invalid answers by reason: {'1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 161 | 164 |
| SMALL_TALK | 43 | 40 | 43 |
| MODIFY_ORDER | 18 | 18 | 18 |
| MENU_QUESTION | 14 | 13 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 4 | 5 |
| ORDER_PROBLEM | 5 | 4 | 4 |
| OUT_OF_SCOPE | 5 | 5 | 6 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 2 |

Mistakes (gold → predicted):

- UNKNOWN → SMALL_TALK: 3
- SMALL_TALK → PLACE_ORDER: 2
- PLACE_ORDER → None: 2
- SMALL_TALK → UNKNOWN: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- ORDER_PROBLEM → REFUND_REQUEST: 1
