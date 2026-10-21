"""Kaggle LoRA smoke test: the summary skips warm-up steps and scales steady speed to one pass over the set."""

from orderslm.train import kaggle_smoke as ks


def step(n, kind="random", seconds=1.0, tokens=1000, loss=1.0, **kw):
    return {
        "step": n,
        "kind": kind,
        "split": "single",
        "tokens": tokens,
        "seconds": seconds,
        "loss": loss,
        "loss_finite": True,
        "grad_finite": True,
        "peak_memory_gb": 5.0,
        **kw,
    }


def test_summary_leaves_out_warmup_and_estimates_a_pass():
    steps = [step(1, seconds=30.0), step(2, seconds=10.0)] + [step(n) for n in range(3, 7)]
    steps.append(step(7, kind="longest", tokens=9805, seconds=12.0))
    s = ks.phase_summary(steps, total_tokens=3_600_000, n_rows=1800)
    assert s["steady_steps"] == 4 and s["tokens_per_second"] == 1000.0
    assert s["single_pass_hours_by_tokens"] == 1.0 and s["single_pass_hours_by_steps"] == 0.5
    assert s["longest"][0]["tokens"] == 9805 and s["nonfinite_loss_steps"] == 0


def test_summary_counts_nan_and_oom():
    steps = [
        step(1),
        step(2),
        step(3, loss=float("nan"), loss_finite=False),
        {
            "step": 4,
            "kind": "longest",
            "split": "mixed",
            "tokens": 9805,
            "seconds": 1.0,
            "error": "OOM: CUDA out of memory",
            "peak_memory_gb": 15.0,
        },
    ]
    s = ks.phase_summary(steps, total_tokens=1, n_rows=1)
    assert s["nonfinite_loss_steps"] == 1 and s["errors"][0]["tokens"] == 9805


def test_phases_try_torch_then_fla_then_2b():
    names = [p["name"] for p in ks.PHASES]
    assert names[0] == "0.8b-torch-fp16" and names[1] == "0.8b-fla-fp16" and names[-1].startswith("2b")
    assert all(p["dtype"] == "float16" for p in ks.PHASES if p.get("if") != "fp16_unstable")


def test_summary_reports_a_compile_step_separately():
    steps = [step(1), step(2)] + [step(n) for n in range(3, 8)] + [step(8, seconds=5.0)]
    s = ks.phase_summary(steps, total_tokens=3_600_000, n_rows=1800)
    assert s["compile_outliers"] == [{"step": 8, "tokens": 1000, "seconds": 5.0}]
    assert s["tokens_per_second_excl_outliers"] == 1000.0 and s["single_pass_hours_excl_outliers"] == 1.0
