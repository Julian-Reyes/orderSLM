# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.1% | 2.5% | 0.861 | 76.7% | 76.7% |
| qwen3.5-0.8b-single-v2-q8_0 | 92.1% | 2.5% | 0.867 | 76.7% | 76.7% |
| qwen3.5-0.8b-single-v2-q4_k_m | 90.6% | 3.6% | 0.855 | 73.3% | 74.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v2-q8_0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | -0.6 [-2.1, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | 0 / 0 | 0 / 0 | 1.000 (1.000) |
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v2-q4_k_m | +1.4 [-2.2, +5.3] | -1.1 [-4.4, +1.8] | +0.6 [-4.7, +5.8] | +3.3 [-3.3, +10.0] | +2.2 [-4.4, +8.9] | 11 / 7 | 6 / 3 | 0.508 (1.000) |
| qwen3.5-0.8b-single-v2-q8_0 vs qwen3.5-0.8b-single-v2-q4_k_m | +1.4 [-2.2, +5.3] | -1.1 [-4.4, +1.8] | +1.2 [-3.8, +6.2] | +3.3 [-3.3, +10.0] | +2.2 [-4.4, +8.9] | 11 / 7 | 6 / 3 | 0.508 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2-fresh`
- `qwen3.5-0.8b-single-v2-q8_0` (student-data@0.2): `runs/student-dev/20261105T121614Z-qwen3.5-0.8b-single-v2-q8_0-fresh`
- `qwen3.5-0.8b-single-v2-q4_k_m` (student-data@0.2): `runs/student-dev/20261105T121614Z-qwen3.5-0.8b-single-v2-q4_k_m-fresh`
