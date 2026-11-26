# M6 students compared on fresh3, paired (110 chats, 321 customer messages)

Same requests for every student. Fresh3 chats, written after the v4 fixes that used dev, fresh and fresh2 (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) | 90.0% | 1.6% | 0.942 | 84.5% | 85.5% |
| qwen3.5-0.8b-single-v6-q8_0 | 89.7% | 2.2% | 0.927 | 81.8% | 82.7% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) vs qwen3.5-0.8b-single-v6-q8_0 | +0.3 [-0.7, +1.5] | -0.6 [-1.6, +0.0] | +1.5 [+0.0, +4.1] | +2.7 [+0.0, +6.4] | +2.7 [+0.0, +6.4] | 2 / 1 | 3 / 0 | 0.250 (0.250) |

**standard** (90 chats): qwen3.5-0.8b-single-v6 (constrained) 83.3% fully correct, 89.4% intents; qwen3.5-0.8b-single-v6-q8_0 81.1% fully correct, 89.4% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 2 / 0, McNemar p 0.500

**future_day** (20 chats): qwen3.5-0.8b-single-v6 (constrained) 90.0% fully correct, 92.9% intents; qwen3.5-0.8b-single-v6-q8_0 85.0% fully correct, 91.1% intents. qwen3.5-0.8b-single-v6 (constrained) / qwen3.5-0.8b-single-v6-q8_0 only right: 1 / 0, McNemar p 1.000

Inputs:

- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh3-cd`
- `qwen3.5-0.8b-single-v6-q8_0` (student-data@0.6): `runs/student-dev/20261126T125414Z-qwen3.5-0.8b-single-v6-q8_0-fresh3`
