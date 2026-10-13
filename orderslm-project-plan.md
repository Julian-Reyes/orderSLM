# OrderSLM: Food-Order Understanding, Decision Routing, and Distilled Small Models

Updated October 7, 2026 (evaluation data revised speed-first the same day, §7). Updated October 8, 2026: test-set contamination rule (§12), student intent output (§3, §4, §10), five roles for the decision providers and the architecture comparison (§11). This document replaces `pedido-facil-project-plan.md`. It keeps that plan's core principles (evidence-backed extraction, evaluation separate from training data, deterministic pricing, no fabricated results) but narrows the scope to an English-first V1 and adds model-selection experiments.

## 1. Goal

Small food businesses (burger shops, pizzerias, cafés) take many orders by chat, in informal, abbreviated, typo-filled messages spread across several texts:

> "hey can i get 2 cheeseburgers and a coke"
> "actually make one of them no onions"
> "and swap the coke for a sprite"
> "pickup at 7, paying cash"

OrderSLM turns a conversation like that into a **structured, menu-matched order**, detects what's missing and asks a clarifying question, and shows the business a clean order ticket.

It is an ML portfolio project built around four measured comparisons:

1. **Teacher bake-off:** which cheap frontier model labels training data best per dollar?
2. **Student bake-off:** which small open model is the best starting point?
3. **Distillation:** how close does a LoRA-trained small model get to the teacher, and what does it save in cost, speed, and privacy?
4. **Decision providers and router benchmark:** which decision provider (Julia-1, Jev, OpenAI Decisions) best identifies what the customer wants, how well they work as independent checkers next to the extractor, and whether a separate router is worth having at all. The question throughout: do decision providers approach LLM-level quality at a fraction of the cost and time?

Every model choice in the project is backed by a saved, reproducible comparison.

## 2. Scope

| | V1 (this plan) | Later (V2+) |
|---|---|---|
| Language | English | Brazilian Portuguese, including a test of whether the English-trained student transfers |
| Domain | Food ordering (3 fictional menus + 1 held-out menu) | Appointment-based businesses (salons, clinics): durations, staff, conflicts |
| Ordering | Place, modify, cancel, confirm; corrections across messages; clarifying questions | Reorders from history |
| Timing | Requested pickup/delivery time as stated ("at 7", "asap") | Full scheduling: slots, capacity, rescheduling, recurring orders |
| Support | Router recognizes status, problems, refunds; mocked lookups and staff handoff. Menu, delivery, hours and payment questions get template answers from menu data only | Full returns/refund workflows, inventory and substitutions, promotions |
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
| Student (extractor) | Items, quantities, sizes, modifications, fulfillment, time, address, payment, evidence, order patches, and its own **intent** label for the message |
| Deterministic core | Menu matching, prices, totals, valid state transitions. **Prices and totals are never produced by a model.** |
| Mocked tools | Order lookup, order status, staff handoff queue |
| Reply layer | Templates filled from verified results; clear pending vs. confirmed status |

Customer claims are not facts: "I already paid" records a payment claim, not a confirmed payment.

**Design rules (October 8, 2026):**
- **The extractor's input never includes the router's label.** The router only decides whether the extractor is called (docs/ARCHITECTURE.md).
- **The student also outputs an intent** (one of the 15 router labels) alongside the order (M4, M6). Because it never sees the router's label, its intent is a genuine second opinion: router and student can cross-check each other (a router that mislabels an order as a non-order would otherwise skip the extractor and lose items), and an extractor-only architecture becomes possible. M7 measures whether a separate router is worth having (§11).

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
- `intent`: the router label (§5) of the latest customer message, decided independently of the router. **Required** for the trained student (added to the contract in M4; the M3 teacher bake-off schema is unchanged).
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

### Evaluation data (speed-first; revised October 7, 2026)
Synthetic training data mostly measures how well a model imitates the teacher, so evaluation uses separate, reviewed data from three sources. **Every result is reported per source.**

- **Source A: Claude-written chats (290: dev 91, test 199).** (80 + 170 at first; Julian's card review on October 8, 2026 added 3 test + 1 dev card per rare label and implicit category mentions, §11e; held-out menu ~25% of test.)
  1. First generate **scenario cards** covering every router label, every menu (the held-out menu only in test), writing styles (typos, abbreviations, emoji, multi-message bursts, ALL CAPS), and the tricky cases: two-request messages, corrections (including after confirmation), ambiguous references ("one of them", "the usual"), off-menu items, missing info, context-dependent "yes", and implicit category mentions ("pop", item names without category words, "something sweet").
  2. Claude writes one conversation per card with gold extraction and router labels, validated by the schema and the grounding checks.
  3. Dev/test are split **by scenario card**, so no near-duplicates cross splits (also checked automatically). Source A is **evaluation data only, never training data**: the cards and conversations never feed synthetic generation, prompts' few-shot examples (except dev for prompt tuning), or training.
  4. Julian reviews in the annotation tool: **all of dev, and a spot-check of at least 25% of test**. Every review is logged (changed or not), and the **correction rate** is reported.
- **Source B: PIZZA.** The 199 converted orders from the PIZZA test split (amazon-science/pizza-semantic-parsing-dataset, CC-BY-NC-4.0; docs/PIZZA.md) are the external **human-written** test set, scored on items only. Never committed or redistributed.
- **Source C (optional): Julian-written.** Julian may later write ~30 conversations as a small human-written test slice. A blind relabel a week later is optional, for this source only.
- The test sets (A test, B, C) are **sealed**: used only for final results. Dev (A dev) is used for the teacher and student bake-offs and prompt tuning.
- Limitation to report: Source A shares one author (Claude), so it may favor models whose phrasing resembles it; Source B and C are the human-written checks. The synthetic-training generator is a different model from Source A's author.

### Synthetic training data
- A cheap model generates conversations from combinations of (menu × customer persona × scenario × writing style). Control diversity with explicit attributes, deduplicate near-duplicates, and log the distribution.
- Prefer a **different model for generation than for labeling**, to reduce the teacher agreeing with its own phrasing.
- Start with a **200-conversation pilot**, audit it by hand, then scale to **1,000–2,000** conversations.
- The teacher labels each customer message's **router intent** (the 15 labels) along with the order, so the student can learn to output both (§4).
- **Mega-menu conversations:** ~20% extra conversations on the combined food-court menu (§11e), teacher-labeled, for the mixed 2B student only.
- **Training-label audit:** before training, the decision providers check the teacher's labels (intent and order); disagreements are reviewed or dropped (§11d).
- The winning teacher labels them with structured output + evidence (batch API where available, cached system prompt).
- Automatic consistency checks: evidence quotes exist in the conversation, item IDs exist in the catalog, JSON validates. Drop failures and log the drop rate.

### Rules
- Never train on test conversations or anything derived from them. Deduplicate across splits.
- **Test-set contamination rule** (§12): test results that led to a fix are reported as "used for fixes", never as clean held-out results.
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
1. Run ~40 dev conversations (Source A dev) through every candidate with the identical prompt and schema.
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

For each chosen student, evaluate on the sealed test sets, reported per source (A test, B PIZZA, C if written):

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
- **The student outputs an `intent` field alongside the order** (required, not optional; §3, §4). Intent accuracy is scored against the reviewed gold labels like every router (§11a).
- **Menu-narrowing training experiment (2B student only, §11e):** a single-menu student (per-restaurant conversations only) vs. a mixed student (the same data + ~20% mega-menu conversations).
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

## 11. Experiment 4: Decision providers and router benchmark

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
- Do not fine-tune Julia-1 in V1 (its training pipeline isn't published, and it is not a generative model). Fine-tuning it is a V2 candidate (§18).
- Treat provider confidence scores as provider-specific; do not compare them directly without calibration on dev data.
- The student's own intent output (§4) is one more row in every routing comparison.

### Five roles for the decision providers (October 8, 2026)

The extractor reads the whole message anyway, so routing alone may add little (its main benefits are skipping the extractor on non-order messages and handling non-order intents). These roles give the decision providers jobs the extractor doesn't already do, so they are useful as **independent checkers**, while the router benchmark still measures how well each one categorizes.

- **Primary roles:** the order checker (b) and the training-label auditor (d). **Supporting roles:** router (a), menu narrowing (e), item chooser (c, optional).
- Each role is **tuned on dev and scored once on test**, with **identical wording for every provider**. Where an LLM could do the same job, also compare against the **teacher LLM** (the bake-off winner), so the key question is answered throughout: do decision providers approach LLM-level quality at a fraction of the cost and time?

**a) Router benchmark + cross-check (M7).**
- Routers compared on every test message: rules baseline, Julia-1, Jev, OpenAI Decisions, the student's intent output, and the teacher LLM. Report accuracy, latency p50/p95 and cost per 1,000 messages for each.
- The router and the student label **independently**: the student never receives the router's label as input (§3 design rule), so its intent is a genuine second opinion, not a copy. That independence is what makes the cross-check meaningful.
- Cross-check: if router and student agree, proceed. If they disagree, run the extractor anyway; if still unclear, ask a clarifying question or flag staff. Log every disagreement and report how many router misses the student caught, and vice versa.
- Product behavior: follow the router when it's confident; when it's unsure, also run the student and cross-check. Calibrate the "unsure" threshold on dev. During testing, run every router and the student on every message.
- Label descriptions may be improved using dev mistakes, applied identically to all providers.
- When reading results: the student learned intents from the teacher's labels, so it may share the teacher's mistakes. Everything is scored against the reviewed gold labels.

**b) Order checker (primary, M6/M7).** Two versions, both run for every provider (updated October 13, 2026):
- **Whole order:** one yes/no check: "Does this order match what the customer asked for?" Input: the conversation plus the extracted order written out in plain text.
- **Line by line:** one yes/no question per order line and per detail ("Did the customer ask for 1 cheeseburger with no onions?", "Did they choose pickup?", "Did they say they'd pay cash?"). A "no" points to the line that is wrong, so the bot can ask about that line instead of flagging the whole order. Report the extra calls and latency this costs.
- Flagged orders go to staff review instead of straight to the kitchen.
- Compare each provider against the teacher LLM doing the same check (both versions).
- **Planted mistakes:** real model errors may be too few to measure catch rates (a good student might make only 10–20 on test). Code plants known errors into correct (gold) orders, one per copy: a dropped or added modification, a wrong quantity, a swapped item, a wrong size, a missing item, an extra item, pickup ↔ delivery, a wrong payment method. Each type is reported separately ("catches 85% of dropped modifications"). The planting code is deterministic (fixed seed) and tested. Tune the checkers on planted dev mistakes; score them once on planted test mistakes, generated by the same code at final eval only (needs Julian's OK under the sealed-test rule: evaluation-only copies, never used for training or tuning).
- Measure on the test set, for real student errors and planted ones separately: catch rate (% of wrong orders flagged), false-alarm rate (% of correct orders flagged), latency, and cost per 1,000 checks. For line by line, also whether the flagged line is the wrong one.
- Report the results whichever way they come out, including "the checker adds nothing over the AI layer".

**c) Item chooser (optional, M7).**
- Runs only for items the extractor marked unmatched.
- Code builds a shortlist of ≤20 menu items with descriptions (fuzzy matching or same category); the provider picks one or "none"; the bot confirms with the customer ("Did you mean the Diablo Burger?").
- Pilot on dev off-menu and vague-reference cases first, comparing: (i) asking the customer with the fuzzy matcher's top 3, (ii) the student's own guess, (iii) each provider choosing.
- Keep it in the product only if it clearly beats (i) and (ii). Report the result either way.

**d) Training-label auditor (primary, M4).**
- Before training, the providers check the teacher's labels (intent and order) on the training set; disagreements are flagged for review or dropped.
- Compare against the teacher LLM (or a stronger LLM) doing the same audit.
- Report flag rate, precision on a hand-checked sample of flags, latency, and cost per 1,000 checks.
- Also measure catch rate with **planted mistakes** in training labels (the same planting code as the order checker, §11b), per error type.

**e) Menu narrowing (required, M7).**
- Before extraction, each provider answers yes/no per menu category ("Does this conversation involve burgers? pizza? drinks? sides?…"), and the extractor receives only the relevant sections. If an item can't be matched, retry with the full menu, so a miss costs time, not correctness.
- **Mega-menu condition:** combine the three menus into one food-court-style menu (~80–100 items); also run it on the PIZZA benchmark catalog.
- Narrowing methods compared: rules baseline (keyword match on category names), Julia-1, Jev, OpenAI Decisions.
- Test conversations must include **implicit category mentions** (synonyms like "pop"/"something fizzy", item names without category words, vague requests like "something sweet"); Source A cards include them (scenario tag `implicit_category`). Report narrowing accuracy separately for explicit vs. implicit mentions.
- **Training experiment (2B student only):** train (1) a single-menu student on per-restaurant conversations only and (2) a mixed student on the same data plus ~20% mega-menu conversations (teacher-labeled in M4). Test both on: single menu, mega menu full, and mega menu narrowed. Report whether big-menu training alone closes the gap and how much narrowing helps each version.
- Measure: prompt tokens, latency p50/p95, extraction accuracy, retry rate, and how often narrowing dropped a needed category.

### Architecture comparison (M7)

Compare on the test set:

| | Architecture |
|---|---|
| A | Router, then extractor (extractor only for order labels) |
| B | Extractor only (the student outputs intent + order for every message) |
| C | Router and extractor in parallel |

- **Method:** run the extractor once on every test message (this is B) and each router once on every test message, then compose A from those results. Time each component separately and compute composed latency; confirm with a small live run of each architecture.
- **Report:** routing accuracy, extraction accuracy, latency p50/p95 per message and per conversation, cost per 1,000 messages, the share of messages where the extractor was skipped, and the break-even router latency for the test set's message mix.

**Metrics (routing):** macro-F1, per-label precision/recall **with confidence intervals** (labels with few test examples are noisy, and the report says so), confusion matrix, secondary-label recall, `UNKNOWN` handling (abstain vs. confident wrong guess), stability across 3 repeated runs, sensitivity to option order, latency (p50/p95), cost per 1,000 messages.

Expected cost: cents for OpenAI Decisions; Jev depends on its input price (check before running). The teacher-LLM comparisons in roles a–e add API cost: estimate each before running and ask first if over $2.

## 12. Evaluation (all on the sealed test sets unless noted, reported per source)

- Every metric is reported separately for Source A (Claude-written test), Source B (PIZZA, items only), and Source C (Julian-written, if any), never only pooled.

- Order exact match (everything correct).
- Item-level F1: an item counts as correct only if menu item + quantity + size + modifications all match. Also per-component accuracy.
- Field accuracy: fulfillment, time, address components, payment.
- Correction handling accuracy on conversations with corrections or cancellations.
- Clarification detection: precision/recall of `missing_or_ambiguous`, plus a rubric rating of `clarification_question` (an LLM judge is allowed only if validated against Julian's ratings on 50 samples).
- Hallucination rate: items or values not supported by the conversation.
- Unverified-request fallback rate: how often the code had to ask "Just checking, we may not be able to do X…" because an output left a request with no menu id unclassified, or called something a kitchen note that the menu doesn't accept (`core/requests.request_counts`, logged per run).
- JSON validity rate.
- Generalization: results on the held-out menu reported separately.
- Cost per 1,000 orders and per successful workflow, including retries and fallbacks.
- Latency (p50/p95) and peak memory, on GPU and on CPU/Apple Silicon with the quantized model.
- Slices by writing style, business, and conversation length.
- `docs/ERROR_ANALYSIS.md` with categorized failures and examples.
- Per-label scores (router and intent) with confidence intervals; labels with few test examples are marked as noisy.
- **Every reported number must come from committed eval outputs. No fabricated or estimated results in tables.**

### Test-set contamination rule (October 8, 2026)
- If a test-set run reveals a problem that we then fix, those test results are reported as **"used for fixes"**, not as clean held-out results.
- The fix is measured on **fresh unseen data**: new PIZZA orders from the ~1,150 not yet sampled, or a newly generated Claude-written test batch (new scenario cards, written and reviewed the same way).
- Lessons from test failures are added to dev as new cases (never by copying test conversations).

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
| Decision-provider roles + teacher-LLM comparisons (M4 audit, M6/M7 checks) | Estimate before running; ask if > $2 |
| Training compute | $0 (free GPUs); ask before renting |
| Buffer | remainder |

- **Ask Julian before any single spend over $2**, and keep a running total in `docs/COSTS.md` from actual usage.
- Always run a priced pilot before a bulk job.
- Set spend caps on every provider account where possible.

## 15. AgentDesk reuse

Julian's earlier project, AgentDesk (https://github.com/Julian-Reyes/AgentDesk), is an English online-store agent-ops project. **It is written in TypeScript** (Node 24, Hono, Postgres/Drizzle, Zod, React + Vite). OrderSLM is Python, so reuse means **porting patterns and logic into Python**, not copying TypeScript files.

**Candidates to port** (verify each in Milestone 0; paths as of October 7, 2026):

| AgentDesk pattern | Path | Use in OrderSLM |
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
| Static results export for GitHub Pages | `server/src/static/export.ts` | Same approach for OrderSLM's results site |
| Working rules, pre-commit hook, PROGRESS.md style | `CLAUDE.md`, `.githooks/pre-commit` | Adapt for a Python toolchain |

**Frontend:** non-visual logic may be adapted (e.g. chat state handling, streaming/SSE client, comparison data shaping in `web/src/storefront/chat-state.ts`, `web/src/lib/sse.ts`, `web/src/ops/comparison.ts`). **Do not copy AgentDesk's styling, layout, or page designs** (`web/src/styles.css`, page components). OrderSLM's UI must look clearly different: its own colors, typography, and layout suited to a food-ordering product.

**Do not reuse:** the Larchgrove catalog, refund/coupon/goodwill policies, the multi-agent loop and handoffs (OrderSLM does extraction, not agents), or Postgres (JSON files or SQLite are enough).

**Spending note:** AgentDesk has its own provider spend caps (e.g. Gemini, Groq). Use separate API keys or projects for OrderSLM so its costs are tracked independently.

Record what was ported, from which path, and what changed in `docs/AGENTDESK_REUSE.md`. Do not modify AgentDesk. OrderSLM must run independently.

## 16. Demo (V1)

- **Chat simulator** (web): pick a business, type messages as the customer, watch the order update live next to the chat. The bot replies with a confirmation or a clarifying question, e.g.:
  > "Got it: 1 Cheeseburger, 1 Cheeseburger (no onions), 1 Sprite. Pickup at 7pm. Total $20.00, paying cash. Is that right?"
- **Answers to simple questions** (`MENU_QUESTION`, `DELIVERY_QUESTION`, `PAYMENT_QUESTION`; added October 13, 2026): templates filled from the menu only, never by a model. Delivery: available, fee, minimum (no delivery-area claims). Hours: opening and closing time. Payment: accepted methods. Menu: whether an item exists, its sizes and options (no dietary or allergen claims). Anything the menu can't answer: say so and offer staff. The answer comes first, then any clarifying question ("We deliver: $3.99 fee, $15 minimum. Would you like it delivered to …?"). Not annotated in gold and not scored.
- **Order ticket view** for the business: incoming orders and a simple status flow (new → preparing → ready).
- **Comparison view:** teacher vs. students on the same conversation, and the router providers' answers side by side, with cost and latency.
- Hosting: static or lightweight; never expose paid API keys publicly. Rate-limit anything public.

## 17. Deliverables

- Reproducible repo with a `Makefile`: `make menus`, `make annotate`, `make teacher-bakeoff`, `make synth`, `make label`, `make student-bakeoff`, `make train`, `make eval`, `make router-bench`, `make demo`.
- Hugging Face release: LoRA adapters + quantized models, model cards, the menus, and the Source A (and C, if written) evaluation sets. Never PIZZA data (CC-BY-NC, no redistribution).
- `REPORT.md`: problem, data strategy (synthetic training vs. evaluation Sources A/B/C, review correction rate), the four experiments with results tables and charts, error analysis, cost comparison, limitations.
- Tests: schema validation, deterministic pricing, menu matching, evidence checking, order-state logic, metrics.

## 18. Milestones (V1)

| # | Work | Acceptance evidence |
|---|---|---|
| 0 | AgentDesk inspection; repo layout; `SCHEMA.md`, `TAXONOMY.md`, `ARCHITECTURE.md`, `ANNOTATION_GUIDE.md`; provider/tool interfaces with mocks; `PROGRESS.md` | Versioned contracts, sample conversations, reuse doc with file paths, passing schema tests |
| 1 | Menus (3 + 1 held-out), pricing engine, order state logic, rules baselines (extraction + routing) | Deterministic tests pass; no model needed |
| 2 | Annotation tool; PIZZA conversion; scenario cards → Claude-written dev + test (Source A); Julian's review | Locked split with counts per source, label, menu, style and scenario; all dev + ≥25% of test reviewed, correction rate logged; 199 PIZZA cases |
| 3 | Teacher bake-off | Results table + accuracy-vs-cost chart; teacher chosen by the stated rule; actual cost logged |
| 4 | Synthetic generation: 200-conversation pilot → audit → 1–2k bulk, labeled by the winning teacher (order **and** router intents); ~20% mega-menu conversations for the mixed student; training-label audit by the decision providers (§11d) | Data audit, distribution log, drop rate, audit flag rate + precision, actual cost |
| 5 | Student bake-off (zero-shot, local) | License/tooling checks; results table; students chosen |
| 6 | LoRA training (student outputs intent + order); zero-shot vs. few-shot vs. fine-tuned vs. teacher on the test set; single-menu vs. mixed 2B student; order checker (§11b); error analysis | Reproducible training configs and eval outputs; intent accuracy |
| 7 | Decision providers: router benchmark + cross-check with the student's intent (§11a), order checker (b), item chooser pilot (c, optional), menu narrowing incl. mega menu (e); architecture comparison A/B/C | Verified API contracts, per-label metrics with CIs, stability, latency and cost results; disagreement log; break-even router latency |
| 8 | Demo (incl. template answers to menu/delivery/hours/payment questions, §16), report, Hugging Face release | Working demo; every number traceable to saved outputs |

**V2 candidates (separate plan later):** food scheduling (slots, capacity, rescheduling); Brazilian Portuguese (new data and test set, transfer experiment); appointment-based business domain; inventory, promotions, and full returns workflows; live WhatsApp integration; automatic payment verification (e.g. a Pix provider's payment notification marks the order paid; until then a customer's "I already paid" stays an unverified claim on the ticket); fine-tuning Julia-1 on teacher-labeled router data, reported separately as "off-the-shelf vs. fine-tuned" (first check that a fine-tuning path exists, §11).

## 19. Working rules

- One milestone per instruction. After each: update `PROGRESS.md`, run tests, commit.
- Ask before spending over $2, adding major dependencies, or downloading large models.
- Verify provider and model contracts, licenses, and prices against primary sources before integrating. Do not invent APIs, capabilities, confidence values, or results.
- Keep the sealed test set isolated. Log provider, model version, prompt version, and data version for every run.
- Test results that led to a fix are reported as "used for fixes"; the fix is measured on fresh unseen data (§12).
