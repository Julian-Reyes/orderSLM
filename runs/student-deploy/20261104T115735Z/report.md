# `qwen3.5-0.8b-single-v2` packaged with llama.cpp (b11700): session 20261104T115735Z

Merged fp16 (base `Qwen/Qwen3.5-0.8B` @ `2fc06364715b` + adapter `a06b298f585e`), converted to GGUF and quantized on Kaggle; greedy, the same requests and token ids as the transformers runs. Hardware: ['Tesla T4, 580.178.04, 15360 MiB', 'Tesla T4, 580.178.04, 15360 MiB'], CPU Intel(R) Xeon(R) CPU @ 2.00GHz × 4. Dev is tuning data; fresh helped shape finalize@0.2 (used for fixes). $0.

| format | GGUF size |
|---|---|
| F16 | 1.52 GB (`563ebb6ebaba`) |
| Q8_0 | 0.81 GB (`5afc64c6632a`) |
| Q4_K_M | 0.53 GB (`7eee1e463869`) |

| job | split | answered | exact / same action | same text as fp16 transformers | latency p50 / p95 (s) | prompt / output tok/s (p50) | peak memory |
|---|---|---|---|---|---|---|---|
| transformers fp16 (reference) | dev | 268 | | | 13.5 / 19.8 | | |
| transformers fp16 (reference) | fresh | 278 | | | 13.8 / 23.2 | | |
| gpu-f16 | dev | 268 (done) | 69/91 / 71/91 | 265/268 | 90.9 / 152.8 | 58 / 8 | RSS 2.17 GB (**GPU not used: ran on the CPU**) |
| gpu-f16-fresh | fresh | 139 (paused) |  | 136/139 | 94.0 / 158.0 | 58 / 8 | RSS 2.14 GB (**GPU not used: ran on the CPU**) |
| gpu-q8_0 | dev | 268 (done) | 69/91 / 71/91 | 252/268 | 112.1 / 204.7 | 35 / 9 | RSS 1.46 GB (**GPU not used: ran on the CPU**) |
| gpu-q8_0-fresh | fresh | 45 (paused) |  | 44/45 | 111.6 / 202.1 | 35 / 9 | RSS 1.42 GB (**GPU not used: ran on the CPU**) |
| gpu-q4_k_m | dev | 0 (paused) |  | 0/0 | ? | ? / ? | RSS 0.98 GB |
| gpu-q4_k_m-fresh | fresh | 0 (paused) |  | 0/0 | ? | ? / ? | RSS 0.98 GB |
| cpu-q8_0 | dev | 0 (paused) |  | 0/0 | ? | ? / ? | RSS 1.05 GB |
| cpu-q4_k_m | dev | 0 (paused) |  | 0/0 | ? | ? / ? | RSS 0.98 GB |

Speed on the same seeded sample of dev requests (one request at a time, no prompt cache):

| job | where it ran | answered | latency p50 / p95 (s) | prompt / output tok/s (p50) |
|---|---|---|---|---|
| gpu-f16 | CPU | 50 | 84.3 / 152.4 | 58 / 8 |
| gpu-q8_0 | CPU | 50 | 106.3 / 207.7 | 35 / 9 |

CPU answers vs the same format on the GPU (same text): cpu-q8_0 0/0, cpu-q4_k_m 0/0
