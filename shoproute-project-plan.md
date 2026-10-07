# ShopRoute: Food-Order Understanding, Decision Routing, and Distilled Small Models

Updated October 7, 2026. This document replaces `pedido-facil-project-plan.md`. It keeps that plan's core principles (evidence-backed extraction, human-written evaluation, deterministic pricing, no fabricated results) but narrows the scope to an English-first V1 and adds model-selection experiments.

## 1. Goal

Small food businesses (burger shops, pizzerias, cafés) take many orders by chat, in informal, abbreviated, typo-filled messages spread across several texts:

> "hey can i get 2 cheeseburgers and a coke"
> "actually make one of them no onions"
> "and swap the coke for a sprite"
> "pickup at 7, paying cash"

ShopRoute turns a conversation like that into a **structured, menu-matched order**, detects what's missing and asks a clarifying question, and shows the business a clean order ticket.

It is an ML portfolio project built around four measured comparisons:

1. **Teacher bake-off:** which cheap frontier model labels training data best per dollar?
2. **Student bake-off:** which small open model is the best starting point?
3. **Distillation:** how close does a LoRA-trained small model get to the teacher, and what does it save in cost, speed, and privacy?
4. **Router benchmark:** which decision provider (Julia-1, Jev, OpenAI Decisions) best identifies what the customer wants?

Every model choice in the project is backed by a saved, reproducible comparison.

## 2. Scope

| | V1 (this plan) | Later (V2+) |
|---|---|---|
| Language | English | Brazilian Portuguese, including a test of whether the English-trained student transfers |
| Domain | Food ordering (3 fictional menus + 1 held-out menu) | Appointment-based businesses (salons, clinics): durations, staff, conflicts |
| Ordering | Place, modify, cancel, confirm; corrections across messages; clarifying questions | Reorders from history |
| Timing | Requested pickup/delivery time as stated ("at 7", "asap") | Full scheduling: slots, capacity, rescheduling, recurring orders |
| Support | Router recognizes status, problems, refunds; mocked lookups and staff handoff | Full returns/refund workflows, inventory and substitutions, promotions |
| Channel | Web chat simulator | Live WhatsApp Cloud API |

Design the schema and business logic to be **language-neutral** from the start. Only messages, reply templates, and test sets are tied to a language. Keep V2 items out of V1 code except where a field or label needs to exist so V2 can be added later without breaking changes.

## 3. Architecture

```
customer message(s) + conversation context + draft order state
        │
        ▼
  Router (decision provider)  ──►  label: PLACE_ORDER, ORDER_STATUS, ...
        │
        ├─ order-related ──► Student (extractor) ──► order patch + evidence
        │                                                │
        └─ other ──────────────────────────────┐         ▼
                                               ▼   Deterministic core
                                    mocked tools ◄── (menu matching, prices,
                                                      totals, state rules)
                                               │
                                               ▼
                               reply (template from verified results)
                               + business order ticket
```

| Component | Responsibility |
|---|---|
| Router | Primary label, optional secondary label, urgency, context flags |
| Student (extractor) | Items, quantities, sizes, modifications, fulfillment, time, address, payment, evidence, order patches |
| Deterministic core | Menu matching, prices, totals, valid state transitions. **Prices and totals are never produced by a model.** |
| Mocked tools | Order lookup, order status, staff handoff queue |
| Reply layer | Templates filled from verified results; clear pending vs. confirmed status |

Customer claims are not facts: "I already paid" records a payment claim, not a confirmed payment.

## 4. Extraction task (student and teacher)

**Input:** the business's menu catalog (JSON) + the conversation so far (customer and business messages with timestamps) + the current draft order.

**Output (Pydantic schema; write `docs/SCHEMA.md` first):**

- `items[]`: `menu_item_id` (must exist in the catalog, or `null` + `unmatched_text` if not on the menu), quantity, size/variant, modifications (removals, additions, substitutions), per-item notes.
- `fulfillment`: delivery | pickup | unknown, plus the requested time as stated and normalized when unambiguous.
- `address`: street, number, unit, reference point, raw text.
- `payment`: card | cash (with change needed) | other | unknown.
- `customer_name`, general notes.
- `missing_or_ambiguous[]`: fields needing clarification.
- `clarification_question`: one natural question covering what's missing.
- `evidence`: for each item and field, the message index and quoted text it came from.

Corrections and cancellations ("actually", "nvm", "swap X for Y", "remove the coke") must update the order correctly across messages. Keep unknown values distinct from absent or not applicable.

## 5. Router taxonomy (V1)

15 primary labels, chosen to fit every provider's option limits in a single call (Julia-1's native maximum is 20).

| # | Label | Example |
|---|---|---|
| 1 | `PLACE_ORDER` | "2 cheeseburgers and fries" |
| 2 | `MODIFY_ORDER` | "swap the coke for a sprite" |
| 3 | `CANCEL_ORDER` | "nvm cancel it" |
| 4 | `CONFIRM_ORDER` | "yep that's right" |
| 5 | `MENU_QUESTION` | "do you have veggie burgers?" |
| 6 | `DELIVERY_QUESTION` | "do you deliver to Oak St? how much?" |
| 7 | `PAYMENT_QUESTION` | "can I pay cash?" |
| 8 | `PAYMENT_CLAIM` | "I already paid" |
| 9 | `ORDER_STATUS` | "where's my food??" |
| 10 | `ORDER_PROBLEM` | "the bacon was missing" |
| 11 | `REFUND_REQUEST` | "I want my money back" |
| 12 | `HUMAN_REQUEST` | "let me talk to a person" |
| 13 | `SMALL_TALK` | "hi", "thanks!" |
| 14 | `OUT_OF_SCOPE` | "are you hiring?" |
| 15 | `UNKNOWN` | too unclear to label |

Also per message:
- **Secondary label** (optional) for messages with two requests.
- **Urgency:** normal | time-sensitive | needs staff now (written rubric; frustration alone is not urgency).
- **Context flags:** refers to current draft vs. placed order; asks for a human.

Keep each label description short (Julia-1 limits each option to 48 tokens). Write label descriptions once and send the identical wording to every provider.

## 6. Language realism (English V1)

- Abbreviations and slang: u, ur, pls, thx, lemme, gimme, gonna, nvm, rn, idk.
- Typos, missing punctuation, ALL CAPS, emojis, several short messages in a row.
- Number words ("two", "a couple", "another one"), sizes (S/M/L, 12-inch, half-and-half pizza), combos.
- Vague references ("the usual", "same as before", "one of them").
- Off-menu requests, chit-chat mid-order, a complaint mid-order.

## 7. Data

### Menus
Create 3 fictional food businesses as catalog JSON (e.g. burger shop, pizzeria with half-and-half, café/bakery) with sizes, add-ons, combos, and prices. Create 1 additional **held-out menu** used only in testing, to measure generalization to an unseen business.

### Human-written dev and test sets (essential)
Synthetic data mostly measures how well a model imitates the teacher, so evaluation uses **human-written** conversations.
- Julian writes conversations against the menus, including fast phone-style messages. Others may contribute with a simple form (a menu plus a scenario card).
- Target 200–300 conversations total: **dev ~80** (used for the teacher and student bake-offs and prompt tuning) and **test ~200, sealed** (used only for final results).
- Label each conversation with gold extraction output and router labels using the annotation tool.
- Relabel 30 test conversations a week later, blind, to measure self-consistency.
- Include tricky cases deliberately: two-request messages, corrections after confirmation, ambiguous references, off-menu items, missing info, context-dependent "yes".

### Synthetic training data
- A cheap model generates conversations from combinations of (menu × customer persona × scenario × writing style). Control diversity with explicit attributes, deduplicate near-duplicates, and log the distribution.
- Prefer a **different model for generation than for labeling**, to reduce the teacher agreeing with its own phrasing.
- Start with a **200-conversation pilot**, audit it by hand, then scale to **1,000–2,000** conversations.
- The winning teacher labels them with structured output + evidence (batch API where available, cached system prompt).
- Automatic consistency checks: evidence quotes exist in the conversation, item IDs exist in the catalog, JSON validates. Drop failures and log the drop rate.

### Rules
- Never train on test conversations or anything derived from them. Deduplicate across splits.
- **Privacy:** no real customer chats in the repo or training data.
- **Terms:** before bulk labeling, check each provider's terms on using outputs to train models, and record the conclusion in `docs/TERMS.md`.

## 8. Experiment 1: Teacher bake-off

**Candidates** (prices verified October 7, 2026 from official pages; re-verify before spending):

| Model | Standard (in / out per 1M tokens) | Discounted | Notes |
|---|---|---|---|
| OpenAI `gpt-6-luna` | $0.10 / $0.50 | Batch: $0.05 / $0.25 | Cheapest OpenAI model |
| Google `gemini-3.1-flash-lite` | $0.25 / $1.50 | Batch: $0.125 / $0.75 | Cheapest Gemini. Free tier exists, but free-tier content is used to improve Google's products |
| DeepSeek `deepseek-flash` | $0.30 / $1.20 (peak) | Off-peak: $0.15 / $0.60 | No batch API; off-peak is outside 01:00–04:00 and 06:00–10:00 UTC on weekdays |
| *Optional:* `gemini-3.8-flash` | $0.75 / $3.75 (promo until Dec 31, 2026) | Batch: $0.375 / $1.875 | Newest Gemini Flash; include only if budget allows |

**Method:**
1. Run the ~40 labeled dev conversations through every candidate with the identical prompt and schema.
2. Score order exact match, item-level F1, correction handling, JSON validity, hallucinations, and cost per 1,000 orders.
3. **Selection rule:** the cheapest candidate within 3 percentage points of the best on item-level F1. Plot accuracy vs. cost for all candidates.
4. Record model versions, prompts, token usage, and actual cost.

Expected cost: well under $1 total.

## 9. Experiment 2: Student bake-off

**Candidates:**

| Model | Notes |
|---|---|
| Qwen3.5-0.8B | Default student #1 |
| Qwen3.5-2B | Default student #2 |
| Qwen3-1.7B | Text-only fallback with mature tooling |
| Gemma 4 E2B | Second model family (~2.3B effective parameters, Apache 2.0) |

**Before running:** verify each model's license, that LoRA training works in the chosen tool (Qwen3.5 small models include a vision encoder that may complicate tooling), and that it can be quantized for local inference.

**Method:** run ~20 dev conversations zero-shot through each candidate locally. Score JSON validity and item-level F1. Keep the default pair (Qwen3.5-0.8B and 2B) unless another candidate is clearly better or tooling fails; document the decision either way.

Cost: $0 (local).

## 10. Experiment 3: Distillation

For each chosen student, evaluate on the sealed test set:

| Condition | What it is |
|---|---|
| Zero-shot | Base model with instructions only |
| Few-shot | Base model with 2–3 worked examples in the prompt |
| Fine-tuned | Base model + LoRA adapter trained on teacher-labeled data |
| Teacher | The bake-off winner, for reference |
| Rules baseline | Regex + fuzzy menu matching (shows why the task is hard) |

**Training:**
- Use **LoRA**. Use QLoRA only if a model doesn't fit in available memory; record which was used.
- Same training data, schema, prompt format, and comparable tuning budget for every student. Document any differences.
- Training on teacher outputs is output-level distillation implemented through supervised fine-tuning.
- Optional: constrained decoding (JSON-schema-guided generation with menu-constrained item IDs), reported with and without.
- Optional: one full fine-tune of the 0.8B model to compare against LoRA.
- Optional: learning curve over training-set size (250 / 500 / 1,000 / 2,000).
- Use 3 seeds for the final configuration if time allows.

**Deployment format:** merge adapter into the base model and quantize (GGUF for llama.cpp/Ollama, or MLX) for local inference.

**What "savings" means in the results.** Report all of these, measured, for each student vs. the teacher:
- **Running cost:** cost per 1,000 orders and per successful order (teacher = API fees; student = $0 in API fees on local hardware).
- **Setup cost:** one-time teacher labeling + training compute, and the resulting **break-even point** (orders after which the student has paid for itself).
- **Speed:** latency p50/p95, local student vs. teacher API round-trip.
- **Footprint:** peak memory and model file size.
- **Privacy and independence:** student runs fully offline; customer messages never leave the machine; no dependence on provider pricing or availability.

The teacher candidates are very cheap per order, so do not overstate per-order savings at small volume; present the cost, speed, and privacy results together.

## 11. Experiment 4: Router benchmark

**Providers** (verified October 7, 2026 from official docs):

| Provider | How it runs | Option limit | Output | Cost |
|---|---|---|---|---|
| Rules baseline | Local keyword rules | n/a | Label | $0 |
| Julia-1 (Supersonic Labs) | Local, CPU is fine; 144.3M-parameter encoder, ~550 MiB weights, Apache 2.0, Python 3.11+ | **2–20 options per call**; each option ≤48 tokens; 8,192-token combined limit | Choice + probabilities | $0 |
| Jev (TypeSafe) | Hosted: `POST /v1/systemone`, bearer auth, models listed at `GET /v1/models` | No maximum documented; **test early** with all 15 labels | Choice + confidence + probabilities | Input tokens billed (price not in docs); output tokens currently free |
| OpenAI Decisions | Hosted: `POST /v1/decisions`, public beta, `gpt-6-luna` only | No maximum documented in the guide | Choice + confidence + probabilities, or refusal | $0.10 per 1M input tokens; no output charges |

All three accept a state/input, named questions, and choice/score/boolean question types, so one `DecisionProvider` interface covers them.

**Rules:**
- Identical messages, context, and label descriptions for every provider. Keep extraction fixed when comparing routers.
- Do not fine-tune Julia-1 (its training pipeline isn't published, and it is not a generative model).
- Treat provider confidence scores as provider-specific; do not compare them directly without calibration on dev data.
- Optional: have the teacher also label router decisions and train a student to route, adding it as one more row.

**Metrics:** macro-F1, per-label precision/recall, confusion matrix, secondary-label recall, `UNKNOWN` handling (abstain vs. confident wrong guess), stability across 3 repeated runs, sensitivity to option order, latency (p50/p95), cost per 1,000 messages.

Expected cost: cents for OpenAI Decisions; Jev depends on its input price (check before running).

## 12. Evaluation (all on the sealed test set unless noted)

- Order exact match (everything correct).
- Item-level F1: an item counts as correct only if menu item + quantity + size + modifications all match. Also per-component accuracy.
- Field accuracy: fulfillment, time, address components, payment.
- Correction handling accuracy on conversations with corrections or cancellations.
- Clarification detection: precision/recall of `missing_or_ambiguous`, plus a rubric rating of `clarification_question` (an LLM judge is allowed only if validated against Julian's ratings on 50 samples).
- Hallucination rate: items or values not supported by the conversation.
- JSON validity rate.
- Generalization: results on the held-out menu reported separately.
- Cost per 1,000 orders and per successful workflow, including retries and fallbacks.
- Latency (p50/p95) and peak memory, on GPU and on CPU/Apple Silicon with the quantized model.
- Slices by writing style, business, and conversation length.
- `docs/ERROR_ANALYSIS.md` with categorized failures and examples.
- **Every reported number must come from committed eval outputs. No fabricated or estimated results in tables.**

## 13. Hardware and tooling

- **Milestones 0–5:** Julian's current computer. No model training needed; Julia-1 and the zero-shot student bake-off run on CPU.
- **Training:** free Colab or Kaggle GPU with Unsloth or Hugging Face TRL. Later, optionally an M2 Mac mini (16GB) with MLX.
- **Local inference:** quantized students via llama.cpp, Ollama, or MLX.
- **Language: Python.** All backend, data, labeling, training, evaluation, and inference code is Python (Pydantic for schemas). The ML tooling (Unsloth, TRL, MLX, llama.cpp bindings) and Julia-1's runtime are Python-only, so do not split the backend across languages.
- **Frontend:** a lightweight web frontend for the demo, dashboard, and annotation tool. It must have its **own visual design**, distinct from AgentDesk's (see section 15).

## 14. Budget and spend rules

Total budget: **$5–10 USD**.

| Item | Planned |
|---|---|
| Teacher bake-off | < $1 |
| Synthetic generation + bulk labeling (1–2k conversations) | $1–4 |
| Router benchmark (Jev, OpenAI Decisions) | < $1 (confirm Jev pricing) |
| Training compute | $0 (free GPUs); ask before renting |
| Buffer | remainder |

- **Ask Julian before any single spend over $2**, and keep a running total in `docs/COSTS.md` from actual usage.
- Always run a priced pilot before a bulk job.
- Set spend caps on every provider account where possible.

## 15. AgentDesk reuse

Julian's earlier project, AgentDesk (https://github.com/Julian-Reyes/AgentDesk), is an English online-store agent-ops project. **It is written in TypeScript** (Node 24, Hono, Postgres/Drizzle, Zod, React + Vite). ShopRoute is Python, so reuse means **porting patterns and logic into Python**, not copying TypeScript files.

**Candidates to port** (verify each in Milestone 0; paths as of October 7, 2026):

| AgentDesk pattern | Path | Use in ShopRoute |
|---|---|---|
| Models as config; one OpenAI-compatible client for all providers | `server/config/models.json`, `server/src/llm/openai-compatible.ts`, `server/src/llm/config.ts`, `server/src/llm/factory.ts` | Python provider client and model config (OpenAI, Gemini, DeepSeek all expose OpenAI-compatible APIs; verify each) |
| Response cache and rate throttling | `server/src/llm/cache.ts`, `server/src/llm/throttle.ts` | Port |
| Fake provider so tests never call real APIs | `server/src/llm/fake.ts` | Port the approach |
| Cost estimate before a run | `server/src/evals/runner/estimate.ts` | Port; implements the priced-pilot rule |
| Model comparison with confidence intervals and a "clear winner" rule | `server/src/evals/runner/compare.ts`, `comparison-sets.ts` | Port; use for all four experiments |
| LLM-judge agreement check against human grades | `server/src/evals/judge/agreement.ts`, `sample.ts` | Port, for the clarification-question rubric |
| Eval run storage layout and reports | `server/src/evals/runner/store.ts`, `report.ts`, `server/eval-results/` | Adapt the structure |
| Tracing of each step | `server/src/tracing/tracer.ts` | Adapt for router/extractor/tool traces |
| Conventions: injected clock, integer-cents money, `{ok, data}` / `{ok: false, error}` tool results | `server/src/domain/clock.ts`, `server/src/domain/money.ts`, `server/src/tools/define.ts` | Same conventions in Python |
| Static results export for GitHub Pages | `server/src/static/export.ts` | Same approach for ShopRoute's results site |
| Working rules, pre-commit hook, PROGRESS.md style | `CLAUDE.md`, `.githooks/pre-commit` | Adapt for a Python toolchain |

**Frontend:** non-visual logic may be adapted (e.g. chat state handling, streaming/SSE client, comparison data shaping in `web/src/storefront/chat-state.ts`, `web/src/lib/sse.ts`, `web/src/ops/comparison.ts`). **Do not copy AgentDesk's styling, layout, or page designs** (`web/src/styles.css`, page components). ShopRoute's UI must look clearly different: its own colors, typography, and layout suited to a food-ordering product.

**Do not reuse:** the Larchgrove catalog, refund/coupon/goodwill policies, the multi-agent loop and handoffs (ShopRoute does extraction, not agents), or Postgres (JSON files or SQLite are enough).

**Spending note:** AgentDesk has its own provider spend caps (e.g. Gemini, Groq). Use separate API keys or projects for ShopRoute so its costs are tracked independently.

Record what was ported, from which path, and what changed in `docs/AGENTDESK_REUSE.md`. Do not modify AgentDesk. ShopRoute must run independently.

## 16. Demo (V1)

- **Chat simulator** (web): pick a business, type messages as the customer, watch the order update live next to the chat. The bot replies with a confirmation or a clarifying question, e.g.:
  > "Got it: 1 Cheeseburger, 1 Cheeseburger (no onions), 1 Sprite. Pickup at 7pm. Total $20.00, paying cash. Is that right?"
- **Order ticket view** for the business: incoming orders and a simple status flow (new → preparing → ready).
- **Comparison view:** teacher vs. students on the same conversation, and the router providers' answers side by side, with cost and latency.
- Hosting: static or lightweight; never expose paid API keys publicly. Rate-limit anything public.

## 17. Deliverables

- Reproducible repo with a `Makefile`: `make menus`, `make annotate`, `make teacher-bakeoff`, `make synth`, `make label`, `make student-bakeoff`, `make train`, `make eval`, `make router-bench`, `make demo`.
- Hugging Face release: LoRA adapters + quantized models, model cards, the menus, and the human-written test set (only data Julian and consenting writers created).
- `REPORT.md`: problem, data strategy (synthetic training vs. human test), the four experiments with results tables and charts, error analysis, cost comparison, limitations.
- Tests: schema validation, deterministic pricing, menu matching, evidence checking, order-state logic, metrics.

## 18. Milestones (V1)

| # | Work | Acceptance evidence |
|---|---|---|
| 0 | AgentDesk inspection; repo layout; `SCHEMA.md`, `TAXONOMY.md`, `ARCHITECTURE.md`, `ANNOTATION_GUIDE.md`; provider/tool interfaces with mocks; `PROGRESS.md` | Versioned contracts, sample conversations, reuse doc with file paths, passing schema tests |
| 1 | Menus (3 + 1 held-out), pricing engine, order state logic, rules baselines (extraction + routing) | Deterministic tests pass; no model needed |
| 2 | Annotation tool; Julian writes and labels dev + test sets; test set sealed | Locked split with counts per label and scenario; self-consistency sample scheduled |
| 3 | Teacher bake-off | Results table + accuracy-vs-cost chart; teacher chosen by the stated rule; actual cost logged |
| 4 | Synthetic generation: 200-conversation pilot → audit → 1–2k bulk, labeled by the winning teacher | Data audit, distribution log, drop rate, actual cost |
| 5 | Student bake-off (zero-shot, local) | License/tooling checks; results table; students chosen |
| 6 | LoRA training; zero-shot vs. few-shot vs. fine-tuned vs. teacher on the test set; error analysis | Reproducible training configs and eval outputs |
| 7 | Router benchmark: rules vs. Julia-1 vs. Jev vs. OpenAI Decisions | Verified API contracts, per-label metrics, stability and cost results |
| 8 | Demo, report, Hugging Face release | Working demo; every number traceable to saved outputs |

**V2 candidates (separate plan later):** food scheduling (slots, capacity, rescheduling); Brazilian Portuguese (new data and test set, transfer experiment); appointment-based business domain; inventory, promotions, and full returns workflows; live WhatsApp integration.

## 19. Working rules

- One milestone per instruction. After each: update `PROGRESS.md`, run tests, commit.
- Ask before spending over $2, adding major dependencies, or downloading large models.
- Verify provider and model contracts, licenses, and prices against primary sources before integrating. Do not invent APIs, capabilities, confidence values, or results.
- Keep the sealed test set isolated. Log provider, model version, prompt version, and data version for every run.
