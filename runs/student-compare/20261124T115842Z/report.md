# M6 students compared on fresh2, paired (90 chats, 275 customer messages)

Same requests for every student. Fresh2 chats, written after the v3 fixes that used fresh (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) | 94.2% | 0.0% | 0.888 | 78.9% | 80.0% |
| qwen3.5-0.8b-single-v5 (constrained) | 94.9% | 0.0% | 0.927 | 83.3% | 83.3% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) vs qwen3.5-0.8b-single-v5 (constrained) | -0.7 [-3.2, +1.4] | +0.0 [+0.0, +0.0] | -3.8 [-7.5, -0.6]* | -4.4 [-11.1, +1.1] | -3.3 [-8.9, +2.2] | 3 / 5 | 2 / 6 | 0.289 (0.289) |

Inputs:

- `qwen3.5-0.8b-single-v4 (constrained)` (student-data@0.4): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v4-fresh2-cd`
- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-fresh2-cd`
