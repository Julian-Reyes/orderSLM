# Costs

Budget: **$5–10 USD total** (spec §14). Ask Julian before any single spend over $2. Every row in the
ledger comes from actual usage (provider dashboard or the run's recorded token counts × verified price),
never from an estimate. Estimates go in the "Planned" table and in each run's preflight output.

## Running total

| | Amount |
|---|---|
| Spent to date | **$4.4372** (smoke tests $0.0007; bake-off pilot $0.0968; second bake-off $0.5811; head-to-head $0.1225; prompt checks $0.1090; repeat run $0.0547; M4 mini-pilots $0.0317; M4 pilot p3 $0.5157; label prompt on dev $0.2298; M4 bulk b1 + mega m1 $1.9104; p3 relabel $0.3266; v0.6 dev check + targeted relabel + Jev smoke $0.3657; label audit dev $0.0925) |
| Remaining (of $10 ceiling) | $5.5628 |
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
| 2026-10-16 | M4 | DeepSeek flash none, Gemini flash-lite minimal, Haiku off-low | Mini-pilot generation, 5 chats each, `synth-write@0.1` (estimate $0.0211) | 27,180 / 2,529 | 0.006070 | recorded usage × verified price | `runs/synth/p1` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Mini-pilot labels, 14 chats, `teacher-label@0.1` (estimate $0.0343) | 151,044 / 7,362 | 0.010185 | recorded usage × verified price | `runs/synth/p1` |
| 2026-10-16 | M4 | same 3 generators | Second mini-pilot after fixes (cards 0.2, `synth-write@0.2`), 5 each | 25,285 / 2,769 | 0.005425 | recorded usage × verified price | `runs/synth/p2` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Second mini-pilot labels, 15 chats, `teacher-label@0.2` | 152,730 / 8,144 | 0.010055 | recorded usage × verified price | `runs/synth/p2` |
| 2026-10-16 | M4 | DeepSeek 200, Gemini 200, Haiku 100 | Pilot generation, 500 cards (cards 0.3, `synth-write@0.2`; estimate $0.7717, projection ~$0.25) | 891,554 / 84,215 | 0.188789 | recorded usage × verified price | `runs/synth/p3` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Pilot labels, 498 chats, `teacher-label@0.2` (estimate $1.2052, projection ~$0.35) | 5,246,079 / 265,331 | 0.326883 | recorded usage × verified price | `runs/synth/p3` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | `teacher-label@0.2` scored on all 91 dev (estimate $0.2193) | 949,901 / 44,649 | 0.056934 | recorded usage × verified price | `runs/label-dev/20261016T153544Z-openai__gpt-6-luna@low` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | `teacher-label@0.3` scored on all 91 dev | 963,915 / 44,561 | 0.057721 | recorded usage × verified price | `runs/label-dev/20261016T160210Z-openai__gpt-6-luna@low` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | `teacher-label@0.4` scored on all 91 dev | 968,647 / 44,688 | 0.057834 | recorded usage × verified price | `runs/label-dev/20261016T160414Z-openai__gpt-6-luna@low` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | `teacher-label@0.5` scored on all 91 dev | 976,837 / 43,597 | 0.057376 | recorded usage × verified price | `runs/label-dev/20261016T161207Z-openai__gpt-6-luna@low` |
| 2026-10-16 | M4 | DeepSeek / Haiku / Gemini | Bulk generation, 1500 chats (cards 0.5, `synth-write@0.2`) | 2,572,995 / 232,379 | 0.371658 | recorded usage × verified price | `runs/synth/b1` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Bulk labels, 1481 chats (`teacher-label@0.5`) | 15,957,501 / 733,808 | 0.940673 | recorded usage × verified price | `runs/synth/b1` |
| 2026-10-16 | M4 | DeepSeek / Haiku / Gemini | Mega-menu generation, 396 chats (cards 0.5, `synth-write@0.2`) | 1,298,916 / 62,957 | 0.137161 | recorded usage × verified price | `runs/synth/m1` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Mega-menu labels, 394 chats (`teacher-label@0.5`) | 6,333,646 / 198,771 | 0.460865 | recorded usage × verified price | `runs/synth/m1` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Relabel pilot p3 with `teacher-label@0.5` (498 chats; v0.2 labels kept in `label-v0.2/`) | see calls log | 0.326613 | recorded usage × verified price | `runs/synth/p3` |
| 2026-10-16 | M4 | TypeSafe jev-latest (= jev-1.13.0) | Smoke test: 1 choice call, 15 intent labels, dev a-dev-053 msg 0 | 715 / 160 | 0.000031 (estimate) | 715 × $0.042/1M input (price from a Google summary, **not yet verified on TypeSafe's pricing page**; output reported free) | `runs/jev-smoke/20261016T174016Z` |
| 2026-10-16 | M4 | OpenAI Decisions (gpt-6-luna) | Smoke test: 1 choice call, 15 intent labels, dev a-dev-053 msg 0 | 396 / 0 | 0.000040 | 396 × $0.10/1M input (verified) | `runs/decisions-smoke/20261016T183457Z` |
| 2026-10-16 | M4 | Jev + OpenAI Decisions | Label audit on dev (`label-audit@0.1`): 91 gold + 473 planted | 368,163 + 283,513 / 0 | 0.044358 | input × price (Jev price unverified) | `runs/label-audit/20261016T183925Z-dev` |
| 2026-10-16 | M4 | Jev + OpenAI Decisions | Label audit on dev (`label-audit@0.2`): 91 gold + 473 planted | 395,085 + 310,379 / 0 | 0.048166 | input × price (Jev price unverified) | `runs/label-audit/20261016T185011Z-dev` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | `teacher-label@0.6` scored on all 91 dev | see manifest | 0.058087 | recorded usage × verified price | `runs/label-dev/20261016T173049Z-openai__gpt-6-luna@low` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Relabel p3 chats hit by the v0.6 rule (`teacher-label@0.6`, ids in `relabel_v0.6_ids.json`) | see calls log | 0.064876 | recorded usage × verified price | `runs/synth/p3/calls/20261016T173321Z-label.json` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Relabel b1 chats hit by the v0.6 rule (`teacher-label@0.6`, ids in `relabel_v0.6_ids.json`) | see calls log | 0.149907 | recorded usage × verified price | `runs/synth/b1/calls/20261016T173516Z-label.json` |
| 2026-10-16 | M4 | openai/gpt-6-luna@low | Relabel m1 chats hit by the v0.6 rule (`teacher-label@0.6`, ids in `relabel_v0.6_ids.json`) | see calls log | 0.092768 | recorded usage × verified price | `runs/synth/m1/calls/20261016T173914Z-label.json` |

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
| OpenAI `gpt-6-luna` | $0.10 / $0.50 (cached input $0.01, cache writes $0.125; cache-write price first seen 2026-10-16) | Batch $0.05 / $0.25 (cache writes $0.0625) | 2026-10-14, re-checked 2026-10-16 (all four models unchanged), [OpenAI pricing](https://developers.openai.com/api/docs/pricing). Short context (≤ 272K input); long context costs more (not relevant here) |
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
