# Progress

Read this first each session. Spec: `orderslm-project-plan.md` (authoritative; replaces the Pedido Fácil plan).

_Last updated 2026-10-16._

## Start here next session

- **State:** M0–M3 done and merged into local `main` (**not pushed**: ask Julian first, run a secrets check).
  M4 step 1 (code, no spend) done on branch `milestone-4`; see "M4 so far".
- **Next: M4 step 2**, the priced mini-pilot: re-verify the four prices on the official pages, then
  `make synth ARGS="generate --batch p1 --limit 5 --yes"` (15 chats, est. $0.02) and
  `make label ARGS="--batch p1 --limit 5 --yes"` (est. $0.04). Read the chats and labels, then re-project the full
  500 from measured tokens; ask Julian if it is over $2. Then step 3: the full pilot, the analysis, Julian's audit.
- Still open before **bulk** labeling (not needed for the pilot):
  1. Check whether OpenAI bills `cache_write_tokens`; plan the OpenAI Batch API (half price) for bulk labeling.
  2. `docs/TERMS.md`: each provider's terms on training with outputs (spec §7). Now this covers DeepSeek, Google
     and Anthropic as generators as well as OpenAI as teacher.
  3. Per-prefix training rows (the intent at every customer turn plus the order at that point): decide after the
     pilot how to label the order at earlier turns.
  4. Mega-menu cards (~20% for the mixed student, spec §11e) are not planned yet.
- **Case study:** every experiment records all numbers per model/setting (accuracy counts, tokens, run cost and per
  1,000, latency, before/after views) in `runs/<experiment>/` + a summary/chart-data JSON (Julian, 2026-10-15).

## Milestones

| # | Work | Status |
|---|---|---|
| 0 | AgentDesk inspection, layout, contracts, docs, interfaces + mocks, samples, tests | ✅ Done 2026-10-07 |
| 1 | Menus (3 + held-out), pricing engine, order state, rules baselines | ✅ Done 2026-10-07 |
| 2 | Annotation tool; PIZZA conversion; scenario cards → Claude-written dev/test (Source A); Julian's review; lock | ✅ Done 2026-10-14: dev 91/91 reviewed, test 58/199 reviewed (0 changed), test split locked (199, sha256 `3f09234131e3825d`); see "Test review and lock" |
| 3 | Teacher bake-off | ✅ Done 2026-10-15 (merged to main, not pushed): **teacher `openai/gpt-6-luna@low`**, prompt `teacher-extract@0.4`, code rules `core/finalize`; write-up `docs/TEACHER_BAKEOFF.md`; spend $0.96; details in "M3 so far" |
| 4 | Synthetic generation + labeling (order + intents; mega-menu share; label audit) | In progress: step 1 (contract, cards, prompts, checks, CLI) done 2026-10-16; no spend yet |
| 5 | Student bake-off | Not started |
| 6 | LoRA training (intent + order) + distillation eval; order checker | Not started |
| 7 | Decision providers (router + cross-check, checker, narrowing, item chooser) + architecture comparison | Not started |
| 8 | Demo, report, Hugging Face release | Not started |

**Spend to date: $0.8011** (docs/COSTS.md): M3 smoke tests, teacher bake-off pilot, second bake-off, head-to-head. No model downloads,
training or deployment so far.
No results exist yet: the rules baselines have **not** been scored on anything (no dev/test set exists).

## M4 so far (2026-10-16)

- **Julian's decisions (2026-10-16):** pilot = **DeepSeek flash 200, Gemini flash-lite 200, Haiku 5.5 lowest 100**,
  decide the rest after the analysis (recorded in spec §7). The writer is kept different from the teacher and from
  Source A's author because a model reads its own text the way it meant it (its label errors line up with its
  writing), and because training on Claude-style chats could inflate Source A scores. Haiku is the measured
  exception: results are reported per generator. Contract: **drop the missing list and question from model output,
  keep ambiguity flags**. Intents: **per customer message, one call per chat**. Estimate given before starting:
  about $1.2–1.7 (upper bound).
- **Contract** `label@0.1` / `student@0.1` (`schema/label.py`, docs/SCHEMA.md): `ModelOrder` = order facts + 2
  ambiguity flags; `TeacherLabel` = intents per customer message + order; `StudentOutput` = latest intent + order.
  `ExtractionOutput` is unchanged (`extraction@0.4`). `core.finalize.finalize_order` builds the finalized order.
  Tested: every dev gold → label contract → finalize gives back gold's missing list and decision.
- **Cards** (`synth/cards.py`, `synth-cards@0.1`): seeded plan from 24 scenarios (≈78% build an order, 22% the
  non-order intents), 5 styles, 24 personas written for this (none from Source A), 3 training menus (never the
  held-out one). Each card names the final order (menu ids, sizes, removals, add-ons, swaps, combo picks, half-and-
  half, off-menu dish) so the label can be checked against it. Generators assigned in scenario order: exactly
  200/200/100. Batch `p1` planned: `runs/synth/p1/cards.jsonl` + `plan.json` (distribution).
- **Generator** (`synth/generate.py`, prompt `synth-write@0.1`): menu without prices or ids, card in words; code adds
  indices and seeded timestamps. Drops: invalid JSON, last message not the customer's, a business message with a
  price. Dedup (`synth/dedup.py`): customer-text word 3-gram Jaccard ≥ 0.8 within the batch and against dev.
- **Labels** (`synth/label.py`, prompt `teacher-label@0.1` = v0.4 minus the missing list and question, plus flags and
  intents with the label descriptions from `LABEL_DESCRIPTIONS`): drops for contract errors, intents not covering
  each customer message, finalize errors, failed grounding checks, evidence citing a business message. **Card
  agreement** (items, item details, expected labels, decision) is flagged for the audit, not dropped.
- **CLI** `make synth` / `make label` (`synth/run.py`): estimate first, $2 guard, `--max-cost`, record/replay cache,
  `calls/<time>-<stage>.json` per live stage, `report` → `summary.json` per generator (kept/drops, labels/drops,
  card agreement, tokens, cost per 1k, latency).
- **Estimates for the full p1 pilot** (chars/3, peak price, no caching): generation $0.76 (DeepSeek $0.33,
  Gemini $0.36, Haiku $0.07); labeling ~$1.20 (luna `low`, $0.0024/chat). M3's measured luna cost was $0.57–0.63
  per 1,000 with caching, so expect less. Total ≤ ~$1.96.

## M3 so far (2026-10-15)

- **Accounts:** OrderSLM-only keys for OpenAI, Anthropic, Google, DeepSeek, each with a cap (docs/COSTS.md,
  "Spend controls"). OpenAI project allows `gpt-6-luna` only; Gemini key restricted to the Gemini API.
- **Client layer** (`src/orderslm/llm/`, `config/models.json`): OpenAI-compatible client (OpenAI, Gemini,
  DeepSeek) + native Anthropic client over `httpx`; retry 429/5xx with Retry-After, fail fast on auth/quota;
  cost in integer micro-USD from recorded usage × verified price (DeepSeek peak/off-peak, Haiku > 100K
  prompts; an unverified long-context price refuses instead of guessing); record/replay cache
  (`LLM_CACHE`); rpm throttle; scripted fake. Clients never edit the prompt.
- **Smoke test** (`make smoke ARGS=--yes`, `runs/smoke/20261015T173802Z/`): all 4 return valid JSON.
- **Open, decide before the bake-off:**
  1. Reasoning settings: **Julian chose to pilot both** (2026-10-15): lowest vs. provider default, 5 conversations
     × 4 models × 2 settings, then decide from the data. Lowest (config now): luna `none`, Gemini `minimal`,
     DeepSeek thinking off, Haiku thinking disabled + effort `low`. Defaults: luna `medium`, Gemini model
     default, DeepSeek thinking on `high`, Haiku adaptive thinking at effort `medium` (Anthropic effort docs;
     the smoke call ran Haiku at its default and skipped thinking on the easy prompt).
  2. DeepSeek has JSON-object mode only, so the shared prompt must describe the JSON itself (same prompt for all).
  3. Gemini: json_schema enforcement on the OpenAI-compatible endpoint and thinking-token accounting are not
     documented; the smoke call had no thinking tokens, so still unproven. Parser bills hidden thinking either way.
  4. OpenAI usage reports `prompt_tokens_details.cache_write_tokens`; check whether OpenAI bills cache
     writes before bulk labeling (no cache-write price in COSTS yet).
  5. Haiku's structured-output mode adds ~200 input tokens per call (273 vs 39–79 for the others).
- **Variants (Julian, 2026-10-15):** 12 configs, `provider/model@variant`: luna none/low/medium; Haiku
  thinking off/on × effort low/medium; Gemini minimal/default; DeepSeek none/low/high. All 12 pass the smoke test.
- **Pilot** (`runs/teacher-bakeoff/20261015T180442Z-pilot5/report.md`; 5 dev conversations, far too few to rank
  accuracy): every variant with reasoning on (luna low/medium, Haiku on-low/on-medium, DeepSeek low) got 5/5
  valid and all items right; the no-reasoning variants missed the half-and-half pizza (a-dev-017) or another item.
  Cost per 1,000 conversations: luna $0.76–0.94, DeepSeek $0.81–1.14, Haiku $1.66–2.04, Gemini $3.19–3.31.
- **Pilot findings:**
  1. Anthropic structured output allows at most 16 union-typed parameters; ExtractionOutput has 24 (HTTP 400 on
     every Haiku call in the first run, not billed). Haiku now runs prompt-only JSON like DeepSeek: the prompt is
     identical for all; luna and Gemini have schema-constrained decoding, Haiku and DeepSeek don't (report this).
  2. Unconstrained models set `menu_item_id` and `halves` together on a half-and-half (a-dev-017; DeepSeek
     none/high, Haiku off-*). A clearer prompt line would likely fix it; not changed, because tuning on bake-off
     conversations would bias the comparison (Julian to decide).
  3. Gemini default ≈ minimal (same tokens, no reasoning reported); docs don't state flash-lite's default.
  4. Gemini caches prompts implicitly (`cached_tokens` up to 8.3K of 9.9K); no verified cached price, so its
     cost is billed at full input price and may be overstated. Verify before the full run.
  5. Input tokens differ by tokenizer for the same prompt: luna 10.4K, Haiku 13.3K, DeepSeek 9.0K, Gemini 8.7K.
  6. A test reached the network once (fake key, 401, no cost) after the Anthropic change; tests now block real
     HTTP (`conftest.no_real_http`).
- **Second bake-off** (`runs/teacher-bakeoff/20261015T182916Z-full-skip5/report.md`; Julian: prompt v0.2 with the
  half-and-half wording, run on the 35 bake-off conversations the pilot never used, so no scored conversation shaped
  the prompt). 58 gold items. Best item F1: Haiku on-medium 100% (58/58, exact 33/35, $1.90/1k); luna low 98.3%
  (58/58 found, 2 extra, exact 32/35, $0.63/1k); luna none 97.4% (exact 30/35, $0.58/1k); DeepSeek low 95.5% (exact
  33/35, $0.84/1k). Gemini worst and priciest (74–78%, $2.82–2.94/1k). More reasoning was not better: luna medium and
  DeepSeek high scored below their `low` (invalid outputs: decision evidence, off-menu line with a variant).
  Exact-match 95% CIs overlap for the top four (e.g. 81–98% vs 78–97%): 35 conversations can't separate them.
  Spec rule (cheapest within 3 pp of best item F1) → luna `none`; Julian to decide (see the run report).
- **Head-to-head** (Julian: luna `low` vs Haiku `on-medium` on more chats; the sealed test split can't be used, so the
  51 dev conversations outside the bake-off set: `runs/teacher-bakeoff/20261015T185040Z-full-remaining/`). Tied:
  both found all 79 gold items with 2 extras (F1 98.8%); fully correct 48/51 (luna) vs 47/51 (Haiku); Haiku had 2
  invalid outputs (address on a pickup order). Cost $0.0292 vs $0.0933 ($0.57 vs $1.83 per 1k): luna got automatic
  prompt caching (340K of 491K input tokens cached); Haiku had none (Anthropic needs explicit cache_control, not
  used) and spends ~680 reasoning tokens per chat. Combined with the second bake-off (86 conversations, 137 gold
  items): luna 137 found / 4 extra, 80/86 fully correct; Haiku 137 / 2, 80/86.
- **Teacher decision (Julian, 2026-10-15): `openai/gpt-6-luna@low`.** Tied with Haiku on-medium on accuracy over 86
  conversations at about a third of the cost, and not exposed to the Claude-written-data bias.
- **Extras (false-positive items), luna low:** all 4 in conversations with no new order: a complaint about a missing
  croissant (a-dev-044), a catering request asking for a manager (a-dev-021: "30 large pizzas" → off-menu line), and an
  already-placed order with a payment claim (a-dev-056: latte + croissant). Haiku's 2 extras: the same a-dev-056.
  No extras in real ordering chats. **M4 labeling prompt:** say explicitly that items mentioned about a past or
  already-placed order (complaint, status, "I ordered X earlier") or a request to talk to someone are not a new
  order; check on dev before bulk labeling.
- **Teacher prompt fixes on dev (Julian, 2026-10-15), luna low, all 91 dev:**
  - v0.3 (no items for past/placed orders or handoff requests, `runs/…T190341Z-full-all`): the 4 extras are gone
    (a-dev-021/044/056 now correct). But 3 chats (a-dev-023/059/064: confirm, then change) became invalid: luna cited
    the change as evidence on a plain `pending` decision; the same error appeared for luna none/medium in the v0.2 run.
  - v0.4 (plain pending has no evidence, `runs/…T191233Z-full-all`): 91/91 valid, items 143 found / 3 extra / 3 missed
    of 146 (F1 97.9%), fully correct 83/91. The 3 fixed; 5 others changed with nothing in v0.4 touching them
    (unstated cheeseburger size filled with the default `single` ×2, missing pizza size / pickup name not flagged,
    payment asked despite a payment claim): **luna's answers vary between runs of the same prompt.**
  - These dev results are prompt tuning, not held-out numbers (the fixes came from these chats).
  - Ideas for M4 (not done): measure run-to-run variation (same prompt twice); compute `missing_or_ambiguous` in code
    (core/missing.py already has the rules) instead of trusting the model; normalize an unstated default variant.
- **Code applies the rules (Julian, 2026-10-15)**, `core/finalize.py` (`finalize@0.1`): fills an unstated default
  variant ("2 cheeseburgers" = single); recomputes `missing_or_ambiguous` with `core/missing.py`, keeping only the
  model's "ambiguous" calls (unmatched item, variant) that need the text; builds the question from the template
  (a pickup-only café is never asked "pickup or delivery?"); turns "confirmed" with gaps into pending +
  agreed_while_incomplete. The model's own missing list and question are ignored. Tested by rebuilding every dev
  gold missing list from its facts (raw-JSON path included). **Scoring `scorer@0.2`:** blank = default variant
  on both sides; all saved reports rebuilt, so numbers differ from the first ones reported (Gemini minimal item
  F1 74%→91%, DeepSeek none 81%→88%, luna medium 90%→94%); ranking and teacher choice unchanged. Each run now
  also has `report.finalize.md` / `metrics.finalize.json` (same saved outputs, scored after finalize).
- **Run-to-run variation (luna low, v0.4, all 91 dev, twice; second run cache off):** raw answers differ in 3/91
  chats (never in items); after finalize in 1/91 (a no-order complaint, where only the unused missing list
  differs). Both runs after finalize: 91/91 valid, 146/146 items, 0 extra, 90/91 fully correct (the miss:
  a-dev-049 "one of the other one" shake flavor, ambiguous vs missing: same question to the customer).
  Still prompt tuning on dev, not a held-out result.
- **M4 to-dos from this:** labels for chats with no items are stored as "no order" (null), like gold; labeling runs
  through finalize; the decision providers' label audit (§11d) checks "new order vs. past order".
- **Case-study data:** every run's metrics, tokens, costs and settings are in `runs/teacher-bakeoff/summary.json`
  (`--summary` rebuilds it from the saved run folders; reports from saved outputs only).

## Plan updates (Julian, 2026-10-08)

Recorded in the spec (§3, §4, §7, §10, §11, §12, §14, §18, §19), CLAUDE.md and docs/ARCHITECTURE.md. Nothing built
for M4/M6/M7 yet.

1. **Test-set contamination rule** (spec §12, CLAUDE.md): test results that led to a fix are reported as "used for
   fixes"; the fix is measured on fresh unseen data (unused PIZZA orders, ~1,150 left, or a new Claude-written test
   batch); lessons go into dev as new cases.
2. **Student outputs an intent** (required; M4 teacher labels the 15 router intents with the order, M6 trains it).
   Design rule (ARCHITECTURE.md): the extractor's input never includes the router's label, so the student's intent
   is an independent second opinion. `ExtractionRequest` already has no routing field.
3. **Five roles for the decision providers** (spec §11): primary: (b) order checker (M6/M7), (d) training-label
   auditor (M4); supporting: (a) router benchmark + router/student cross-check (M7), (e) menu narrowing incl. a
   ~80–100-item mega menu and a single-menu vs. mixed 2B student (M7, required), (c) item chooser (M7, optional
   pilot). Each tuned on dev, scored once on test, identical wording for every provider, compared with the teacher LLM.
4. **Architecture comparison** (M7): A router → extractor, B extractor only, C in parallel; composed from per-component
   runs, confirmed by a small live run; reports break-even router latency.
5. **Rare labels:** per-label scores with confidence intervals and a noise note.
6. **V2 candidate:** fine-tuning Julia-1 on teacher-labeled router data ("off-the-shelf vs. fine-tuned").

## Rename (2026-10-07)

ShopRoute → **OrderSLM** (Julian's request), committed as `a2bf6cb` after the two M0 commits:
`src/shoproute` → `src/orderslm` (`git mv`, history follows), spec → `orderslm-project-plan.md`, env var
→ `ORDERSLM_UNSEAL_TEST`, every mention in docs, Makefile, CLAUDE.md, tests, `pyproject.toml`; `uv.lock`
regenerated. Earlier commit messages keep the old name. Julian renamed the local folder to
`~/Documents/GitHub/orderslm` and recreated `.venv`; GitHub remote: `origin` = Julian-Reyes/orderSLM (private).

## M1 summary

- **Menus** (`data/menus/`, docs/MENUS.md): Corner Patty (burgers) and Halfmoon Pizza from the M0 samples,
  Morning Crumb Café (new; pickup only; **name required for pickup**), and the new held-out Lucky Lime
  Taqueria in `data/menus/held_out/`. `load_menus()` excludes the held-out menu unless asked
  (`include_held_out=True`); `make menus` validates and prints each menu's content hash.
- **Halfmoon is a realistic pizzeria** (M1 review, item 4): 8 pizzas × 5 sizes, 23 toppings, 3 sauces,
  4 crusts, 2 sides, 6 drinks. PIZZA evaluation gets its own benchmark catalog, generated by the M2 script
  into `data/external/` (docs/MENUS.md). No PIZZA-derived file is committed (tested). PIZZA's license
  confirmed CC-BY-NC-4.0 from the dataset's LICENSE/README.
- **Contract changes** (samples and docs updated):
  - `extraction@0.2`: `Modification.amount` = `normal | extra | light` ("extra cheese", "light on the sauce").
  - `menu@0.3`: modifiers are ingredients/add-ons (`ingredient_ids`, `addon_ids` per item) instead of
    add/remove kinds (every topping would otherwise need both an add and a remove entry); variant and modifier aliases;
    `exclusive_groups` (one crust, one milk). Pizza items are now `*_pizza` ids named "… Pizza".
- **Deterministic core** (`src/orderslm/core/`):
  - `pricing.py`: `DeterministicPricing` → verified `Quote` or a `ToolErr` listing every problem; rules in
    docs/PRICING.md (half-and-half = dearer half + half-priced toppings, rounded up; extra = one more portion).
  - `missing.py`: the annotation guide's "what counts as missing" as code (all 10 sample golds agree with it).
  - `diff.py`: snapshot → patch for the business (`ExtractionOutput.empty()` added for the first turn).
  - `state.py`: status transitions; customer changes to a placed order → `NEEDS_STAFF`; a "yes" only
    confirms when a summary was sent and nothing changed.
  - `replies.py`: English templates keyed by language; amounts only from the Quote; a model's clarification
    question is replaced by a template if it states any amount.
  - `matching.py`: menu lexicon with span-preserving, plural- and typo-tolerant longest-match lookup.
- **Rules baselines** (`src/orderslm/baselines/`): `RulesExtractor` (an `OrderExtractor`; corrections,
  half-and-half, toppings, amounts, combos, contextual yes, times normalized against opening hours,
  addresses, payment/claims/change, names; always schema-valid and grounded) and `KeywordDecisionProvider`
  (a `DecisionProvider` reading the same `DecisionRequest` the hosted providers get, via the new
  `router.parse_input`). `render_input` now collapses whitespace per message → `router-prompt@0.2`.
- **Samples:** updated to the new ids; added sample-011 (café, name required, milk substitution, 08:15) and
  sample-012 (pizza with crust + light/extra amounts, canned drinks). Baseline tests use their own
  invented conversations, never the samples.

## M1 files

```
added     data/menus/{corner-patty,halfmoon-pizza,morning-crumb}.json  data/menus/held_out/lucky-lime.json
          data/samples/conversations/sample-011.json  sample-012.json
          src/orderslm/menus.py  src/orderslm/core/{__init__,pricing,missing,diff,state,replies,matching}.py
          src/orderslm/baselines/{__init__,rules_extractor,rules_router}.py
          docs/PRICING.md  docs/MENUS.md
          tests/builders.py  tests/{test_menus,test_pricing,test_order_logic,test_replies,test_baselines}.py
removed   data/samples/menus/ (now data/menus/)
changed   src/orderslm/schema/{common,menu,extraction,order}.py  src/orderslm/{checks,router}.py
          data/samples/conversations/sample-001…010.json  Makefile (make menus)
          docs/{SCHEMA,ANNOTATION_GUIDE,ARCHITECTURE}.md  tests/{conftest,test_samples,test_contracts,
          test_extraction_schema,test_docs_sync}.py  PROGRESS.md
```

## Checks run (M1)

- `make check`: `ruff check` clean, `ruff format --check` clean, **pytest: 227 passed**.
- `make menus`: all four menus validate (Halfmoon: 16 items, 54 variants, 30 modifiers).
- Pricing tests assert hand-worked amounts (e.g. sample-005-style half-and-half: $18.99 + 2 × $5.99 +
  $2.99 fee = $33.96); the business messages in samples 006/009 ($14.48, $19.98) match the engine.

## M1 review (Julian, 2026-10-07)

1. Pricing rules approved as documented (docs/PRICING.md).
2. PIZZA drink-size mappings: review during the M2 conversion with real examples.
3. No PIZZA-derived file is ever committed: the coverage map is generated by the M2 script under
   `data/external/`. The unpushed local history was rewritten so neither `pizza-coverage.json` nor the
   PIZZA-catalog version of Halfmoon (85 toppings, 23 styles, 22 drinks, copied from the dataset's
   catalogs) appears in any commit.
4. Menus split: Halfmoon is realistic (chat data + demo); a separate PIZZA benchmark catalog is generated
   by the M2 script from a fixed-seed sample of ~200 test orders plus distractors (~30–40 toppings), used
   only for the PIZZA evaluation. Orders are never filtered to fit a menu.

**Bug fixed after M1** (found while trimming Halfmoon): `DeterministicPricing.quote` priced lines that
`check_catalog` had already rejected, so a proposal with an unknown modifier id raised `AssertionError`
instead of returning a `ToolErr`. Rejected lines are now skipped; 3 regression tests (whole item, half,
other lines still reported). 221 tests.

Still open from M1: **"w oat milk" on a latte** is annotated as a substitute of the included milk (guide
updated); the rules baseline records it as an add, which prices the same.

Workflow: one branch per milestone, merged into main when done; push after each merge, **only with
Julian's permission each time**.

## Decisions (Julian, 2026-10-07, answers to the M0 open questions)

1. Snapshot output approved: the model outputs the full order; code derives the patch.
2. Corner Patty and Halfmoon Pizza are 2 of the 3 real menus; the held-out menu is new. **Done in M1.**
   (The original "pizzeria covers PIZZA's vocabulary" plan was replaced in the M1 review, item 4.)
3. Customer name optional in the schema; per-business `name_required_for_pickup`, enabled for one business.
   **Done (Morning Crumb).**
4. Samples may be few-shot examples, never in any evaluation (CLAUDE.md; the M3 eval loader must reject
   `split: sample`, with a test).
5. Test sets are committed, sealing enforced in code. PIZZA data is never committed (CC-BY-NC-4.0): only a
   download + conversion script; `data/external/` is gitignored and tested.
6. Frontend (Vite + Preact + TypeScript, FastAPI) approved, set up in **M2** for the annotation tool.
7. Provider prices re-verified against official pages before each first paid run.

## M0 summary (condensed)

AgentDesk inspected read-only at `c24529c`; reuse map in docs/AGENTDESK_REUSE.md. Ported: integer cents,
injected clock, `ToolOk | ToolErr`, scripted fakes, working rules + pre-commit hook. Contracts and
interfaces with mocks (`DecisionProvider`, `OrderExtractor`, `BusinessTools`, `PricingEngine`), grounding
checks, sealed-test guard, 10 annotated samples, docs (SCHEMA, TAXONOMY, ARCHITECTURE, ANNOTATION_GUIDE,
COSTS). Environment: uv 0.12.23 from its GitHub release (sha256 verified) in `~/.local/bin`, managing
Python 3.12; `brew install uv` was stopped because it was compiling cmake from source.

## M2: tooling (merged to main 2026-10-07)

Acceptance (spec §18, revised): locked split with counts per source, label, menu, style and scenario; all dev +
≥25% of test reviewed, correction rate logged; 199 PIZZA cases.

- **PIZZA benchmark** (`make pizza`, docs/PIZZA.md): test split pinned to commit `814d6d0`, sha256 in
  `data/external/pizza/MANIFEST.json`; 200 of 1,357 orders sampled with seed 20261007 (never filtered).
  Entities the sample uses: **29 toppings, 7 recipe styles, 4 crusts, 6 pizza sizes, 10 drinks, 6 drink
  variants, 2 topping amounts**; distractors bring toppings to 35. **199/200 converted**; 1 reported
  (row 784: two crusts + a recipe, wording ambiguous against the parse). 10 orders had one word missing from
  the dataset's own catalog and took its value from the EXR parse; 15 "no extra cheese" kept the default amount.
  Everything (catalog, cases, coverage map, report with drink-variant examples) is under `data/external/`.
- **Splits** (`orderslm.data.splits`, docs/SPLITS.md): save/load with the tool's checks; stats; near-duplicate
  check; `lock` (hashes, counts, 30-conversation blind relabel from lock + 7 days); after the lock, gold changes
  need a logged reason (`CHANGES.jsonl`) and `verify` catches unlogged edits.
- **Annotation API** (`orderslm.app.main`): menus, list/get/save, a check endpoint (findings, derived missing
  info, template question, deterministic quote), stats, blind relabel (never sends earlier labels). The test
  split answers 403 unless the server process has `ORDERSLM_UNSEAL_TEST` (`make annotate-test`).
- **Frontend** (`web/`, Vite 8.3.3 + Preact 10.29.8 + TypeScript 7.0.2 + @preact/preset-vite 2.10.6): conversation
  editor (messages, roles, timestamps in the menu's timezone, scenarios, style, notes), routing table, gold
  JSON editor with evidence-from-selection, "+ item line" from the menu, "fill missing info from the rules",
  live check panel with the quote, stats tab, blind relabel tab, menu reference. Follows the documented
  "order counter" palette. Checked with headless Chrome screenshots on two samples (light and dark).
- **Contract:** `conversation@0.2` adds `Split.benchmark` (PIZZA cases).
- **Guards:** a test allowlists the only modules that may mention `test_split_dir`, `include_held_out=True`,
  `UNSEAL_ENV`, `load_cases` or `_TEST`; the PIZZA benchmark's `load_cases()` is sealed like the test split.
- **Dependencies added (approved):** fastapi 0.142.2, uvicorn 0.54.0, httpx 0.28.1 (dev); npm packages above
  (`web/package-lock.json`). Transitive npm licenses: MIT/ISC/BSD/Apache, plus MPL-2.0 (lightningcss) and
  CC-BY-4.0 (caniuse-lite data), both build-time only; the shipped bundle contains only Preact (MIT).
- **Checks:** `make check` 273 passed; `npm run build` (tsc + vite) clean. Spend: $0.

### Decisions (Julian, 2026-10-07, M2 review)

1. **Evaluation data is speed-first** (spec §7 rewritten): Source A = Claude-written from scenario cards (dev ~80,
   test ~170), reviewed by Julian (all dev, ≥25% test, correction rate logged); Source B = the 199 PIZZA cases
   (external human-written test set); Source C = optional ~30 Julian-written. Week-later blind relabel dropped
   (optional, Source C only). Every result reported per source.
2. PIZZA drink sizes stay separate options. 3. "No extra cheese" = no change. 4. No `httpx2` for now.
5. Fonts decided in M8. 6. M2 tooling merged into main; conversations on branch `m2-eval-data`.
7. Only `main` lives on GitHub; local `milestone-0`/`milestone-1` deleted (fully merged).

## M2: evaluation data (branch `m2-eval-data`)

- **Contracts:** `conversation@0.3`: `Source.claude_written`; `AnnotatedConversation.card_id` (required exactly
  for claude_written); new `Scenario` tags `simple_order`, `menu_question`, `delivery_question`,
  `payment_question`, `refund_request`, `unclear_message`.
- **Scenario cards** (`orderslm.data.cards`, docs/SPLITS.md): 80 dev (`data/dev/cards.jsonl`) + 170 test (sealed
  `data/test/cards.jsonl`), seed 20261007; 23 situations with fixed per-split quotas; every router label, style,
  feature and tricky case in both splits; held-out menu only in test (tested).
- **Splits:** dev/test accept Source A and C; Source A must follow its card; `review()` + `REVIEWS.jsonl` +
  correction rate; `lock` requires all dev and ≥25% test reviewed, records per-source counts and review stats,
  relabel only with `--relabel-human`. API/tool: "Save as reviewed", review badges, review stats.
- **Checks:** `make check` 286 passed; web `tsc` + build clean.

### Card review (Julian, 2026-10-08): approved with changes

- **Supplement batch** appended (own RNG stream `20261007-supplement-2026-10-08`; the first 80 + 170 cards are
  unchanged, tested): +1 dev / +3 test per rare label (HUMAN_REQUEST, ORDER_PROBLEM, ORDER_STATUS, PAYMENT_CLAIM,
  OUT_OF_SCOPE, REFUND_REQUEST, UNKNOWN → 3 dev / 7–8 test each) and a new `implicit_category` situation (4 dev,
  8 test, spread over every menu) for the menu-narrowing evaluation (spec §11e). Totals: **91 dev, 199 test**;
  held-out menu **50/199 = 25.1%** of test.
- **Contract:** `conversation@0.4` adds `Scenario.implicit_category`.
- `cards generate --split dev|test`; dev cards regenerated (`data/dev/cards.jsonl`, 91; a test checks the file
  matches the generator). Julian regenerated the sealed test cards on 2026-10-08 (`cards generate --split test --force`): 199 cards, the
  first 170 lines unchanged, 29 appended.
- **Checks:** `make check` 293 passed.

### Dev conversations (Source A, 2026-10-08): written, not yet reviewed

- **91 conversations**, one per dev card (`data/dev/a-dev-001.json` … `a-dev-091.json`), `annotator`
  "claude-opus-5.5 (Source A)", each with `annotation_notes` for its judgment calls. Saved through `splits.save`
  (the annotation tool's checks); re-checked from disk and through the API: **0 findings** (no warnings either),
  no near-duplicates within dev.
- **Counts:** 266 customer messages; 30 Corner Patty / 31 Halfmoon / 30 Morning Crumb; styles clean 18, texting 27,
  rapid_fire 18, emoji 16, shouty 12; 64 with an order, 27 without (status, problems, refunds, questions, small talk).
  Primary labels: PLACE_ORDER 160, SMALL_TALK 26, MENU_QUESTION 16, MODIFY_ORDER 15, CONFIRM_ORDER 8,
  ORDER_PROBLEM 8, OUT_OF_SCOPE 5, CANCEL_ORDER 4, DELIVERY_QUESTION 4, HUMAN_REQUEST 4, ORDER_STATUS 4,
  REFUND_REQUEST 4, PAYMENT_QUESTION 3, UNKNOWN 3, PAYMENT_CLAIM 2 (+1 as secondary).
- **Pricing:** 54 gold orders price cleanly; the other 10 fail on purpose (4 off-menu/ambiguous items, 4 missing
  sizes, 1 unclear quantity, 1 missing combo choice). Every total in a business message comes from the pricing engine.
- Authoring helper kept outside the repo (scratchpad); the JSON files are the source of truth.

### Dev review rulings (Julian, 2026-10-08), applied before any test conversation exists

- **Contracts:** `extraction@0.3` (`Modification.not_on_menu`, `ItemProposal.unmatched_variant_text`,
  `CustomerDecision.agreed_while_incomplete`; `confirmed` only when nothing is missing) and `menu@0.4`
  (`Variant.diameter_cm`/`slices`). Samples and dev files migrated (version string only); the local PIZZA
  cases were regenerated and are identical apart from the new default fields.
- **Rulings:** (1) any change after confirming is `MODIFY_ORDER`; (2) `confirmed` only when the order is complete,
  a yes with gaps is `pending` + `agreed_while_incomplete` (a-dev-032 updated); (3) a size the item doesn't have
  keeps the item on the menu, `item_variant / missing`, the wording kept in `unmatched_variant_text` (a-dev-079);
  (4) an option the menu doesn't offer is `not_on_menu`, `item_modification / off_menu`, never priced
  (`OPTION_NOT_ON_MENU`) or summarized, with a reply "We don't have X for the Y. Would you like it without, or
  something else?" (a-dev-034); kitchen requests ("warm") stay free notes. All in the annotation guide, SCHEMA,
  PRICING, TAXONOMY.
- **Pizza sizes:** Halfmoon's 40 pizza variants have `diameter_cm` and `slices` (20/25/30/36/41 cm, 4/6/8/10/12
  slices), reply layer only: `ExtractionRequest` rejects a menu that still has them; extractors get
  `menu.extractor_view()`. Verified unchanged: every base price and size delta, all 74 gold order prices except
  a-dev-034 (was $26.98 with the artichoke silently ignored; now `OPTION_NOT_ON_MENU`, as ruled), and every card
  (frozen 80 + 170 and all 91 + 199).
- **Checks:** `make check` 312 passed (19 new tests in `tests/test_options_and_completeness.py`); dev: 0 findings.

### Second round of rulings (Julian, 2026-10-08), before review

- **`extraction@0.4`:** `Modification.kitchen_note`. Every request with no menu id is explicitly `not_on_menu` or
  `kitchen_note`; gold that is neither fails (`UNCLASSIFIED_REQUEST`). Re-check of all 91 dev files + 12 samples
  flagged **only a-dev-074** ("warm"), now a kitchen note.
- **`menu@0.5`:** `accepted_kitchen_requests` on every menu (docs/MENUS.md). `core/requests.py` matches them first
  (a match is a free kitchen note whatever the model said); `not_on_menu` is told firmly; anything else is
  unverified: `item_modification / ambiguous`, never priced (`REQUEST_UNVERIFIED`), asked "Just checking, we may not
  be able to do X on the Y. Want it without, or keep it as a note for the kitchen?", never on the ticket.
- **Reply layer:** `next_reply` asks the missing question first; `summary()` refuses while anything is missing.
  a-dev-032 rewritten: the bot asks "Is this for pickup or delivery?", the customer replies "👍 SOUNDS GOOD"
  without answering (CONFIRM_ORDER as intent; decision `pending` + `agreed_while_incomplete`).
- **Payment claims:** the summary says "You mentioned you've already paid, and the restaurant will confirm it";
  the new business ticket (`core/ticket.py`) prints "Payment: customer says paid, not verified" (only
  `payment_confirmed`, set by staff/payment system, prints as paid). Automatic payment verification (e.g. Pix
  notifications) added to the spec's V2 candidates.
- **Card fix:** a-dev-020's card now says fulfillment `delivery` (`cards.CARD_FIXES`, applied after generation).
- **Verified unchanged:** all 290 cards apart from that one field; every base price and size delta (menus only gained
  lines); all gold prices except a-dev-034 (ruled earlier). a-dev-079's question now reads "We don't have **a**
  party size…" (the template fix landed after that file's last save). Local PIZZA cases regenerated: 199 load, none
  unclassified.

### Independent audit + third round of rulings (2026-10-08)

A fresh agent (no prior view of the conversations) audited all 91 dev files read-only: 68 had no finding.
Julian's rulings, all applied:
- **Strict kitchen notes** accepted for V1; `requests.request_counts` gives the unverified-fallback rate per run
  (spec §12 metric).
- **Definite errors fixed:** 016 (pickup in ~10 min → time_sensitive), 032 (the 👍 that doesn't answer "pickup or
  delivery?" is UNKNOWN; the customer then chooses delivery and confirms a real summary), 064 (pickup stated, so the
  summary is legitimate), 073 (raw_text "10:30"; draft time change → normal), 075 ("pay w 2 hundreds").
- **Code:** cash smaller than the total → `CASH_BELOW_TOTAL` with a reply; pickup-only businesses ask "Is this for
  pickup, and can I get a name for the order?" (the name rule applies when the method can only be pickup);
  half-and-half without a size asks "What size would you like for the pizza (…)?".
- **Card generator:** `simple_order`, `contextual_yes`, `correction_after_confirmation` always state pickup or
  delivery (5 dev, 11 test cards; only that field changed, verified). Dev conversations 028, 041, 042 now state it.
  Morning Crumb cards switched to pickup don't get the brief's name hint (that would change a second field); the
  validation rules still require the name.
- **Conventions 1–8** in the annotation guide (detail on an item just stated = PLACE_ORDER; urgency of changes;
  disputed charges; MODIFY + secondary PLACE; refers_to for UNKNOWN and absent orders; pickup-only; payment
  claims; resets, carried-over time, "to <address>", topping-only halves, no allergen claims). Applied to 005, 020,
  037, 038, 050, 072, 076, 086, 088, 090. Low-priority fixes: 002 evidence, 042 tag, 053/069 timestamps.
- **Verified:** prices and size deltas unchanged; gold prices differ from the morning snapshot only for 034 (ruled)
  and 032/042 (now delivery: + fee). 91 dev files: 0 findings, 0 warnings, no near-duplicates. `make check` 335 passed.
- **Sealed test cards need regenerating** (11 cards now state pickup/delivery).

**Judgment calls from the first draft** (all now ruled: 1, 2, 4, 5 in round one; 3, 6, 7, 8 in round two, and in
the annotation guide):
1. After the customer confirms, later messages refer to the `placed_order`; any change then (including adding an
   item) is `MODIFY_ORDER`, `time_sensitive` if it changes what the kitchen makes (023, 059, 067), `normal` for a
   payment switch (064). The decision resets to `pending`.
2. A confirmation can leave things missing: a-dev-032 confirms items + payment, but pickup/delivery was never chosen
   (the card said "unstated").
3. A vague item that is later resolved ("the usual", "the same as last time") is dropped and the resolved items get
   new line ids (038, 040); one that is never resolved stays as `unmatched_text` + `ambiguous` (016, 038).
4. A size that doesn't exist ("party size", 079): menu item kept, no variant, `item_variant` with reason `off_menu`.
5. An off-menu topping ("artichoke hearts", 034) or kitchen request ("warm", 074) is a modification with no
   `modifier_id`; the V1 missing-info rules list nothing for it.
6. Menu questions mid-order are `refers_to: draft`; before any order, `none`. A customer's "yes" to "Want one?" adds the
   item (`PLACE_ORDER`, 091), per the taxonomy's boundary rule.
7. a-dev-020's card said fulfillment "unstated" but its variant is "pickup → delivery"; the variant won.
8. Payment claims during an order: `PLACE_ORDER` + secondary `PAYMENT_CLAIM` (072) or primary `PAYMENT_CLAIM` (089);
   method stays `unknown`, `customer_claims_paid: true`, so payment isn't asked again.

### Dev review fixes (Julian, 2026-10-13)

- **Off-menu option question reworded** (replies@0.2): "Would you like it without, or something else?" read as
  "without artichoke hearts", which the restaurant can't make anyway. Now "Would you like it as it comes, or with
  something else instead?" (covers add and substitute). Only a-dev-034 uses it; its gold question was regenerated
  from the template. No test conversations exist yet and no PIZZA case has an off-menu option.
- **Items sold by the order** (menu@0.6, replies@0.3): a-dev-045's "some garlic knots" was asked as "How many garlic
  knots would you like?", which invites a piece count. `MenuItem.sold_as: order` + optional `pieces_per_order`
  (Julian: knots 6, breadsticks 4; fries and onion rings without a count). The question is now "How many orders of
  garlic knots would you like (6 per order)?"; a-dev-045 regenerated. Not defaulted to 1: the card tests an unclear
  quantity. Annotation rule: a piece count that divides evenly becomes orders ("12 knots" = 2), else ambiguous.
  The extractor sees the piece count. Held-out menu unchanged; no wings on any menu.
- **Plural in the quantity question** (replies@0.4): "How many veggie burgers would you like?" A small English rule
  (`replies._plural_en`; names ending in s stay as they are), tested on every item counted one by one. No gold
  question used the plain quantity template, so no data changed. The held-out menu's chips & salsa / chips & guac
  stay counted one by one ("How many chips & salsas would you like?"; Julian, 2026-10-13).
- **a-dev-050:** the business reply to "do you have any vegan pastries?" now says it can't confirm that here and
  staff can check (the audit had removed the vegan claim but left no answer; guide: no dietary claims). Gold unchanged.
- **Address given, method not chosen** (replies@0.5): a-dev-077 ("do u deliver to the harbor inn on water st?")
  now asks "Would you like it delivered to the harbor inn on water st, or will you pick it up? Also, will you pay by
  card or cash?" (the customer's own words; pickup-only menus unchanged). Regenerated; the only dev case. Open for
  the reply layer: answering the DELIVERY_QUESTION itself (fee and minimum from the menu; menus have no delivery
  area, so "yes, we deliver to Water St" can't be verified).
- **Plural in summary lines** (replies@0.6): "2 Muffin (Blueberry)" now reads "2 Muffins (Blueberry)" (same rule as
  the quantity question). Found while generating test business messages; no gold changes.
- **Decision (Julian):** the M8 demo answers simple menu, delivery, hours and payment questions with templates
  filled from menu data only (spec §2, §16, §18). Not part of gold or any reported number.
- **Decision (Julian):** the order checker (spec §11b) runs in two versions, whole-order yes/no and line-by-line
  yes/no, and is measured with **planted mistakes** (code plants known errors into gold orders, per error type),
  also for the training-label auditor (§11d). Planted copies of *test* gold at final eval are allowed (Julian,
  2026-10-13): made by fixed code for scoring only, never inspected, trained on or used for tuning.
- **Decision (Julian):** the M8 demo replies to off-topic messages with one fixed sentence ("I can only help with
  orders at Corner Patty. Want to order something?") and to small talk with a short greeting; it never answers the
  off-topic question (spec §16). Re-inspect AgentDesk's reply checks and off-topic handling before building replies.
- **Decision (Julian):** new decision-provider role (f) **closed-field comparison** (spec §11, M7): fulfillment
  method, payment method, customer decision and paid claim, each answered side by side by rules, Julia-1, Jev,
  OpenAI Decisions, the student and the teacher. An experiment only; the student still fills the whole order.
- **Noticed, not changed:** a-dev-016, 038, 046 and 049 have hand-written questions that differ from the template.

### Dev review complete (Julian, 2026-10-13)

- All **91/91** Source A dev conversations reviewed (`data/dev/REVIEWS.jsonl`, now committed); every review's
  `sha256_after` matches the file on disk, including the four changed today before their review.
- **Correction rate:** the tool logs **0.0** (no edits saved through the tool). That understates it: during review,
  four conversations changed at Julian's direction before he saved them: 034 (off-menu question wording), 045
  (orders-of question), 050 (vegan answer), 077 (address question). Report the correction rate as **4/91 (4.4%)**
  changed during review, 0 in the tool.
- Rulings from this review are in the entries above (templates replies@0.2–0.5, menu@0.6, spec §2/§11/§16/§18).

### Test conversations (Source A, 2026-10-13): written, awaiting Julian's spot-check

- **199 conversations**, one per sealed test card (`data/test/a-test-001.json` … `a-test-199.json`), written under
  `ORDERSLM_UNSEAL_TEST="author Source A cards"`, saved through `splits.save` (the tool's checks), each with
  `annotation_notes`. Authoring helper outside the repo; questions from the templates unless noted; every summary or
  price in a business message generated by the pricing engine / `replies.summary`.
- **Checks:** 199/199 cards covered; 0 blocking findings, 0 warnings; no near-duplicates within test or against dev.
  `make check` 344 passed.
- **Counts:** 600 customer messages; 50 per menu (Morning Crumb 49), held-out Lucky Lime 50 (25.1%); styles texting
  60, clean 40, rapid_fire 40, emoji 36, shouty 23; 132 with an order (113 price; 19 fail on purpose: 6 off-menu
  items, 6 missing sizes, 3 combo choices, 2 off-menu options, 2 unclear quantities), 67 without. Primary labels:
  PLACE_ORDER 345, SMALL_TALK 65, MODIFY_ORDER 31, ORDER_PROBLEM 24, MENU_QUESTION 23, ORDER_STATUS 19,
  CONFIRM_ORDER 16, HUMAN_REQUEST 13, PAYMENT_CLAIM 12, DELIVERY_QUESTION 11, CANCEL_ORDER 9, OUT_OF_SCOPE 8,
  PAYMENT_QUESTION 8, REFUND_REQUEST 8, UNKNOWN 8. Urgency: time_sensitive 19, needs_staff_now 11.
- **Cards that couldn't be written as stated** (noted in each file): 043 (three labels in one message: split over
  two messages), 061 and 175 (the card expects a SMALL_TALK label, and a greeting in the same message as a request
  gets no label of its own, so the greeting is a separate message), 151 (pickup vs. "change the address": the variant
  wins, as with a-dev-020). Greeting + order in one message is allowed and common (labeled PLACE_ORDER only): 31 dev
  and 73 test messages. **Julian approved all four, the two conventions and 121's urgency (2026-10-13).**
- **New conventions** (annotation guide, for Julian to confirm): a combo slot with one choice is filled with it
  (Lucky Lime plate side; 005, 065, 096); a payment channel ("through the app", "on the phone") is not a method, a
  named method the business doesn't take (Venmo) is `other` (089, 191).
- **Judgment calls to check:** 121 (dairy in a burrito ordered without cheese, not eaten) is `needs_staff_now` as a
  safety problem; an allergy *question* stays normal. Unresolved vague items ('same as last time' 133, 'THE USUAL'
  165) use `item_menu_match / ambiguous`; the rules code reports every unmatched item as off_menu (the validator
  compares fields only).
- **Hand-written questions** (template wording didn't fit): 020 (lower case), 043 (two combo slots), 124 (offers
  the two times), 133 and 165 (can't see past orders).
- **Plain-English view wording:** an unstated variant said "size not stated" even for muffin flavors or taco fillings
  (Julian, reviewing a-test-010). It now names the options: "not stated (Blueberry, Chocolate chip, Banana nut)";
  the editor's dropdown says "not stated". Display only; no gold changed.
- **Combo question names the slot** (replies@0.7, Julian reviewing a-test-034): "What would you like with the coffee &
  pastry (Croissant or Muffin)?" is now "Which pastry would you like with the coffee & pastry (…)?"; several missing
  slots read "…, and which drink (…)"; a picked choice that still needs a size is asked too. Regenerated from the
  template: a-dev-011 (reviewed earlier; wording only, not counted as a review correction), a-test-013, 034, 043
  (043 no longer hand-written).
- **Template issues noticed, not changed:** an
  ambiguous time asks a generic "What time would you like it?"; an unmatched item is quoted as written (caps,
  "same as last time").

### Test review and lock (Julian, 2026-10-14)

- **Reviewed 58/199 (29%)**, not the seeded sample first proposed (finding scattered ids in the tool was too slow):
  a contiguous block a-test-001–046, the four flagged ones beyond it (061, 121, 151, 175), and one conversation of
  each situation type missing from that block (047 off-topic, 048 contextual yes, 052 unclear, 056 delivery
  question, 063 order status, 070 half-and-half, 077 payment question, 172 implicit category). Every menu and all
  24 situations are covered. Report it as a contiguous block plus targeted additions, not a random sample.
- **Correction rate (test): 0/58.** 013 and 043 changed after their first review (combo-question template fix,
  wording only) and were re-reviewed before the lock; every review matches the locked file.
- **Correction rates as LOCK.json records them:** dev 0.0 and test 0.0, the tool's count. Report dev as **4/91
  (4.4%) changed during review** (034, 045, 050, 077, changed at Julian's direction before he saved them), test as
  0/58.
- **Locked** with `make lock-test`: 199 test conversations, sha256 `3f09234131e3825d`; `make verify-test` passes.
  From now on a test file changes only with a logged reason (CHANGES.jsonl), and results after any model run on test
  follow the contamination rule (CLAUDE.md).

### Open for Julian (M2)

1. Merge `m2-eval-data` into `main` and push when you want (ask first; secrets check before any push);
   `milestone-2` is merged and can be deleted locally.
2. Rare labels now have 3 dev / 7–8 test cards each; per-label test metrics are still noisy (reported with CIs).
3. Mega menu (spec §11e): the three menus combined have **36 items** (100 item/variant combinations), not ~80–100
   items. Decide in M7 whether "items" means item/variant combinations or the mega menu needs more items.
