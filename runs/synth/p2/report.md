# Synthetic pilot `p2`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch p2"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 100 | 200 | 200 |
| chats kept | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) |
| generation drops | 0 | 0 | 0 |
| repairs | trimmed_trailing_business_message 1 | trimmed_trailing_business_message 2 | 0 |
| labels kept | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) |
| label drops | 0 | 0 | 0 |
| card agrees with label | 3/5 (60%) | 5/5 (100%) | 2/5 (40%) |
| disagreement types | labels 1, item_details 1 | 0 | labels 2, item_details 1 |
| card address used | – | 1/1 (100%) | – |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0017 | $0.0010 | $0.0027 |
| generation: per 1,000 chats | $0.335 | $0.207 | $0.543 |
| generation: tokens in (cached) / out | 9,883 (0) / 1,367 | 9,011 (4,864) / 659 | 6,391 (0) / 743 |
| generation: latency p50 ms | 1979 | 1792 | 1484 |
| labels (luna low): cost | $0.0032 | $0.0032 | $0.0037 |
| labels (luna low): per 1,000 chats | $0.642 | $0.6384 | $0.7306 |
| labels (luna low): tokens in (cached) / out | 48,496 (36,885) / 3,356 | 56,044 (36,885) / 1,812 | 48,190 (29,508) / 2,976 |
| labels (luna low): latency p50 ms | 6786 | 3713 | 6099 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 3.6 | 3.4 | 2.6 |
| business messages per chat | 2.4 | 1.8 | 1.6 |
| words per customer message | 12.5 | 9.8 | 14.2 |
| share lowercase messages | 0.722 | 0.882 | 0.385 |
| share all caps messages | 0.0 | 0.0 | 0.385 |
| share messages with emoji | 0.222 | 0.294 | 0.154 |
| distinct openers | 0.8 | 0.8 | 0.8 |
| top openers | 'hey lemme' 2; 'hi there' 1; 'hey do' 1 | 'hey my' 2; 'yo my' 1; 'hey do' 1 | 'hey morning' 2; 'hi i' 1; 'hey quick' 1 |
| mean nearest similarity | 0.005 | 0.005 | 0.022 |
| max nearest similarity | 0.013 | 0.012 | 0.042 |
| distinct 3gram share | 0.995 | 0.993 | 0.971 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| contextual_yes | 1/1 | 1/1 | 1/1 |
| correction_after_confirmation | 0/1 | – | – |
| human_request | – | 1/1 | – |
| implicit_category | 0/1 | – | – |
| menu_question | – | 1/1 | – |
| missing_info | – | – | 1/1 |
| multi_message_order | – | – | 0/1 |
| off_menu | – | – | 0/1 |
| order_problem | – | 1/1 | – |
| simple_order | 1/1 | 1/1 | – |
| two_requests | 1/1 | – | 0/1 |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CONFIRM_ORDER | 2 | 1 | 2 |
| DELIVERY_QUESTION | 1 | 0 | 0 |
| HUMAN_REQUEST | 0 | 2 | 0 |
| MENU_QUESTION | 1 | 3 | 1 |
| MODIFY_ORDER | 2 | 0 | 1 |
| ORDER_PROBLEM | 0 | 1 | 0 |
| ORDER_STATUS | 0 | 3 | 0 |
| PLACE_ORDER | 11 | 4 | 8 |
| SMALL_TALK | 0 | 3 | 1 |
| UNKNOWN | 1 | 0 | 0 |

Audit sample: `audit.md` (15 chats, seed 20261016).
