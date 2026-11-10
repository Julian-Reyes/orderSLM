# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.1% | 2.5% | 0.861 | 76.7% | 76.7% |
| qwen3.5-0.8b-single-v3 | 90.3% | 2.2% | 0.919 | 84.4% | 85.6% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-0.8b-single-v3 | +1.8 [-3.1, +6.4] | +0.4 [-2.2, +3.0] | -5.8 [-11.7, -0.7]* | -7.8 [-16.7, +0.0] | -8.9 [-17.8, -1.1]* | 21 / 16 | 4 / 11 | 0.118 (0.118) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2-fresh`
- `qwen3.5-0.8b-single-v3` (student-data@0.3): `runs/student-dev/20261110T113810Z-qwen3.5-0.8b-single-v3-fresh`
