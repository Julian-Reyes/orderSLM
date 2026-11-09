# Synthetic pilot `t5`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t5"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-opus-5-5 |
|---|---|
| cards | 300 |
| chats kept | 12/12 (100%) |
| generation drops | 0 |
| repairs | 0 |
| labels kept | – |
| label drops | 0 |
| card agrees with label | 10/12 (83%) |
| disagreement types | items 1, item_details 1 |
| card address used | 2/3 (67%) |

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
| customer messages per chat | 3.25 |
| business messages per chat | 0.33 |
| words per customer message | 7.0 |
| share lowercase messages | 0.564 |
| share all caps messages | 0.205 |
| share messages with emoji | 0.026 |
| distinct openers | 0.833 |
| top openers | 'can i' 2; 'hi can' 2; 'hey' 1 |
| mean nearest similarity | 0.043 |
| max nearest similarity | 0.081 |
| distinct 3gram share | 0.948 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-opus-5-5 |
|---|---|
| correction | 1/1 |
| correction_after_confirmation | 3/3 |
| missing_info | 1/2 |
| multi_message_order | 1/1 |
| simple_order | 4/5 |

## Labeled intents (primary)

| intent | claude-opus-5-5 |
|---|---|
| CONFIRM_ORDER | 3 |
| MENU_QUESTION | 1 |
| MODIFY_ORDER | 4 |
| PLACE_ORDER | 25 |
| SMALL_TALK | 6 |

Audit sample: `audit.md` (10 chats, seed 20261016).
