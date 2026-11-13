# Synthetic pilot `t7`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t7"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-opus-5-5 |
|---|---|
| cards | 240 |
| chats kept | 240/240 (100%) |
| generation drops | 0 |
| repairs | 0 |
| labels kept | – |
| label drops | 0 |
| card agrees with label | 182/240 (76%) |
| disagreement types | items 53, item_details 4, labels 1 |
| card address used | 57/57 (100%) |

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
| customer messages per chat | 3.18 |
| business messages per chat | 0.33 |
| words per customer message | 6.0 |
| share lowercase messages | 0.795 |
| share all caps messages | 0.079 |
| share messages with emoji | 0.115 |
| distinct openers | 0.554 |
| top openers | 'hey' 18; 'hi' 17; 'hi can' 6 |
| mean nearest similarity | 0.072 |
| max nearest similarity | 0.4 |
| distinct 3gram share | 0.817 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-opus-5-5 |
|---|---|
| ambiguous_reference | 8/8 |
| correction | 23/24 |
| correction_after_confirmation | 19/21 |
| implicit_category | 5/10 |
| missing_info | 20/51 |
| multi_message_order | 55/62 |
| simple_order | 38/45 |
| two_requests | 4/9 |
| unclear_message | 10/10 |

## Labeled intents (primary)

| intent | claude-opus-5-5 |
|---|---|
| CONFIRM_ORDER | 21 |
| MENU_QUESTION | 30 |
| MODIFY_ORDER | 45 |
| PLACE_ORDER | 581 |
| SMALL_TALK | 72 |
| UNKNOWN | 15 |

Audit sample: `audit.md` (10 chats, seed 20261016).
