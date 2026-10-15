# Teacher bake-off: 20261015T180115Z-pilot5 (finalize@0.1)

Scored with `scorer@0.2` after `finalize@0.1`: code computes the missing list, the clarification question and default variants from the model's facts. Raw model scores: `report.md`.

pilot 5 conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.1`, schema `extraction@0.4`, commit `c6e5984ccb4f4fb535fcc98048a972e2a4924cd6`, cache `record`. Actual cost of this run: $0.0602 (estimate $0.2281).

**Pilot: 5 conversations is far too few to compare accuracy.** Use it for validity, tokens, cost and latency; accuracy differences here are noise.

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@none` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 10378.8 | 403.8 | 0.0 | $0.0038 | $0.76 | 7416 |
| `openai/gpt-6-luna@low` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 10378.8 | 476.6 | 73.2 | $0.0040 | $0.80 | 4855 |
| `openai/gpt-6-luna@medium` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 10378.8 | 749.8 | 230.8 | $0.0047 | $0.94 | 8340 |
| `anthropic/claude-haiku-5-5@off-low` | 0/5 | 0 / 0 / 9 (of 9) | 0.0% | 0/5 (0.0%–43.4%) | 0 | — | — | — | $0.0000 | $0.00 | None |
| `anthropic/claude-haiku-5-5@off-medium` | 0/5 | 0 / 0 / 9 (of 9) | 0.0% | 0/5 (0.0%–43.4%) | 0 | — | — | — | $0.0000 | $0.00 | None |
| `anthropic/claude-haiku-5-5@on-low` | 0/5 | 0 / 0 / 9 (of 9) | 0.0% | 0/5 (0.0%–43.4%) | 0 | — | — | — | $0.0000 | $0.00 | None |
| `anthropic/claude-haiku-5-5@on-medium` | 0/5 | 0 / 0 / 9 (of 9) | 0.0% | 0/5 (0.0%–43.4%) | 0 | — | — | — | $0.0000 | $0.00 | None |
| `google/gemini-3.1-flash-lite@minimal` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 8747.6 | 666.8 | 0.0 | $0.0159 | $3.19 | 2793 |
| `google/gemini-3.1-flash-lite@default` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 8747.6 | 746.6 | 0.0 | $0.0165 | $3.31 | 2972 |
| `deepseek/deepseek-flash@none` | 4/5 | 7 / 0 / 2 (of 9) | 87.5% | 4/5 (37.6%–96.4%) | 0 | 9001.2 | 509.8 | 0.0 | $0.0040 | $0.81 | 2868 |
| `deepseek/deepseek-flash@low` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 9026.2 | 1065.0 | 646.2 | $0.0057 | $1.14 | 6318 |
| `deepseek/deepseek-flash@high` | 4/5 | 7 / 0 / 2 (of 9) | 87.5% | 4/5 (37.6%–96.4%) | 0 | 9026.2 | 1009.4 | 595.6 | $0.0055 | $1.10 | 5513 |
| **all variants** | | | | | | | | | **$0.0602** | | |

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
