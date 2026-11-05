# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.9% | 1.1% | 0.872 | 75.8% | 78.0% |
| qwen3.5-0.8b-single-v2-q8_0 | 92.5% | 1.5% | 0.871 | 75.8% | 78.0% |
| qwen3.5-0.8b-single-v2-q4_k_m | 91.0% | 2.2% | 0.847 | 72.5% | 73.6% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v2-q8_0 | +0.4 [+0.0, +1.2] | -0.4 [-1.2, +0.0] | +0.1 [-0.9, +1.2] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | 1 / 0 | 0 / 0 | 1.000 (1.000) |
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v2-q4_k_m | +1.9 [+0.4, +3.6]* | -1.1 [-2.6, +0.0] | +2.5 [-2.0, +7.1] | +3.3 [-3.3, +9.9] | +4.4 [-2.2, +11.0] | 6 / 1 | 6 / 3 | 0.508 (1.000) |
| qwen3.5-0.8b-single-v2-q8_0 vs qwen3.5-0.8b-single-v2-q4_k_m | +1.5 [+0.0, +3.3] | -0.7 [-2.3, +0.7] | +2.4 [-2.2, +7.2] | +3.3 [-3.3, +9.9] | +4.4 [-2.2, +11.0] | 6 / 2 | 6 / 3 | 0.508 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2`
- `qwen3.5-0.8b-single-v2-q8_0` (student-data@0.2): `runs/student-dev/20261104T115735Z-qwen3.5-0.8b-single-v2-q8_0`
- `qwen3.5-0.8b-single-v2-q4_k_m` (student-data@0.2): `runs/student-dev/20261105T121614Z-qwen3.5-0.8b-single-v2-q4_k_m`
