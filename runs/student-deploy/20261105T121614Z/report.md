# `qwen3.5-0.8b-single-v2` packaged with llama.cpp (b11700): session 20261105T121614Z

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
| gpu-f16-timing | dev | 50 (done) |  | 49/50 | 3.9 / 5.5 | 7166 / 88 | GPU 1739 MiB, RSS 1.73 GB |
| gpu-q4_k_m | dev | 268 (done) | 66/91 / 67/91 | 178/268 | 2.4 / 3.4 | 6215 / 168 | GPU 783 MiB, RSS 1.10 GB |
| gpu-f16-fresh | fresh | 278 (done) | 69/90 / 69/90 | 275/278 | 4.3 / 7.4 | 6951 / 86 | GPU 1741 MiB, RSS 1.54 GB |
| gpu-q8_0-timing | dev | 50 (done) |  | 46/50 | 2.6 / 3.7 | 6454 / 143 | GPU 1049 MiB, RSS 1.44 GB |
| gpu-q4_k_m-fresh | fresh | 278 (done) | 66/90 / 67/90 | 178/278 | 2.4 / 4.0 | 6236 / 169 | GPU 783 MiB, RSS 1.28 GB |
| gpu-q8_0-fresh | fresh | 278 (done) | 69/90 / 69/90 | 264/278 | 2.8 / 4.6 | 6341 / 142 | GPU 1049 MiB, RSS 1.16 GB |
| cpu-q8_0 | dev | 50 (done) |  | 46/50 | 50.3 / 101.5 | 77 / 16 | RSS 1.41 GB |
| cpu-q4_k_m | dev | 50 (done) |  | 31/50 | 39.0 / 76.1 | 110 / 19 | RSS 1.40 GB |

Speed on the same seeded sample of dev requests (one request at a time, no prompt cache):

| job | where it ran | answered | latency p50 / p95 (s) | prompt / output tok/s (p50) |
|---|---|---|---|---|
| gpu-f16-timing | GPU | 50 | 3.9 / 5.5 | 7166 / 88 |
| gpu-q4_k_m | GPU | 50 | 2.3 / 3.3 | 6216 / 169 |
| gpu-q8_0-timing | GPU | 50 | 2.6 / 3.7 | 6454 / 143 |
| cpu-q8_0 | CPU | 50 | 50.3 / 101.5 | 77 / 16 |
| cpu-q4_k_m | CPU | 50 | 39.0 / 76.1 | 110 / 19 |

CPU answers vs the same format on the GPU (same text): cpu-q8_0 46/50, cpu-q4_k_m 42/50
