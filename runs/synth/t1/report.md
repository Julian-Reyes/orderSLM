# Synthetic pilot `t1`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t1"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 100 | 400 | 100 |
| chats kept | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) |
| generation drops | 0 | 0 | 0 |
| repairs | 0 | 0 | 0 |
| labels kept | 5/5 (100%) | 5/5 (100%) | 4/5 (80%) |
| label drops | 0 | 0 | check_failed 1 |
| card agrees with label | 4/5 (80%) | 3/5 (60%) | 4/4 (100%) |
| disagreement types | items 1 | items 1, labels 1 | 0 |
| card address used | 1/1 (100%) | 1/1 (100%) | 2/2 (100%) |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0019 | $0.0010 | $0.0035 |
| generation: per 1,000 chats | $0.3856 | $0.1904 | $0.6986 |
| generation: tokens in (cached) / out | 12,959 (0) / 1,260 | 6,698 (3,456) / 755 | 9,378 (0) / 764 |
| generation: latency p50 ms | 2292 | 2449 | 1747 |
| labels (luna low): cost | $0.0034 | $0.0040 | $0.0038 |
| labels (luna low): per 1,000 chats | $0.6878 | $0.799 | $0.7556 |
| labels (luna low): tokens in (cached) / out | 55,321 (39,175) / 2,862 | 50,691 (31,340) / 3,489 | 58,302 (39,175) / 2,940 |
| labels (luna low): latency p50 ms | 5740 | 6952 | 5768 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 3.6 | 3.8 | 2.8 |
| business messages per chat | 1.8 | 2.2 | 1.4 |
| words per customer message | 10.1 | 9.3 | 12.9 |
| share lowercase messages | 0.389 | 0.842 | 0.714 |
| share all caps messages | 0.444 | 0.0 | 0.286 |
| share messages with emoji | 0.0 | 0.421 | 0.0 |
| distinct openers | 0.8 | 1.0 | 0.8 |
| top openers | 'hey i' 2; 'hi can' 1; "hi it's" 1 | 'hey morning' 1; 'heyyy quick' 1; 'hey quick' 1 | 'hey its' 2; 'hey are' 1; 'hi i' 1 |
| mean nearest similarity | 0.005 | 0.009 | 0.015 |
| max nearest similarity | 0.013 | 0.016 | 0.023 |
| distinct 3gram share | 0.994 | 0.987 | 0.976 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| ambiguous_reference | 1/1 | 1/1 | 1/1 |
| correction | 1/1 | 0/1 | 1/1 |
| correction_after_confirmation | 0/1 | – | – |
| multi_message_order | – | 1/1 | – |
| simple_order | 1/1 | 1/1 | 1/1 |
| unclear_message | 1/1 | 0/1 | 1/1 |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CONFIRM_ORDER | 1 | 1 | 1 |
| DELIVERY_QUESTION | 1 | 1 | 1 |
| MODIFY_ORDER | 2 | 0 | 1 |
| PLACE_ORDER | 8 | 15 | 7 |
| SMALL_TALK | 4 | 1 | 1 |
| UNKNOWN | 2 | 1 | 1 |

Audit sample: `audit.md` (14 chats, seed 20261016).
