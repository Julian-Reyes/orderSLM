# `qwen3.5-0.8b-single-v3` on fresh at every customer message

Prompt `student-extract@0.1`, data `student-data@0.3`, scorer `scorer@0.4`, finalize `finalize@0.2`. Fresh split: written after the dev-based fixes, never tuned on (the measure of those fixes).

**Incomplete run: 32 customer messages were never answered (the session stopped first); they count as invalid below. Not a result.**

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 79/90 | ?/? |
| Valid answers, earlier messages | 161/188 | n/a (one call per chat) |
| Intent, all customer messages | 220/278 (79.1%, 95% CI 0.740–0.835) | ? |
| Intent, last message | 77/90 (85.6%, 95% CI 0.768–0.914) | |
| Intent, earlier messages (mid-chat) | 143/188 (76.1%, 95% CI 0.695–0.816) | |
| Items (F1) | 128 found / 10 extra / 28 missed (F1 0.8707482993197279) | ? |
| Fully correct orders | 68/90 (95% CI (0.6575143545381369, 0.8326733660463373)) | ? |
| Same action (bot sends/asks the same; wording aside) | 68/90 (95% CI (0.6575143545381369, 0.8326733660463373)) | |

Field accuracy: {'method': 1.0, 'time': 1.0, 'address': 0.9836065573770492, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.8524590163934426}

Hit the token limit: 0; latency p50/p95 {'p50': 13520, 'p95': 21433} ms (T4, fp16, greedy); output tokens p50 327.5.
Invalid answers by reason: {'no output': 32, '2 validation errors for StudentOutput': 4, '1 validation error for StudentOutput': 2}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 163 | 139 | 144 |
| SMALL_TALK | 43 | 21 | 23 |
| MODIFY_ORDER | 18 | 16 | 16 |
| MENU_QUESTION | 14 | 11 | 11 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 7 | 5 | 17 |
| ORDER_PROBLEM | 5 | 3 | 4 |
| OUT_OF_SCOPE | 5 | 4 | 4 |
| DELIVERY_QUESTION | 4 | 3 | 3 |
| ORDER_STATUS | 4 | 4 | 4 |
| CANCEL_ORDER | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 1 |
| PAYMENT_CLAIM | 1 | 1 | 1 |
| PAYMENT_QUESTION | 1 | 1 | 1 |
| REFUND_REQUEST | 1 | 1 | 1 |

Mistakes (gold → predicted):

- PLACE_ORDER → None: 23
- SMALL_TALK → UNKNOWN: 12
- SMALL_TALK → None: 6
- SMALL_TALK → PLACE_ORDER: 4
- MENU_QUESTION → None: 2
- MODIFY_ORDER → None: 2
- ORDER_PROBLEM → None: 2
- MENU_QUESTION → SMALL_TALK: 1
- UNKNOWN → SMALL_TALK: 1
- DELIVERY_QUESTION → PLACE_ORDER: 1
- PLACE_ORDER → ORDER_PROBLEM: 1
- OUT_OF_SCOPE → None: 1
- UNKNOWN → None: 1
- CONFIRM_ORDER → None: 1
