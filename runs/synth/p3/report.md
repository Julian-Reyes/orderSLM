# Synthetic pilot `p3`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch p3"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 100 | 200 | 200 |
| chats kept | 100/100 (100%) | 198/200 (99%) | 200/200 (100%) |
| generation drops | 0 | invalid_output 2 | 0 |
| repairs | trimmed_trailing_business_message 8 | trimmed_trailing_business_message 47 | trimmed_trailing_business_message 9 |
| labels kept | 99/100 (99%) | 196/198 (99%) | 199/200 (100%) |
| label drops | check_failed 1 | check_failed 2 | check_failed 1 |
| card agrees with label | 93/99 (94%) | 186/196 (95%) | 175/199 (88%) |
| disagreement types | labels 5, items 1 | labels 8, items 3 | items 8, labels 16, item_details 1 |
| card address used | 13/16 (81%) | 42/43 (98%) | 37/37 (100%) |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0383 | $0.0254 | $0.1251 |
| generation: per 1,000 chats | $0.3832 | $0.1269 | $0.6255 |
| generation: tokens in (cached) / out | 259,206 (0) / 24,705 | 317,759 (268,928) / 28,589 | 314,589 (0) / 30,921 |
| generation: latency p50 ms | 2028 | 2025 | 1568 |
| labels (luna low): cost | $0.0698 | $0.1288 | $0.1280 |
| labels (luna low): per 1,000 chats | $0.6982 | $0.6506 | $0.6399 |
| labels (luna low): tokens in (cached) / out | 1,097,547 (767,300) / 58,142 | 2,140,065 (1,519,254) / 102,870 | 2,155,875 (1,534,600) / 100,806 |
| labels (luna low): latency p50 ms | 6422 | 5652 | 5445 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 4.37 | 3.72 | 3.02 |
| business messages per chat | 1.96 | 1.86 | 1.45 |
| words per customer message | 8.6 | 9.3 | 11.4 |
| share lowercase messages | 0.789 | 0.69 | 0.565 |
| share all caps messages | 0.062 | 0.058 | 0.083 |
| share messages with emoji | 0.142 | 0.113 | 0.127 |
| distinct openers | 0.39 | 0.374 | 0.25 |
| top openers | 'hey' 26; 'hey lemme' 12; 'hi i' 6 | 'yo u' 17; 'hey' 15; 'yo' 14 | 'hey there' 24; 'hey can' 20; 'hey' 17 |
| mean nearest similarity | 0.051 | 0.072 | 0.077 |
| max nearest similarity | 0.15 | 0.184 | 0.25 |
| distinct 3gram share | 0.859 | 0.784 | 0.749 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| ambiguous_reference | 4/4 | 7/8 | 7/7 |
| cancellation | 4/4 | 8/8 | 8/8 |
| combo | 4/4 | 10/10 | 8/10 |
| contextual_yes | 6/6 | 10/11 | 9/11 |
| correction | 7/8 | 16/16 | 18/18 |
| correction_after_confirmation | 2/5 | 8/10 | 2/9 |
| delivery_question | 2/2 | 4/4 | 4/4 |
| half_and_half | 3/3 | 7/7 | 8/8 |
| human_request | 2/2 | 4/4 | 4/4 |
| implicit_category | 5/5 | 10/10 | 9/9 |
| menu_question | 2/2 | 4/4 | 3/4 |
| missing_info | 5/6 | 11/11 | 12/12 |
| multi_message_order | 10/10 | 19/19 | 19/20 |
| off_menu | 3/4 | 6/7 | 6/8 |
| order_problem | 2/2 | 4/4 | 4/4 |
| out_of_scope | 2/2 | 4/4 | 4/4 |
| payment_claim | 2/2 | 3/4 | 1/4 |
| payment_question | 2/2 | 4/4 | 4/4 |
| refund_request | 2/2 | 4/4 | 2/4 |
| simple_order | 14/14 | 28/28 | 26/27 |
| small_talk | 2/2 | 4/4 | 4/4 |
| status_question | 2/2 | 4/4 | 4/4 |
| two_requests | 4/4 | 7/7 | 8/8 |
| unclear_message | 2/2 | 0/4 | 1/4 |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CANCEL_ORDER | 4 | 9 | 10 |
| CONFIRM_ORDER | 25 | 46 | 45 |
| DELIVERY_QUESTION | 15 | 55 | 19 |
| HUMAN_REQUEST | 3 | 7 | 7 |
| MENU_QUESTION | 19 | 32 | 24 |
| MODIFY_ORDER | 28 | 43 | 43 |
| ORDER_PROBLEM | 6 | 13 | 9 |
| ORDER_STATUS | 6 | 18 | 14 |
| OUT_OF_SCOPE | 3 | 6 | 6 |
| PAYMENT_CLAIM | 2 | 3 | 0 |
| PAYMENT_QUESTION | 4 | 4 | 4 |
| PLACE_ORDER | 218 | 356 | 290 |
| REFUND_REQUEST | 1 | 3 | 3 |
| SMALL_TALK | 96 | 132 | 124 |
| UNKNOWN | 3 | 1 | 2 |

Audit sample: `audit.md` (30 chats, seed 20261016).
