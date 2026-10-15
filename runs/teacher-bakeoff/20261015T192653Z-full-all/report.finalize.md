# Teacher bake-off: 20261015T192653Z-full-all (finalize@0.1)

Scored with `scorer@0.2` after `finalize@0.1`: code computes the missing list, the clarification question and default variants from the model's facts. Raw model scores: `report.md`.

full 91 (all dev) conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.4`, schema `extraction@0.4`, commit `ba8e6a104f83aca2d4510a53cb3429019034b6e7`, cache `off`. Actual cost of this run: $0.0547 (estimate $0.1799).

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@low` | 91/91 | 146 / 0 / 0 (of 146) | 100.0% | 90/91 (94.0%–99.8%) | 0 | 9868.5 | 439.5 | 77.7 | $0.0547 | $0.60 | 4887 |
| **all variants** | | | | | | | | | **$0.0547** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.
