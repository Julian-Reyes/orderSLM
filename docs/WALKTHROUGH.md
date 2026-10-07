# OrderSLM walkthrough (for learning the project)

Written 2026-10-07, after Milestone 2's tooling and the Source A scenario cards, before any evaluation
conversations exist. Nothing here is a result: **no model has been run or scored yet**. Where this page shows
output, it is real output from running the code on a sample conversation, not a measurement.

Contents: 1 Big picture · 2 Milestones so far · 3 Repo map · 4 One order traced through the code ·
5 Glossary · 6 Commands to try · 7 Ten questions (answers at the end)

---

## 1. Big picture

**The problem.** Small food businesses take orders by chat, and customers write like this:

> hi / large pizza half pepperoni half hawaiian / and garlic knots / actually make it 2 garlic knots /
> delivery to 18 Elm Street apt 3B, ring the side door / card

A person reads that and knows the order. Software has to turn it into something exact: *one large
half-pepperoni/half-Hawaiian pizza, two garlic knots, delivery to 18 Elm Street apt 3B, card*. It also
has to notice what's still missing ("pickup or delivery?") and ask one clear question.

**What OrderSLM does.** It splits the job in two, on purpose:

- **Models do the fuzzy part.** A *router* decides what each message is about (placing an order, asking where
  the food is, complaining, chit-chat...). An *extractor* reads the conversation and proposes the order as
  structured JSON, quoting the exact words each item came from (*evidence*).
- **Plain code does everything that must be exact.** Checking ids against the menu, prices, totals, delivery
  fees, what's missing, order status rules and the reply text. **A model never produces a price.** The model's
  output format doesn't even have a price field, so a model that invents one fails validation.

**Why it's an ML project.** The interesting question is *which model should do the fuzzy part, and how cheap
can it get?* The plan answers that with four experiments, each saved and reproducible:

| # | Experiment | Question | Milestone |
|---|---|---|---|
| 1 | Teacher bake-off | Which cheap hosted model (`gpt-6-luna`, `gemini-3.1-flash-lite`, `deepseek-flash`, optional `gemini-3.8-flash`) extracts orders best per dollar? The winner becomes the **teacher**. Rule: cheapest model within 3 points of the best item-level F1. | M3 |
| 2 | Student bake-off | Which small open model (Qwen3.5-0.8B / 2B, Qwen3-1.7B, Gemma 4 E2B) is the best starting point, zero-shot, on a laptop? | M5 |
| 3 | Distillation | The teacher labels 1–2k synthetic conversations; the student is LoRA-fine-tuned on them. How close does it get to the teacher, and what does it save (cost, speed, memory, privacy)? | M4, M6 |
| 4 | Router benchmark | Which decision provider (keyword rules, Julia-1, Jev, OpenAI Decisions) best labels what the customer wants? | M7 |

Then M8 is a demo (chat simulator + kitchen ticket) and a report. The guiding rule: **every number in the final
report comes from a saved run in `runs/`**, and nothing is estimated or invented.

**Evaluation data** (changed in M2, see §2): models are judged on conversations kept apart from training data,
from three sources reported separately. A = conversations Claude writes from *scenario cards*, reviewed by
Julian. B = 199 real human-written orders from the public PIZZA dataset. C = optionally, ~30 written by Julian.

---

## 2. Milestone by milestone

### Milestone 0: foundations (commits `093f9cf`, `93804d5`)

**Built:** the *contracts* (Pydantic models for every piece of data), the docs that explain them, interfaces
for the swappable parts with fake implementations for tests, 10 hand-written sample conversations, and the
test suite.

**Why first:** everything later (models, metrics, the tool) has to agree on one exact data format. Writing the
format and its tests before any model code means a model's output can be checked automatically from day one.

**Key decisions and trade-offs:**
- **AgentDesk reuse, as patterns only.** Julian's earlier project AgentDesk is TypeScript; OrderSLM is Python. It
  was inspected read-only (commit `c24529c`), and its ideas were *ported*: integer-cent money, an injected clock,
  `ToolOk | ToolErr` results, scripted fake providers. No visual design was copied (docs/AGENTDESK_REUSE.md).
- **Snapshot, not diff.** The model outputs the *whole order as it stands now*. Code computes what changed
  (`core/diff.py`). Snapshots are easier for a small model to get right and easier to score.
- **Unknown ≠ absent ≠ not applicable.** Fields carry a state (`provided`, `ambiguous`, `not_mentioned`,
  `not_applicable`), so "no address yet" and "no address needed (pickup)" are different.
- **Language-neutral codes.** Labels and ids are codes like `PLACE_ORDER`; only the customer's text and reply
  templates are English, so Portuguese can be added in V2 without changing the schema.
- Julian's answers to the M0 questions (recorded in PROGRESS.md): snapshot output approved; customer name
  optional except at one business; samples may be few-shot examples but never evaluated; the test set is sealed
  in code; frontend = Vite + Preact + TypeScript.

### The rename (commit `1f2cf81`)

The project started as **ShopRoute**; Julian renamed it **OrderSLM** ("SLM" = small language model). Code,
docs, env var (`ORDERSLM_UNSEAL_TEST`) and spec file were renamed; the local folder was renamed by Julian.

### Milestone 1: the deterministic core (commit `6f21b20` + fixes)

**Built:** real menus, the pricing engine, the missing-info rules, order state rules, reply templates, menu
matching, and two **rules baselines** (a regex extractor and a keyword router) that need no model at all.

**Why:** the spec says "deterministic tests pass; no model needed". This is the half of the system that must be
exactly right, and it's what every model's output gets checked against. The baselines give a floor: any model
has to beat simple rules to be worth its cost.

**Key decisions and trade-offs:**
- **Four menus.** Corner Patty (burgers, a combo), Halfmoon Pizza (half-and-half), Morning Crumb Café (pickup
  only; name required for pickup), and **Lucky Lime Taqueria, held out**: used only in test conversations, to
  see whether models handle a business they've never seen. Opening hours were chosen so "at 7" means 7 pm at the
  burger shop and 7 am at the café.
- **Pricing rules** (docs/PRICING.md, approved by Julian): half-and-half costs the dearer half plus half-price
  toppings rounded up; "extra" on an included ingredient costs one more portion; combo choices are included but
  upsizing costs the difference; no delivery fee while fulfillment is unknown.
- **Contract changes for real-world orders:** `extraction@0.2` added `amount` (normal/extra/light, for "extra
  cheese", "light on the sauce"); `menu@0.3` described modifiers as ingredients and add-ons per item, plus
  exclusive groups (one crust, one milk).
- **The menu split and the history rewrite (M1 review).** The first Halfmoon menu copied the PIZZA dataset's whole
  vocabulary (85 toppings, 23 styles, 22 drinks) plus an entity map file. PIZZA is licensed CC-BY-NC-4.0 (no
  redistribution), so Julian asked that **nothing derived from it ever be committed**. Because nothing had been
  pushed yet, the M1 commit was *rewritten*: Halfmoon became a realistic pizzeria (8 pizzas, 5 sizes, 23
  toppings, 4 crusts, 6 drinks), and a separate **PIZZA benchmark catalog** became something a script generates
  locally in M2. Trade-off: a little extra work, but the repo can be public without license risk.
- **A real bug found by that change** (commit `87d4964`): the pricing engine crashed on an unknown modifier id
  instead of returning an error. Found because a test used a topping (pesto) that the trimmed menu no longer
  had. Now fixed, with regression tests: a model inventing an id gets a `ToolErr`, never a crash.
- **Before the first push:** a full-history secrets scan, `.env.*` added to `.gitignore` (commit `339df0c`), and
  every commit's email rewritten to Julian's GitHub no-reply address. Only `main` lives on GitHub.

### Milestone 2: evaluation data tooling (commits `a5b9599` … `da84d27`)

**Built:**
1. **PIZZA benchmark script** (`make pizza`): downloads the PIZZA test split pinned to one dataset commit,
   samples 200 orders with a fixed seed (never filtered to fit a menu), builds the benchmark catalog from what
   those orders mention plus distractor items (35 toppings), and converts each order into a gold answer.
   **199 of 200 convert**; one is reported, not guessed. All of it stays in the gitignored `data/external/`.
2. **Split tooling** (`data/splits.py`): save/load conversations with validation, counts, near-duplicate
   detection, a review log, and the *lock* that seals the test set.
3. **The annotation tool** (`make annotate`): a FastAPI backend plus a Vite/Preact web page for editing a
   conversation and its gold labels. It re-checks everything on each edit and shows the price the code computes.
4. **Scenario cards** (`data/cards.py`): 80 dev + 170 test cards, the recipe for Source A.

**Key decisions and trade-offs:**
- **PIZZA handling.** PIZZA gives two parses per order: EXR (canonical values) and TOP (which words meant what).
  The converter takes values from EXR and evidence quotes from TOP, and requires the two to agree. Where a
  customer's word isn't in PIZZA's own word list ("bell peppers", "more cheese"), the value comes from EXR.
  "No extra cheese" means the default amount, so it creates no change (15 cases). Drink sizes stay separate
  options (`large`, `can`, `2_liter`...) so nothing is lost. All three choices were approved by Julian. PIZZA is
  scored on items only, because it never mentions delivery, payment, and so on.
- **Speed-first evaluation data (the big change).** The original plan had Julian hand-write ~280 test
  conversations and relabel 30 a week later. That was too slow, so the plan changed (spec §7):
  - **Source A**: Claude writes ~250 conversations (dev ~80, test ~170) from scenario cards, with gold labels.
    Julian reviews all of dev and at least 25% of test; every review is logged, and the **correction rate** is
    reported.
  - **Source B**: the 199 PIZZA cases are the external, human-written test set.
  - **Source C** (optional): ~30 Julian-written conversations, the only ones a blind relabel would apply to.
  - **Every result is reported per source.** Trade-off, stated in the spec as a limitation: Source A has a
    single author, so it may favor models whose phrasing is similar. Sources B and C are the check on that.
  - Source A is **evaluation-only**: never used as training input (now also in CLAUDE.md).
- **Splitting by card.** Each card is written once, and cards are assigned to dev or test before any writing,
  so a test conversation can't be a rewrite of a dev one. Lock time also checks text similarity across splits.
- **Coverage by construction.** Cards come from fixed quotas per *situation* (23 of them, e.g.
  `correction_after_confirmation`, `refund_request`), so every router label, menu, style and tricky case is
  guaranteed to appear in both splits. Tests enforce this.

**Where M2 stands:** tooling merged to `main`; cards committed on branch `m2-eval-data`; conversations not
written yet; nothing locked.

---

## 3. Repo map

| Path | What it does | Milestone |
|---|---|---|
| `orderslm-project-plan.md` | The spec. Authoritative; §7 rewritten in M2 | 0 (M2 edit) |
| `PROGRESS.md` | Status, decisions, open questions; read first each session | 0, updated each milestone |
| `CLAUDE.md` | Working rules and non-negotiables for Claude | 0 |
| `Makefile` | All commands (§6). Unbuilt milestones fail loudly | 0, 1, 2 |
| `.githooks/pre-commit` | Runs lint + tests before every commit | 0 |
| `src/orderslm/schema/` | **The contracts.** `extraction.py` (the model's proposal: items, fulfillment, evidence, missing info), `routing.py` (15 labels + descriptions), `conversation.py`, `annotation.py` (gold format), `menu.py`, `order.py` (verified results: `Quote`, `ToolOk/ToolErr`), `common.py` (version numbers) | 0, extended 1–2 |
| `src/orderslm/domain/` | `money.py` (integer cents), `clock.py` (injected "now") | 0 |
| `src/orderslm/interfaces/` | The swappable parts as Protocols: `OrderExtractor`, `DecisionProvider`, `PricingEngine`, `BusinessTools` | 0 |
| `src/orderslm/mocks/` | Fakes for tests: scripted extractor/router, in-memory order lookup | 0 |
| `src/orderslm/checks.py` | Grounding checks: does each evidence quote exist in that message? Is each id on the menu and allowed? | 0, 1 |
| `src/orderslm/router.py` | Builds the identical request every router provider gets | 0, 1 |
| `src/orderslm/menus.py` | Loads menus; hides the held-out one unless asked | 1 |
| `src/orderslm/core/` | **The deterministic core:** `matching.py`, `pricing.py`, `missing.py`, `diff.py`, `state.py`, `replies.py` | 1 |
| `src/orderslm/baselines/` | `rules_extractor.py` (`RulesExtractor`), `rules_router.py` (`KeywordDecisionProvider`) | 1 |
| `src/orderslm/data/pizza.py`, `sexp.py` | PIZZA download, sampling, benchmark catalog, conversion | 2 |
| `src/orderslm/data/splits.py` | Dev/test storage, validation, review log, lock, verify | 2 |
| `src/orderslm/data/cards.py` | Scenario-card generator for Source A | 2 |
| `src/orderslm/app/main.py` | FastAPI backend for the annotation tool | 2 |
| `src/orderslm/paths.py` | Where data lives + the **seal** on the test split | 0, 2 |
| `web/` | The annotation tool's web page (Vite + Preact + TypeScript) | 2 |
| `data/menus/` | The three business menus; `held_out/lucky-lime.json` | 1 |
| `data/samples/conversations/` | 12 worked examples (`split: sample`, never evaluated) | 0, 1 |
| `data/dev/cards.jsonl`, `data/test/cards.jsonl` | Scenario cards (the test ones are sealed) | 2 |
| `data/external/` | Gitignored: PIZZA files and everything derived from them | 2 |
| `docs/SCHEMA.md`, `TAXONOMY.md` | The output format and the router labels, explained | 0 |
| `docs/ANNOTATION_GUIDE.md` | How to label gold: what counts as missing, corrections, "yes" | 0 |
| `docs/ARCHITECTURE.md` | Components, folder layout, planned commands, visual design | 0 |
| `docs/AGENTDESK_REUSE.md` | What was ported from AgentDesk | 0 |
| `docs/COSTS.md` | Actual spend (still $0) | 0 |
| `docs/PRICING.md`, `MENUS.md` | Pricing rules; the menus and why they're shaped that way | 1 |
| `docs/PIZZA.md`, `SPLITS.md` | The PIZZA benchmark; sources, cards, review, lock | 2 |
| `tests/` | ~286 tests, one file per area (`test_pricing.py`, `test_pizza.py`, `test_splits.py`, ...) | 0–2 |

---

## 4. One order traced through the code

The conversation is `data/samples/conversations/sample-005.json` (Halfmoon Pizza), six customer messages:

```
#0 hi
#1 large pizza half pepperoni half hawaiian
#2 and garlic knots
#3 actually make it 2 garlic knots          ← the correction
#4 delivery to 18 Elm Street apt 3B, ring the side door
#5 card
```

No model exists yet, so the extractor here is the **rules baseline**. A trained model would take its place
at step 2 and produce the same kind of JSON. Every step after that is identical, and that's the point of the design.

**Step 0: the data is schema-checked.** `AnnotatedConversation.model_validate_json(...)`
(`schema/annotation.py`) loads the file. `Conversation` (`schema/conversation.py`) checks that message indices
run 0..5 in order and timestamps are timezone-aware and increasing. Unknown fields are an error everywhere
(`Strict`, `extra="forbid"`, `schema/common.py`).

**Step 1: routing (what is each message about?).** `router.build_router_request(RouterContext(...))` builds the
request every provider gets: the label descriptions from `schema/routing.py`, and the conversation rendered by
`router.render_input`:

```
Order in progress: yes.
Placed order exists: no.
Earlier messages:
customer: hi
...
Latest customer message: card
```

`KeywordDecisionProvider.decide` (`baselines/rules_router.py`) answers from keywords. On this conversation it
labels #0 `SMALL_TALK`, #3 `MODIFY_ORDER` and #4–#5 `PLACE_ORDER`, matching the gold. It labels #1 and #2
`UNKNOWN`, while the gold says `PLACE_ORDER`: a keyword router doesn't know "hawaiian" is a pizza. (That's one
example, not a score, and it's exactly why Experiment 4 compares smarter routers.)

**Step 2: menu matching.** The extractor needs to find menu words in messy text. `MenuLexicon(menu).find(text)`
(`core/matching.py`) does longest-match lookup over item names, aliases, variants and modifiers, tolerant of
plurals and typos, and keeps the character positions (spans) so evidence can quote the exact words. On message #1 it finds:

```
variant  'large'     (0–5)    → the 'large' size of each pizza
item     'pizza'     (6–11)   → cheese_pizza
item     'pepperoni' (17–26)  → pepperoni_pizza   (and the pepperoni topping)
item     'hawaiian'  (32–40)  → hawaiian_pizza
```

**Step 3: extraction, one snapshot per message.** `extract_rules(menu, messages)`
(`baselines/rules_extractor.py`, wrapped by `RulesExtractor.extract`) outputs an `ExtractionOutput`
(`schema/extraction.py`): the whole order so far. Running it after each message and comparing snapshots with
`diff_orders(previous, current)` (`core/diff.py`) gives the patch the business would see:

| After | Items | Patch | Missing (`required_missing`) |
|---|---|---|---|
| #0 | none | none | items, fulfillment_method, payment_method |
| #1 | L1 half pepperoni/half hawaiian, large, ×1 | `lines_added: [L1]` | fulfillment_method, payment_method |
| #2 | + L2 garlic_knots ×1 | `lines_added: [L2]` | same |
| #3 | L2 → ×2 | `lines_changed: [{L2, fields: [quantity]}]` | same |
| #4 | unchanged | `fields_changed: [fulfillment.method, address]` | payment_method |
| #5 | unchanged | `fields_changed: [payment]` | none |

Look at row #3: the correction **changes** line L2 rather than adding a third line. That's the behavior the
annotation guide requires ("corrections replace, not add") and one of the main things the experiments measure.

Each item carries evidence, e.g. L1: `{"message_index": 1, "quote": "large pizza half pepperoni half hawaiian"}`.
`check_all(output, conversation, menu)` (`checks.py`) confirms every quote really appears in that message and
every id exists and is allowed. It returned no issues here.

**Step 4: missing-info rules.** `required_missing(output, menu)` (`core/missing.py`) is the annotation guide's
"what counts as missing" written as code: no items, a size not stated where there's no default, an unclear
quantity, unknown fulfillment, delivery without an address, no payment method, and pickup without a name at a
business that requires one. The "Missing" column above is its output. When something is missing,
`replies.template_question(missing, output, menu)` (`core/replies.py`) writes **one** question covering all of it:

```
after #0: What would you like to order, is this for pickup or delivery, and will you pay by card or cash?
after #4: Will you pay by card or cash?
```

**Step 5: pricing.** `DeterministicPricing().quote(menu, output)` (`core/pricing.py`) first runs
`check_catalog`, then prices each line with `_price_line`, and returns `ToolOk[Quote]` (or a `ToolErr` listing
every problem). For this order:

```
L1  Pizza, Large 14-inch: half Pepperoni / half Hawaiian   1 × $18.99 = $18.99
    (the dearer half: Hawaiian $14.99 + large $4.00)
L2  Garlic Knots                                           2 × $5.99  = $11.98
subtotal $30.97 + delivery fee $2.99 = total $33.96
verified_by "pricing@0.1", menu_version "halfmoon-pizza@fccb086de25f"
```

`Quote` (`schema/order.py`) re-checks its own arithmetic (unit × quantity = line total; lines + fee = total), so a
wrong total can't even be constructed.

**Step 6: state and reply.** `state.ready_for_confirmation(output, menu, quote)` (`core/state.py`) is `True`:
nothing is missing and the quote is OK. `replies.summary(menu, quote, output)` builds the confirmation message from the
**verified quote**, never from model text:

```
Got it: 1 Pizza (Large 14-inch, half Pepperoni, half Hawaiian), 2 Garlic Knots. Delivery to 18 Elm Street
apt 3B as soon as possible. Total $33.96 (incl. $2.99 delivery), paying by card. Is that right?
```

If the customer then says "yes", `state.event_from_turn` only counts it as a confirmation because a summary
was just sent and nothing changed (a context-dependent "yes").

**Comparing with gold.** The sample's gold answer has the same items as the rules baseline. But gold also records
the note "ring the side door", and the rules baseline missed it. Small misses like this are why a model is
needed, and why the metrics look at fields as well as items.

---

## 5. Glossary

| Term | Meaning here |
|---|---|
| **Gold / gold label** | The correct answer for a conversation, written by the annotator: `gold_extraction` (the order) and `gold_routing` (a label per customer message). Models are scored against it. |
| **Proposal vs. verified result** | What a model says (`schema/extraction.py`, untrusted) vs. what code computed and checked (`schema/order.py`: `Quote`, tool results). Replies only state verified facts. |
| **Evidence** | `{message_index, quote}`: the exact words an item or field came from. Checked automatically (`checks.check_evidence`). |
| **Grounding / grounded** | Every value is backed by evidence that really exists in the conversation, and every id is on the menu. |
| **Snapshot / patch** | The model outputs the full current order (snapshot); `diff_orders` computes what changed (patch). |
| **Slot state** | `provided` / `ambiguous` / `not_mentioned` / `not_applicable`, so "unknown" and "doesn't apply" stay different. |
| **Missing info** | `missing_or_ambiguous`: what must be clarified before confirming, defined by rules in `core/missing.py`. |
| **Router / label** | Decides what a message is about, one of 15 labels (`PLACE_ORDER`, `ORDER_STATUS`, `UNKNOWN`, ...), with an optional secondary label, urgency and context flags. |
| **Extractor** | Turns a conversation into an `ExtractionOutput`. The teacher and the students are both extractors. |
| **Teacher / student / distillation** | Teacher = a big hosted model that labels training data. Student = a small local model trained (LoRA) on those labels. Distillation = that training, measured against the teacher. |
| **LoRA** | A cheap way to fine-tune: train small add-on matrices instead of the whole model. |
| **Baseline (rules baseline)** | A no-model solution (regex + keyword rules). It sets the floor a model must beat. |
| **Dev split** | Data used while building: prompt tuning, bake-offs. Allowed to look at. |
| **Test split** | Data used only for final results. |
| **Sealed** | The test split is reachable only through `paths.test_split_dir()`, which refuses unless `ORDERSLM_UNSEAL_TEST=<reason>` is set. A test checks that only allowed modules mention it. |
| **Locked** | `make lock-test` records a hash of every test file and the counts. After that, any gold change needs a logged reason, and `verify` catches unlogged edits. |
| **Held-out menu** | Lucky Lime Taqueria: appears only in test, to measure how models handle an unseen business. `load_menus()` hides it by default. |
| **Sample split** | The 12 worked examples in `data/samples/`. May be few-shot examples in prompts; never evaluated. |
| **Source A / B / C** | Evaluation sources: A = Claude-written from cards (reviewed), B = PIZZA (human-written, external), C = optional Julian-written. Results are reported per source. |
| **Scenario card** | A recipe for one Source A conversation: business, situation, labels it must contain, style, features, persona, brief. |
| **Correction rate** | Share of reviewed Source A conversations that Julian had to change. A quality measure for Claude-written gold. |
| **Near-duplicate** | Two conversations whose customer words overlap ≥ 80% (token-set Jaccard). Blocked across splits. |
| **PIZZA, EXR, TOP** | PIZZA = Amazon's public pizza-order dataset (CC-BY-NC-4.0). EXR = its canonical parse ("what was ordered"); TOP = its word-level parse ("which words meant it"). |
| **Benchmark catalog** | The menu generated for PIZZA evaluation only (in `data/external/`), separate from Halfmoon. |
| **Contract / version** | A Pydantic model that is part of the interface (e.g. `extraction@0.2`, `conversation@0.3`). Bumped whenever the shape changes; every run logs it. |
| **`ToolOk` / `ToolErr`** | How tools return results: business outcomes ("size missing") are values, never exceptions. |
| **Cents** | All money is integer cents (`domain/money.py`), so there are no floating-point rounding errors. |
| **Injected clock** | Code gets "now" from a `Clock` argument, so tests can fix the time. |
| **Item-level F1** | The main extraction metric (M3): an item counts only if menu item, quantity, size and modifications all match. |
| **Bake-off** | A side-by-side comparison of candidates on the same data with the same prompt. |

---

## 6. Commands to try

Run these from the repo root. None of them spends money or calls a model.

| Command | What you'll see / what to look for |
|---|---|
| `make check` | Ruff lint + format check, then ~286 tests. Everything should pass. The one warning (Starlette suggesting `httpx2`) is known and accepted. |
| `uv run pytest tests/test_pricing.py -vv` | Each pricing rule as a named test (`-vv` because the config adds `-q`), e.g. `test_half_and_half_costs_the_dearer_half_plus_half_priced_toppings`. The test names read as the spec. |
| `make menus` | Each menu validated, with its content hash (`halfmoon-pizza@fccb086de25f`) and item/variant/modifier counts. Lucky Lime is marked HELD OUT. |
| `make annotate`, then open http://127.0.0.1:8765 | The annotation tool. Click **New conversation**, type a message, select some words to make evidence, use **+ item line**, and watch the check panel: findings, "rules say missing", and the computed quote. `?open=<id>` opens one directly. |
| `make pizza` | Downloads PIZZA into `data/external/pizza/` and rebuilds the benchmark. It prints counts (`toppings used=29 distractors=6 menu=35`, `converted 199`). Then open `data/external/pizza/benchmark/report.json` for the drink-size examples and the failure. Run `git status`: nothing new should appear, because it's gitignored. |
| `uv run python -m orderslm.data.cards summary --split dev` | Dev card counts per label, menu, style, feature and tricky case. Adding `--split test` fails with a `SealedSplitError` traceback; that's the seal working. |
| `uv run python -m orderslm.data.splits stats dev` | Split counts (zero until conversations are written). |
| `ORDERSLM_UNSEAL_TEST="read cards" uv run python -m orderslm.data.cards summary` | Both splits' card counts, with the seal deliberately opened. |
| `uv run python -c "from orderslm.paths import test_split_dir; test_split_dir()"` | Raises `SealedSplitError`: the seal in one line. |
| `git log --oneline` | The history from §2. |

To trace an order yourself, adapt §4: load `sample-005.json`, call `extract_rules(menu, messages[:k])` for
k = 1..6, and print `diff_orders`, `required_missing` and `DeterministicPricing().quote`.

---

## 7. Ten questions

1. Why does a model never output a price, and what stops it from doing so anyway?
2. What's the difference between `schema/extraction.py` and `schema/order.py`?
3. The customer writes "actually make it 2 garlic knots". What should happen to the order, and which function shows the business what changed?
4. What is the held-out menu for, and how does the code keep it out of dev and training?
5. What does "sealed" mean in practice? What would you have to do to read the test cards?
6. Why was the M1 commit rewritten, and why was that safe to do then but not now?
7. How is a PIZZA order turned into a gold answer, and why is PIZZA scored on items only?
8. What are Sources A, B and C, and why must results be reported per source?
9. Why are dev and test split by scenario card, and what else guards against overlap?
10. In the traced example, what did the rules baseline get right, and what did it miss (extraction and routing)?

### Answers

1. Prices must be exact and auditable, and models make arithmetic and lookup mistakes. The extraction schema has
   **no price fields** and every contract forbids unknown fields (`extra="forbid"`), so a model that adds
   `"price": 12` fails validation. Prices come only from `DeterministicPricing` and the menu.
2. `extraction.py` is the **model's proposal** (untrusted: items, fields, evidence, missing info).
   `order.py` holds **verified results** computed by code: `Quote` (with self-checking arithmetic),
   `OrderRecord`, `ToolOk`/`ToolErr`. The reply layer may state only verified facts.
3. The existing garlic-knots line (L2) changes quantity from 1 to 2. No new line is added, because corrections
   replace. `core/diff.diff_orders` reports it as `lines_changed: [{L2, fields: [quantity]}]`.
4. To measure generalization to a business no model has seen. `load_menus()` excludes it unless called with
   `include_held_out=True`; `splits.validate` blocks it outside test; cards put it only in test; and a guard test
   allows `include_held_out=True` only in a few named modules.
5. Test data is reachable only via `paths.test_split_dir()`, which raises `SealedSplitError` unless
   `ORDERSLM_UNSEAL_TEST` is set to a reason. To read the test cards you'd run e.g.
   `ORDERSLM_UNSEAL_TEST="read cards" uv run python -m orderslm.data.cards summary`. That's appropriate for
   authoring or final eval, never for tuning or training.
6. It contained PIZZA-derived files (an entity map and a menu copied from PIZZA's catalogs), and PIZZA's
   CC-BY-NC license forbids redistribution. Rewriting was safe because **nothing had been pushed**, so no one else
   had the old commits. Now `main` is on GitHub, and rewriting it would break other clones and wouldn't remove
   copies already pulled.
7. `data/pizza.py` reads both parses: values from EXR, the customer's words from TOP for evidence. They must agree.
   It builds an `ExtractionOutput` against the benchmark catalog and fills missing info with the same rules
   (`core/missing.py`). PIZZA orders never mention delivery, payment, time or name, so those fields are only
   rule-filled defaults. Scoring them would measure our rules, not the model.
8. A = Claude-written from cards, reviewed by Julian (dev ~80, test ~170). B = the 199 PIZZA orders,
   human-written. C = optional ~30 Julian-written. Per-source reporting matters because A has one author whose style
   models might favor; B and C show whether results hold on human writing. Pooling would hide that.
9. If one situation instance were written once for dev and once for test, test would partly measure memorized
   dev examples. Cards are assigned to a split *before* writing, one conversation per card. The lock also blocks
   any test conversation whose customer text is ≥ 80% similar to another test or dev conversation.
10. Extraction: it got all items exactly right, including the half-and-half pizza, the size, and the quantity
    correction (1 → 2 garlic knots). It also got delivery, the address and card payment, but missed the note
    "ring the side door". Routing: it labeled "hi", the correction and the delivery/payment messages correctly,
    but called the two item messages `UNKNOWN` instead of `PLACE_ORDER`.
