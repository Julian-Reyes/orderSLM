# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.9% | 1.1% | 0.872 | 75.8% | 78.0% |
| qwen3.5-0.8b-single-v3 | 92.2% | 1.9% | 0.912 | 82.4% | 82.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v3 | +0.7 [-2.6, +3.9] | -0.7 [-3.4, +1.9] | -4.0 [-8.0, -0.4]* | -6.6 [-13.2, -1.1]* | -4.4 [-11.0, +1.1] | 10 / 8 | 1 / 7 | 0.070 (0.070) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2`
- `qwen3.5-0.8b-single-v3` (student-data@0.3): `runs/student-dev/20261109T142855Z-qwen3.5-0.8b-single-v3`
