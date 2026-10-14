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

Spec prices (stated as verified 2026-10-07). The M3 teacher candidates were re-checked against the official
pricing pages on **2026-10-14**; all match the spec. Re-check again on the day of each paid run.

| Model | Standard in / out per 1M | Discounted | Verified by OrderSLM |
|---|---|---|---|
| OpenAI `gpt-6-luna` | $0.10 / $0.50 (cached input $0.01) | Batch $0.05 / $0.25 | 2026-10-14, [OpenAI pricing](https://developers.openai.com/api/docs/pricing). Short context (≤ 272K input); long context costs more (not relevant here) |
| Google `gemini-3.1-flash-lite` | $0.25 / $1.50 (text in; output includes thinking tokens) | Batch $0.125 / $0.75 | 2026-10-14, [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Paid tier only: free-tier data is used to improve Google's products, paid-tier data is not |
| DeepSeek `deepseek-flash` | $0.30 / $1.20 peak (cache hit $0.006) | Off-peak $0.15 / $0.60 (cache hit $0.003) | 2026-10-14, [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing). Peak = 01:00–04:00 and 06:00–10:00 UTC Mon–Fri (excl. Chinese public holidays). `deepseek-flash` = DeepSeek-V4.1-Flash |
| Google `gemini-3.8-flash` (optional) | $0.75 / $3.75 until 2026-12-31, then $1.50 / $7.50 | Batch $0.375 / $1.875 (then $0.75 / $3.75) | 2026-10-14, [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Output includes thinking tokens |
| OpenAI Decisions (`gpt-6-luna`) | $0.10 per 1M input, no output charge | — | not yet (not on the OpenAI pricing page as of 2026-10-14; check the Decisions guide before M7) |
| Jev (TypeSafe) | input billed, price not documented; output free | — | not yet (M7) |
| Julia-1 | local, $0 | — | license (Apache 2.0) to confirm in M7 |

## Spend controls

- Separate OrderSLM API keys/projects, with provider-side spend caps where offered (record the cap here when set).
- Preflight estimate → priced pilot → compare pilot actual vs. estimate → bulk run.
- `LLM_CACHE=replay` reruns cost $0 (M3).
