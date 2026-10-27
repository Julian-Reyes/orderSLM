# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders |
|---|---|---|---|---|
| qwen3.5-2b-mixed | 89.2% | 1.8% | 0.764 | 57.8% |
| qwen3.5-2b-mixed-v2 | 90.6% | 2.9% | 0.883 | 77.8% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|
| qwen3.5-2b-mixed vs qwen3.5-2b-mixed-v2 | -1.4 [-4.3, +1.5] | -1.1 [-3.2, +0.7] | -11.9 [-18.7, -6.2]* | -20.0 [-28.9, -11.1]* | 6 / 10 | 1 / 19 | 0.000 (0.000) |

Inputs:

- `qwen3.5-2b-mixed` (student-data@0.1): `runs/student-dev/20261027T123832Z-qwen3.5-2b-mixed-fresh`
- `qwen3.5-2b-mixed-v2` (student-data@0.2): `runs/student-dev/20261027T123832Z-qwen3.5-2b-mixed-v2-fresh`
