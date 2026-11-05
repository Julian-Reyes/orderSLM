# M6 packaging: the picked student as GGUF with llama.cpp

The picked student (**Qwen3.5-0.8B single v2**, adapter `a06b298f585e`) merged into its base, converted to GGUF,
quantized, and served with llama.cpp **b11700** on Kaggle (2 × T4, 4-core Xeon 2.0 GHz). Every format answered the
same requests, as the same token ids, as the fp16 transformers scoring runs, greedy, and was scored with the same scorer
(scorer@0.4, finalize@0.2). $0 (Kaggle). Done on Kaggle because the Mac mini wasn't at hand (Julian, 2026-11-04);
Apple Silicon and MLX numbers come later.

Dev is tuning data. Fresh helped shape finalize@0.2, so fresh numbers are "used for fixes", not held out. The
test split was not used.

## Results

| format | GGUF size | dev exact / same action (of 91) | fresh exact / same action (of 90) | same answer text as fp16 transformers (dev / fresh) | peak GPU memory |
|---|---|---|---|---|---|
| fp16 transformers (reference) | 1.5 GB (safetensors) | 69 / 71 | 69 / 69 | | |
| **F16** | 1.52 GB | 69 / 71 ¹ | 69 / 69 | 265/268 ¹ / 275/278 | 1.74 GB |
| **Q8_0** | 0.81 GB | 69 / 71 ¹ | 69 / 69 | 252/268 ¹ / 264/278 | 1.05 GB |
| **Q4_K_M** | 0.53 GB | 66 / 67 | 66 / 67 | 178/268 / 178/278 | 0.78 GB |

¹ From run 1, which ran on the CPU (see below); the answers are those of the same GGUF file, so they count for
accuracy, not for speed.

Peak GPU memory includes the 8,192-token context.

**Paired comparisons** (`runs/student-compare/20261105T143617Z` dev, `…T143627Z` fresh; bootstrap over chats, McNemar,
Holm):
- **Q8_0 vs fp16:** the same fully correct orders on both splits (0 chats differ). On dev, Q8_0 gets one more
  message's intent wrong (92.5% vs 92.9%).
- **Q4_K_M vs fp16:** 3 fewer fully correct orders on each split (dev: 6 chats only fp16 right, 3 only Q4_K_M right;
  fresh: the same 6 / 3). **Not significant** (McNemar p = 0.51, Holm 1.0). Intents on dev are 1.9 pp lower, the
  only interval that excludes 0. It also has slightly more invalid answers (dev 2.2% vs 1.1%, fresh 3.6% vs 2.5%).
  Q4_K_M changes the answer text in about a third of the requests.

## Speed

Measured on the same 50 seeded dev requests, one request at a time, with no prompt cache. Prompts are about
2.7–5.4k tokens, answers about 180–600.

| format | where | latency p50 / p95 | prompt tok/s | output tok/s |
|---|---|---|---|---|
| fp16 transformers (reference, all dev) | T4 | 13.5 / 19.8 s | | |
| F16 | T4 | 3.9 / 5.5 s | 7,166 | 88 |
| Q8_0 | T4 | 2.6 / 3.7 s | 6,454 | 143 |
| Q4_K_M | T4 | 2.3 / 3.3 s | 6,216 | 169 |
| Q8_0 | CPU, 4 cores | 50.3 / 101.5 s | 77 | 16 |
| Q4_K_M | CPU, 4 cores | 39.0 / 76.1 s | 110 | 19 |

- On a T4, llama.cpp answers **3.5–6× faster** than the transformers runs. The first request of a server takes
  25–43 s (warm-up), and that is not in the p50.
- On Kaggle's 4-core CPU, most of the time goes to reading the long prompt (menu + instructions + chat) at 77–110
  tok/s, so a turn takes ~40–50 s. That is too slow for a live chat as measured.
  - Not measured yet: reusing the cached menu/instruction prefix across turns (llama-server `cache_prompt`, off
    here for clean timing), which would cut most of that prompt time.
  - Not measured yet: the Mac mini (Apple Silicon, Metal or MLX).
- CPU answers match the same format on the GPU in 46/50 (Q8_0) and 42/50 (Q4_K_M) requests.

## Recommendation

**Ship Q8_0.**
- It gives the same orders as the fp16 model on dev and fresh.
- It's about half the size of F16 (0.81 GB) and only about 10% slower than Q4_K_M on the GPU.
- Q4_K_M saves 0.28 GB but loses 3 exact orders per split, gets more answers invalid, and its answers vary more
  between GPU and CPU. The loss isn't significant at 90 chats, but nothing here pays for it.

Julian decides.

## How it was run

- `make deploy ARGS="export"` stages the adapter, dev + fresh requests and `run.json`.
- `make kaggle-push JOB=m6-deploy`, then `make kaggle-pull JOB=m6-deploy` (the GGUF files are skipped and stay
  in the kernel output).
- `make deploy ARGS="import runs/student-deploy/<id>"` scores each full GPU job into `runs/student-dev/` and
  writes the deploy run's `report.md`.

Kernel steps (`kaggle/m6-deploy/run.py`):
1. Merge in fp16 with peft (`Qwen3_5ForCausalLM`, 52 s).
2. `convert_hf_to_gguf.py --outtype f16`, then `llama-quantize`.
3. Render the chat template to token ids.
4. llama-server, one per GPU, `-ngl 999 -c 8192 -np 1`, greedy (`samplers: ["top_k"]`, `top_k: 1`).
5. The CPU build after the GPU jobs.

Runs:
- **Run 1, `runs/student-deploy/20261104T115735Z`** (2026-11-04, 11.3 h):
  - The prebuilt CUDA build silently ran on the CPU.
  - Dev answered in full for F16 and Q8_0; fresh partial; Q4_K_M and the CPU jobs never started. Its speed numbers
    are void.
  - Cause, found by run 2's device check: the kernel *replaced* `LD_LIBRARY_PATH` with the llama.cpp folders, so
    `libcuda.so.1` (the NVIDIA driver) wasn't found and llama.cpp quietly fell back to the CPU.
- **Run 2, `runs/student-deploy/20261105T121614Z`** (Julian: "the smaller run", "make sure it stops if it doesn't
  work"). Stop rules:
  - llama-server must list a CUDA device before anything runs; if the prebuilt build lists none, a source build for
    the T4 is tried.
  - Each GPU job's first answer must use ≥ 256 MiB of GPU memory and ≥ 20 output tok/s.
  - 3 failed requests in a row stop everything.
  - 4 h deadline.

  Attempts:
  - Kernel v2 stopped itself after 4 min (no device; `libcuda.so.1 => not found`); the source build failed for the
    same reason.
  - Kernel v3 keeps the machine's library path: all jobs ran on the GPU in 2.2 h (GPU 38 min, CPU 1.5 h).
