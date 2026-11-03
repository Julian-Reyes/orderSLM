# `qwen3.5-2b-mixed-v2` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.2`, scorer `scorer@0.3`, finalize `finalize@0.1`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 182/188 | n/a (one call per chat) |
| Intent, all customer messages | 257/278 (92.5%, 95% CI 0.887–0.950) | ? |
| Intent, last message | 81/90 (90.0%, 95% CI 0.821–0.946) | |
| Intent, earlier messages (mid-chat) | 176/188 (93.6%, 95% CI 0.892–0.963) | |
| Items (F1) | 136 found / 16 extra / 20 missed (F1 0.8831168831168831) | ? |
| Fully correct orders | 70/90 (95% CI (0.6815249725824009, 0.8512877671833321)) | ? |
| Same action (bot sends/asks the same; wording aside) | 72/90 (95% CI (0.7058607285729566, 0.8695770303740351)) | |

Field accuracy: {'method': 0.9855072463768116, 'time': 1.0, 'address': 0.9855072463768116, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8405797101449275}

Hit the token limit: 0; latency p50/p95 {'p50': 14860, 'p95': 25412} ms (T4, fp16, greedy); output tokens p50 327.0.
Invalid answers by reason: {'1 validation error for StudentOutput': 8}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 152 | 155 |
| SMALL_TALK | 43 | 43 | 49 |
| MODIFY_ORDER | 18 | 16 | 16 |
| MENU_QUESTION | 14 | 12 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 4 | 5 |
| ORDER_PROBLEM | 5 | 4 | 5 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 3 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 7
- MODIFY_ORDER → PLACE_ORDER: 2
- UNKNOWN → SMALL_TALK: 2
- PLACE_ORDER → SMALL_TALK: 2
- MENU_QUESTION → SMALL_TALK: 1
- PLACE_ORDER → MENU_QUESTION: 1
- UNKNOWN → None: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- ORDER_STATUS → ORDER_PROBLEM: 1
- PLACE_ORDER → ORDER_STATUS: 1
- MENU_QUESTION → UNKNOWN: 1
- ORDER_PROBLEM → SMALL_TALK: 1
