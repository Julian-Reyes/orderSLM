# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) | 94.2% | 1.4% | 0.944 | 87.8% | 90.0% |
| qwen3.5-0.8b-single-v6-q8_0 | 93.9% | 1.1% | 0.935 | 86.7% | 87.8% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v6 (constrained) vs qwen3.5-0.8b-single-v6-q8_0 | +0.4 [-0.8, +1.7] | +0.4 [+0.0, +1.1] | +1.0 [+0.0, +2.6] | +1.1 [+0.0, +3.3] | +2.2 [+0.0, +5.6] | 2 / 1 | 1 / 0 | 1.000 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v6 (constrained)` (student-data@0.6): `runs/student-dev/20261125T130650Z-qwen3.5-0.8b-single-v6-fresh-cd`
- `qwen3.5-0.8b-single-v6-q8_0` (student-data@0.6): `runs/student-dev/20261126T125414Z-qwen3.5-0.8b-single-v6-q8_0-fresh`
