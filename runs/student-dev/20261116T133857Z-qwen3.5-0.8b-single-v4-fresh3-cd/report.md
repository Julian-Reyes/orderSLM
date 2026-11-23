# `qwen3.5-0.8b-single-v4` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

**Incomplete run: the scoring code crashed on 321 customer messages (no answer, e.g. a decoding error); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 0/110 | ?/? |
| Valid answers, earlier messages | 0/211 | n/a (one call per chat) |
| Intent, all customer messages | 0/321 (0.0%, 95% CI 0.000–0.012) | ? |
| Intent, last message | 0/110 (0.0%, 95% CI 0.000–0.034) | |
| Intent, earlier messages (mid-chat) | 0/211 (0.0%, 95% CI 0.000–0.018) | |
| Items (F1) | 0 found / 0 extra / 186 missed (F1 0.0) | ? |
| Fully correct orders | 0/110 (95% CI (0.0, 0.03374513358912735)) | ? |
| Same action (bot sends/asks the same; wording aside) | 0/110 (95% CI (0.0, 0.03374513358912735)) | |

Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}

Hit the token limit: 0; latency p50/p95 None ms (T4, fp16, greedy); output tokens p50 None.
Invalid answers by reason: {'RuntimeError:': 321}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 0 | 0 |
| SMALL_TALK | 35 | 0 | 0 |
| MODIFY_ORDER | 21 | 0 | 0 |
| MENU_QUESTION | 18 | 0 | 0 |
| CONFIRM_ORDER | 9 | 0 | 0 |
| UNKNOWN | 9 | 0 | 0 |
| OUT_OF_SCOPE | 6 | 0 | 0 |
| DELIVERY_QUESTION | 5 | 0 | 0 |
| ORDER_PROBLEM | 5 | 0 | 0 |
| ORDER_STATUS | 5 | 0 | 0 |
| CANCEL_ORDER | 2 | 0 | 0 |
| REFUND_REQUEST | 2 | 0 | 0 |
| HUMAN_REQUEST | 1 | 0 | 0 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 201
- SMALL_TALK → None: 35
- MODIFY_ORDER → None: 21
- MENU_QUESTION → None: 18
- UNKNOWN → None: 9
- CONFIRM_ORDER → None: 9
- OUT_OF_SCOPE → None: 6
- DELIVERY_QUESTION → None: 5
- ORDER_STATUS → None: 5
- ORDER_PROBLEM → None: 5
- CANCEL_ORDER → None: 2
- REFUND_REQUEST → None: 2
- HUMAN_REQUEST → None: 1
- PAYMENT_QUESTION → None: 1
- PAYMENT_CLAIM → None: 1
