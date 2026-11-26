# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) | 93.7% | 0.4% | 0.948 | 90.1% | 90.1% |
| qwen3.5-0.8b-single-v6-q8_0 | 92.9% | 0.7% | 0.951 | 90.1% | 90.1% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) vs qwen3.5-0.8b-single-v6-q8_0 | +0.7 [+0.0, +1.9] | -0.4 [-1.2, +0.0] | -0.3 [-1.1, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | 2 / 0 | 0 / 0 | 1.000 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-cd`
- `qwen3.5-0.8b-single-v6-q8_0` (student-data@0.6): `runs/student-dev/20261126T125414Z-qwen3.5-0.8b-single-v6-q8_0`
