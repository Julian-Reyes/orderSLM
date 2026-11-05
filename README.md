# OrderSLM

Turns informal, multi-message food-order chats into structured, menu-matched orders with a **fine-tuned 0.8B
model**, and measures every model choice along the way. Prices and totals are always computed in code, never by a
model.

**Case study with charts: [julianreyes.dev/orderslm](https://julianreyes.dev/orderslm/)**

## Results so far (November 2026)

| | |
|---|---|
| Picked student | Qwen3.5-0.8B + LoRA, trained on 2,528 teacher-labeled synthetic chats (free Kaggle T4s) |
| Fully correct orders | **69/90 fresh chats (77%)**, 69/91 dev; teacher (GPT-6 Luna, low) 90/91 dev |
| Customer-message intents | 256/278 fresh (92%) |
| Shipped format | GGUF Q8_0, 0.81 GB, same accuracy as fp16 on dev and fresh, 2.6 s per answer on a T4 (fp16 transformers: 13.5 s) |
| API spend, whole project | $6.63 (`docs/COSTS.md`) |

The four measured comparisons:

1. **Teacher bake-off**: 12 settings across OpenAI, Anthropic, Google and DeepSeek, to find which labels best per
   dollar (`docs/TEACHER_BAKEOFF.md`).
2. **Student bake-off**: which small open model is the best starting point (`docs/STUDENT_BAKEOFF.md`).
3. **Distillation**: LoRA students, error review and a data fix (fresh exact orders 54 → 69 of 90), and packaging
   with llama.cpp (`docs/STUDENT_ERRORS.md`, `docs/PACKAGING.md`).
4. **Decision providers**: an order checker so far (`docs/ORDER_CHECK.md`); the router benchmark is next.

Dev numbers guided tuning. Fresh chats were written after the dev-based fixes; a few of them also led to fixes, and
those gains are labeled "used for fixes". The 199-chat test split is sealed until the final evaluation. Every number
comes from saved outputs in `runs/`; `make site-data` regenerates the website's data file
(`docs/site/case-study.json`).

Status and next steps: [PROGRESS.md](PROGRESS.md). Plan: [orderslm-project-plan.md](orderslm-project-plan.md).

## Setup

```sh
uv sync                 # Python 3.12 venv
make test               # tests (no network)
make lint
git config core.hooksPath .githooks   # once per clone: tests + lint before each commit
```

## Layout

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Contracts: [docs/SCHEMA.md](docs/SCHEMA.md),
[docs/TAXONOMY.md](docs/TAXONOMY.md). Labeling rules: [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md).
Spend log: [docs/COSTS.md](docs/COSTS.md). Kaggle jobs: [docs/KAGGLE.md](docs/KAGGLE.md). Patterns ported from
AgentDesk: [docs/AGENTDESK_REUSE.md](docs/AGENTDESK_REUSE.md).
