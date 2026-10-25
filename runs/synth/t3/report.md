# Synthetic pilot `t3`: per-generator report

Built from the saved files in this folder (`make synth ARGS="report --batch t3"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.

## Yield

| | deepseek-flash@none |
|---|---|
| cards | 600 |
| chats kept | 578/600 (96%) |
| generation drops | invalid_output 21, near_duplicate_of 1 |
| repairs | removed_schema_type_key 8, trimmed_trailing_business_message 100 |
| labels kept | 568/578 (98%) |
| label drops | invalid_contract 4, check_failed 5, finalize 1 |
| card agrees with label | 497/568 (88%) |
| disagreement types | items 35, labels 40, item_details 10 |
| card address used | 129/130 (99%) |

## Cost and tokens

| | deepseek-flash@none |
|---|---|
| generation: cost | $0.0895 |
| generation: per 1,000 chats | $0.1491 |
| generation: tokens in (cached) / out | 986,122 (821,888) / 103,444 |
| generation: latency p50 ms | 1989 |
| labels (luna low): cost | $0.4319 |
| labels (luna low): per 1,000 chats | $0.7473 |
| labels (luna low): tokens in (cached) / out | 6,383,637 (4,528,630) / 401,737 |
| labels (luna low): latency p50 ms | 6268 |

## Style of the customer text

| | deepseek-flash@none |
|---|---|
| customer messages per chat | 4.28 |
| business messages per chat | 2.26 |
| words per customer message | 9.9 |
| share lowercase messages | 0.699 |
| share all caps messages | 0.076 |
| share messages with emoji | 0.15 |
| distinct openers | 0.235 |
| top openers | 'yo u' 49; 'hey can' 35; 'hey quick' 30 |
| mean nearest similarity | 0.079 |
| max nearest similarity | 0.263 |
| distinct 3gram share | 0.642 |

Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the same generator (lower = more varied; dedup drops ≥ 0.8).

## Card agreement by scenario (agree / labeled)

| scenario | deepseek-flash@none |
|---|---|
| ambiguous_reference | 38/41 |
| correction | 67/75 |
| correction_after_confirmation | 62/78 |
| missing_info | 60/60 |
| multi_message_order | 127/133 |
| out_of_scope | 39/39 |
| simple_order | 77/83 |
| unclear_message | 27/59 |

## Labeled intents (primary)

| intent | deepseek-flash@none |
|---|---|
| CONFIRM_ORDER | 201 |
| DELIVERY_QUESTION | 113 |
| MENU_QUESTION | 80 |
| MODIFY_ORDER | 172 |
| OUT_OF_SCOPE | 63 |
| PAYMENT_QUESTION | 4 |
| PLACE_ORDER | 1332 |
| SMALL_TALK | 413 |
| UNKNOWN | 42 |

Audit sample: `audit.md` (10 chats, seed 20261016).
