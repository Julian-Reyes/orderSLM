# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders |
|---|---|---|---|---|
| qwen3.5-0.8b-single | 91.0% | 0.7% | 0.811 | 70.3% |
| qwen3.5-2b-single | 88.1% | 4.9% | 0.763 | 64.8% |
| qwen3.5-2b-mixed | 89.9% | 3.4% | 0.819 | 71.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single vs qwen3.5-2b-single | +3.0 [-1.9, +8.4] | -4.1 [-8.3, -0.8]* | +4.8 [-2.2, +12.7] | +5.5 [-2.2, +14.3] | 18 / 10 | 10 / 5 | 0.302 (0.604) |
| qwen3.5-0.8b-single vs qwen3.5-2b-mixed | +1.1 [-3.1, +5.7] | -2.6 [-5.8, +0.0] | -0.7 [-7.0, +5.4] | -1.1 [-7.7, +6.6] | 15 / 12 | 5 / 6 | 1.000 (1.000) |
| qwen3.5-2b-single vs qwen3.5-2b-mixed | -1.9 [-5.3, +1.1] | +1.5 [-0.8, +4.2] | -5.6 [-12.5, +0.5] | -6.6 [-14.3, +0.0] | 5 / 10 | 3 / 9 | 0.146 (0.438) |

Inputs:

- `qwen3.5-0.8b-single`: `runs/student-dev/20261023T140955Z-qwen3.5-0.8b-single`
- `qwen3.5-2b-single`: `runs/student-dev/20261023T115559Z-qwen3.5-2b-single`
- `qwen3.5-2b-mixed`: `runs/student-dev/20261023T140955Z-qwen3.5-2b-mixed`
