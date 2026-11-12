# `qwen3.5-0.8b-single-v3` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.3`, scorer `scorer@0.5`, finalize `finalize@0.2`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 90/90 | ?/? |
| Valid answers, earlier messages | 185/185 | n/a (one call per chat) |
| Intent, all customer messages | 255/275 (92.7%, 95% CI 0.890–0.952) | ? |
| Intent, last message | 85/90 (94.4%, 95% CI 0.876–0.976) | |
| Intent, earlier messages (mid-chat) | 170/185 (91.9%, 95% CI 0.871–0.950) | |
| Items (F1) | 146 found / 22 extra / 25 missed (F1 0.8613569321533924) | ? |
| Fully correct orders | 67/90 (95% CI (0.645621572349918, 0.823253638643927)) | ? |
| Same action (bot sends/asks the same; wording aside) | 68/90 (95% CI (0.6575143545381369, 0.8326733660463373)) | |

Field accuracy: {'method': 1.0, 'time': 0.9852941176470589, 'address': 1.0, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8529411764705882}

Hit the token limit: 0; latency p50/p95 {'p50': 14465, 'p95': 21109} ms (T4, fp16, greedy); output tokens p50 340.
Invalid answers by reason: none

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 169 | 173 |
| SMALL_TALK | 25 | 18 | 21 |
| MODIFY_ORDER | 18 | 17 | 19 |
| MENU_QUESTION | 12 | 11 | 12 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 4 | 10 |
| OUT_OF_SCOPE | 6 | 6 | 8 |
| ORDER_STATUS | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 4 |
| ORDER_PROBLEM | 4 | 4 | 4 |
| REFUND_REQUEST | 4 | 3 | 3 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 2 |
| PAYMENT_QUESTION | 2 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 5
- UNKNOWN → SMALL_TALK: 3
- PLACE_ORDER → MODIFY_ORDER: 2
- PAYMENT_CLAIM → PLACE_ORDER: 1
- MODIFY_ORDER → PLACE_ORDER: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → DELIVERY_QUESTION: 1
- MENU_QUESTION → OUT_OF_SCOPE: 1
- PLACE_ORDER → UNKNOWN: 1
- PLACE_ORDER → MENU_QUESTION: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PAYMENT_QUESTION → PLACE_ORDER: 1
- REFUND_REQUEST → PAYMENT_CLAIM: 1
