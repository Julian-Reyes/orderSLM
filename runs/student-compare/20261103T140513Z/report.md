# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders |
|---|---|---|---|---|
| qwen3.5-2b-single | 88.1% | 4.9% | 0.763 | 64.8% |
| qwen3.5-2b-single-v2 | 91.4% | 3.4% | 0.861 | 75.8% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|
| qwen3.5-2b-single vs qwen3.5-2b-single-v2 | -3.4 [-7.4, +0.4] | +1.5 [-1.3, +4.6] | -9.8 [-17.0, -3.5]* | -11.0 [-18.7, -3.3]* | 5 / 14 | 2 / 12 | 0.013 (0.013) |

Inputs:

- `qwen3.5-2b-single` (student-data@0.1): `runs/student-dev/20261023T115559Z-qwen3.5-2b-single`
- `qwen3.5-2b-single-v2` (student-data@0.2): `runs/student-dev/20261103T115227Z-qwen3.5-2b-single-v2`
