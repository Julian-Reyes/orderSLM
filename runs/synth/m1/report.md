# Synthetic pilot `m1`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch m1"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 66 | 264 | 66 |
| chats kept | 66/66 (100%) | 262/264 (99%) | 66/66 (100%) |
| generation drops | 0 | invalid_output 2 | 0 |
| repairs | trimmed_trailing_business_message 8 | trimmed_trailing_business_message 58 | trimmed_trailing_business_message 3 |
| labels kept | 65/66 (98%) | 261/262 (100%) | 65/66 (98%) |
| label drops | check_failed 1 | check_failed 1 | invalid_contract 1 |
| card agrees with label | 60/65 (92%) | 245/261 (94%) | 62/65 (95%) |
| disagreement types | labels 3, items 2 | items 5, labels 9, item_details 4 | labels 2, items 1 |
| card address used | 16/19 (84%) | 59/60 (98%) | 16/16 (100%) |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0402 | $0.0330 | $0.0640 |
| generation: per 1,000 chats | $0.609 | $0.125 | $0.9693 |
| generation: tokens in (cached) / out | 326,416 (0) / 15,041 | 779,938 (724,864) / 37,373 | 192,562 (0) / 10,543 |
| generation: latency p50 ms | 1802 | 1904 | 1712 |
| labels (luna low): cost | $0.0782 | $0.3066 | $0.0772 |
| labels (luna low): per 1,000 chats | $1.1842 | $1.1702 | $1.1702 |
| labels (luna low): tokens in (cached) / out | 1,062,748 (507,558) / 35,052 | 4,215,741 (2,013,086) / 132,119 | 1,059,477 (506,838) / 33,730 |
| labels (luna low): latency p50 ms | 6173 | 5514 | 5719 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 3.79 | 3.63 | 3.09 |
| business messages per chat | 1.76 | 1.83 | 1.21 |
| words per customer message | 9.5 | 9.4 | 11.2 |
| share lowercase messages | 0.72 | 0.686 | 0.52 |
| share all caps messages | 0.108 | 0.062 | 0.064 |
| share messages with emoji | 0.152 | 0.144 | 0.074 |
| distinct openers | 0.455 | 0.282 | 0.409 |
| top openers | 'hey lemme' 10; 'hey' 10; 'hey can' 8 | 'yo' 23; 'hey can' 21; 'yo u' 17 | 'hey there' 7; 'hello i' 7; 'hey can' 6 |
| mean nearest similarity | 0.055 | 0.09 | 0.053 |
| max nearest similarity | 0.2 | 0.476 | 0.172 |
| distinct 3gram share | 0.887 | 0.762 | 0.873 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| ambiguous_reference | 0/1 | 9/9 | 2/2 |
| cancellation | 2/2 | 9/9 | 2/2 |
| combo | 3/3 | 10/10 | 3/3 |
| contextual_yes | 2/3 | 12/12 | 4/4 |
| correction | 5/5 | 17/19 | 4/4 |
| correction_after_confirmation | 1/2 | 5/11 | 1/3 |
| delivery_question | 2/2 | 9/9 | 2/2 |
| half_and_half | 2/2 | 9/9 | 2/2 |
| human_request | 2/2 | 9/9 | 2/2 |
| implicit_category | 3/3 | 11/11 | 2/2 |
| menu_question | 2/2 | 8/8 | 1/1 |
| missing_info | 4/4 | 12/12 | 3/3 |
| multi_message_order | 5/5 | 21/21 | 6/6 |
| off_menu | 1/2 | 7/8 | 2/2 |
| order_problem | 3/3 | 8/8 | 2/2 |
| out_of_scope | 2/2 | 8/8 | 2/2 |
| payment_claim | 2/2 | 9/9 | 2/2 |
| payment_question | 2/2 | 9/9 | 2/2 |
| refund_request | 2/2 | 7/8 | 3/3 |
| simple_order | 8/8 | 25/28 | 7/7 |
| small_talk | 2/2 | 9/9 | 1/2 |
| status_question | 2/2 | 9/9 | 2/2 |
| two_requests | 2/2 | 8/8 | 3/3 |
| unclear_message | 1/2 | 5/8 | 2/2 |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CANCEL_ORDER | 2 | 9 | 2 |
| CONFIRM_ORDER | 16 | 66 | 20 |
| DELIVERY_QUESTION | 14 | 66 | 11 |
| HUMAN_REQUEST | 4 | 18 | 2 |
| MENU_QUESTION | 9 | 55 | 6 |
| MODIFY_ORDER | 17 | 47 | 15 |
| ORDER_PROBLEM | 10 | 28 | 4 |
| ORDER_STATUS | 6 | 21 | 5 |
| OUT_OF_SCOPE | 2 | 10 | 2 |
| PAYMENT_CLAIM | 1 | 15 | 1 |
| PAYMENT_QUESTION | 2 | 15 | 2 |
| PLACE_ORDER | 123 | 396 | 90 |
| REFUND_REQUEST | 2 | 10 | 3 |
| SMALL_TALK | 37 | 186 | 34 |
| UNKNOWN | 1 | 6 | 4 |

Audit sample: `audit.md` (30 chats, seed 20261016).
