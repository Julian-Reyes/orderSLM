# Kaggle LoRA smoke test `20261021T145441Z`

GPU Tesla T4, Tesla T4 (sm 7.5); torch 2.11.0+cu128, transformers 5.20.2, peft 0.21.2, triton 3.6.0, CUDA 12.8. One GPU per phase, batch 1, gradient checkpointing, LoRA r 8 on all linear layers, answer-only loss.

| Phase | Delta rule | Steady tok/s | s/step (mean row tokens) | Peak GB (random) | Non-finite loss | Longest rows (tokens: s, GB) | One pass single/train, 1 T4 (excl. compile steps) |
|---|---|---:|---:|---:|---:|---|---:|
| 0.8b-torch-fp16 | transformers | 525.9 | 6.89 (3,621) | 3.76 | 0/22 | 6,323: 14.551 s, 3.96 GB; 9,805: 30.912 s, 5.15 GB | 3.74 h (3.74 h) |
| 0.8b-fla-fp16 | fla | 526.1 | 6.88 (3,621) | 3.72 | 0/22 | 6,323: 9.724 s, 3.66 GB; 9,805: 39.005 s, 3.98 GB | 3.74 h (3.1 h) |
| 2b-fla-fp16 | fla | 504.7 | 6.1 (3,081) | 6.15 | 0/12 | 6,323: 11.908 s, 6.29 GB; 9,805: 20.163 s, 7.23 GB | 3.9 h (3.9 h) |

fla check (0.8b-fla-fp16): `{"shape": [1, 2048, 16, 128], "y_rel_l2": 0.0005505328881554306, "grad_rel_l2": [0.0005510030896402895, 0.000589666364248842, 0.0005128236953169107], "finite": true, "seconds_first_call": {"torch": 0.265, "fla": 253.308}}`

fla check (2b-fla-fp16): `{"shape": [1, 2048, 16, 128], "y_rel_l2": 0.0005505328881554306, "grad_rel_l2": [0.0005510030896402895, 0.000589666364248842, 0.0005128236953169107], "finite": true, "seconds_first_call": {"torch": 0.262, "fla": 1.389}}`

Raw: `kernel/steps.jsonl`, `kernel/env.json`, `kernel/run.log`; numbers: `summary.json`.
