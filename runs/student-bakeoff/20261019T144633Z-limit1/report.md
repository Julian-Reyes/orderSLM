# Student bake-off, zero-shot (teacher-label@0.7, 1 dev chats, seed 20261019)

Dev numbers (model choice), not held out. Same request and scorer as the teacher's labels; fp32, greedy.

| model | JSON (raw) | JSON (fence stripped) | contract valid | item F1 | items found/extra/missed | exact orders | intents right | hit token limit | run errors | latency p50 |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b | 0/1 | 0/1 | 0/1 | None | 0/0/0 | 0/1 | 0/2 | 1 | 0 | 168.4 s |
| qwen3.5-2b | 1/1 | 1/1 | 0/1 | None | 0/0/0 | 0/1 | 0/2 | 0 | 0 | 21.8 s |
| qwen3-1.7b | 0/1 | 0/1 | 0/1 | None | 0/0/0 | 0/1 | 0/2 | 0 | 1 | – |
| gemma-4-e2b-it | 0/1 | 0/1 | 0/1 | None | 0/0/0 | 0/1 | 0/2 | 0 | 1 | – |
| teacher-gpt-6-luna@low | –/1 | –/1 | 1/1 | None | 0/0/0 | 1/1 | 2/2 | – | – | – |

Run errors (out of memory, load failure) score as invalid; the message is in `<model>/outputs/`.
Per-model details: `<model>/report.md`. Raw outputs: `kernel/outputs.jsonl`.
