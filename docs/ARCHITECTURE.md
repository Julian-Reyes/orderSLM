# Architecture

All backend, data, labeling, training, evaluation and inference code is **Python 3.12** (Pydantic v2,
managed with `uv`). The only non-Python code is the lightweight web frontend (M8).

## Flow (one customer message)

```
customer message(s) + conversation context + draft order state
        │
        ▼
  Router: DecisionProvider ──► RouterDecision {primary, secondary?, urgency, flags}
        │                       (router.py builds identical questions for every provider)
        ├─ order label (primary or secondary)
        │        ▼
        │   OrderExtractor ──► ExtractionOutput (proposal: ids, quantities, evidence; no prices)
        │        ▼
        │   checks.py: evidence quotes exist, ids exist in menu  ──► reject/flag hallucinations
        │        ▼
        │   Deterministic core (M1): menu matching, PricingEngine.quote → Quote (verified, integer cents),
        │   order state transitions, diff vs. previous draft (the patch shown to the business)
        │
        └─ other label ──► BusinessTools: lookup_order / order_status / request_handoff → ToolOk | ToolErr
                                    ▼
             Reply layer (M1/M8): templates filled only from verified results;
             pending vs. confirmed shown explicitly; clarification_question when something is missing
                                    ▼
                         chat reply + business order ticket
```

Customer claims are recorded as claims (`customer_claims_paid`), never as facts (`OrderRecord.payment_confirmed`).

## Repository layout

Directories marked *(Mx)* are created in that milestone; everything else exists now.

```
shoproute/
├── pyproject.toml, uv.lock, Makefile, CLAUDE.md, PROGRESS.md, README.md
├── .githooks/pre-commit          lint + tests before every commit
├── config/                       (M3) models.json: provider, model, pricing, rpm/tpm; label/prompt versions
├── src/shoproute/
│   ├── schema/                   versioned contracts (docs/SCHEMA.md)
│   │   ├── common.py             versions, Strict base, Evidence
│   │   ├── conversation.py       Message, Conversation, Split, Source
│   │   ├── menu.py               MenuCatalog, MenuItem, Variant, Modifier, ComboSlot
│   │   ├── extraction.py         ExtractionOutput (model proposal)
│   │   ├── routing.py            RouterLabel, descriptions, RouterDecision
│   │   ├── order.py              Quote, OrderRecord, HandoffTicket, ToolOk/ToolErr (verified)
│   │   └── annotation.py         AnnotatedConversation (gold format), Scenario, WritingStyle
│   ├── domain/                   money.py (Cents), clock.py (injected Clock)
│   ├── interfaces/               decision.py, extractor.py, tools.py (Protocols)
│   ├── mocks/                    scripted DecisionProvider/OrderExtractor, in-memory BusinessTools
│   ├── router.py                 DecisionRequest builder + response parser
│   ├── checks.py                 evidence + catalog grounding checks
│   ├── paths.py                  data locations, sealed test-split guard
│   ├── core/                     (M1) pricing.py, matching.py, state.py, diff.py, replies.py
│   ├── baselines/                (M1) rules extractor (regex + fuzzy menu match), keyword router
│   ├── llm/                      (M3) client.py, config.py, cache.py, throttle.py, fake.py
│   ├── providers/                (M7) julia1.py, jev.py, openai_decisions.py (DecisionProvider adapters)
│   ├── extractors/               (M3/M5) teacher.py (API), local.py (llama.cpp/MLX/transformers)
│   ├── data/                     (M2/M4) loaders, split builder, synthetic generation, dedup
│   ├── eval/                     (M3) metrics.py, stats.py, estimate.py, store.py, report.py, judge_agreement.py
│   ├── train/                    (M6) LoRA configs and scripts (run on Colab/Kaggle)
│   ├── tracing.py                (M6/M8) step traces to JSONL/SQLite
│   └── app/                      (M8) FastAPI demo API: chat simulator, tickets, comparison
├── data/
│   ├── samples/                  M0 examples: menus/ + conversations/ (split "sample", never scored)
│   ├── menus/                    (M1) 3 business menus + 1 held-out menu
│   ├── dev/                      (M2) ~80 human-written, labeled
│   ├── test/                     (M2) ~200 human-written, SEALED (paths.test_split_dir guard)
│   └── synthetic/                (M4) pilot + bulk, with distribution logs
├── runs/                         (M3) committed eval outputs: manifest + raw outputs + metrics + report
├── web/                          (M8) frontend
├── docs/
└── tests/
```

**Storage:** JSON/JSONL files for data and runs (diffable, committed); SQLite only if the demo needs a
live ticket store. No Postgres.

## Key interfaces (implemented in M0 with mocks)

| Interface | File | Implementations |
|---|---|---|
| `DecisionProvider.decide(DecisionRequest) → DecisionResponse` | `interfaces/decision.py` | `ScriptedDecisionProvider` (M0); keyword baseline (M1); Julia-1, Jev, OpenAI Decisions adapters (M7) |
| `OrderExtractor.extract(ExtractionRequest) → ExtractionResult` | `interfaces/extractor.py` | `ScriptedExtractor` (M0); rules baseline (M1); teacher API extractors (M3); local students (M5/M6) |
| `BusinessTools.lookup_order / order_status / request_handoff → ToolResult` | `interfaces/tools.py` | `InMemoryBusinessTools` (M0) |
| `PricingEngine.quote(menu, proposal) → ToolResult[Quote]` | `interfaces/tools.py` | deterministic engine (M1) |

Every model-backed extractor parses through `parse_model_output`, which never raises: invalid JSON is kept
as `raw_text` + `error`, so JSON-validity rates come from saved outputs.

## Frontend (M8): own visual design

Lightweight: **Vite + Preact + TypeScript**, plain CSS with custom properties, no component library.
Served as a static build (GitHub Pages) reading exported JSON, plus a local "live" mode against the FastAPI
app. Never exposes paid API keys; anything public is rate-limited or replay-only.

Non-visual logic may be adapted from AgentDesk (chat-state reducer, SSE parser, comparison data shaping;
docs/AGENTDESK_REUSE.md). **Nothing visual is copied.** AgentDesk uses forest green / stone / rust with
system sans-serif and an ops-dashboard layout; ShopRoute deliberately looks like a food counter:

- **Concept: "order counter."** The order is a paper kitchen ticket, not a dashboard card.
- **Palette:** receipt paper `#FFFDF6`, ink `#1F1B2E`, mustard `#F2B705` (highlights, "new" tickets),
  cobalt `#2D5BFF` (links, router output), ketchup `#D7263D` reserved for errors/off-menu. Dark mode
  inverts to ink background with paper-tinted text.
- **Type:** Space Grotesk for headings/UI, JetBrains Mono for tickets, prices and model outputs.
- **Layout (desktop):** three panes. Left: phone-frame chat simulator with business picker. Center:
  the live ticket (perforated edge, line items appearing as they're extracted, pending fields with dashed
  underline, "changed" lines struck through, total computed by code). Right: "under the hood" drawer:
  router label + secondary + urgency per message, extractor JSON with evidence highlighted in the chat.
  **Phone:** single column with tabs (Chat / Ticket / Inspect).
- **Pages:** Chat simulator · Ticket board (columns new → preparing → ready) · Comparison (same
  conversation through teacher vs. students; router providers side by side, with cost/latency) · Results
  (the four experiments' tables and charts, each linking to its saved run).

## Planned commands (later milestones)

All via `make` (thin wrappers over `uv run python -m shoproute.<module>`). Targets for unimplemented
milestones exit with an error today. Anything that spends money prints an estimate and requires `--yes`
(and asks Julian first if > $2).

| Milestone | Command | What it will do |
|---|---|---|
| 1 | `make menus` | Validate `data/menus/*.json` (3 + held-out), print item/variant/modifier counts. |
| 1 | `make test` | Pricing, matching, order-state, rules-baseline tests. |
| 2 | `make annotate` | Local annotation tool (writes AnnotatedConversation JSON; blind relabel mode for the 30-conversation self-consistency check). |
| 2 | `uv run python -m shoproute.data.split --seal` | Lock dev/test, write counts per label/scenario, record test-file hashes. |
| 3 | `make teacher-bakeoff ARGS="--estimate"` → `ARGS="--pilot 5"` → full | Same prompt/schema across `gpt-6-luna`, `gemini-3.1-flash-lite`, `deepseek-flash` (+ optional `gemini-3.8-flash`) on ~40 dev conversations; writes `runs/teacher-bakeoff/<id>/`, report + accuracy-vs-cost chart. |
| 4 | `make synth ARGS="--pilot 200"` | Generate pilot conversations (generator model ≠ teacher), dedup, distribution log. |
| 4 | `make label ARGS="--pilot"` / `make label` | Teacher labels (batch API where available), consistency checks, drop-rate log, actual cost. |
| 5 | `make student-bakeoff` | Zero-shot local run of Qwen3.5-0.8B/2B, Qwen3-1.7B, Gemma 4 E2B on ~20 dev conversations (after license/tooling checks; model downloads need approval). |
| 6 | `make train` | Prints/exports the Colab/Kaggle notebook + config; training runs there (LoRA; QLoRA only if needed). |
| 6 | `make eval ARGS="--split test"` | Requires `SHOPROUTE_UNSEAL_TEST=<reason>`; zero-shot vs few-shot vs fine-tuned vs teacher vs rules. |
| 7 | `make router-bench` | Rules vs Julia-1 vs Jev vs OpenAI Decisions; 3 repeats, option-order shuffles, latency, cost. |
| 8 | `make demo` | FastAPI app + Vite dev server; `make site` exports the static results site. |
