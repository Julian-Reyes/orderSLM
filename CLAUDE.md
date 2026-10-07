# ShopRoute: working rules
Spec: shoproute-project-plan.md (authoritative). Status: PROGRESS.md. Read PROGRESS.md first each session.

## How to work
- One milestone per instruction. After each: update PROGRESS.md, run `make check`, commit.
- Run the tests before saying something works. Never weaken a test to make it pass.
- Pre-commit hook (`.githooks/pre-commit`) runs lint + tests. Enable with `git config core.hooksPath .githooks`. Never use `--no-verify`.
- Ask before: any spend over $2 (give an estimate first), adding major dependencies, downloading large models.
- Verify provider/model contracts, licenses and prices against official docs before integrating. Never invent APIs, capabilities, confidence values or results.
- Keep secrets out of the repo; maintain .env.example. Use ShopRoute-specific API keys.

## Non-negotiables
- Prices, fees and totals are computed in code (pricing engine), never by a model. Model output schemas have no price fields.
- Model proposals (schema/extraction.py) and verified results (schema/order.py, tool results) stay separate. The reply layer states only verified facts.
- Customer claims are not facts: "I already paid" is `customer_claims_paid`, never a confirmed payment.
- The test split is sealed: only `shoproute.paths.test_split_dir()` reaches it, and only with SHOPROUTE_UNSEAL_TEST set for a final eval. Never train, tune prompts or generate data from it.
- Every reported number comes from saved, reproducible outputs in `runs/`. Log provider, model, prompt version and data version for every run, and actual cost in docs/COSTS.md.
- No real customer chats anywhere in the repo or training data.
- Never commit third-party datasets (PIZZA is CC-BY-NC-4.0, no redistribution): only download + conversion scripts; data lives in gitignored `data/external/`.
- Samples (`split: sample`) may be few-shot examples in prompts but never appear in any evaluation.

## Conventions
- Python 3.12, Pydantic v2, `uv`. All backend/ML/eval code is Python.
- Money is integer cents (`Cents`, strict). Percentages are integers.
- Tools return `ToolOk | ToolErr` and never raise for business outcomes.
- "Now" comes from an injected `Clock`.
- Enum values are language-neutral codes; only message text, quotes and reply templates are per-language.
- Contracts use `extra="forbid"`. Bump the version constant in schema/common.py when a contract changes.
