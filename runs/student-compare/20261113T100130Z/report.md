# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v3 | 92.2% | 1.9% | 0.919 | 83.5% | 83.5% |
| qwen3.5-0.8b-single-v4 | 93.7% | 0.4% | 0.931 | 86.8% | 86.8% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v3 vs qwen3.5-0.8b-single-v4 | -1.5 [-4.4, +1.4] | +1.5 [+0.0, +3.5] | -1.1 [-3.5, +1.1] | -3.3 [-8.8, +1.1] | -3.3 [-8.8, +1.1] | 5 / 9 | 1 / 4 | 0.375 (0.375) |

Inputs:

- `qwen3.5-0.8b-single-v3` (student-data@0.3): `runs/student-dev/20261109T142855Z-qwen3.5-0.8b-single-v3`
- `qwen3.5-0.8b-single-v4` (student-data@0.4): `runs/student-dev/20261112T215707Z-qwen3.5-0.8b-single-v4`
