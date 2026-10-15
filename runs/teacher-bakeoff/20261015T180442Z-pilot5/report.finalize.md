# Teacher bake-off: 20261015T180442Z-pilot5 (finalize@0.1)

Scored with `scorer@0.2` after `finalize@0.1`: code computes the missing list, the clarification question and default variants from the model's facts. Raw model scores: `report.md`.

pilot 5 conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.1`, schema `extraction@0.4`, commit `a4310b1a2a557e31d92a95e26760f5ea08efd4f4`, cache `record`. Actual cost of this run: $0.0366 (estimate $0.2281).

**Pilot: 5 conversations is far too few to compare accuracy.** Use it for validity, tokens, cost and latency; accuracy differences here are noise.

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@none` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 10378.8 | 403.8 | 0.0 | $0.0038 | $0.76 | 7416 |
| `openai/gpt-6-luna@low` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 10378.8 | 476.6 | 73.2 | $0.0040 | $0.80 | 4855 |
| `openai/gpt-6-luna@medium` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 10378.8 | 749.8 | 230.8 | $0.0047 | $0.94 | 8340 |
| `anthropic/claude-haiku-5-5@off-low` | 3/5 | 6 / 1 / 3 (of 9) | 75.0% | 2/5 (11.8%–76.9%) | 0 | 13270.2 | 672.2 | 0.0 | $0.0083 | $1.66 | 3068 |
| `anthropic/claude-haiku-5-5@off-medium` | 3/5 | 6 / 1 / 3 (of 9) | 75.0% | 2/5 (11.8%–76.9%) | 0 | 13270.2 | 698.0 | 0.0 | $0.0084 | $1.68 | 2847 |
| `anthropic/claude-haiku-5-5@on-low` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 13271.2 | 1228.2 | 559.8 | $0.0097 | $1.94 | 5420 |
| `anthropic/claude-haiku-5-5@on-medium` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 13271.2 | 1427.6 | 755.6 | $0.0102 | $2.04 | 5821 |
| `google/gemini-3.1-flash-lite@minimal` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 8747.6 | 666.8 | 0.0 | $0.0159 | $3.19 | 2793 |
| `google/gemini-3.1-flash-lite@default` | 5/5 | 8 / 1 / 1 (of 9) | 88.9% | 4/5 (37.6%–96.4%) | 0 | 8747.6 | 746.6 | 0.0 | $0.0165 | $3.31 | 2972 |
| `deepseek/deepseek-flash@none` | 4/5 | 7 / 0 / 2 (of 9) | 87.5% | 4/5 (37.6%–96.4%) | 0 | 9001.2 | 509.8 | 0.0 | $0.0040 | $0.81 | 2868 |
| `deepseek/deepseek-flash@low` | 5/5 | 9 / 0 / 0 (of 9) | 100.0% | 5/5 (56.6%–100.0%) | 0 | 9026.2 | 1065.0 | 646.2 | $0.0057 | $1.14 | 6318 |
| `deepseek/deepseek-flash@high` | 4/5 | 7 / 0 / 2 (of 9) | 87.5% | 4/5 (37.6%–96.4%) | 0 | 9026.2 | 1009.4 | 595.6 | $0.0055 | $1.10 | 5513 |
| **all variants** | | | | | | | | | **$0.0968** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.

## Errors and invalid outputs

- `anthropic/claude-haiku-5-5@off-low`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
- `anthropic/claude-haiku-5-5@off-low`: a-dev-081: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-081: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `deepseek/deepseek-flash@none`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
- `deepseek/deepseek-flash@high`: a-dev-017: 1 validation error for ExtractionOutput
items.0
  Value error, L1: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4) [type=value_error, input_value={'line_id': 'L1', 'menu_i...
