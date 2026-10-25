# AgentDesk reuse

AgentDesk (https://github.com/Julian-Reyes/AgentDesk) is TypeScript (Node, Hono, Postgres/Drizzle, Zod,
React + Vite). OrderSLM is Python, so reuse means **porting patterns into Python**, not copying files.
AgentDesk is not a dependency and was not modified; OrderSLM runs on its own.

Inspected at commit `c24529c1d58ebafa765f5a6e11459b29bbd3edb2` (2026-10-06), shallow clone, read-only.
Every path in spec §15 exists at that commit. One correction to the spec's table: the "clear winner" rule
is `pickWinner` in `comparison-sets.ts`, and the Wilson interval is in `evals/judge/agreement.ts`
(`compare.ts` imports it). `compare.ts` itself is mostly AgentDesk-specific grading (leak phrases, emojis).

Status key: **Ported (M0)** = already in OrderSLM · **Planned (Mx)** = port in that milestone ·
**Not reused**.

## Ported or planned

| # | AgentDesk path | What it does there | OrderSLM equivalent | Status / what changes |
|---|---|---|---|---|
| 1 | `server/src/domain/money.ts` | Integer cents, `percentOf` half-up, `formatCents` | `src/orderslm/domain/money.py` (`Cents`, `percent_of`, `format_cents`) | **Ported (M0).** `Cents` is a strict Pydantic int ≥ 0: floats and strings are rejected, not coerced. |
| 2 | `server/src/domain/clock.ts` | Fixed store date, injected clock | `src/orderslm/domain/clock.py` (`Clock`, `fixed_clock`, `system_clock`) | **Ported (M0).** Timezone-aware datetimes required (businesses have local times for "at 7"). No return-window helpers (no returns in V1). |
| 3 | `server/src/tools/define.ts` | `ToolResult = {ok, data} \| {ok:false, error}`, `callTool` validates args with Zod | `src/orderslm/schema/order.py` (`ToolOk[T]`, `ToolErr`, `ToolResult`), `interfaces/tools.py`, `mocks/tools.py` | **Ported (M0).** Adds `verified_by` on every result so verified facts are traceable. No `policyDecision` or agent assignment (no agents, no refund policies). |
| 4 | `server/src/llm/fake.ts` | Scripted provider: plays back responses, records requests, throws when exhausted | `src/orderslm/mocks/decision.py` (`ScriptedDecisionProvider`), `mocks/extractor.py` (`ScriptedExtractor`) | **Ported (M0)** for both new interfaces. The extractor mock goes through the same `parse_model_output` path as real models, so broken JSON is tested. M3 adds a scripted chat provider for the LLM client. |
| 5 | `server/src/llm/types.ts`, `openai-compatible.ts`, `config.ts`, `factory.ts`, `server/config/models.json` | One OpenAI-compatible chat client (plain fetch), models as config with pricing/rpm/tpm/tier, env expansion, retry with `Retry-After`, daily-quota detection, cost in micro-dollars | `src/orderslm/llm/{types,client,config,factory}.py`, `config/models.json` | **Ported (M3, 2026-10-15).** Python `httpx` client (Julian approved the runtime dependency). Anthropic uses its native Messages API (`output_config.format`), not an OpenAI-compatible layer. Keep: config ids include provider; key env var name only in config; retry 429/5xx; fail fast on daily quota; `cost_micros`. Add: JSON-schema structured output (`response_format`) per provider, **verified against each provider's docs first** (OpenAI, Gemini OpenAI-compat endpoint, DeepSeek). Drop: tool-call repair (`repairReplyCall`, `withCorrection`): OrderSLM does single-shot structured extraction, not tool loops. |
| 6 | `server/src/llm/cache.ts` | Record/replay cache keyed by sha256 of stable-JSON(request + config), modes off/record/replay/refresh, atomic writes, original latency kept | `src/orderslm/llm/cache.py` | **Ported (M3).** Same key material and modes; `replay` mode guarantees a $0 rerun. Also wraps `DecisionProvider` adapters in M7. Cache dir `.llm-cache/` (gitignored). |
| 7 | `server/src/llm/throttle.ts` | Sliding-window rpm/tpm limiter shared per provider+model, reserve-then-correct token estimate, every retry takes a slot | `src/orderslm/llm/throttle.py` | **Ported (M3), rpm only:** token-window limiter not ported yet. Synchronous version first (threads only if bulk labeling needs it); same "limiter inside the cache" layering so replays never wait. Batch APIs (OpenAI/Gemini) bypass it. |
| 8 | `server/src/evals/runner/estimate.ts` | Preflight: calls, tokens, time and cost per model before a run | `src/orderslm/eval/teacher_bakeoff.py` (`estimate_micros`, `--max-cost`) | **Ported (M3)**, inside the bake-off runner for now; moves to `eval/estimate.py` when M4 labeling needs it. Implements the priced-pilot rule (spec §14): estimate → pilot → actual vs. estimate → ask if > $2. Estimates from measured tokens per conversation, not guesses, once a pilot exists. |
| 9 | `server/src/evals/judge/agreement.ts` (`wilson`) + `server/src/evals/runner/comparison-sets.ts` (`pickWinner`) | Wilson 95% CI; winner = best rate among models with zero policy violations, "not significant" if CIs overlap | `src/orderslm/eval/stats.py` | **Planned (M3).** Port `wilson` and the overlap rule as-is for rates. Add what OrderSLM's comparisons need: **paired** tests on the same items (McNemar for exact match, paired bootstrap CI for item-F1/macro-F1), since every model sees identical conversations. The teacher rule is the spec's: cheapest within 3 pp of the best item-F1. **Paired tests done 2026-10-25 (M6):** `mcnemar_exact`, `holm`, `percentile_interval` in `stats.py`; paired bootstrap over chats in `eval/student_compare.py`. |
| 10 | `server/src/evals/judge/agreement.ts`, `sample.ts` | Blind stratified sample (seeded), separate sample/key files, exact / ±1 agreement with Wilson CIs, per-model breakdown | `src/orderslm/eval/judge_agreement.py` | **Planned (M6)** for the clarification-question rubric: 50 blind samples rated by Julian vs. the LLM judge (spec §12). Keep the sample/key split so the grader never sees model names. Add Cohen's κ / quadratic-weighted κ alongside raw agreement. |
| 11 | `server/src/evals/runner/store.ts`, `report.ts`, `server/eval-results/` | One file per finished item (atomic, resumable), manifest per run, judge results in their own tree, markdown report rebuilt from saved files | `src/orderslm/eval/teacher_bakeoff.py` (`report`), `runs/` | **Ported (M3)** for the bake-off: same layout; report rebuilt from saved outputs only (`--report`). Shared store/report modules when a second experiment needs them. Layout: `runs/<experiment>/<run_id>/manifest.json` (provider, model, prompt version, schema version, data version, git commit, cost), `outputs/<config>/<conversation_id>.json` (raw text + parsed + usage + latency), `report.md`, `metrics.json`. Reports are always rebuilt from saved outputs (spec §12: no number without a saved output). |
| 12 | `server/src/tracing/tracer.ts` | Run/step tracer interface; memory tracer for tests, Postgres tracer for real runs | `src/orderslm/tracing.py` | **Planned (M6/M8).** Same interface (router → extractor → pricing → tools → reply steps, with tokens/latency/cost/prompt version), but JSONL files or SQLite instead of Postgres. |
| 13 | `server/src/static/export.ts`, `static/git.ts` | Answers every GET in-process and writes static JSON for GitHub Pages; deterministic bytes | `src/orderslm/site/export.py` | **Planned (M8).** Results site reads exported JSON built from `runs/`; never calls a paid API. |
| 14 | `CLAUDE.md`, `.githooks/pre-commit`, `PROGRESS.md` | Working rules, hook running typecheck + tests, short status file | `CLAUDE.md`, `.githooks/pre-commit`, `PROGRESS.md` | **Ported (M0)**, adapted to Python (`ruff` + `pytest` via `uv`). AgentDesk's provider spend rules are replaced by OrderSLM's budget (docs/COSTS.md). |
| 15 | `web/src/storefront/chat-state.ts`, `web/src/lib/sse.ts`, `web/src/ops/comparison.ts` | Pure reducer for chat state; incremental SSE parser for POST streams; comparison data shaping | `web/src/chat-state.ts`, `web/src/sse.ts`, `web/src/comparison.ts` | **Planned (M2 setup, M8 demo).** The frontend starts in M2 for the annotation tool; Non-visual logic only, re-typed for OrderSLM's API (order panel state, ticket statuses). |

## Not reused

| AgentDesk | Why not |
|---|---|
| `web/src/styles.css`, all page components (`Storefront.tsx`, `Ops.tsx`, `*Page.tsx`, `Timeline.tsx`) | Spec: OrderSLM's UI must have its own visual design. See docs/ARCHITECTURE.md, "Frontend". |
| `server/src/seed/*` (Larchgrove catalog), `server/src/policy/*` (refunds, coupons, goodwill, returns, promotions) | Different domain. OrderSLM's menus are its own (M1). |
| `server/src/agents/*` (router + multi-agent loop, handoffs, reply checks) | OrderSLM does structured extraction + routing via decision providers, not an agent loop. **Revisit in M8** (Julian, 2026-10-13): reply checks and off-topic/handoff wording, as patterns for the demo's template replies (spec §16). |
| `server/src/db/*`, `server/drizzle/*` | No Postgres: JSON files and SQLite are enough (spec §15). |
| `server/src/evals/grading/*`, `compare.ts` leak/emoji checks | Graded AgentDesk's free-text agent replies. OrderSLM grades structured outputs against gold (item-F1, exact match, field accuracy). |
| `server/src/llm/openai-compatible.ts` tool-call repair | No tool-calling loop in OrderSLM. |

## Spending isolation

AgentDesk has its own caps on Gemini and Groq. OrderSLM uses separate API keys/projects
(`.env.example`) so its spend is tracked independently in docs/COSTS.md.
