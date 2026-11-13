# M6 students compared on fresh, paired (90 chats, 278 customer messages)

Same requests for every student. Fresh chats, written after the dev-based fixes (evaluation-only). Differences are A − B in percentage points with a 95% paired bootstrap interval over chats (10,000 resamples, seed 20261025); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where the two disagree, Holm-adjusted over the pairs.

| student | intents right | invalid answers | item F1 | fully correct orders | same action |
|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v3 | 90.3% | 2.2% | 0.925 | 85.6% | 86.7% |
| qwen3.5-0.8b-single-v4 | 95.0% | 0.7% | 0.955 | 91.1% | 92.2% |

| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | same action (pp) | messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-0.8b-single-v3 vs qwen3.5-0.8b-single-v4 | -4.7 [-9.1, -0.7]* | +1.4 [-1.2, +5.3] | -2.9 [-7.4, +1.3] | -5.6 [-12.2, +1.1] | -5.6 [-13.3, +2.2] | 9 / 22 | 3 / 8 | 0.227 (0.227) |

Inputs:

- `qwen3.5-0.8b-single-v3` (student-data@0.3): `runs/student-dev/20261110T113810Z-qwen3.5-0.8b-single-v3-fresh`
- `qwen3.5-0.8b-single-v4` (student-data@0.4): `runs/student-dev/20261113T100155Z-qwen3.5-0.8b-single-v4-fresh`
