# Progress

Read this first each session. Spec: `shoproute-project-plan.md` (authoritative; replaces the Pedido Fácil plan).

_Last updated 2026-10-07._

## Milestones

| # | Work | Status |
|---|---|---|
| 0 | AgentDesk inspection, layout, contracts, docs, interfaces + mocks, samples, tests | ✅ Done 2026-10-07 |
| 1 | Menus (3 + held-out), pricing engine, order state, rules baselines | Next |
| 2 | Annotation tool; dev + sealed test sets | Not started |
| 3 | Teacher bake-off | Not started |
| 4 | Synthetic generation + labeling | Not started |
| 5 | Student bake-off | Not started |
| 6 | LoRA training + distillation eval | Not started |
| 7 | Router benchmark | Not started |
| 8 | Demo, report, Hugging Face release | Not started |

**Spend to date: $0.00** (docs/COSTS.md). No API calls, model downloads, training or deployment in M0.

## M0 summary

- **AgentDesk inspected** at commit `c24529c` (read-only shallow clone in a scratch directory, not in this
  repo, not modified). All 26 paths from spec §15 exist. Mapping with Python equivalents and status:
  `docs/AGENTDESK_REUSE.md`. Correction to the spec: the winner rule is `pickWinner` in
  `evals/runner/comparison-sets.ts`; `wilson` is in `evals/judge/agreement.ts`.
- **Ported now:** integer cents, injected clock, `ToolOk | ToolErr` results, scripted fake providers,
  working rules + pre-commit hook. **Planned:** LLM client/cache/throttle/estimate/run store (M3), stats
  with paired tests (M3), judge agreement (M6), tracing (M6/M8), static export + frontend logic (M8).
- **Contracts** (`src/shoproute/schema/`, versioned): `extraction@0.1` (snapshot proposal with evidence,
  explicit slot states, no price fields, `extra="forbid"`), `router@0.1` + `taxonomy@0.1` (15 labels,
  secondary, urgency, context flags; descriptions sent verbatim to every provider), conversation, menu,
  verified `Quote`/`OrderRecord`/tool results (arithmetic-checked integer cents).
- **Interfaces + mocks:** `DecisionProvider` (provider-neutral choice/score/boolean questions, option-limit
  check, response validation), `OrderExtractor` (single `parse_model_output` path that never raises),
  `BusinessTools` and `PricingEngine` protocols; `ScriptedDecisionProvider`, `ScriptedExtractor`,
  `InMemoryBusinessTools`. `router.py` builds identical requests for all providers and reports any repair
  it applies to an answer.
- **Grounding checks** (`checks.py`): evidence quotes exist in the cited message; items, variants,
  modifiers, combo choices and halves exist in the menu.
- **Samples:** 2 sample menus, 10 annotated English conversations covering multi-message orders,
  corrections (incl. after confirmation), missing info, two-request messages, off-menu, combo,
  half-and-half, contextual yes, status question, order problem + refund + human, payment claim,
  cancellation, out-of-scope. Split `sample`: examples only, never scored.
- **Sealed test guard:** `paths.test_split_dir()` refuses unless `SHOPROUTE_UNSEAL_TEST` is set.

## Files added

```
pyproject.toml  uv.lock  Makefile  README.md  CLAUDE.md  PROGRESS.md  .gitignore  .env.example
.githooks/pre-commit
docs/  AGENTDESK_REUSE.md  SCHEMA.md  TAXONOMY.md  ARCHITECTURE.md  ANNOTATION_GUIDE.md  COSTS.md
src/shoproute/  __init__.py  router.py  checks.py  paths.py
  schema/       __init__.py common.py conversation.py menu.py extraction.py routing.py order.py annotation.py
  domain/       __init__.py money.py clock.py
  interfaces/   __init__.py decision.py extractor.py tools.py
  mocks/        __init__.py decision.py extractor.py tools.py
data/samples/menus/          corner-patty.json  halfmoon-pizza.json
data/samples/conversations/  sample-001.json … sample-010.json
tests/  __init__.py conftest.py test_extraction_schema.py test_samples.py test_taxonomy_and_router.py
        test_verified_results.py test_contracts.py test_docs_sync.py
```
(`shoproute-project-plan.md` was already present and is committed unchanged.)

## Checks run

- `make check` → `ruff check` clean, `ruff format --check` clean, **pytest: 102 passed** (after recording
  the decisions below; 100 at the M0 commit).
- Toolchain: Python 3.12.15 (uv-managed), pydantic 2.13.5, pytest 9.1.1, ruff 0.16.10, uv 0.12.23.
- Tests cover: schema rules (identity, slots, evidence, clarification, pickup/address, cash change,
  cancellation), no price fields + extra-field rejection on every contract, language-neutral enum codes,
  quote arithmetic and strict cents, tool results and mock tools, protocol conformance, invalid model output
  kept not raised, router request limits/identical wording/parsing/abstention/repairs, every sample valid
  and grounded, grounding checks catch each error type, scenario coverage, taxonomy doc ↔ code sync,
  sealed test guard.

## Environment notes

- The machine had only Python 3.9. `brew install uv` started compiling cmake from source, so it was
  stopped (nothing was installed by it). uv 0.12.23 was installed from its official GitHub release
  (sha256 verified) to `~/.local/bin`; it manages Python 3.12 and the project venv (`.venv`).
- `requires-python >=3.12` (Julia-1 needs ≥ 3.11; 3.12 for `type` aliases).

## Decisions (Julian, 2026-10-07, answers to the M0 open questions)

1. **Snapshot output approved:** the model outputs the full order; code derives the patch.
2. **Menus:** Corner Patty and Halfmoon Pizza become 2 of the 3 real menus. The pizzeria menu must cover
   the toppings, sizes and drinks used in the PIZZA dataset (amazon-science/pizza-semantic-parsing-dataset)
   so it can be converted in M2. The held-out menu must be new.
3. **Customer name** stays optional in the schema. Added the per-business setting
   `name_required_for_pickup` (menu schema `menu@0.2`, default false, tested); M1 enables it for one business
   so missing-name clarifications get tested. Annotation guide and SCHEMA.md updated.
4. **Samples** may be few-shot examples but never appear in any evaluation (rule in CLAUDE.md; the M3 eval
   loader must reject `split: sample`, with a test).
5. **Test sets are committed**, sealing is enforced in code. **Exception: PIZZA data is never committed**
   (CC-BY-NC-4.0, no redistribution): only a download + conversion script. `data/external/` is gitignored
   and a test fails if anything under it is tracked. The license will be checked against the dataset's own
   LICENSE file when the script is written (M2).
6. **Frontend stack approved** (Vite + Preact + TypeScript, FastAPI). Set up in **M2** for the
   annotation/review tool, not M8. ARCHITECTURE.md and AGENTDESK_REUSE.md updated.
7. **Prices** are re-verified against each provider's official page before its first paid run.

## Next: Milestone 1

Menus (3 businesses incl. a pizzeria with half-and-half and a café/bakery, + 1 held-out menu) under
`data/menus/`; `core/pricing.py` implementing `PricingEngine` (variants, modifiers, combos, half-and-half
rule, delivery fee/minimum) → `Quote`; `core/state.py` order transitions; `core/diff.py` snapshot → patch;
`core/replies.py` templates from verified results; rules baselines (regex + fuzzy menu matching extractor,
keyword router) implementing the M0 interfaces; deterministic tests. No model, no spend.
Also from the decisions: the pizzeria menu covers the PIZZA dataset's toppings, sizes and drinks (to be
checked against the dataset's vocabulary; reading it for this is fine, committing it is not); a new held-out
menu; `name_required_for_pickup` enabled for one business.

**M2 additions:** PIZZA download + conversion script (data stays in `data/external/`); FastAPI + Vite/Preact
set up for the annotation/review tool.
