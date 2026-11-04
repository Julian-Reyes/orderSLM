# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-2b-single | 89.2% | 3.6% | 0.752 | 56.7% | 62.2% |
| qwen3.5-2b-single-v2 | 94.6% | 1.1% | 0.856 | 76.7% | 78.9% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-2b-single vs qwen3.5-2b-single-v2 | -5.4 [-9.1, -2.2]* | +2.5 [+0.7, +5.1]* | -10.4 [-18.1, -3.3]* | -20.0 [-30.0, -11.1]* | -16.7 [-25.6, -7.8]* | 2 / 17 | 2 / 20 | 0.000 (0.000) |

Inputs:

- `qwen3.5-2b-single` (student-data@0.1): `runs/student-dev/20261027T123832Z-qwen3.5-2b-single-fresh`
- `qwen3.5-2b-single-v2` (student-data@0.2): `runs/student-dev/20261103T115227Z-qwen3.5-2b-single-v2-fresh`
