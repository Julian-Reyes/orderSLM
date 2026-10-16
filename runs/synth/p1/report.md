# Synthetic pilot `p1`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch p1"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cards | 100 | 200 | 200 |
| chats kept | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) |
| generation drops | 0 | 0 | 0 |
| repairs | 0 | trimmed_trailing_business_message 1 | 0 |
| labels kept | 5/5 (100%) | 4/4 (100%) | 5/5 (100%) |
| label drops | 0 | 0 | 0 |
| card agrees with label | 4/5 (80%) | 4/4 (100%) | 4/5 (80%) |
| disagreement types | labels 1 | 0 | items 1, labels 1 |
| card address used | – | – | – |

## Cost and tokens

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| generation: cost | $0.0016 | $0.0010 | $0.0034 |
| generation: per 1,000 chats | $0.324 | $0.202 | $0.688 |
| generation: tokens in (cached) / out | 10,301 (0) / 1,175 | 7,828 (3,456) / 570 | 9,051 (0) / 784 |
| generation: latency p50 ms | 1814 | 1919 | 1614 |
| labels (luna low): cost | $0.0031 | $0.0034 | $0.0038 |
| labels (luna low): per 1,000 chats | $0.6108 | $0.8438 | $0.7512 |
| labels (luna low): tokens in (cached) / out | 49,859 (36,780) / 2,752 | 44,475 (22,068) / 1,824 | 56,710 (36,780) / 2,786 |
| labels (luna low): latency p50 ms | 5821 | 5579 | 6041 |

## Style of the customer text

| | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| customer messages per chat | 4.4 | 3.0 | 2.6 |
| business messages per chat | 2.2 | 1.2 | 1.6 |
| words per customer message | 7.7 | 9.4 | 17.7 |
| share lowercase messages | 0.591 | 0.267 | 0.308 |
| share all caps messages | 0.0 | 0.6 | 0.0 |
| share messages with emoji | 0.0 | 0.0 | 0.0 |
| distinct openers | 0.8 | 0.8 | 1.0 |
| top openers | 'hey' 2; 'hi i' 1; 'hi hope' 1 | 'hey morning' 2; 'hey i' 1; 'yo u' 1 | 'hello i' 1; 'hi i' 1; 'good morning' 1 |
| mean nearest similarity | 0.026 | 0.0 | 0.025 |
| max nearest similarity | 0.065 | 0.0 | 0.033 |
| distinct 3gram share | 0.981 | 1.0 | 0.968 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| cancellation | 1/1 | 1/1 | 1/1 |
| correction | – | 1/1 | 1/1 |
| correction_after_confirmation | 0/1 | – | – |
| implicit_category | 1/1 | 1/1 | 1/1 |
| multi_message_order | – | – | 0/1 |
| simple_order | 1/1 | – | 1/1 |
| status_question | – | 1/1 | – |
| two_requests | 1/1 | – | – |

## Labeled intents (primary)

| intent | claude-haiku-5-5@off-low | deepseek-flash@none | gemini-3.1-flash-lite@minimal |
|---|---|---|---|
| CANCEL_ORDER | 1 | 1 | 1 |
| CONFIRM_ORDER | 1 | 0 | 0 |
| DELIVERY_QUESTION | 0 | 1 | 0 |
| MODIFY_ORDER | 3 | 1 | 1 |
| ORDER_STATUS | 0 | 2 | 0 |
| PAYMENT_QUESTION | 1 | 0 | 0 |
| PLACE_ORDER | 13 | 7 | 11 |
| SMALL_TALK | 3 | 2 | 0 |

Audit sample: `audit.md` (14 chats, seed 20261016).
