# `qwen3.5-0.8b-single-v4` on fresh2 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh2 split: written after the v3 fixes that used fresh, never tuned on (the measure of those fixes).

**Incomplete run: the scoring code crashed on 275 customer messages (no answer, e.g. a decoding error); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 0/90 | ?/? |
| Valid answers, earlier messages | 0/185 | n/a (one call per chat) |
| Intent, all customer messages | 0/275 (0.0%, 95% CI 0.000–0.014) | ? |
| Intent, last message | 0/90 (0.0%, 95% CI 0.000–0.041) | |
| Intent, earlier messages (mid-chat) | 0/185 (0.0%, 95% CI 0.000–0.020) | |
| Items (F1) | 0 found / 0 extra / 171 missed (F1 0.0) | ? |
| Fully correct orders | 0/90 (95% CI (0.0, 0.04093706842168078)) | ? |
| Same action (bot sends/asks the same; wording aside) | 0/90 (95% CI (0.0, 0.04093706842168078)) | |

Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}

Hit the token limit: 0; latency p50/p95 None ms (T4, fp16, greedy); output tokens p50 None.
Invalid answers by reason: {'RuntimeError:': 275}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 173 | 0 | 0 |
| SMALL_TALK | 25 | 0 | 0 |
| MODIFY_ORDER | 18 | 0 | 0 |
| MENU_QUESTION | 12 | 0 | 0 |
| CONFIRM_ORDER | 9 | 0 | 0 |
| UNKNOWN | 7 | 0 | 0 |
| OUT_OF_SCOPE | 6 | 0 | 0 |
| ORDER_STATUS | 5 | 0 | 0 |
| DELIVERY_QUESTION | 4 | 0 | 0 |
| ORDER_PROBLEM | 4 | 0 | 0 |
| REFUND_REQUEST | 4 | 0 | 0 |
| CANCEL_ORDER | 2 | 0 | 0 |
| HUMAN_REQUEST | 2 | 0 | 0 |
| PAYMENT_CLAIM | 2 | 0 | 0 |
| PAYMENT_QUESTION | 2 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 173
- SMALL_TALK → None: 25
- MODIFY_ORDER → None: 18
- MENU_QUESTION → None: 12
- CONFIRM_ORDER → None: 9
- UNKNOWN → None: 7
- OUT_OF_SCOPE → None: 6
- ORDER_STATUS → None: 5
- DELIVERY_QUESTION → None: 4
- ORDER_PROBLEM → None: 4
- REFUND_REQUEST → None: 4
- PAYMENT_CLAIM → None: 2
- CANCEL_ORDER → None: 2
- PAYMENT_QUESTION → None: 2
- HUMAN_REQUEST → None: 2
