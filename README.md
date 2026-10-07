# OrderSLM

Turns informal, multi-message food-order chats into structured, menu-matched orders, and measures every
model choice along the way:

1. **Teacher bake-off**: which cheap frontier model labels training data best per dollar.
2. **Student bake-off**: which small open model is the best starting point.
3. **Distillation**: how close a LoRA-trained small model gets to the teacher, and what it saves.
4. **Router benchmark**: Julia-1 vs. Jev vs. OpenAI Decisions (plus a rules baseline) as message routers.

English first; the schema is language-neutral so Brazilian Portuguese can follow. Prices and totals are
always computed in code, never by a model.

**Status:** Milestone 0 (contracts, docs, mocks). No model has been called yet, so there are no results.
See [PROGRESS.md](PROGRESS.md) and the plan in [orderslm-project-plan.md](orderslm-project-plan.md).

## Setup

```sh
uv sync                 # Python 3.12 venv with pydantic, pytest, ruff
make test               # schema and contract tests
make lint
git config core.hooksPath .githooks   # once per clone: tests + lint before each commit
```

## Layout

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Contracts: [docs/SCHEMA.md](docs/SCHEMA.md),
[docs/TAXONOMY.md](docs/TAXONOMY.md). Labeling rules: [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md).
Spend log: [docs/COSTS.md](docs/COSTS.md). Patterns ported from AgentDesk: [docs/AGENTDESK_REUSE.md](docs/AGENTDESK_REUSE.md).
