# M6 students compared on fresh4, paired (110 chats, 343 customer messages)

Same requests for every student. Fresh4 chats, written after the v5 fixes that used dev, fresh, fresh2 and fresh3 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) | 95.0% | 0.0% | 0.880 | 80.9% | 81.8% |
| qwen3.5-0.8b-single-v5 (constrained) | 94.5% | 0.9% | 0.912 | 85.5% | 85.5% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) vs qwen3.5-0.8b-single-v5 (constrained) | +0.6 [-1.4, +2.6] | -0.9 [-2.3, +0.0] | -3.3 [-6.7, +0.1] | -4.5 [-10.9, +0.9] | -3.6 [-9.1, +1.8] | 6 / 4 | 3 / 8 | 0.227 (0.227) |

**standard** (90 chats): qwen3.5-0.8b-single-v4 (constrained) 80.0% fully correct, 94.9% intents; qwen3.5-0.8b-single-v5 (constrained) 83.3% fully correct, 94.2% intents. qwen3.5-0.8b-single-v4 (constrained) / qwen3.5-0.8b-single-v5 (constrained) only right: 3 / 6, McNemar p 0.508

**future_day** (20 chats): qwen3.5-0.8b-single-v4 (constrained) 85.0% fully correct, 95.5% intents; qwen3.5-0.8b-single-v5 (constrained) 95.0% fully correct, 95.5% intents. qwen3.5-0.8b-single-v4 (constrained) / qwen3.5-0.8b-single-v5 (constrained) only right: 0 / 2, McNemar p 0.500

Inputs:

- `qwen3.5-0.8b-single-v4 (constrained)` (student-data@0.4): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v4-fresh4-cd`
- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-fresh4-cd`
