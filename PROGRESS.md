# Progress

Read this first each session. Spec: `orderslm-project-plan.md` (authoritative; replaces the Pedido Fácil plan).

_Last updated 2026-10-23._

## Start here next session

_Updated 2026-10-22 (M6 session 1 imported)._

- **M5 student bake-off done (2026-10-20, free on Kaggle 2 × T4):** `docs/STUDENT_BAKEOFF.md`, run
  `runs/student-bakeoff/20261019T182539Z/`. **Decision: keep Qwen3.5-0.8B + 2B** (no candidate clearly better, tooling
  works). Zero-shot nobody writes valid labels; Qwen3.5-2B is closest (JSON 19/20, type slips, item ids F1 0.75 vs
  teacher), Gemma 4 E2B 0.73 but JSON broken 9/20 and ~15 min per answer (fp32 offload), Qwen3-1.7B 0.47 (wrong
  structure), Qwen3.5-0.8B loops to the token limit 20/20. M6 risk: if the 0.8B still fails after LoRA, Qwen3-1.7B is
  the fallback. **Julian, 2026-10-20: release option (b) for now** (train on the luna labels, weights private).
- **M6 step 1, training data (2026-10-20, free):** `make student-data` → `runs/student-data/student-data@0.1/`
  (manifest committed; jsonl gitignored, sha256 in the manifest). Julian: **full chats only** (no per-prefix rows
  unless the student struggles mid-chat); **two students, Qwen3.5-0.8B + 2B**, the 2B trained twice (single vs
  mixed, §11e). Prompt `student-extract@0.1` (~1.1k chars of instructions vs the teacher's ~23k + schema) + menu +
  chat; target `StudentOutput` = last customer message's intent + the teacher's raw `ModelOrder`. Sets: `single`
  (p3 + b1) 1,865 train / 98 valid; `mixed` (+ m1) 2,236 / 118; same valid chats (seeded 5%); 2 audit exclusions
  left out. Row size p50 ~11.2k chars (~3k tokens), max 33k (food-court menu); answer p50 1.2k chars. Format:
  `{"messages": [...]}` (Unsloth/TRL and MLX-LM). Note: one row per chat means the intent target is the *last*
  message's (40% PLACE_ORDER, 18% CONFIRM, 17% SMALL_TALK; UNKNOWN 14 rows). **Julian, 2026-10-20: keep it as
  is** (the order often can't be labeled until the end; the student labels each message as it arrives). After
  training, **score the student at every customer message of dev** (dev gold has a box per message); if mid-chat
  boxes are weak, add the free box-only rows from the teacher's per-message intents and retrain.
- **Mac mini ready (2026-10-21):** Apple **M1, 16 GB**, macOS 15.6.1, 84 GB free. Clone at
  `~/Documents/GitHub/orderslm` on `milestone-4`, hooks + postBuffer set, `uv sync` + `make check` pass,
  `make student-data` rebuilt: counts and sha256 match this clone. Julian runs Claude Code on the Mac mini from now.
- **MLX smoke test (2026-10-21, $0): stock mlx-lm can't train Qwen3.5 on our rows on the M1 16 GB.** Added the
  optional `mlx` dependency group (`mlx-lm[train]==0.32.2`, Apple Silicon only; `make check` doesn't need it),
  `make mlx-smoke` (`src/orderslm/train/mlx_smoke.py`: throughput + longest-row phases, `--probe` lengths).
  Qwen3.5-0.8B downloaded to `models/qwen3.5-0.8b` (rev `2fc06364`, sha256 matches HF). Validation forward works
  (loss 1.533 on 2 rows), but the **first training step runs out of GPU memory**. Probe (one step, random tokens):
  128 → 2.7 s / 2.5 GB, 512 → 11.6 s / 5.0 GB, 1,024 → 32 s / 9.3 GB, 1,536 → 74 s / 14.3 GB (GPU limit 11.45 GB);
  our rows: p50 3.2k, max 6.3k (single) / 9.8k (mixed) tokens. Cause: the Gated DeltaNet Metal kernel has no backward,
  so training uses a per-token Python loop that keeps a 1 MB state per token per layer (~9.6 MB/token). Known
  upstream (mlx-lm #1956, PR #1870 chunkwise training path; mlx #3539). Details: `runs/mlx-smoke/NOTES.md`.
  Token counts (Qwen3.5 tokenizer): single train 7.09M tokens/epoch, mixed 10.48M. 2B not downloaded.
  **MLX patch (Julian: option 1, from PR #1870):** `src/orderslm/train/gated_delta_patch.py` vendors the PR's
  chunkwise gated delta rule (commit `3b04b9f1`, MIT, attributed) with the 8×8 base-block fix for the ~8k-token
  Metal resource limit; 18 unit tests; real-row check (`--check`, `runs/mlx-smoke/20261021T144642Z-…/check.json`):
  forward 3× faster than stock at 9.8k tokens (17 s vs 66 s, 7.8 vs 12.7 GB); bf16 logits differ 1.7% from stock,
  the same as the inference kernel vs stock (rounding); **fp32: 3e-6 logits, 7e-6 LoRA gradients**. **Parked
  (Julian, 2026-10-21): Kaggle is the primary training path**; probe re-run and the 12 h check not done.
  Deployment note: mlx-lm's `--export-gguf` covers only Llama/Mistral-style fp16, so Qwen3.5 GGUF needs llama.cpp's
  `convert_hf_to_gguf.py` on the fused HF-format model (check its Qwen3.5 support when we get there).
- **Kaggle LoRA smoke test (job C, 2026-10-21, $0, ~0.5 h GPU): done; Kaggle is the training path.**
  `make train-smoke` (`src/orderslm/train/kaggle_smoke.py`, kernel `kaggle/train-smoke/run.py`), run
  `runs/train-smoke/20261021T145441Z/` (`report.md`, `summary.json`, `kernel/`; `attempt-1/` = first push, every
  phase failed on import: peft 0.21.2 refuses Kaggle's torchao 0.10, so the kernel now uninstalls torchao). Private
  dataset `JReyes33/orderslm-student-data` (single + mixed train rows). Setup: 1 T4 per phase, fp16 base + fp32
  LoRA r 8 / alpha 16 on all linear layers (0.8B 5.4M trainable, 2B 8.4M), AdamW 1e-4, GradScaler, grad
  checkpointing, batch 1, answer-only logits (`logits_to_keep`). torch 2.11, transformers 5.20.2, peft 0.21.2,
  triton 3.6, fla-core 0.5.2 (`--no-deps`). Mac mini's Kaggle token + CLI set up (`~/.local/bin/kaggle`).
  - **Kernels:** without fla, transformers falls back to its PyTorch `torch_chunk_gated_delta_rule` (recorded from
    the wrapper); with fla installed it calls `fla.ops.gated_delta_rule.chunk.chunk_gated_delta_rule`, which **runs
    on the T4** (sm 7.5) and matches the PyTorch version to 5.5e-4 in fp16 (outputs and q/k/v gradients). First call
    compiles for ~4 min; a new length range compiles again once (0.8B step 8: 30 s instead of ~9 s).
    `causal-conv1d` not installed (source-only; the conv stays on PyTorch).
  - **fp16:** stable. No non-finite loss in 56 steps; the GradScaler skipped the first 7 updates of each run
    (overflowing gradients while its scale fell 65,536 → 512; 2B also skipped 2 more at steps 8–9), normal dynamic
    loss scaling. Loss on the rows seen fell 1.8 → 0.3–0.4 (0.8B) and 1.6 → 0.66 (2B).
  - **Speed / memory** (steady = random rows after 2 warm-up steps; per-token cost from the same rows):

    | Run | s per 1k tokens (median) | Peak GB, random rows | 6,323 tokens | 9,805 tokens | One pass single/train (7,085,224 tokens), 1 T4 |
    |---|---:|---:|---|---|---:|
    | 0.8B, PyTorch delta rule | 1.74 (grows with length: ~1.6 at 2–3k, ~2.2 at 5.8k) | 3.76 | 14.6 s, 4.0 GB | 30.9 s, 5.2 GB | **3.7 h** |
    | 0.8B, fla | 1.61 (flat ~1.55 at 2–6k) | 3.72 | 9.7 s, 3.7 GB | 39.0 s*, 4.0 GB | **3.1 h** excl. the one compile step (3.7 h incl.) |
    | 2B, fla | 2.04 | 6.15 | 11.9 s, 6.3 GB | 20.2 s, 7.2 GB | **3.9 h** |

    \* probably a compile for a new length range (the 2B's 9.8k step took 20 s); to confirm in the first real run.
    Everything fits easily in a T4's 15 GB, so the two T4s can train the 0.8B and the 2B side by side in one session
    (the session limit is 12 h). Mixed (10.48M tokens) ≈ 1.5 × single. Estimates scale measured speed to total
    tokens; they are not a measured full run.
  - **MLX:** parked (patch kept and verified; see above).
- **M6 full LoRA training (Julian, 2026-10-21): session 1 ran 2026-10-21 17:40 → 2026-10-22 01:47 UTC, imported
  2026-10-22 (on the MacBook; Julian: either machine, once the other has pushed). Session 2 ran 2026-10-22 12:33 →
  23:49 UTC, imported 2026-10-23 (only the 2B mixed ran; see below). **Session 3 staged, not pushed** (waiting for
  Julian's OK): `make kaggle-push JOB=m6`; when it ends: `make kaggle-pull JOB=m6`,
  `make train ARGS="import runs/train/20261023T114452Z"`.**
  Settings: fla + fp16; up to 2 epochs, validation loss every half epoch (and at step 0 as the base reference), best
  checkpoint by validation loss; LoRA r 16 / alpha 32 / dropout 0.05 on all linear layers (attention, MLP, Gated
  DeltaNet `in_proj_qkv/z/a/b`, `out_proj`; confirmed in the local test); LR 2e-4 (0.8B) / 1e-4 (2B), 5% warmup,
  cosine; effective batch 8 (grad accumulation; each row's mean token loss weighs the same); AdamW, no weight decay,
  clip 1.0; seed 20261021 (same data order for all students). Spec check: no conflict; documented differences: LR
  per student (§10 allows with documentation), own loop on transformers + PEFT instead of TRL/Unsloth (§13), one
  seed (§10's 3 seeds are for the final config, "if time allows").
  - Code: `make train ARGS="export --train … [--score …]"` / `import runs/train/<id>` (`train/kaggle_train.py`),
    kernel `kaggle/m6/run.py` (dataset `JReyes33/orderslm-m6`, kernel `JReyes33/orderslm-m6-run`), dev scoring
    `eval/student_dev.py` (`make student-dev ARGS="report …"`). Each session stops itself at 11.25 h (Kaggle keeps
    output only when a session ends normally), saving `last/` (LoRA, AdamW, scheduler, scaler, data position, RNG)
    every 20 steps and at the stop; the next export stages `last/` and resumes exactly. Weights go to gitignored
    `models/m6/<student>/{best,last}`; `runs/train/<session>/` keeps config, steps, validation, adapter sha256.
  - Tests: local CPU run of the real kernel on a tiny random Qwen3.5 (real tokenizer + rows; scratch venv torch
    2.14.1 CPU): paused at step 2 + resumed = bit-identical LoRA tensors and validation curve vs uninterrupted;
    scoring ran in parallel. Scorer positive control: the teacher's dev labels as per-message answers reproduce its
    dev numbers exactly (`tests/test_student_dev.py`). 484 tests pass.
  - Dev scoring: 268 requests (every customer message; chat cut after it, same builder as the training rows);
    intents vs gold per message (split last vs earlier), order at the last customer message (3 dev chats end on a
    business message: the call stops at the last customer message, as in training), contract validity everywhere;
    greedy, max 1,536 new tokens.
  - Plan: **session 1** = `runs/train/20261021T170010Z/` (T4 #0 0.8B single ~6.5 h, T4 #1 2B single ~8 h);
    **session 2** = `export --train qwen3.5-2b-mixed --score qwen3.5-0.8b-single,qwen3.5-2b-single`; session 3 if
    the mixed run pauses (+ its scoring). Secrets check on the staged upload + kernel: clean (0 hits).
  - **Session 1 result** (`runs/train/20261021T170010Z/`, `summary.json`; $0; weights in `models/m6/`):
    - **2B single: done**, 468/468 steps (2 epochs), 7.76 h of steps, 507 tokens/s, peak GPU 6.7 GB, 6 skipped
      updates (GradScaler warm-up). Validation loss 1.329 (base) → 0.0154 / 0.0113 / 0.0093 / **0.0089** at
      0.5 / 1 / 1.5 / 2 epochs: best = last (adapter sha256 `2366b279…`).
    - **0.8B single: killed after step 147** (~0.63 epoch, ~2 h in, 19:50 UTC): exit −9 (SIGKILL; one job per GPU, so
      bash had exec'd Python), no Python error, GPU peak 3.4–4.0 GB (normal). Most likely the host's out-of-memory
      killer; **not confirmed** (session 1 logged no host RAM). Not the data: step 148's rows are ordinary
      (7.7k–19.3k chars, rebuilt from the seed). Validation 1.479 (base) → **0.0162** at 0.5 epoch; 625 tokens/s;
      `last/` at step 140 (steps 141–147 get redone on resume).
    - Validation loss is next-token loss on the teacher's labels for the 98 held-back training chats: it shows the
      format is learned, not dev accuracy. Dev scoring is the result.
  - **Host-RAM logging added to the kernel (2026-10-22):** `memory.jsonl` every 30 s (MemAvailable, Shmem = tmpfs,
    cgroup use/limit, RSS of each GPU's process tree), `rss_gb` + `mem_available_gb` per step, `/tmp` and
    `/kaggle/working` filesystem types in env.json (models download to `/tmp/models`: if that is tmpfs, ~6.4 GB of
    model files sit in RAM; unverified). A failed reading is logged and never ends the session. Import copies
    `memory.jsonl` and summarizes it (`host_memory` in summary.json). Tests: `tests/test_m6_kernel.py`; the `/proc`
    readers are only exercised on Kaggle (no Linux here).
  - **Session 2 = `runs/train/20261022T123143Z/`, pushed to Kaggle 2026-10-22 ~12:35 UTC (kernel version 2, RUNNING;
    secrets check clean, dev requests all Source A dev):** `export --train qwen3.5-2b-mixed,qwen3.5-0.8b-single --score
    qwen3.5-2b-single` → T4 #0 2B mixed (~21M tokens at 507 tok/s ≈ 11.5 h + validation: pauses at the 11.25 h stop
    near ~1.8 epochs); T4 #1 0.8B resumed at step 140 (~4.7 h), then dev scoring of the 2B single (268 requests,
    untimed; guess 1–3 h). Same two-trainings-at-once setup as the kill, so it may repeat; checkpoints every 20 steps
    bound the loss and the new logging should show the cause. **Session 3:** finish 2B mixed (~1 h) + score the
    0.8B and 2B mixed. GPU quota 30 h/week: session 1 ≈ 8.1 h, session 2 ≈ 11.3 h (check the remaining quota first).
  - **Session 2 result** (`runs/train/20261022T123143Z/`, `summary.json`; $0):
    - **2B mixed: paused at the 11.25 h stop at step 534/560** (epoch 1.91), 10.84 h of steps, 514 tokens/s, peak GPU
      7.6 GB, 6 skipped updates. Validation loss 1.335 (base) → 0.0154 / 0.0114 / **0.0098** at 0.5 / 1 / 1.5 epochs
      (best = step 420, adapter sha256 `a5c9a74c…`); the 2-epoch validation comes with the last 26 steps.
    - **T4 #1 did nothing (our bug):** the 0.8B resume and the 2B single's scoring both failed within 2 minutes because
      the published dataset had **no `resume/` or `adapters/` folders**. The Kaggle CLI skips subfolders unless given
      `--dir-mode` (session 1 had none, so it didn't show). The import left `models/m6/qwen3.5-0.8b-single/` (session
      1's step-140 checkpoint) untouched. Cost: ~11 h of one T4, no data lost.
    - **Host RAM (new logging):** the 2B mixed's process grew **4.1 → 25.9 GB** through its first epoch (~10 MB per
      new training row, steady), then stayed flat through epoch 2 (rows repeat); lowest free RAM 6.5 GB of 33.7
      (cgroup limit 32.2). Our loop keeps nothing per row, so the growth follows new input lengths: most likely a
      kernel compile/autotune cache (fla/Triton). **Not confirmed.** This explains session 1's kill: two trainings
      growing at once pass 32 GB around the step where the 0.8B died (very likely; session 1 had no RAM log).
  - **Fixes (2026-10-23):** (1) `make kaggle-push` uploads subfolders (`--dir-mode zip`), then checks that Kaggle
    lists every staged file and refuses to start the kernel if any is missing. (2) The kernel checks every input
    run.json names before any job starts and ends at once if one is missing. (3) A training pauses cleanly (saving
    `last/`, status `paused` + `reason`) when free host RAM drops below 2 GB, rather than being killed. (4) `--score`
    may name a student trained in the same session: it is scored right after its training on the same GPU, from
    that session's best adapter, only if the training finished (else `skipped`). The kernel records the scored
    adapter's sha256 and the import checks it against the imported best. Tests: `tests/test_m6_kernel.py`;
    `make check` **474 passed** (the "484" above was a miscount: 470 at the previous commit).
  - **Kaggle GPU quota (checked by Julian 2026-10-23 ~12:00 UTC): 27.36 of 30 h used**, resets ~21:00 local today.
    The 19.4 h estimate above missed other GPU runs this week (smoke test, M5). Check the quota on the site before
    every push (the CLI can't show it): a session cut off by the quota likely loses all its output.
  - **Session 3a = `runs/train/20261023T115559Z/`, pushed 2026-10-23 12:00 UTC (kernel version 3, RUNNING; ends by
    ~13:50 UTC)** (fits the 2.6 h left; `export --train qwen3.5-2b-mixed --score
    qwen3.5-2b-single,qwen3.5-2b-mixed --deadline-hours 1.75`): T4 #0 finishes the 2B mixed (26 steps + 2-epoch
    validation, ~45 min) then scores it; T4 #1 scores the 2B single. Jobs stop at 1.75 h; scoring that doesn't
    finish still gives measured per-request timing (scoring doesn't resume across sessions). New export option
    `--deadline-hours` (default 11.25). Upload check worked: Kaggle lists all 16 staged files with their subfolders
    (`adapters/…`, `resume/…`); its first run tripped on a CLI warning line (fixed). Secrets scan 0 hits; input check passes. Next, after the reset: the 0.8B
    resume (step 140) + its scoring, and any scoring 3a didn't finish. (A first session-3 staging,
    `20261023T114452Z`, was replaced before pushing.)
- **Julian's standing rules (also in the other machine's Claude memory):** ask before every push (secrets check
  first); record every model/setting's counts, tokens, run and per-1k cost, before/after, for the website; end every
  task with a plain-English summary (changes + why, files, direct answers).

- **Git:** M0–M3 on `main` (GitHub's `main` matches local). M4, M5 and M6 so far are on branch **`milestone-4`**,
  **pushed 2026-10-20** after a secrets check (not merged; merge after M6). Ask Julian before every push, secrets
  check first. Large pushes need `git config http.postBuffer 524288000` (set in this clone).
- **Spend:** $5.80 of $10 (docs/COSTS.md). M4 so far: data generation, labeling, relabels, audits.
- **M4 state:** training data done: **1,963 single-menu + 391 mega-menu** labeled chats (`runs/synth/{p3,b1,m1}`,
  exclusions in `runs/synth/excluded.json`); label prompt `teacher-label@0.7`; label audit by Jev + OpenAI Decisions
  done (`runs/label-audit/`); every drop / repair / flag / catch rate: `make m4-report` → `runs/m4-report/`.
- **TERMS.md done (2026-10-19, late: spec §7 wanted it before bulk labeling):** `docs/TERMS.md`. DeepSeek and Julia-1
  allow training on outputs; Jev (TypeSafe MCA §2.3(b)) forbids distillation/imitation, so Jev output never becomes a
  label (audit use only is fine); OpenAI, Anthropic, Google forbid models that *compete* with theirs (our reading: a
  narrow order extractor doesn't). **Julian, 2026-10-19: option (b) or (c)** (no public weights trained on OpenAI labels); pick b vs c before M6 training, since (c) = relabel first. OpenAI's safe-harbour for classifiers needs the
  model *not distributed*, but §17 plans a Hugging Face release of weights (options a–d in TERMS.md).
- **Julia-1 dev audit on Kaggle (2026-10-19, free):** `runs/label-audit/20261019T135301Z-julia-dev` (same requests as
  Jev/Decisions, `label-audit@0.3`). Intents = gold **54.5%** (Jev 95.9%, Decisions 96.3%); correct orders flagged
  **45%** (Jev 5.5%, Decisions 0%); planted caught **49%** (Jev 89%, Decisions 78%): the order check is at chance, so
  Julia-1 is not useful as a label auditor with this wording. Top confusions: SMALL_TALK→PLACE_ORDER ×20,
  MODIFY→PLACE ×13, MENU_QUESTION→PLACE ×12. 5.3 min on 4 CPUs (p50 270 ms per chat). Train run: Julian to decide.
  Sanity check (`runs/label-audit/20261019T140603Z-julia-sanity`, 33 made-up clear cases): model card example right
  (billing, p 0.85), so the setup works; one-message intents 7/12 alone but 4/12 in the audit's chat format
  ("customer message [0]"); strong pull toward PLACE_ORDER ("thanks so much" → PLACE_ORDER); yes/no order checks 6/8
  with weak probabilities. Julian: Julia should work eventually (free); same wording for all providers unless an
  API-only field, which is reported as a separate "Julia-1 tuned" setting. (b) yes/no descriptions: on hold.
  **Tuning test on dev** (`runs/label-audit/20261019T141916Z-julia-variants-dev`, `make julia-variants`, one change
  each, same job): baseline 54.5% intents (rerun identical); short context (business msg before + customer msg) 19%;
  3 shuffled option orders 16–18% (averaged 17%); yes/no with descriptions: catches 57% but flags 57% of correct
  orders (still chance). Why: the baseline's 54.5% is mostly a PLACE_ORDER habit (picked 73% of the time; gold is
  60% PLACE_ORDER); its choices change with the option order (two shuffles agree on 34% of messages; all three on
  16%) and mean P(match) is 0.52 for correct vs 0.49 for planted orders. Verdict: Julia-1 doesn't read our 15 labels
  reliably; not usable as an auditor here.
  Pipeline: `make julia-audit` export/import, `make kaggle-push/status/pull JOB=julia-audit`.
- **Kaggle ready (2026-10-19):** user `JReyes33`, token works, CLI 2.2.4 installed, GPU quota 30 h/week. Next: build
  `kaggle/` + `make kaggle-push/pull`, job A (Julia-1 audit: 1-chat timing test, then dev + train), then job B (M5).
- **Still open:** per-prefix training rows (the intent at every customer turn + the order at that point): decide before
  M6. Julian's preferences: end every task with a plain-English summary (changes + why, files, direct answers); record
  every drop and catch rate for the reports/dashboard.
- **Case study:** every experiment records all numbers per model/setting (accuracy counts, tokens, run cost and per
  1,000, latency, before/after views) in `runs/<experiment>/` + a summary/chart-data JSON (Julian, 2026-10-15).

## Milestones

| # | Work | Status |
|---|---|---|
| 0 | AgentDesk inspection, layout, contracts, docs, interfaces + mocks, samples, tests | ✅ Done 2026-10-07 |
| 1 | Menus (3 + held-out), pricing engine, order state, rules baselines | ✅ Done 2026-10-07 |
| 2 | Annotation tool; PIZZA conversion; scenario cards → Claude-written dev/test (Source A); Julian's review; lock | ✅ Done 2026-10-14: dev 91/91 reviewed, test 58/199 reviewed (0 changed), test split locked (199, sha256 `3f09234131e3825d`); see "Test review and lock" |
| 3 | Teacher bake-off | ✅ Done 2026-10-15 (merged to main, not pushed): **teacher `openai/gpt-6-luna@low`**, prompt `teacher-extract@0.4`, code rules `core/finalize`; write-up `docs/TEACHER_BAKEOFF.md`; spend $0.96; details in "M3 so far" |
| 4 | Synthetic generation + labeling (order + intents; mega-menu share; label audit) | Data generated and labeled 2026-10-16 (p3 pilot, b1 bulk 1,476, m1 mega 391; M4 spend $2.69); label audit (§11d) open |
| 5 | Student bake-off | ✅ Done 2026-10-20 (on `milestone-4`, not pushed): **keep Qwen3.5-0.8B + 2B**; write-up `docs/STUDENT_BAKEOFF.md`; $0 (Kaggle) |
| 6 | LoRA training (intent + order) + distillation eval; order checker | Started 2026-10-20: training data built (`make student-data`); MLX smoke test 2026-10-21: stock mlx-lm OOM, PR #1870 patch verified then parked; **Kaggle T4 smoke test done 2026-10-21** (fla works, fp16 stable, one pass ≈ 3.1 h 0.8B / 3.9 h 2B); **session 1 2026-10-22**: 2B single done (val 0.0089), 0.8B killed at step 147; **session 2 2026-10-23**: 2B mixed paused at 534/560 (val 0.0098), 0.8B resume + scoring failed (dataset upload skipped subfolders; fixed); session 3a (2B mixed finish + 2B scoring, 1.75 h cap) |
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

- **Step 2, mini-pilots (2026-10-16, $0.0317 total).** Prices re-checked on the four official pages: unchanged,
  but OpenAI now lists a luna **cache-write price ($0.125/1M)**: added to config (it was billed as plain input).
  - `p1` (cards 0.1, `synth-write@0.1`, `teacher-label@0.1`): 15 chats, 14 kept (1 ended on a business message), 14/14
    labeled. Found: every address on "Maple" (mode collapse), a card repeating an item, Haiku skipping the
    confirm step, Gemini's "clean" style reading like a letter, one intent ("regular pls" answering a size question
    as MODIFY_ORDER).
  - Fixes: code picks the address (cards 0.2), no item twice in an order, `synth-write@0.2` (steps in order, card
    address, no letters, business doesn't assume details), trailing business messages trimmed and logged as a
    repair instead of a drop, `teacher-label@0.2` (answering a size question is PLACE_ORDER).
  - `p2`: 15/15 kept, 15/15 labeled, varied addresses. All 30 labels read by hand: no teacher errors found; the 5
    card disagreements were generator drift (greeting merged into the order message, Haiku again skipping the
    confirm: 2 of 2 correction-after-confirmation cards, a business asking for a default size). Cards 0.3: the card
    says "no size mentioned" for default sizes; a greeting is no longer an expected SMALL_TALK label.
  - Measured cost per 1,000 chats: generation DeepSeek $0.20 (off-peak; ×2 at peak), Haiku $0.32, Gemini $0.69;
    labels $0.61–0.84. Full pilot batch `p3` (cards 0.3) planned.

- **Step 3, pilot `p3` (2026-10-16, $0.5157: generation $0.1888, labels $0.3269; estimate $1.98, projection ~$0.6).**
  Report `runs/synth/p3/report.md`, summary `summary.json`, audit sample `audit.md`. Labeling ran with
  `--workers 8` (the rpm throttle is now thread-safe).
  - Yield: 498/500 chats kept (2 DeepSeek outputs echoed schema keys `"type":"object"`); 64 trailing business
    messages trimmed (DeepSeek 47); 493/498 labels kept (5 teacher errors caught by the checks: 2 ambiguous time
    with a kind, 3 quotes not in the chat).
  - Card agrees with label: Haiku 90/99 (91%), DeepSeek 180/194 (93%), Gemini 179/200 (90%) (after fixing the check:
    substitute = remove + add; re-confirming after a change is fine). Weakest scenarios for every generator:
    correction_after_confirmation (8/23: they change the order instead of confirming first) and unclear_message
    (2/10: they write clear "wrong chat" messages).
  - Hand review of all 48 original disagreements: ~30 generator drift, ~10 card wording/bugs (fixed in cards 0.4:
    "regular one" leaked into chats, address-gap contradiction, swap of an item for itself, payment-claim and
    unclear-message briefs), 3 check rules (fixed), **4 clear teacher errors** (dropped a kept combo; missed
    "sesame"; a menu question turned into an order line; an extra line from the leaked wording) + 3 debatable.
  - Cost per 1,000 chats: generation DeepSeek $0.13 (off-peak + cached prompt), Haiku $0.38, Gemini $0.63; labels
    $0.64–0.70 (input 66–70% cached). Labels dominate: 1,500 more chats ≈ $1.0 labels standard ($0.5 with Batch).
  - Style/diversity (customer text): Haiku most varied (distinct 3-grams 86%, distinct openers 39%), DeepSeek 78% /
    37%, Gemini 75% / 25% ("hey there" ×24) and wordiest (11.4 words/message). DeepSeek's "yo u guys open rn"
    openers make DELIVERY_QUESTION its third-largest intent (54 vs 14–18).

- **Label prompt v0.3 → v0.4 (2026-10-16, Julian approved fixes 1–3 from the audit; dev re-checks $0.0577 + $0.0578):**
  v0.3 (PLACE = adds, MODIFY = changes; answers take the request's label; garbled text → UNKNOWN, no items): intents
  263/268, orders 91/91, but "a name for a lookup" was over-applied (complaint/refund names → ORDER_STATUS). v0.4
  (an answer keeps its own request's label: status/complaint/refund; additions after a confirm are MODIFY):
  **intents 264/268 (98.5%), orders 90/91** (a-dev-038 "whatever i had to drink" varies between runs; v0.2 had it
  right). Remaining misses are run-to-run flips. **v0.4 is the bulk label prompt**; no more tuning on dev.
  Julian: "👍 SOUNDS GOOD" (a-dev-032) stays UNKNOWN. Open: a-dev-074 "hey ordering for the office" (gold
  PLACE_ORDER) is the same case as a-dev-075 (ruled SMALL_TALK).
- **Bulk decisions (Julian, 2026-10-16):** 1,500 more single-menu chats, **DeepSeek 1,000 / Haiku 250 / Gemini 250**,
  rebalanced toward rare intents (cards 0.5: non-order 35%, ~48 cards per rare intent); additions to a placed order
  add no order line; no Batch API (saving ~$0.50 isn't worth the build); a-dev-074 left to Claude → SMALL_TALK like
  a-dev-075 (logged review). Label prompt **v0.5** (order announcements are SMALL_TALK, placed-order additions add no
  items): dev orders **91/91**, intents **265/268 (98.9%)** (one of the gains is the a-dev-074 gold change).
- **Mega-menu (Julian: yes):** `make mega-menu` → `data/menus/mega/food-court.json` (34 items, 54 modifiers; coke/sprite
  merged, clashing cheese/avocado renamed; built by `orderslm/mega.py`, tested to equal the committed file). Not a
  4th regular menu (`load_menus()` excludes it; `load_menu("food-court")` finds it). Mega batch `m1` planned: 396
  cards (~20% of ~2,000 single-menu), 264/66/66.
- **Kaggle plan (2026-10-16, Julian: use Kaggle until the Mac mini is ready):** `docs/KAGGLE.md`. Torch jobs (A Julia-1
  audit on CPU, B M5 bake-off on T4, C M6 LoRA) run as private script kernels driven from this repo; inputs built
  locally and uploaded as private datasets (never test or PIZZA, no secrets); outputs pulled and scored locally.
  Waiting on Julian: Kaggle account + phone verification, API token in `~/.kaggle/access_token`, username, GPU quota.
- **Audit fixes (2026-10-16, Julian):** audit wording v0.3 (an earlier order the customer describes is not part of
  the record): dev false alarms Jev 5.5%, Decisions 0% (planted caught 89% / 78%). Label prompt **v0.7** (follow-ups
  keep the request's label; "did the payment go through" = PAYMENT_CLAIM; dev: 1 contract flake dropped, otherwise as
  v0.6); 67 audit-flagged chats relabeled. Re-audit of the training labels: orders flagged by both 31 → 13, intent
  messages both dispute 425 → 374. Excluded from training: syn-p3-0160, syn-b1-0356 (`runs/synth/excluded.json`).
  Training set: **1,963 single-menu + 391 mega-menu**. Every drop/repair/relabel/flag/catch rate: `make m4-report`
  → `runs/m4-report/m4_report.json` (dashboard data) + `M4_REPORT.md` (Julian: show drops in reports/dashboard).
  Real miss example for the write-up: a-dev-007 "no mayo" on a veggie burger dropped, judged matching by both.
- **Label audit by Jev + OpenAI Decisions (2026-10-16; `make label-audit`; Julia-1 waits for an Apple-Silicon Mac or
  Kaggle: this Intel Mac can't install torch ≥ 2.6).** Dev (`label-audit@0.2`, after fixing cancelled / no-order /
  unclear-item wording on dev): intents vs gold Jev 95.5%, Decisions 96.3% (teacher 98.9%); correct orders flagged
  Jev 12%, Decisions 2%; planted mistakes caught Jev 89%, Decisions 82% (weakest: dropped modification 22–35%).
  Train (runs/label-audit/20261016T185956Z-train, $0.60): intents = teacher 88%; orders flagged Jev 6.6%, Decisions 1.7%; both: 31 orders,
  425 intent messages. Hand check (`review.md` there): order flags ≈ 50% precision on chats with an order (7 real
  teacher errors; 17 false alarms from status chats that describe an earlier order); intent flags ≈ 24–36%
  (real: read-back "that's it" still SMALL_TALK, follow-ups in status/complaint/refund chats; the rest are Julian's
  PLACE/MODIFY and announcement conventions). Rates: Jev 120 rpm, Decisions 300 rpm (Julian).
- **Bulk run `b1` + mega `m1` (2026-10-16):** b1 generation $0.3714 (1,481/1,500 kept: DeepSeek 14 schema-echo
  outputs, 3 business prices, 1 exact duplicate), labels $0.9407 (1,476 kept, 5 dropped); m1 generation $0.1372
  (394/396), labels $0.4609 (391/394). Card agreement: b1 Haiku 91%, DeepSeek 95%, Gemini 92%; m1 91% / 94% / 94%.
  Rare intents now ≥ 36 messages each in b1 (UNKNOWN 36, REFUND_REQUEST 49, PAYMENT_CLAIM 61). DeepSeek's "u open
  rn" openers still inflate DELIVERY_QUESTION (244 of its messages). Reports: `runs/synth/{b1,m1}/report.md`.
- **Audit of p3 (2026-10-16, by Claude at Julian's request, `runs/synth/p3/audit_review.md`):** 30 chats: realistic
  28/30, intents fully right 26/30, order right 27/30. Teacher patterns for label prompt v0.3: PLACE vs MODIFY when
  adding a detail to an item being ordered; an answer takes the label of the request it serves; garbled text is
  UNKNOWN with no items; no new order lines for additions to a placed order.
- **Gold change (Julian, 2026-10-16):** a-dev-075 msg 0 "ok party order incoming" is SMALL_TALK (was PLACE_ORDER),
  logged in data/dev/REVIEWS.jsonl. Label-dev intents now 263/268 (98.1%). The M3 bake-off reports used the old gold
  (routing is not scored there, so their numbers are unaffected).
- **Label prompt on dev (2026-10-16, $0.0569, `runs/label-dev/20261016T153544Z-openai__gpt-6-luna@low/report.md`, `make label-dev`):** `teacher-label@0.2`
  on all 91 dev chats, scored against reviewed gold. Orders after finalize: **91/91 fully correct, items 146/146, 0
  extra** (v0.4 extraction prompt in M3: 90/91; the miss, a-dev-049, now right through the `item_variant` flag).
  Intents: **primary 262/268 (97.8%, CI 95.2–99.0%)**, primary + secondary 258/268 (96.3%). Mistakes are boundary
  calls: PLACE↔MODIFY ×5 (one, a-dev-040 "make the fries large", caused by the v0.2 rule "a size not stated before is
  PLACE_ORDER": gold says MODIFY), a missing secondary PLACE_ORDER on a change + details message ×3, "ok party order
  incoming" as SMALL_TALK, "👍 SOUNDS GOOD" as SMALL_TALK (gold UNKNOWN). Dev numbers: the M3 prompt fixes came
  from dev, so these are tuning results, not held out.

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
