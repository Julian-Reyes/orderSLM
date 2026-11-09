# Synthetic pilot `t5`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t5"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-opus-5-5 |
|---|---|
| cards | 300 |
| chats kept | 300/300 (100%) |
| generation drops | 0 |
| repairs | 0 |
| labels kept | – |
| label drops | 0 |
| card agrees with label | 184/300 (61%) |
| disagreement types | items 101, item_details 9, labels 6 |
| card address used | 56/66 (85%) |

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
| customer messages per chat | 3.16 |
| business messages per chat | 0.21 |
| words per customer message | 5.6 |
| share lowercase messages | 0.717 |
| share all caps messages | 0.094 |
| share messages with emoji | 0.102 |
| distinct openers | 0.463 |
| top openers | 'hey' 39; 'hi' 11; "hi i'd" 10 |
| mean nearest similarity | 0.103 |
| max nearest similarity | 0.462 |
| distinct 3gram share | 0.738 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-opus-5-5 |
|---|---|
| correction | 32/34 |
| correction_after_confirmation | 26/26 |
| missing_info | 30/110 |
| multi_message_order | 27/37 |
| simple_order | 69/93 |

## Labeled intents (primary)

| intent | claude-opus-5-5 |
|---|---|
| CONFIRM_ORDER | 26 |
| DELIVERY_QUESTION | 2 |
| MENU_QUESTION | 34 |
| MODIFY_ORDER | 60 |
| PLACE_ORDER | 702 |
| SMALL_TALK | 125 |

Audit sample: `audit.md` (10 chats, seed 20261016).
