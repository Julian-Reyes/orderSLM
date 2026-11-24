# M6 students compared on fresh3, paired (110 chats, 321 customer messages)

Same requests for every student. Fresh3 chats, written after the v4 fixes that used dev, fresh and fresh2 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 | 93.5% | 1.2% | 0.918 | 83.6% | 85.5% |
| qwen3.5-0.8b-single-v4 (constrained) | 94.4% | 0.3% | 0.938 | 84.5% | 86.4% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 vs qwen3.5-0.8b-single-v4 (constrained) | -0.9 [-2.1, +0.0] | +0.9 [+0.0, +2.1] | -2.0 [-5.7, +0.0] | -0.9 [-2.7, +0.0] | -0.9 [-2.7, +0.0] | 0 / 3 | 0 / 1 | 1.000 (1.000) |

**standard** (90 chats): qwen3.5-0.8b-single-v4 82.2% fully correct, 94.0% intents; qwen3.5-0.8b-single-v4 (constrained) 83.3% fully correct, 94.7% intents. qwen3.5-0.8b-single-v4 / qwen3.5-0.8b-single-v4 (constrained) only right: 0 / 1, McNemar p 1.000

**future_day** (20 chats): qwen3.5-0.8b-single-v4 90.0% fully correct, 91.1% intents; qwen3.5-0.8b-single-v4 (constrained) 90.0% fully correct, 92.9% intents. qwen3.5-0.8b-single-v4 / qwen3.5-0.8b-single-v4 (constrained) only right: 0 / 0, McNemar p 1.000

Inputs:

- `qwen3.5-0.8b-single-v4` (student-data@0.4): `runs/student-dev/20261113T100155Z-qwen3.5-0.8b-single-v4-fresh3`
- `qwen3.5-0.8b-single-v4 (constrained)` (student-data@0.4): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v4-fresh3-cd`
