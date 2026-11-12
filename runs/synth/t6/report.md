# Synthetic pilot `t6`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t6"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-opus-5-5 |
|---|---|
| cards | 240 |
| chats kept | 240/240 (100%) |
| generation drops | 0 |
| repairs | 0 |
| labels kept | – |
| label drops | 0 |
| card agrees with label | 204/240 (85%) |
| disagreement types | items 29, labels 7 |
| card address used | 53/53 (100%) |

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
| customer messages per chat | 3.33 |
| business messages per chat | 0.27 |
| words per customer message | 6.4 |
| share lowercase messages | 0.745 |
| share all caps messages | 0.091 |
| share messages with emoji | 0.143 |
| distinct openers | 0.429 |
| top openers | 'hey' 25; 'hey can' 18; 'hi' 16 |
| mean nearest similarity | 0.079 |
| max nearest similarity | 0.208 |
| distinct 3gram share | 0.763 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-opus-5-5 |
|---|---|
| ambiguous_reference | 8/8 |
| combo | 6/10 |
| correction | 15/16 |
| correction_after_confirmation | 4/9 |
| implicit_category | 10/10 |
| missing_info | 45/71 |
| multi_message_order | 57/57 |
| simple_order | 59/59 |

## Labeled intents (primary)

| intent | claude-opus-5-5 |
|---|---|
| CONFIRM_ORDER | 4 |
| DELIVERY_QUESTION | 9 |
| MENU_QUESTION | 36 |
| MODIFY_ORDER | 40 |
| PLACE_ORDER | 615 |
| SMALL_TALK | 95 |

Audit sample: `audit.md` (10 chats, seed 20261016).
