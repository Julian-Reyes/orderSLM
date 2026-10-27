# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders |
|---|---|---|---|---|
| qwen3.5-2b-mixed | 89.9% | 3.4% | 0.819 | 71.4% |
| qwen3.5-2b-mixed-v2 | 93.7% | 1.9% | 0.890 | 80.2% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|
| qwen3.5-2b-mixed vs qwen3.5-2b-mixed-v2 | -3.7 [-7.5, -0.4]* | +1.5 [-0.8, +4.4] | -7.2 [-12.4, -2.6]* | -8.8 [-15.4, -2.2]* | 3 / 13 | 1 / 9 | 0.021 (0.021) |

Inputs:

- `qwen3.5-2b-mixed` (student-data@0.1): `runs/student-dev/20261023T140955Z-qwen3.5-2b-mixed`
- `qwen3.5-2b-mixed-v2` (student-data@0.2): `runs/student-dev/20261027T123832Z-qwen3.5-2b-mixed-v2`
