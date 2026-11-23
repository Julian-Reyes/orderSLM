# `qwen3.5-0.8b-single-v4` on fresh4 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.4`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh4 split: written after the v5 fixes that used dev, fresh, fresh2 and fresh3, never tuned on.

**Incomplete run: the scoring code crashed on 343 customer messages (no answer, e.g. a decoding error); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 0/110 | ?/? |
| Valid answers, earlier messages | 0/233 | n/a (one call per chat) |
| Intent, all customer messages | 0/343 (0.0%, 95% CI 0.000–0.011) | ? |
| Intent, last message | 0/110 (0.0%, 95% CI 0.000–0.034) | |
| Intent, earlier messages (mid-chat) | 0/233 (0.0%, 95% CI 0.000–0.016) | |
| Items (F1) | 0 found / 0 extra / 195 missed (F1 0.0) | ? |
| Fully correct orders | 0/110 (95% CI (0.0, 0.03374513358912735)) | ? |
| Same action (bot sends/asks the same; wording aside) | 0/110 (95% CI (0.0, 0.03374513358912735)) | |

Field accuracy: {'method': None, 'time': None, 'address': None, 'payment': None, 'name': None, 'decision': None, 'missing': None}

Hit the token limit: 0; latency p50/p95 None ms (T4, fp16, greedy); output tokens p50 None.
Invalid answers by reason: {'RuntimeError:': 343}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 215 | 0 | 0 |
| SMALL_TALK | 49 | 0 | 0 |
| MODIFY_ORDER | 20 | 0 | 0 |
| MENU_QUESTION | 16 | 0 | 0 |
| CONFIRM_ORDER | 8 | 0 | 0 |
| OUT_OF_SCOPE | 7 | 0 | 0 |
| UNKNOWN | 7 | 0 | 0 |
| DELIVERY_QUESTION | 5 | 0 | 0 |
| ORDER_STATUS | 4 | 0 | 0 |
| CANCEL_ORDER | 2 | 0 | 0 |
| HUMAN_REQUEST | 2 | 0 | 0 |
| ORDER_PROBLEM | 2 | 0 | 0 |
| PAYMENT_CLAIM | 2 | 0 | 0 |
| PAYMENT_QUESTION | 2 | 0 | 0 |
| REFUND_REQUEST | 2 | 0 | 0 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 215
- SMALL_TALK → None: 49
- MODIFY_ORDER → None: 20
- MENU_QUESTION → None: 16
- CONFIRM_ORDER → None: 8
- OUT_OF_SCOPE → None: 7
- UNKNOWN → None: 7
- DELIVERY_QUESTION → None: 5
- ORDER_STATUS → None: 4
- PAYMENT_QUESTION → None: 2
- REFUND_REQUEST → None: 2
- CANCEL_ORDER → None: 2
- PAYMENT_CLAIM → None: 2
- ORDER_PROBLEM → None: 2
- HUMAN_REQUEST → None: 2
