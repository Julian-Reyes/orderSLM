# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) | 94.0% | 0.0% | 0.927 | 86.8% | 86.8% |
| qwen3.5-0.8b-single-v5 (constrained) | 94.0% | 0.4% | 0.907 | 82.4% | 82.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) vs qwen3.5-0.8b-single-v5 (constrained) | +0.0 [-2.3, +2.3] | -0.4 [-1.2, +0.0] | +2.0 [-2.0, +6.2] | +4.4 [-3.3, +12.1] | +4.4 [-3.3, +12.1] | 5 / 5 | 8 / 4 | 0.388 (0.388) |

Inputs:

- `qwen3.5-0.8b-single-v4 (constrained)` (student-data@0.4): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v4-cd`
- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-cd`
