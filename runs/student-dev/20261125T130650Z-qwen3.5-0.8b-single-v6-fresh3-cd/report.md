# `qwen3.5-0.8b-single-v6` on fresh3 at every customer message

Prompt `student-extract@0.1`, data `student-data@0.6`, scorer `scorer@0.5`, finalize `finalize@0.4`. Fresh3 split: written after the v4 fixes that used dev, fresh and fresh2, never tuned on.

| | Student | Teacher (`teacher-label@0.7`, reference) |
|---|---|---|
| Valid answers, last customer message | 106/110 | ?/? |
| Valid answers, earlier messages | 210/211 | n/a (one call per chat) |
| Intent, all customer messages | 289/321 (90.0%, 95% CI 0.863–0.928) | ? |
| Intent, last message | 96/110 (87.3%, 95% CI 0.798–0.923) | |
| Intent, earlier messages (mid-chat) | 193/211 (91.5%, 95% CI 0.869–0.945) | |
| Items (F1) | 170 found / 5 extra / 16 missed (F1 0.9418282548476454) | ? |
| Fully correct orders | 93/110 (95% CI (0.7663799761205109, 0.9012142952179102)) | ? |
| Same action (bot sends/asks the same; wording aside) | 94/110 (95% CI (0.7767209782912426, 0.9084415633455579)) | |

Field accuracy: {'method': 0.9882352941176471, 'time': 0.9647058823529412, 'address': 0.9882352941176471, 'payment': 1.0, 'name': 1.0, 'decision': 1.0, 'missing': 0.9176470588235294}

Hit the token limit: 0; latency p50/p95 {'p50': 13550, 'p95': 18289} ms (T4, fp16, greedy); output tokens p50 324.
Invalid answers by reason: {'1 validation error for StudentOutput': 5}

| gold label | messages | primary correct | predicted as this |
|---|---|---|---|
| PLACE_ORDER | 201 | 192 | 199 |
| SMALL_TALK | 35 | 28 | 32 |
| MODIFY_ORDER | 21 | 19 | 23 |
| MENU_QUESTION | 18 | 18 | 22 |
| CONFIRM_ORDER | 9 | 8 | 8 |
| UNKNOWN | 9 | 4 | 9 |
| OUT_OF_SCOPE | 6 | 4 | 4 |
| DELIVERY_QUESTION | 5 | 2 | 2 |
| ORDER_PROBLEM | 5 | 3 | 3 |
| ORDER_STATUS | 5 | 5 | 7 |
| CANCEL_ORDER | 2 | 2 | 2 |
| REFUND_REQUEST | 2 | 2 | 2 |
| HUMAN_REQUEST | 1 | 1 | 2 |
| PAYMENT_CLAIM | 1 | 0 | 0 |
| PAYMENT_QUESTION | 1 | 1 | 1 |

Mistakes (gold → predicted):

- SMALL_TALK → UNKNOWN: 4
- UNKNOWN → SMALL_TALK: 3
- PLACE_ORDER → MODIFY_ORDER: 3
- PLACE_ORDER → None: 3
- SMALL_TALK → PLACE_ORDER: 3
- PLACE_ORDER → MENU_QUESTION: 3
- MODIFY_ORDER → None: 2
- DELIVERY_QUESTION → PLACE_ORDER: 2
- DELIVERY_QUESTION → ORDER_STATUS: 1
- UNKNOWN → MENU_QUESTION: 1
- CONFIRM_ORDER → SMALL_TALK: 1
- UNKNOWN → PLACE_ORDER: 1
- OUT_OF_SCOPE → UNKNOWN: 1
- ORDER_PROBLEM → ORDER_STATUS: 1
- ORDER_PROBLEM → MODIFY_ORDER: 1
- PAYMENT_CLAIM → PLACE_ORDER: 1
- OUT_OF_SCOPE → HUMAN_REQUEST: 1
