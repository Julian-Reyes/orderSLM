# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) | 95.0% | 0.7% | 0.955 | 91.1% | 92.2% |
| qwen3.5-0.8b-single-v5 (constrained) | 96.0% | 0.7% | 0.955 | 90.0% | 92.2% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v4 (constrained) vs qwen3.5-0.8b-single-v5 (constrained) | -1.1 [-3.2, +1.0] | +0.0 [-1.1, +1.0] | -0.1 [-4.0, +3.8] | +1.1 [-5.6, +7.8] | +0.0 [-6.7, +6.7] | 4 / 7 | 5 / 4 | 1.000 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v4 (constrained)` (student-data@0.4): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v4-fresh-cd`
- `qwen3.5-0.8b-single-v5 (constrained)` (student-data@0.5): `runs/student-dev/20261123T212018Z-qwen3.5-0.8b-single-v5-fresh-cd`
