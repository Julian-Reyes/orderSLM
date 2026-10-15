# Teacher bake-off: 20261015T185040Z-full-remaining

full 51 (remaining dev: not in the bake-off set) conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.2`, schema `extraction@0.4`, commit `63a79e8d85110d3399c0f3ff633ed89e4f7870ef`, cache `record`. Actual cost of this run: $0.1225 (estimate $0.2635).

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@low` | 51/51 | 79 / 2 / 0 (of 79) | 98.8% | 48/51 (84.1%–98.0%) | 1 | 9632.1 | 417.3 | 59.9 | $0.0292 | $0.57 | 4823 |
| `anthropic/claude-haiku-5-5@on-medium` | 49/51 | 79 / 2 / 0 (of 79) | 98.8% | 47/51 (81.5%–96.9%) | 1 | 12061.6 | 1246.2 | 677.3 | $0.0933 | $1.83 | 5671 |
| **all variants** | | | | | | | | | **$0.1225** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.

## Errors and invalid outputs

- `anthropic/claude-haiku-5-5@on-medium`: a-dev-076: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@on-medium`: a-dev-087: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
