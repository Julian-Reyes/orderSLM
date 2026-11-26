# `qwen3.5-0.8b-single-v6` on fresh4 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh4 split: written after the v5 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 109/110 | ?/? |
| Valid answers, earlier messages | 233/233 | n/a (one call per chat) |
| Intent, all customer messages | 321/343 (93.6%, 95% CI 0.905–0.957) | ? |
| Intent, last message | 102/110 (92.7%, 95% CI 0.863–0.963) | |
| Intent, earlier messages (mid-chat) | 219/233 (94.0%, 95% CI 0.902–0.964) | |
| Items (F1) | 181 found / 14 extra / 14 missed (F1 0.9282051282051282) | ? |
| Fully correct orders | 97/110 (95% CI (0.8082479662756031, 0.9296193862563361)) | ? |
| Same action (bot sends/asks the same; wording aside) | 97/110 (95% CI (0.8082479662756031, 0.9296193862563361)) | |

Field accuracy: {'method': 1.0, 'time': 0.9882352941176471, 'address': 1.0, 'payment': 1.0, 'name': 0.9882352941176471, 'decision': 1.0, 'missing': 0.9529411764705882}

Hit the token limit: 0; latency p50/p95 {'p50': 14626, 'p95': 19696} ms (T4, fp16, greedy); output tokens p50 341.
Invalid answers by reason: {'1 validation error for StudentOutput': 1}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 215 | 212 | 214 |
| SMALL_TALK | 49 | 40 | 45 |
| MODIFY_ORDER | 20 | 19 | 20 |
| MENU_QUESTION | 16 | 16 | 19 |
| CONFIRM_ORDER | 8 | 6 | 6 |
| OUT_OF_SCOPE | 7 | 6 | 7 |
| UNKNOWN | 7 | 4 | 10 |
| DELIVERY_QUESTION | 5 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 6 |
| CANCEL_ORDER | 2 | 2 | 3 |
| HUMAN_REQUEST | 2 | 2 | 2 |
| ORDER_PROBLEM | 2 | 2 | 2 |
| PAYMENT_CLAIM | 2 | 1 | 1 |
| PAYMENT_QUESTION | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 6
- UNKNOWN → SMALL_TALK: 3
- DELIVERY_QUESTION → PLACE_ORDER: 2
- PLACE_ORDER → MENU_QUESTION: 2
- CONFIRM_ORDER → SMALL_TALK: 2
- OUT_OF_SCOPE → MENU_QUESTION: 1
- SMALL_TALK → OUT_OF_SCOPE: 1
- SMALL_TALK → ORDER_STATUS: 1
- PLACE_ORDER → MODIFY_ORDER: 1
- PAYMENT_CLAIM → ORDER_STATUS: 1
- MODIFY_ORDER → None: 1
- SMALL_TALK → CANCEL_ORDER: 1
