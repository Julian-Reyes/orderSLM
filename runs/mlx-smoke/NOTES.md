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
