# M6 students compared on fresh5, paired (110 chats, 358 customer messages)

Same requests for every student. Fresh5 chats, written after the v6 fixes that used dev, fresh, fresh2 and fresh3 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) | 92.5% | 0.0% | 0.931 | 86.4% | 86.4% |
| qwen3.5-0.8b-single-v6-q8_0 | 91.6% | 0.8% | 0.920 | 84.5% | 84.5% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) vs qwen3.5-0.8b-single-v6-q8_0 | +0.8 [+0.0, +2.3] | -0.8 [-2.3, +0.0] | +1.1 [-0.3, +3.0] | +1.8 [+0.0, +4.5] | +1.8 [+0.0, +4.5] | 3 / 0 | 2 / 0 | 0.500 (0.500) |

**standard** (90 chats): qwen3.5-0.8b-single-v6 (constrained) 84.4% fully correct, 92.7% intents; qwen3.5-0.8b-single-v6-q8_0 83.3% fully correct, 92.0% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 1 / 0, McNemar p 1.000

**future_day** (20 chats): qwen3.5-0.8b-single-v6 (constrained) 95.0% fully correct, 91.6% intents; qwen3.5-0.8b-single-v6-q8_0 90.0% fully correct, 90.4% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 1 / 0, McNemar p 1.000

Inputs:

- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh5-cd`
- `qwen3.5-0.8b-single-v6-q8_0` (student-data@0.6): `runs/student-dev/20261126T125414Z-qwen3.5-0.8b-single-v6-q8_0-fresh5`
