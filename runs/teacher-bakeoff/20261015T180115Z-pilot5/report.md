# Teacher bake-off: 20261015T180115Z-pilot5

pilot 5 conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.1`, schema `extraction@0.4`, commit `c6e5984ccb4f4fb535fcc98048a972e2a4924cd6`, cache `record`. Actual cost of this run: $0.0602 (estimate $0.2281).

**Pilot: 5 conversations is far too few to compare accuracy.** Use it for validity, tokens, cost and latency; accuracy differences here are noise.

| Variant | JSON valid | Item F1 | Exact | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@none` | 5/5 | 77.8% | 60.0% | 0 | 10378.8 | 403.8 | 0.0 | $0.76 | 7416 |
| `openai/gpt-6-luna@low` | 5/5 | 100.0% | 100.0% | 0 | 10378.8 | 476.6 | 73.2 | $0.80 | 4855 |
| `openai/gpt-6-luna@medium` | 5/5 | 100.0% | 100.0% | 0 | 10378.8 | 749.8 | 230.8 | $0.94 | 8340 |
| `anthropic/claude-haiku-5-5@off-low` | 0/5 | 0.0% | 0.0% | 0 | — | — | — | $0.00 | None |
| `anthropic/claude-haiku-5-5@off-medium` | 0/5 | 0.0% | 0.0% | 0 | — | — | — | $0.00 | None |
| `anthropic/claude-haiku-5-5@on-low` | 0/5 | 0.0% | 0.0% | 0 | — | — | — | $0.00 | None |
| `anthropic/claude-haiku-5-5@on-medium` | 0/5 | 0.0% | 0.0% | 0 | — | — | — | $0.00 | None |
| `google/gemini-3.1-flash-lite@minimal` | 5/5 | 77.8% | 60.0% | 0 | 8747.6 | 666.8 | 0.0 | $3.19 | 2793 |
| `google/gemini-3.1-flash-lite@default` | 5/5 | 77.8% | 60.0% | 0 | 8747.6 | 746.6 | 0.0 | $3.31 | 2972 |
| `deepseek/deepseek-flash@none` | 4/5 | 75.0% | 60.0% | 0 | 9001.2 | 509.8 | 0.0 | $0.81 | 2868 |
| `deepseek/deepseek-flash@low` | 5/5 | 100.0% | 100.0% | 0 | 9026.2 | 1065.0 | 646.2 | $1.14 | 6318 |
| `deepseek/deepseek-flash@high` | 4/5 | 75.0% | 60.0% | 0 | 9026.2 | 1009.4 | 595.6 | $1.10 | 5513 |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.

## Errors and invalid outputs

- `anthropic/claude-haiku-5-5@off-low`: anthropic/claude-haiku-5-5@off-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays o
- `anthropic/claude-haiku-5-5@off-low`: anthropic/claude-haiku-5-5@off-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays o
- `anthropic/claude-haiku-5-5@off-low`: anthropic/claude-haiku-5-5@off-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays o
- `anthropic/claude-haiku-5-5@off-low`: anthropic/claude-haiku-5-5@off-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays o
- `anthropic/claude-haiku-5-5@off-low`: anthropic/claude-haiku-5-5@off-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays o
- `anthropic/claude-haiku-5-5@off-medium`: anthropic/claude-haiku-5-5@off-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type array
- `anthropic/claude-haiku-5-5@off-medium`: anthropic/claude-haiku-5-5@off-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type array
- `anthropic/claude-haiku-5-5@off-medium`: anthropic/claude-haiku-5-5@off-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type array
- `anthropic/claude-haiku-5-5@off-medium`: anthropic/claude-haiku-5-5@off-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type array
- `anthropic/claude-haiku-5-5@off-medium`: anthropic/claude-haiku-5-5@off-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type array
- `anthropic/claude-haiku-5-5@on-low`: anthropic/claude-haiku-5-5@on-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays or
- `anthropic/claude-haiku-5-5@on-low`: anthropic/claude-haiku-5-5@on-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays or
- `anthropic/claude-haiku-5-5@on-low`: anthropic/claude-haiku-5-5@on-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays or
- `anthropic/claude-haiku-5-5@on-low`: anthropic/claude-haiku-5-5@on-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays or
- `anthropic/claude-haiku-5-5@on-low`: anthropic/claude-haiku-5-5@on-low: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays or
- `anthropic/claude-haiku-5-5@on-medium`: anthropic/claude-haiku-5-5@on-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays
- `anthropic/claude-haiku-5-5@on-medium`: anthropic/claude-haiku-5-5@on-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays
- `anthropic/claude-haiku-5-5@on-medium`: anthropic/claude-haiku-5-5@on-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays
- `anthropic/claude-haiku-5-5@on-medium`: anthropic/claude-haiku-5-5@on-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays
- `anthropic/claude-haiku-5-5@on-medium`: anthropic/claude-haiku-5-5@on-medium: HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Schemas contains too many parameters with union types (24 parameters with type arrays
- `deepseek/deepseek-flash@none`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
- `deepseek/deepseek-flash@high`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
