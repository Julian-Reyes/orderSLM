# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single | 89.2% | 3.2% | 0.777 | 60.0% | 64.4% |
| qwen3.5-0.8b-single-v2 | 92.1% | 2.5% | 0.861 | 76.7% | 76.7% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single vs qwen3.5-0.8b-single-v2 | -2.9 [-7.3, +1.5] | +0.7 [-1.8, +3.4] | -8.3 [-15.7, -1.6]* | -16.7 [-25.6, -7.8]* | -12.2 [-21.1, -3.3]* | 12 / 20 | 2 / 17 | 0.001 (0.001) |

Inputs:

- `qwen3.5-0.8b-single` (student-data@0.1): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-fresh`
- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2-fresh`
