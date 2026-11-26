# M6 students compared on fresh5, paired (110 chats, 358 customer messages)

Same requests for every student. Fresh5 chats, written after the v6 fixes that used dev, fresh, fresh2 and fresh3 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) | 93.3% | 1.4% | 0.895 | 80.9% | 80.9% |
| qwen3.5-0.8b-single-v6 (constrained) | 92.5% | 0.0% | 0.931 | 86.4% | 86.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) vs qwen3.5-0.8b-single-v6 (constrained) | +0.8 [-1.1, +2.8] | +1.4 [+0.3, +3.0]* | -3.6 [-7.0, -0.6]* | -5.5 [-10.9, -0.9]* | -5.5 [-10.9, -0.9]* | 9 / 6 | 1 / 7 | 0.070 (0.070) |

**standard** (90 chats): qwen3.5-0.8b-single-v5 (constrained) 81.1% fully correct, 93.5% intents; qwen3.5-0.8b-single-v6 (constrained) 84.4% fully correct, 92.7% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 1 / 4, McNemar p 0.375

**future_day** (20 chats): qwen3.5-0.8b-single-v5 (constrained) 80.0% fully correct, 92.8% intents; qwen3.5-0.8b-single-v6 (constrained) 95.0% fully correct, 91.6% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 0 / 3, McNemar p 0.250

Inputs:

- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261124T235616Z-qwen3.5-0.8b-single-v5-fresh5-cd`
- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh5-cd`
