"""MLX smoke test helpers: row picks are seeded and the estimate scales measured time to the full set. No mlx needed."""

from orderslm.train import mlx_smoke


def test_pick_rows_is_seeded_and_distinct():
    lengths = list(range(100))
    a = mlx_smoke.pick_rows(lengths, 30, seed=1)
    assert a == mlx_smoke.pick_rows(lengths, 30, seed=1)
    assert len(set(a)) == 30 and a == sorted(a)
    assert mlx_smoke.pick_rows(lengths, 500, seed=1) == lengths


def test_longest_rows_takes_the_longest_first():
    assert mlx_smoke.longest_rows([5, 9, 1, 9, 7], 3) == [1, 3, 4]


def test_estimate_scales_by_tokens_and_by_steps():
    est = mlx_smoke.estimate(seconds=36.0, tokens=10_000, total_tokens=1_000_000, n_rows=300, steps=30)
    assert est == {"seconds_per_1k_tokens": 3.6, "epoch_hours_by_tokens": 1.0, "epoch_hours_by_steps": 0.1}


def test_smoke_never_truncates_the_longest_training_row():
    assert mlx_smoke.MAX_SEQ_LENGTH > 9805  # mixed/train max, Qwen3.5 tokenizer (2026-10-21)
