# Costs

Budget: **$5–10 USD total** (spec §14). Ask Julian before any single spend over $2. Every row in the
ledger comes from actual usage (provider dashboard or the run's recorded token counts × verified price),
never from an estimate. Estimates go in the "Planned" table and in each run's preflight output.

## Running total

| | Amount |
|---|---|
| Spent to date | **$0.00** |
| Remaining (of $10 ceiling) | $10.00 |

## Ledger (actual)

| Date | Milestone | Provider / model | What | Tokens in / out | Cost (USD) | Source | Run id |
|---|---|---|---|---|---|---|---|
| 2026-10-07 | M0 | none | No API calls, downloads or training in M0 | 0 / 0 | 0.00 | — | — |

## Planned (estimates, spec §14)

| Item | Milestone | Planned | Notes |
|---|---|---|---|
| Teacher bake-off (~40 dev conversations × 3–4 models) | 3 | < $1 | Priced pilot first; preflight estimate from measured tokens. |
| Synthetic generation + bulk labeling (1–2k conversations) | 4 | $1–4 | 200-conversation pilot first; batch APIs where available. Ask if > $2. |
| Router benchmark (Jev, OpenAI Decisions) | 7 | < $1 | Jev input price not in its docs (spec §11): confirm before running. |
| Decision-provider roles + teacher-LLM comparisons (label audit, order checker, narrowing) | 4, 6, 7 | estimate first | Spec §11 b–e; ask before any single spend over $2. |
| Training compute | 6 | $0 | Free Colab/Kaggle GPUs; ask before renting anything. |
| Buffer | — | remainder | |

## Prices to re-verify before spending

Copied from the spec (stated as verified 2026-10-07 from official pages). **Not re-verified in M0** (no
provider integration yet). Re-check each against the official pricing page on the day of the run and
record the URL and date here.

| Model | Standard in / out per 1M | Discounted | Verified by OrderSLM |
|---|---|---|---|
| OpenAI `gpt-6-luna` | $0.10 / $0.50 | Batch $0.05 / $0.25 | not yet |
| Google `gemini-3.1-flash-lite` | $0.25 / $1.50 | Batch $0.125 / $0.75 | not yet (free tier data is used by Google: don't use it) |
| DeepSeek `deepseek-flash` | $0.30 / $1.20 peak | Off-peak $0.15 / $0.60 | not yet |
| Google `gemini-3.8-flash` (optional) | $0.75 / $3.75 (promo to 2026-12-31) | Batch $0.375 / $1.875 | not yet |
| OpenAI Decisions (`gpt-6-luna`) | $0.10 per 1M input, no output charge | — | not yet |
| Jev (TypeSafe) | input billed, price not documented; output free | — | not yet |
| Julia-1 | local, $0 | — | license (Apache 2.0) to confirm in M7 |

## Spend controls

- Separate OrderSLM API keys/projects, with provider-side spend caps where offered (record the cap here when set).
- Preflight estimate → priced pilot → compare pilot actual vs. estimate → bulk run.
- `LLM_CACHE=replay` reruns cost $0 (M3).
