# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.1% | 2.5% | 0.841 | 74.4% | 74.4% |
| qwen3.5-2b-mixed-v2 | 92.4% | 2.9% | 0.883 | 77.8% | 80.0% |
| qwen3.5-2b-single-v2 | 94.6% | 1.1% | 0.856 | 76.7% | 78.9% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-2b-mixed-v2 | -0.4 [-4.7, +3.9] | -0.4 [-3.6, +3.1] | -4.2 [-9.4, +0.4] | -3.3 [-11.1, +3.3] | -5.6 [-13.3, +2.2] | 15 / 16 | 4 / 7 | 0.549 (1.000) |
| qwen3.5-0.8b-single-v2 vs qwen3.5-2b-single-v2 | -2.5 [-6.7, +1.1] | +1.4 [-0.7, +4.4] | -1.5 [-7.2, +4.1] | -2.2 [-10.0, +5.6] | -4.4 [-13.3, +4.4] | 9 / 16 | 6 / 8 | 0.791 (1.000) |
| qwen3.5-2b-mixed-v2 vs qwen3.5-2b-single-v2 | -2.2 [-5.3, +0.7] | +1.8 [-0.8, +4.6] | +2.7 [-2.0, +7.7] | +1.1 [-5.6, +7.8] | +1.1 [-5.6, +7.8] | 4 / 10 | 5 / 4 | 1.000 (1.000) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2-fresh`
- `qwen3.5-2b-mixed-v2` (student-data@0.2): `runs/student-dev/20261027T123832Z-qwen3.5-2b-mixed-v2-fresh`
- `qwen3.5-2b-single-v2` (student-data@0.2): `runs/student-dev/20261103T115227Z-qwen3.5-2b-single-v2-fresh`
