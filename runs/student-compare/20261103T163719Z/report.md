# M6 students compared on dev, paired (91 chats, 268 customer messages)

Same requests for every student. Dev numbers (tuning), not held-out results. Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 | 92.9% | 1.1% | 0.872 | 76.9% | 79.1% |
| qwen3.5-2b-mixed-v2 | 93.7% | 1.9% | 0.890 | 80.2% | 81.3% |
| qwen3.5-2b-single-v2 | 91.4% | 3.4% | 0.861 | 75.8% | 75.8% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v2 vs qwen3.5-2b-mixed-v2 | -0.7 [-3.7, +1.9] | -0.7 [-3.0, +1.8] | -1.8 [-6.6, +2.6] | -3.3 [-9.9, +3.3] | -2.2 [-8.8, +4.4] | 5 / 7 | 3 / 6 | 0.508 (1.000) |
| qwen3.5-0.8b-single-v2 vs qwen3.5-2b-single-v2 | +1.5 [-2.1, +5.3] | -2.2 [-5.5, +0.8] | +1.1 [-3.6, +6.3] | +1.1 [-5.5, +7.7] | +3.3 [-3.3, +11.0] | 11 / 7 | 5 / 4 | 1.000 (1.000) |
| qwen3.5-2b-mixed-v2 vs qwen3.5-2b-single-v2 | +2.2 [-0.4, +5.6] | -1.5 [-4.3, +0.7] | +2.9 [-0.3, +6.6] | +4.4 [+0.0, +9.9] | +5.5 [+0.0, +11.0] | 8 / 2 | 5 / 1 | 0.219 (0.656) |

Inputs:

- `qwen3.5-0.8b-single-v2` (student-data@0.2): `runs/student-dev/20261026T131201Z-qwen3.5-0.8b-single-v2`
- `qwen3.5-2b-mixed-v2` (student-data@0.2): `runs/student-dev/20261027T123832Z-qwen3.5-2b-mixed-v2`
- `qwen3.5-2b-single-v2` (student-data@0.2): `runs/student-dev/20261103T115227Z-qwen3.5-2b-single-v2`
