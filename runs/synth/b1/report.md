# Synthetic pilot `b1`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch b1"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 250 | 1000 | 250 |
| chats kept | 250/250 (100%) | 983/1000 (98%) | 248/250 (99%) |
| generation drops | 0 | invalid_output 14, business_states_price 2, near_duplicate_of 1 | business_states_price 1, invalid_output 1 |
| repairs | trimmed_trailing_business_message 41 | trimmed_trailing_business_message 227 | trimmed_trailing_business_message 9 |
| labels kept | 249/250 (100%) | 974/983 (99%) | 248/248 (100%) |
| label drops | check_failed 1 | check_failed 5, invalid_contract 4 | 0 |
| card agrees with label | 227/249 (91%) | 926/974 (95%) | 228/248 (92%) |
| disagreement types | labels 13, items 8, item_details 4 | items 17, item_details 6, labels 34, decision 1 | items 8, labels 13, item_details 1 |
| card address used | 36/47 (77%) | 159/163 (98%) | 43/43 (100%) |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0893 | $0.1214 | $0.1610 |
| generation: per 1,000 chats | $0.357 | $0.1214 | $0.6438 |
| generation: tokens in (cached) / out | 617,210 (0) / 54,854 | 1,561,526 (1,325,824) / 135,992 | 394,259 (0) / 41,533 |
| generation: latency p50 ms | 1864 | 1882 | 1664 |
| labels (luna low): cost | $0.1613 | $0.6265 | $0.1572 |
| labels (luna low): per 1,000 chats | $0.6453 | $0.6373 | $0.6337 |
| labels (luna low): tokens in (cached) / out | 2,702,220 (1,920,830) / 127,701 | 10,583,599 (7,550,959) / 494,477 | 2,683,562 (1,903,804) / 120,007 |
| labels (luna low): latency p50 ms | 5526 | 5540 | 5320 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 3.56 | 3.62 | 2.98 |
| business messages per chat | 1.73 | 1.72 | 1.38 |
| words per customer message | 9.9 | 9.0 | 11.4 |
| share lowercase messages | 0.729 | 0.71 | 0.646 |
| share all caps messages | 0.061 | 0.066 | 0.086 |
| share messages with emoji | 0.183 | 0.147 | 0.103 |
| distinct openers | 0.296 | 0.167 | 0.222 |
| top openers | 'hey' 38; 'hey lemme' 30; 'hey can' 17 | 'hey' 85; 'yo' 74; 'hey can' 66 | 'hey u' 30; 'hey there' 23; 'hey' 20 |
| mean nearest similarity | 0.076 | 0.117 | 0.085 |
| max nearest similarity | 0.209 | 0.636 | 0.286 |
| distinct 3gram share | 0.774 | 0.613 | 0.741 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| ambiguous_reference | 8/8 | 30/31 | 9/9 |
| cancellation | 8/8 | 29/30 | 8/8 |
| combo | 9/10 | 41/41 | 10/10 |
| contextual_yes | 11/12 | 47/48 | 12/12 |
| correction | 17/18 | 67/68 | 18/19 |
| correction_after_confirmation | 5/10 | 21/37 | 5/10 |
| delivery_question | 8/8 | 30/30 | 7/7 |
| half_and_half | 6/8 | 33/33 | 8/8 |
| human_request | 8/8 | 32/32 | 8/8 |
| implicit_category | 7/10 | 37/41 | 10/10 |
| menu_question | 8/8 | 32/32 | 8/8 |
| missing_info | 12/12 | 49/49 | 12/12 |
| multi_message_order | 20/21 | 75/75 | 20/20 |
| off_menu | 8/9 | 29/31 | 7/8 |
| order_problem | 8/8 | 32/32 | 8/8 |
| out_of_scope | 8/8 | 32/32 | 8/8 |
| payment_claim | 8/8 | 30/31 | 7/8 |
| payment_question | 8/8 | 32/32 | 8/8 |
| refund_request | 8/8 | 32/32 | 5/8 |
| simple_order | 25/27 | 110/111 | 26/28 |
| small_talk | 8/8 | 31/32 | 6/8 |
| status_question | 8/8 | 31/31 | 8/8 |
| two_requests | 7/8 | 28/32 | 8/8 |
| unclear_message | 4/8 | 16/31 | 2/7 |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CANCEL_ORDER | 8 | 30 | 10 |
| CONFIRM_ORDER | 50 | 188 | 62 |
| DELIVERY_QUESTION | 52 | 242 | 29 |
| HUMAN_REQUEST | 14 | 54 | 11 |
| MENU_QUESTION | 42 | 162 | 28 |
| MODIFY_ORDER | 48 | 139 | 41 |
| ORDER_PROBLEM | 29 | 126 | 21 |
| ORDER_STATUS | 15 | 104 | 16 |
| OUT_OF_SCOPE | 8 | 44 | 8 |
| PAYMENT_CLAIM | 11 | 41 | 9 |
| PAYMENT_QUESTION | 14 | 59 | 14 |
| PLACE_ORDER | 423 | 1594 | 339 |
| REFUND_REQUEST | 8 | 35 | 6 |
| SMALL_TALK | 156 | 689 | 139 |
| UNKNOWN | 7 | 22 | 7 |

Audit sample: `audit.md` (30 chats, seed 20261016).
