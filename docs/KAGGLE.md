# Kaggle plan (until the Mac mini is ready)

Julian, 2026-10-16. This Mac is an Intel MacBook Pro (2017): PyTorch ≥ 2.3 has no Intel-Mac builds, and Julia-1
(torch ≥ 2.6, transformers 5.0.x), Qwen3.5 and Gemma 4 need recent versions. So everything that needs torch runs on
Kaggle for now. Hosted providers (OpenAI, Jev, …) keep running from this Mac.

## What Kaggle gives us (checked 2026-10-16)

Sources: Kaggle CLI docs on GitHub ([README](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md),
[kernels](https://github.com/Kaggle/kaggle-api/blob/main/docs/kernels.md),
[kernel metadata](https://github.com/Kaggle/kaggle-api/blob/main/docs/kernels_metadata.md),
[datasets](https://github.com/Kaggle/kaggle-api/blob/main/docs/datasets.md)). Kaggle's own notebook docs page didn't
render for us; the session and quota figures below come from a September 2026 review that quotes those docs.

- **Cost:** free. **GPU:** `NvidiaTeslaT4` (2 × T4, 16 GB each, the default GPU); others (A100, L4, H100…) exist but
  some are limited to certain competitions or admins.
- **Session limit:** 12 h for CPU and GPU sessions (docs, via the review). **Weekly GPU quota:** not published; shown
  in account settings, commonly ~30 h, resets weekly. Check it in settings.
- **Internet in a notebook** (to download models from Hugging Face) needs a verified phone number.
- **CLI** (`uv tool install kaggle`): token from kaggle.com/settings/api, stored outside the repo
  (`~/.kaggle/access_token` or `KAGGLE_API_TOKEN`). `kaggle datasets create` makes a **private** dataset by default;
  `kaggle kernels push -p <folder> [--accelerator NvidiaTeslaT4] [-t <seconds>]` runs a script remotely;
  `kaggle kernels status` / `kaggle kernels output -p <dir>` fetch the results.
- `kernel-metadata.json`: `id`, `title`, `code_file`, `language` (python), `kernel_type` (script), `is_private`
  (default true), `enable_gpu`, `enable_internet`, `machine_shape` (e.g. `NvidiaTeslaT4`), `dataset_sources`,
  `model_sources`, `kernel_sources`.

## How we use it: everything driven from this repo

No copy-pasting into notebooks. For each job:

1. **Build inputs locally** with the same code as everywhere else (identical prompts and wording), write them to a
   folder (JSONL), and upload as a **private** Kaggle dataset (`kaggle datasets create` / `version`).
2. **Push a script kernel** from `kaggle/<job>/` (script + `kernel-metadata.json`, `is_private: true`): it pins its
   packages, downloads the model at a pinned revision, runs, and writes raw outputs plus an environment record
   (torch / transformers / CUDA versions, GPU, model revision, timings) to `/kaggle/working/`.
3. **Pull the outputs** (`kaggle kernels output`) into `runs/<experiment>/<run_id>/` and **score them locally** with
   the same scorers as the hosted runs. Every number in a report comes from these saved outputs (CLAUDE.md).

Commands (`src/orderslm/kaggle_jobs.py`): `make kaggle-push JOB=<folder>` (new version of the staged private dataset,
waits until ready, pushes the kernel), `make kaggle-status JOB=…`, `make kaggle-pull JOB=…` (output →
`kaggle/<job>/output/`, gitignored). The kernel slug must differ from its dataset's slug: Kaggle answers
`409 Conflict` otherwise (found 2026-10-19), so kernels are named `<dataset>-run`.

**Job A commands:** `make julia-audit ARGS="export --set dev|train [--limit N]"` (stages `kaggle/julia-audit/upload/`
and a run dir `runs/label-audit/<time>-julia-<set>/`), `make kaggle-push JOB=julia-audit`, then after it finishes
`make kaggle-pull JOB=julia-audit` and `make julia-audit ARGS="import runs/label-audit/<id>"` (writes
`responses/julia-1/`, `kernel/` (env.json, outputs, log), `metrics.json`, `report.md`: the same scoring as Jev/Decisions).

### What may go to Kaggle (private datasets only)

| OK | Never |
|---|---|
| Synthetic training chats + teacher labels (ours) | The sealed test split (Source A test), until the final eval, and then only if Julian agrees |
| Dev conversations and menus as model input (ours) | PIZZA (CC-BY-NC-4.0, no redistribution) |
| Prompts, built requests, our code | API keys or `.env` (no job needs a secret) |

Gold answers stay local: scoring happens on this Mac.

## Jobs

| Job | Hardware | Needs | Est. time | Notes |
|---|---|---|---|---|
| **A. Julia-1 label audit (§11d)** | CPU (no GPU quota) | Julia-1 at rev `a85b1273`, torch ≥ 2.6, transformers 5.0.x | ~1 h | The same `DecisionRequest`s as Jev/Decisions (dev gold + 473 planted, then 2,356 training chats); one `predict(state, questions)` call per chat (the named-question API scores each question as its own row); ≤ 20 options, ≤ 48 tokens per option, 8,192 tokens per row. Checked at export (2026-10-19): longest option 19 tokens, longest row 624 tokens, so nothing is truncated (strict encoding on) |
| **B. M5 student bake-off (§9)** | 2 × T4 | Qwen3.5-0.8B / 2B, Qwen3-1.7B, Gemma 4 E2B; latest transformers | **actual 7.2 h** (Gemma 5.2 h of it) | Done 2026-10-20: `docs/STUDENT_BAKEOFF.md`. 20 dev chats zero-shot per model; scored locally. One process per model; SDPA `enable_gqa` off (else math-kernel OOM at ~8k tokens in fp32); per-GPU caps (total − 2 GiB) |
| **C. M6 LoRA training** | T4 (one per run; two runs can share the session) | Qwen3.5-0.8B / 2B; transformers 5.20.2, peft 0.21.2, fla-core 0.5.2 (`--no-deps`); torchao uninstalled (peft 0.21.2 refuses Kaggle's 0.10) | smoke test: one pass over single/train ≈ 3.1 h (0.8B, fla) / 3.9 h (2B, fla) on one T4 | Smoke test done 2026-10-21 (`make train-smoke`, `runs/train-smoke/20261021T145441Z`): fla's Triton kernels run on the T4 (sm 7.5; first call compiles ~4 min); fp16 stable (no non-finite loss; GradScaler skips the first ~7 updates while it finds its scale); peak 4.0 GB (0.8B) / 7.2 GB (2B) at 9.8k tokens |
| **C2. M6 training + dev scoring** (`kaggle/m6/`) | 2 × T4, one job per GPU | as C; dataset `JReyes33/orderslm-m6` (rows, resume checkpoints, adapters, dev requests) | ≤ 11.25 h per session, then resume | `make train ARGS="export --train … --score …"`, `make kaggle-push JOB=m6`, `make kaggle-pull JOB=m6`, `make train ARGS="import runs/train/<id>"`. Pull a session's output **before** pushing the next (the CLI only sees the latest version) |

### Known risks to check in the first run

- **Stuck in the queue (seen 2026-10-19):** a GPU version sat "queued" for 2 h while a fresh push started at once
  (twice). Rule: if queued > 20 min, push again and cancel the old version on the website (the CLI can't cancel, and
  `kernels status`/`output` only see the latest version; a `/<version>` suffix is ignored).

- **Package conflict:** Julia-1 pins `transformers>=5.0,<5.1`; Qwen3.5 asks for the newest transformers. So separate
  kernels, each with its own pins.
- **T4 has no bfloat16** (fp16 / fp32 only): small models in fp16 can overflow; fall back to fp32 for 0.8–2B models
  if outputs look broken. Gemma 4 E2B (5.1B with embeddings, ~10 GB in 16-bit) fits one T4 only in 16-bit.
- **Kaggle's preinstalled torch** may differ from what we pin; the kernel records the versions it actually ran.
- **Quota and session limits:** check the weekly GPU hours in settings before job B; jobs stay well under 12 h.
- **Julia-1 on CPU speed:** Supersonic reports ~33 ms per call on an Apple M4; Kaggle CPUs are slower, so a 1-chat test
  run comes first to time it.

## Julian's setup (one time)

**Done 2026-10-19:** account `JReyes33`, token in `~/.kaggle/access_token` (works: `kaggle datasets list --mine`),
weekly GPU quota 30 h, CLI installed (`kaggle` 2.2.4 via `uv tool install kaggle`). Phone verification: assumed done
(the token was issued); the first internet-enabled kernel will confirm it.

1. Kaggle account; **verify a phone number** (needed for internet in kernels and for GPUs).
2. kaggle.com/settings/api → **Generate New Token**, then save it outside the repo: `~/.kaggle/access_token`
   (or tell me and I'll walk through `kaggle auth login`). Never paste it into chat or `.env`.
3. Check the **weekly GPU quota** shown in settings.
4. Tell me your Kaggle username (for dataset and kernel ids).

Then: I install the CLI (`uv tool install kaggle`, outside the project), build job A's inputs, run a 1-chat timing
test, then the full Julia-1 audit; then job B.
