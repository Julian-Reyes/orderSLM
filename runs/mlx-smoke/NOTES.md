# MLX smoke test (M6), Mac mini M1 16 GB, 2026-10-21

Tool: mlx 0.32.4, mlx-lm 0.32.2 (`uv run --group mlx`). Model: Qwen/Qwen3.5-0.8B @ `2fc06364`
(safetensors sha256 `04b1c301…` = HF LFS hash). LoRA rank 8, 16 layers, lr 1e-4, batch 1, grad checkpointing,
prompt masked. Cost $0 (local).

## Result: stock mlx-lm cannot train Qwen3.5 on our rows on this machine

- `20261021T135642Z-qwen3.5-0.8b/`: 3-step run on `single/train.jsonl` (rows of 3,206 / 2,323 / 2,258 tokens).
  Validation forward pass works (2 rows, loss 1.533, 12.3 s). The **first training step fails**: Metal
  `kIOGPUCommandBufferCallbackErrorOutOfMemory`. No `summary.json` (the run died).
- `20261021T141113Z-qwen3.5-0.8b/probe.json`: one train step on random tokens per length (`--probe`):

  | tokens | seconds | peak memory |
  |---:|---:|---:|
  | 128 | 2.7 | 2.49 GB |
  | 256 | 5.1 | 3.33 GB |
  | 512 | 11.6 | 5.03 GB |
  | 1,024 | 32.5 | 9.27 GB |
  | 1,536 | 73.9 | 14.25 GB |

  The GPU's recommended working set is 11.45 GB, so ~1.2k tokens is the practical limit. Our rows: single p50 3,246,
  max 6,323; mixed max 9,805 tokens (Qwen3.5 tokenizer).

**Why:** in training mode mlx-lm's `qwen3_5.py` calls `gated_delta_update(use_kernel=not self.training)`: the
Metal kernel for the 18 linear-attention (Gated DeltaNet) layers has no backward pass, so training uses
`gated_delta_ops`, a Python loop over every token that keeps a float32 state (16 × 128 × 128 = 1 MB) per token per
layer for the backward pass. Memory grows ~9.6 MB per token and step time faster than linearly. Upstream reports
match (mlx-lm issue #1956, PR #1870 "chunkwise-parallel gated delta rule for training"; mlx issue #3539).

## Patch: chunkwise gated delta rule (vendored from mlx-lm PR #1870), verified, then parked

`src/orderslm/train/gated_delta_patch.py`: `gated_delta_chunkwise` + `_unit_tri_inv` from PR #1870 (Aditya Karnam,
head commit `3b04b9f1`, MIT, attribution in the file), with one change: `_unit_tri_inv` stops its 2×2 block
recursion at 8×8 blocks (nilpotent product inside them) instead of 1×1, which exceeded Metal's resource limit
(499,000, same on the M1) at ~8k tokens (reported in the PR thread). `install()` routes mlx-lm's ops path through it
for scalar gating without a mask (Qwen3.5 training). Unit tests: `tests/test_gated_delta_patch.py` (18, vs stock
loop: mild/strong decay, padding, grouped heads, correlated keys, gradients, base-block inverse vs `tri_inv`).

**Real rows** (`make mlx-smoke ARGS="--model models/qwen3.5-0.8b --check"` →
`20261021T144642Z-qwen3.5-0.8b/check.json`; `20261021T144051Z-…` is an earlier, partial run of the same check
without the kernel/fp32 references). Model in training mode, LoRA attached (B = 0 at init):

| Row (tokens) | dtype | Forward s: chunkwise / stock / Metal kernel | Peak GB: chunkwise / stock | Logits rel. L2 chunkwise vs stock (kernel vs stock) | Same top token |
|---|---|---|---|---|---|
| shortest single (2,077) | bf16 | 3.3 / 8.6 / 2.5 | 3.44 / 4.08 | 1.75% (1.71%) | 98.9% |
| median single (3,246) | bf16 | 5.3 / 13.9 / 4.0 | 4.02 / 5.46 | 1.72% (1.68%) | 99.3% |
| longest single (6,323) | bf16 | 10.6 / 29.9 / 8.2 | 5.69 / 8.96 | 1.76% (1.79%) | 98.8% |
| longest mixed (9,805) | bf16 | 17.3 / 65.6 / 13.6 | 7.75 / 12.73 | 1.76% (1.74%) | 99.4% |
| shortest single (2,077) | **fp32** | 5.2 / 9.0 / 3.5 | 5.99 / 7.90 | **3.2e-6** (3e-6) | 100% |

LoRA gradients chunkwise vs stock: 4.0% rel. L2 in bf16 (last 1,024 tokens), **6.6e-6 in fp32** (last 512 tokens).
Reading: in bf16 two correct paths (the inference Metal kernel and the stock loop) differ by the same ~1.7%, and in
fp32 the patch matches to ~1e-6, so the bf16 gap is rounding, not an algorithm error.

**Parked (Julian, 2026-10-21):** Kaggle is the primary training path (the Mac mini is much slower). The re-run probe
at 1k/3k/6k/10k tokens and the ≤ 12 h check were not run; the patch stays in the repo (`make mlx-smoke` uses it unless `--recurrence stock`).
