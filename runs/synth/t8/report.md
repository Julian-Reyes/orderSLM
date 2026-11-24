# Synthetic pilot `t8`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t8"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-opus-5-5 |
|---|---|
| cards | 240 |
| chats kept | 240/240 (100%) |
| generation drops | 0 |
| repairs | trimmed_trailing_business_message 1 |
| labels kept | – |
| label drops | 0 |
| card agrees with label | 182/240 (76%) |
| disagreement types | items 45, item_details 9, labels 5 |
| card address used | 51/51 (100%) |

## Cost and tokens

| | claude-opus-5-5 |
|---|---|
| generation: cost | $0.0000 |
| generation: per 1,000 chats | $0.0 |
| generation: tokens in (cached) / out | 0 (0) / 0 |
| generation: latency p50 ms | 0 |
| labels (luna low): cost | $0.0000 |
| labels (luna low): per 1,000 chats | $None |
| labels (luna low): tokens in (cached) / out | 0 (0) / 0 |
| labels (luna low): latency p50 ms | None |

## Style of the customer text

| | claude-opus-5-5 |
|---|---|
| customer messages per chat | 3.28 |
| business messages per chat | 0.33 |
| words per customer message | 6.0 |
| share lowercase messages | 0.745 |
| share all caps messages | 0.084 |
| share messages with emoji | 0.114 |
| distinct openers | 0.558 |
| top openers | 'hey' 19; 'hi' 15; 'hello' 13 |
| mean nearest similarity | 0.068 |
| max nearest similarity | 0.286 |
| distinct 3gram share | 0.822 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-opus-5-5 |
|---|---|
| ambiguous_reference | 15/15 |
| combo | 14/15 |
| contextual_yes | 4/4 |
| correction | 14/14 |
| correction_after_confirmation | 13/16 |
| missing_info | 38/80 |
| multi_message_order | 33/35 |
| off_menu | 12/15 |
| simple_order | 26/32 |
| small_talk | 2/2 |
| two_requests | 2/3 |
| unclear_message | 9/9 |

## Labeled intents (primary)

| intent | claude-opus-5-5 |
|---|---|
| CONFIRM_ORDER | 16 |
| DELIVERY_QUESTION | 5 |
| HUMAN_REQUEST | 4 |
| MENU_QUESTION | 30 |
| MODIFY_ORDER | 31 |
| PLACE_ORDER | 593 |
| SMALL_TALK | 89 |
| UNKNOWN | 19 |

Audit sample: `audit.md` (10 chats, seed 20261016).
