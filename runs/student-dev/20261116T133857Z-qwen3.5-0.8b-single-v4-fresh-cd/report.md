# `qwen3.5-0.8b-single-v4` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

**Incomplete run: the scoring code crashed on 278 customer messages (no answer, e.g. a decoding error); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 0/90 | ?/? |
| Valid answers, earlier messages | 0/188 | n/a (one call per chat) |
| Intent, all customer messages | 0/278 (0.0%, 95% CI 0.000–0.014) | ? |
| Intent, last message | 0/90 (0.0%, 95% CI 0.000–0.041) | |
| Intent, earlier messages (mid-chat) | 0/188 (0.0%, 95% CI 0.000–0.020) | |
| Items (F1) | 0 found / 0 extra / 156 missed (F1 0.0) | ? |
| Fully correct orders | 0/90 (95% CI (0.0, 0.04093706842168078)) | ? |
| Same action (bot sends/asks the same; wording aside) | 0/90 (95% CI (0.0, 0.04093706842168078)) | |

Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}

Hit the token limit: 0; latency p50/p95 None ms (T4, fp16, greedy); output tokens p50 None.
Invalid answers by reason: {'RuntimeError:': 278}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 0 | 0 |
| SMALL_TALK | 43 | 0 | 0 |
| MODIFY_ORDER | 18 | 0 | 0 |
| MENU_QUESTION | 14 | 0 | 0 |
| CONFIRM_ORDER | 9 | 0 | 0 |
| UNKNOWN | 7 | 0 | 0 |
| ORDER_PROBLEM | 5 | 0 | 0 |
| OUT_OF_SCOPE | 5 | 0 | 0 |
| DELIVERY_QUESTION | 4 | 0 | 0 |
| ORDER_STATUS | 4 | 0 | 0 |
| CANCEL_ORDER | 2 | 0 | 0 |
| HUMAN_REQUEST | 1 | 0 | 0 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 0 | 0 |
| REFUND_REQUEST | 1 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 163
- SMALL_TALK → None: 43
- MODIFY_ORDER → None: 18
- MENU_QUESTION → None: 14
- CONFIRM_ORDER → None: 9
- UNKNOWN → None: 7
- OUT_OF_SCOPE → None: 5
- ORDER_PROBLEM → None: 5
- DELIVERY_QUESTION → None: 4
- ORDER_STATUS → None: 4
- CANCEL_ORDER → None: 2
- PAYMENT_QUESTION → None: 1
- HUMAN_REQUEST → None: 1
- REFUND_REQUEST → None: 1
- PAYMENT_CLAIM → None: 1
