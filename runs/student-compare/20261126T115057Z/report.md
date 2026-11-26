# M6 students compared on fresh4, paired (110 chats, 343 customer messages)

Same requests for every student. Fresh4 chats, written after the v5 fixes that used dev, fresh, fresh2 and fresh3 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) | 94.5% | 0.9% | 0.912 | 85.5% | 85.5% |
| qwen3.5-0.8b-single-v6 (constrained) | 93.6% | 0.3% | 0.928 | 88.2% | 88.2% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v5 (constrained) vs qwen3.5-0.8b-single-v6 (constrained) | +0.9 [-1.4, +3.2] | +0.6 [-0.6, +2.1] | -1.6 [-4.1, +0.7] | -2.7 [-7.3, +0.9] | -2.7 [-7.3, +0.9] | 8 / 5 | 1 / 4 | 0.375 (0.375) |

**standard** (90 chats): qwen3.5-0.8b-single-v5 (constrained) 83.3% fully correct, 94.2% intents; qwen3.5-0.8b-single-v6 (constrained) 86.7% fully correct, 93.5% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 1 / 4, McNemar p 0.375

**future_day** (20 chats): qwen3.5-0.8b-single-v5 (constrained) 95.0% fully correct, 95.5% intents; qwen3.5-0.8b-single-v6 (constrained) 95.0% fully correct, 94.0% intents. qwen3.5-0.8b-single-v5 (constrained) / qwen3.5-0.8b-single-v6 (constrained) only right: 0 / 0, McNemar p 1.000

Inputs:

- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-fresh4-cd`
- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh4-cd`
