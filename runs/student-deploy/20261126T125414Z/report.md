# `qwen3.5-0.8b-single-v6` packaged with llama.cpp (b11700): session 20261126T125414Z

Merged fp16 (base `Qwen/Qwen3.5-0.8B` @ `2fc06364715b` + adapter `df14b06055d7`), converted to GGUF and quantized on Kaggle; greedy, the same requests and token ids as the transformers runs. Hardware: ['Tesla T4, 580.178.04, 15360 MiB', 'Tesla T4, 580.178.04, 15360 MiB'], CPU Intel(R) Xeon(R) CPU @ 2.00GHz × 4. Splits: fresh4, fresh5, dev, fresh, fresh2, fresh3 (see PROGRESS.md for which are clean and which are used for fixes). $0.

| format | GGUF size |
|---|---|
| Q8_0 | 0.81 GB (`116eb0f03cdd`) |

| job | split | answered | exact / same action | same text as fp16 transformers | latency p50 / p95 (s) | prompt / output tok/s (p50) | peak memory |
|---|---|---|---|---|---|---|---|
| transformers fp16 (reference) | fresh4 | 343 | | | 14.6 / 19.7 | | |
| transformers fp16 (reference) | fresh5 | 358 | | | 14.2 / 20.8 | | |
| transformers fp16 (reference) | dev | 268 | | | 13.5 / 20.0 | | |
| transformers fp16 (reference) | fresh | 278 | | | 14.0 / 23.6 | | |
| transformers fp16 (reference) | fresh2 | 275 | | | 14.3 / 21.1 | | |
| transformers fp16 (reference) | fresh3 | 321 | | | 13.6 / 18.3 | | |
| gpu-q8_0-timing | dev | 50 (done) |  | 48/50 | 2.5 / 3.7 | 6724 / 149 | GPU 1049 MiB, RSS 1.44 GB |
| gpu-q8_0-fresh4 | fresh4 | 343 (done) | 97/110 / 97/110 | 332/343 | 2.8 / 3.9 | 6462 / 146 | GPU 1049 MiB, RSS 1.17 GB |
| gpu-q8_0-fresh | fresh | 278 (done) | 78/90 / 79/90 | 268/278 | 2.7 / 4.3 | 6465 / 146 | GPU 1049 MiB, RSS 1.17 GB |
| gpu-q8_0-fresh2 | fresh2 | 275 (done) | 76/90 / 78/90 | 261/275 | 2.8 / 4.1 | 6467 / 146 | GPU 1049 MiB, RSS 1.17 GB |
| gpu-q8_0-fresh5 | fresh5 | 358 (done) | 93/110 / 93/110 | 342/358 | 2.8 / 4.1 | 6381 / 144 | GPU 1049 MiB, RSS 1.51 GB |
| gpu-q8_0 | dev | 268 (done) | 82/91 / 82/91 | 256/268 | 2.7 / 3.9 | 6350 / 144 | GPU 1049 MiB, RSS 1.14 GB |
| gpu-q8_0-fresh3 | fresh3 | 321 (done) | 90/110 / 91/110 | 307/321 | 2.7 / 3.8 | 6359 / 144 | GPU 1049 MiB, RSS 1.17 GB |
| cpu-q8_0 | dev | 50 (done) |  | 49/50 | 50.3 / 97.7 | 79 / 16 | RSS 1.42 GB |

Speed on the same seeded sample of dev requests (one request at a time, no prompt cache):

| job | where it ran | answered | latency p50 / p95 (s) | prompt / output tok/s (p50) |
|---|---|---|---|---|
| gpu-q8_0-timing | GPU | 50 | 2.5 / 3.7 | 6724 / 149 |
| gpu-q8_0 | GPU | 50 | 2.7 / 3.7 | 6356 / 144 |
| cpu-q8_0 | CPU | 50 | 50.3 / 97.7 | 79 / 16 |

CPU answers vs the same format on the GPU (same text): cpu-q8_0 47/50
