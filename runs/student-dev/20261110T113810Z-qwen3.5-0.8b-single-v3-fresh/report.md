# `qwen3.5-0.8b-single-v3` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.3`, scorer `scorer@0.4`, finalize `finalize@0.2`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 88/90 | ?/? |
| Valid answers, earlier messages | 184/188 | n/a (one call per chat) |
| Intent, all customer messages | 251/278 (90.3%, 95% CI 0.862–0.932) | ? |
| Intent, last message | 86/90 (95.6%, 95% CI 0.891–0.983) | |
| Intent, earlier messages (mid-chat) | 165/188 (87.8%, 95% CI 0.823–0.917) | |
| Items (F1) | 141 found / 10 extra / 15 missed (F1 0.9185667752442996) | ? |
| Fully correct orders | 76/90 (95% CI (0.755669687335892, 0.9050181099736166)) | ? |
| Same action (bot sends/asks the same; wording aside) | 77/90 (95% CI (0.7683993769120605, 0.9136009299880774)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 0.9852941176470589, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8529411764705882}

Hit the token limit: 0; latency p50/p95 {'p50': 13816, 'p95': 23106} ms (T4, fp16, greedy); output tokens p50 326.5.
Invalid answers by reason: {'2 validation errors for StudentOutput': 4, '1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 156 | 161 |
| SMALL_TALK | 43 | 26 | 28 |
| MODIFY_ORDER | 18 | 18 | 18 |
| MENU_QUESTION | 14 | 13 | 13 |
| CONFIRM_ORDER | 9 | 9 | 9 |
| UNKNOWN | 7 | 6 | 19 |
| ORDER_PROBLEM | 5 | 5 | 6 |
| OUT_OF_SCOPE | 5 | 5 | 5 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 13
- PLACE_ORDER → None: 6
- SMALL_TALK → PLACE_ORDER: 4
- MENU_QUESTION → SMALL_TALK: 1
- UNKNOWN → SMALL_TALK: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PLACE_ORDER → ORDER_PROBLEM: 1
