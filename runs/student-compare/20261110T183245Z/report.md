# M6 students compared on fresh2, paired (90 chats, 275 customer messages)

Same requests for every student. Fresh2 chats, written after the v3 fixes that used fresh (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 90.5% | 1.5% | 0.824 | 68.9% | 70.0% |
| qwen3.5-0.8b-single-v3 | 92.7% | 0.0% | 0.861 | 75.6% | 76.7% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v3 | -2.2 [-5.3, +0.8] | +1.5 [+0.0, +3.4] | -3.7 [-8.0, +0.3] | -6.7 [-14.4, +0.0] | -6.7 [-14.4, +0.0] | 8 / 14 | 3 / 9 | 0.146 (0.146) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261110T162058Z-qwen3.5-0.8b-single-v2-fresh2`
- `qwen3.5-0.8b-single-v3` (student-data@0.3): `runs/student-dev/20261110T162058Z-qwen3.5-0.8b-single-v3-fresh2`
