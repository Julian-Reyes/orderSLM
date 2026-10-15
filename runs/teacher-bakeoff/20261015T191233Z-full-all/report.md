# Teacher bake-off: 20261015T191233Z-full-all

Scored with `scorer@0.2`. Raw model output (no code post-processing); see `report.finalize.md` for the finalized view.

full 91 (all dev) conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.4`, schema `extraction@0.4`, commit `2cf921d4002cb3f043e1b423daa682e776972471`, cache `record`. Actual cost of this run: $0.0547 (estimate $0.1799).

| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@low` | 91/91 | 146 / 0 / 0 (of 146) | 100.0% | 86/91 (87.8%–97.6%) | 0 | 9868.5 | 439.0 | 80.0 | $0.0547 | $0.60 | 5003 |
| **all variants** | | | | | | | | | **$0.0547** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.
