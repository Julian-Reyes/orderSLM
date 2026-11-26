# M6 students compared on fresh3, paired (110 chats, 321 customer messages)

Same requests for every student. Fresh3 chats, written after the v4 fixes that used dev, fresh and fresh2 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) | 94.4% | 0.0% | 0.938 | 81.8% | 83.6% |
| qwen3.5-0.8b-single-v6 (constrained) | 90.0% | 1.6% | 0.942 | 84.5% | 85.5% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) vs qwen3.5-0.8b-single-v6 (constrained) | +4.4 [+1.8, +7.3]* | -1.6 [-3.4, -0.3]* | -0.4 [-3.1, +2.4] | -2.7 [-8.2, +2.7] | -1.8 [-7.3, +3.6] | 15 / 1 | 4 / 7 | 0.549 (0.549) |

**standard** (90 chats): qwen3.5-0.8b-single-v5 (constrained) 82.2% fully correct, 94.3% intents; qwen3.5-0.8b-single-v6 (constrained) 83.3% fully correct, 89.4% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 4 / 5, McNemar p 1.000

**future_day** (20 chats): qwen3.5-0.8b-single-v5 (constrained) 80.0% fully correct, 94.6% intents; qwen3.5-0.8b-single-v6 (constrained) 90.0% fully correct, 92.9% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 0 / 2, McNemar p 0.500

Inputs:

- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-fresh3-cd`
- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh3-cd`
