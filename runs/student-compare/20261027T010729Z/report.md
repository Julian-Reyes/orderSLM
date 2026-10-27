# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders |
|---|---|---|---|---|
| qwen3.5-0.8b-single | 91.0% | 0.7% | 0.811 | 70.3% |
| qwen3.5-0.8b-single-v2 | 93.7% | 1.1% | 0.872 | 76.9% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single vs qwen3.5-0.8b-single-v2 | -2.6 [-6.2, +1.1] | -0.4 [-2.6, +1.4] | -6.1 [-12.5, -0.2]* | -6.6 [-14.3, +1.1] | 6 / 13 | 3 / 9 | 0.146 (0.146) |

Inputs:

- `qwen3.5-0.8b-single` (student-data@0.1): `runs/student-dev/20261023T140955Z-qwen3.5-0.8b-single`
- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2`
