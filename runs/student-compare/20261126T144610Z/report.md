# M6 students compared on fresh4, paired (110 chats, 343 customer messages)

Same requests for every student. Fresh4 chats, written after the v5 fixes that used dev, fresh, fresh2 and fresh3 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) | 93.6% | 0.3% | 0.928 | 88.2% | 88.2% |
| qwen3.5-0.8b-single-v6-q8_0 | 93.6% | 0.6% | 0.933 | 88.2% | 88.2% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) vs qwen3.5-0.8b-single-v6-q8_0 | +0.0 [-0.9, +0.9] | -0.3 [-0.9, +0.0] | -0.5 [-1.6, +0.0] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | 1 / 1 | 0 / 0 | 1.000 (1.000) |

**standard** (90 chats): qwen3.5-0.8b-single-v6 (constrained) 86.7% fully correct, 93.5% intents; qwen3.5-0.8b-single-v6-q8_0 86.7% fully correct, 93.5% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 0 / 0, McNemar p 1.000

**future_day** (20 chats): qwen3.5-0.8b-single-v6 (constrained) 95.0% fully correct, 94.0% intents; qwen3.5-0.8b-single-v6-q8_0 95.0% fully correct, 94.0% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 0 / 0, McNemar p 1.000

Inputs:

- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh4-cd`
- `qwen3.5-0.8b-single-v6-q8_0` (student-data@0.6): `runs/student-dev/20261126T125414Z-qwen3.5-0.8b-single-v6-q8_0-fresh4`
