# Costs

Budget: **$5–10 USD total** (spec §14). Ask Julian before any single spend over $2. Every row in the
ledger comes from actual usage (provider dashboard or the run's recorded token counts × verified price),
never from an estimate. Estimates go in the "Planned" table and in each run's preflight output.

## Running total

| | Amount |
|---|---|
| Spent to date | **$0.9648** (smoke tests $0.0007; bake-off pilot $0.0968; second bake-off $0.5811; head-to-head $0.1225; prompt checks $0.1090; repeat run $0.0547) |
| Remaining (of $10 ceiling) | $9.0352 |
| Prepaid credit bought (not spend) | $12.00 (OpenAI $5, Anthropic $5, DeepSeek $2) |

## Ledger (actual)

| Date | Milestone | Provider / model | What | Tokens in / out | Cost (USD) | Source | Run id |
|---|---|---|---|---|---|---|---|
| 2026-10-07 | M0 | none | No API calls, downloads or training in M0 | 0 / 0 | 0.00 | — | — |
| 2026-10-15 | M3 | 4 teacher candidates, 1 call each | Smoke test (`smoke@0.1`): keys, endpoints, JSON output | 456 / 71 | 0.000107 | recorded usage × verified price | `runs/smoke/20261015T173802Z` |
| 2026-10-15 | M3 | anthropic/claude-haiku-5-5 | Smoke re-run after fixing Haiku's lowest setting (thinking disabled, effort low) | 272 / 21 | 0.000038 | recorded usage × verified price | `runs/smoke/20261015T174904Z` |
| 2026-10-15 | M3 | 12 reasoning variants, 1 call each | Smoke `smoke@0.2`: every variant accepted by its API | 1,650 / 637 | 0.000595 | recorded usage × verified price | `runs/smoke/20261015T175548Z` |
| 2026-10-15 | M3 | luna, Gemini, DeepSeek variants (8) | Teacher bake-off pilot, 5 dev conversations (Haiku calls rejected: HTTP 400, not billed) | 378,426 / 28,139 | 0.060176 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T180115Z-pilot5` |
| 2026-10-15 | M3 | Haiku 5.5 variants (4) | Pilot re-run after prompt-only JSON fix; the other 48 calls replayed from cache ($0) | 265,414 / 20,130 | 0.036619 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T180442Z-pilot5` |
| 2026-10-15 | M3 | all 12 variants | Second bake-off: 35 new dev conversations, prompt `teacher-extract@0.2` (estimate $1.52, projection $0.68) | 4,191,197 / 326,377 | 0.581124 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T182916Z-full-skip5` |
| 2026-10-15 | M3 | luna low, Haiku on-medium | Head-to-head: the 51 remaining dev conversations, prompt v0.2 (estimate $0.26) | 1,106,379 / 84,838 | 0.122479 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T185040Z-full-remaining` |
| 2026-10-15 | M3 | openai/gpt-6-luna@low | Prompt v0.3 check (no items for past orders) on all 91 dev | 893,481 / 39,511 | 0.054384 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T190341Z-full-all` |
| 2026-10-15 | M3 | openai/gpt-6-luna@low | Prompt v0.4 check (plain pending has no evidence) on all 91 dev | 898,031 / 39,946 | 0.054654 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T191233Z-full-all` |
| 2026-10-15 | M3 | openai/gpt-6-luna@low | Repeat of the v0.4 run, cache off: run-to-run variation | 898,031 / 39,990 | 0.054679 | recorded usage × verified price | `runs/teacher-bakeoff/20261015T192653Z-full-all` |

## Prepaid credit (purchases, not spend)

Buying credit is not spending it: spend is counted only in the ledger above, from actual usage.

| Date | Provider | Amount (USD) | Why | Notes |
|---|---|---|---|---|
| 2026-10-15 | OpenAI (OrderSLM project) | 5.00 | Leave the free tier (50 requests/day, small batch queue) | Account moved to a paid usage tier; `gpt-6-luna` now 5,000 RPM, 2M TPM, 20M batch-queue TPD |
| 2026-10-15 | Anthropic | 5.00 | API credit for the Haiku 5.5 teacher candidate | |
| 2026-10-15 | DeepSeek | 2.00 | Prepaid balance for `deepseek-flash` | The balance is DeepSeek's only spend cap |

## Planned (estimates, spec §14)

| Item | Milestone | Planned | Notes |
|---|---|---|---|
| Teacher bake-off (~40 dev conversations × 12 variants) | 3 | ≈ $0.70 | Pilot measured $0.0968 for 5 × 12 (incl. one Haiku retry); second run 35 × 12 with prompt v0.2 projected ≈ $0.68 from measured cost/conversation. Gemini's implicit cache hits are billed at full input price in our numbers: Google says the savings are "passed on" but not at which rate (caching price $0.025/M). Compare with the Google Cloud bill. |
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
| Google `gemini-3.1-flash-lite` | $0.25 / $1.50 (text in; output includes thinking tokens); context caching $0.025 (verified 2026-10-15) | Batch $0.125 / $0.75 (caching $0.0125) | 2026-10-14, [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Paid tier only: free-tier data is used to improve Google's products, paid-tier data is not |
| DeepSeek `deepseek-flash` | $0.30 / $1.20 peak (cache hit $0.006) | Off-peak $0.15 / $0.60 (cache hit $0.003) | 2026-10-14, [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing). Peak = 01:00–04:00 and 06:00–10:00 UTC Mon–Fri (excl. Chinese public holidays). `deepseek-flash` = DeepSeek-V4.1-Flash |
| Anthropic `claude-haiku-5-5` | $0.10 / $0.50 for prompts ≤ 100K tokens (cache hit $0.01); prompts > 100K: $0.50 / $2.50 | Batch $0.05 / $0.25 | 2026-10-15, [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing). Added as a teacher candidate 2026-10-15 (spec §8) |
| Google `gemini-3.8-flash` (optional) | $0.75 / $3.75 until 2026-12-31, then $1.50 / $7.50 | Batch $0.375 / $1.875 (then $0.75 / $3.75) | 2026-10-14, [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Output includes thinking tokens |
| OpenAI Decisions (`gpt-6-luna`) | $0.10 per 1M input, no output charge | — | not yet (not on the OpenAI pricing page as of 2026-10-14; check the Decisions guide before M7) |
| Jev (TypeSafe) | input billed, price not documented; output free | — | not yet (M7) |
| Julia-1 | local, $0 | — | license (Apache 2.0) to confirm in M7 |

## Spend controls

- Separate OrderSLM API keys/projects, with provider-side spend caps where offered (record the cap here when set).
- OpenAI (2026-10-15): OrderSLM project; key is Restricted (Responses/Chat completions: Request, Batch and
  Files: write, everything else None); project limited to `gpt-6-luna` only (the teacher candidate and the
  only model OpenAI Decisions accepts). Project budget cap: **$5/month** (set 2026-10-15).
- Anthropic: create a dedicated `orderslm` workspace (the Default Workspace cannot take spend limits, per
  Anthropic's workspace docs) with a monthly spend limit; key created inside it. Cap: **$5/month** (set 2026-10-15).
- Google (2026-10-15): `orderslm` Cloud project, billing on (paid tier). Key restricted to the Gemini API
  only (Google keys cannot be limited to one model; the model is pinned in config). Budget: **$5/month**,
  alerts plus a hard cap.
- DeepSeek (2026-10-15): prepaid balance **$2** is the cap.
- These provider caps are backstops (up to $15/month post-paid plus prepaid balances). The project ceiling
  above ($10 total) and "ask before any single spend over $2" still govern actual spending.
- Preflight estimate → priced pilot → compare pilot actual vs. estimate → bulk run.
- `LLM_CACHE=replay` reruns cost $0 (M3).
