# Student bake-off, zero-shot (teacher-label@0.7, 20 dev chats, seed 20261019)

Dev numbers (model choice), not held out. Same request and scorer as the teacher's labels; fp32, greedy.

| model | JSON (raw) | JSON (fence stripped) | contract valid | item F1 | items found/extra/missed | exact orders | intents right | hit token limit | run errors | latency p50 |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b | 0/20 | 0/20 | 0/20 | 0.0 | 0/0/29 | 0/20 | 0/54 | 20 | 0 | 184.9 s |
| qwen3.5-2b | 19/20 | 19/20 | 3/20 | 0.0 | 0/0/29 | 3/20 | 5/54 | 1 | 0 | 59.0 s |
| qwen3-1.7b | 20/20 | 20/20 | 0/20 | 0.0 | 0/0/29 | 0/20 | 0/54 | 0 | 0 | 86.6 s |
| gemma-4-e2b-it | 11/20 | 11/20 | 0/20 | 0.0 | 0/0/29 | 0/20 | 0/54 | 0 | 0 | 923.4 s |
| teacher-gpt-6-luna@low | –/20 | –/20 | 20/20 | 1.0 | 29/0/0 | 20/20 | 54/54 | – | – | – |

Diagnostics (not contract scores): menu_item_ids anywhere in the parsed JSON vs the teacher's, ignoring structure; most frequent contract errors (field: type, per error).

| model | item ids right/extra/missed | F1 vs teacher | top contract errors |
|---|---|---|---|
| qwen3.5-0.8b | 0/0/27 | 0.0 | (not JSON) ×20 |
| qwen3.5-2b | 20/6/7 | 0.755 | order.items.combo_selections: list_type ×22; order.items.notes: string_type ×20; order.fulfillment: value_error ×3 |
| qwen3-1.7b | 14/19/13 | 0.467 | order.quantity: extra_forbidden ×20; order.variant_id: extra_forbidden ×20; order.unmatched_variant_text: extra_forbidden ×20 |
| gemma-4-e2b-it | 18/4/9 | 0.735 | order.items.modifications: list_type ×18; order.items.evidence: missing ×17; (not JSON) ×9 |

Run errors (out of memory, load failure) score as invalid; the message is in `<model>/outputs/`.
Per-model details: `<model>/report.md`. Raw outputs: `kernel/outputs.jsonl`.
