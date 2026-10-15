# Teacher bake-off: 20261015T190341Z-full-all (finalize@0.1)

Scored with `scorer@0.2` after `finalize@0.1`: code computes the missing list, the clarification question and default variants from the model's facts. Raw model scores: `report.md`.

full 91 (all dev) conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.3`, schema `extraction@0.4`, commit `7b094c0c10d4cdd0aae79c1f6305cf47705ec3c3`, cache `record`. Actual cost of this run: $0.0544 (estimate $0.1794).

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@low` | 88/91 | 138 / 0 / 8 (of 146) | 97.2% | 87/91 (89.2%–98.3%) | 0 | 9818.5 | 434.2 | 81.9 | $0.0544 | $0.60 | 5410 |
| **all variants** | | | | | | | | | **$0.0544** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.

## Errors and invalid outputs

- `openai/gpt-6-luna@low`: a-dev-023: 1 validation error for CustomerDecision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pendi
- `openai/gpt-6-luna@low`: a-dev-059: 1 validation error for CustomerDecision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pendi
- `openai/gpt-6-luna@low`: a-dev-064: 1 validation error for CustomerDecision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_value={'state': 'pendi
