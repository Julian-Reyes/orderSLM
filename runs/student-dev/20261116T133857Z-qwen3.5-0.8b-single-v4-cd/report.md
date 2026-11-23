# `qwen3.5-0.8b-single-v4` on dev at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Dev numbers (tuning), not held-out results.

**Incomplete run: the scoring code crashed on 268 customer messages (no answer, e.g. a decoding error); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 0/91 | 90/91 |
| Valid answers, earlier messages | 0/177 | n/a (one call per chat) |
| Intent, all customer messages | 0/268 (0.0%, 95% CI 0.000–0.014) | 257/268 |
| Intent, last message | 0/91 (0.0%, 95% CI 0.000–0.041) | |
| Intent, earlier messages (mid-chat) | 0/177 (0.0%, 95% CI 0.000–0.021) | |
| Items (F1) | 0 found / 0 extra / 146 missed (F1 0.0) | F1 0.993103448275862 |
| Fully correct orders | 0/91 (95% CI (0.0, 0.04050543221539915)) | 90/91 |
| Same action (bot sends/asks the same; wording aside) | 0/91 (95% CI (0.0, 0.04050543221539915)) | |

Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}

Hit the token limit: 0; latency p50/p95 None ms (T4, fp16, greedy); output tokens p50 None.
Invalid answers by reason: {'RuntimeError:': 268}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 162 | 0 | 0 |
| SMALL_TALK | 26 | 0 | 0 |
| MENU_QUESTION | 16 | 0 | 0 |
| MODIFY_ORDER | 14 | 0 | 0 |
| CONFIRM_ORDER | 8 | 0 | 0 |
| ORDER_PROBLEM | 8 | 0 | 0 |
| OUT_OF_SCOPE | 5 | 0 | 0 |
| CANCEL_ORDER | 4 | 0 | 0 |
| DELIVERY_QUESTION | 4 | 0 | 0 |
| HUMAN_REQUEST | 4 | 0 | 0 |
| ORDER_STATUS | 4 | 0 | 0 |
| REFUND_REQUEST | 4 | 0 | 0 |
| UNKNOWN | 4 | 0 | 0 |
| PAYMENT_QUESTION | 3 | 0 | 0 |
| PAYMENT_CLAIM | 2 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 162
- SMALL_TALK → None: 26
- MENU_QUESTION → None: 16
- MODIFY_ORDER → None: 14
- CONFIRM_ORDER → None: 8
- ORDER_PROBLEM → None: 8
- OUT_OF_SCOPE → None: 5
- CANCEL_ORDER → None: 4
- UNKNOWN → None: 4
- ORDER_STATUS → None: 4
- HUMAN_REQUEST → None: 4
- DELIVERY_QUESTION → None: 4
- REFUND_REQUEST → None: 4
- PAYMENT_QUESTION → None: 3
- PAYMENT_CLAIM → None: 2
