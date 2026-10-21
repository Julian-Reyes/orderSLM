"""M6 LoRA training smoke test on Kaggle T4 (docs/KAGGLE.md job C): kernels, fp16 stability, speed, memory. Free.

Kaggle is the primary training path (Julian, 2026-10-21: the Mac mini is much slower; the MLX patch is parked).
The kernel (`kaggle/train-smoke/run.py`) runs ~20 LoRA steps of Qwen3.5-0.8B on seeded random single/train rows
plus the longest single and mixed rows, without and with flash-linear-attention, then 10 + 2 steps of Qwen3.5-2B on
the faster path, and records per step: seconds, tokens, peak memory, loss, grad norm, fp16 scale.

    make train-smoke ARGS="export"                      # stage the M6 rows + run dir
    make kaggle-push JOB=train-smoke                    # upload (private dataset), start the GPU kernel
    make kaggle-pull JOB=train-smoke                    # when it's done
    make train-smoke ARGS="import runs/train-smoke/<id>"

Import writes `summary.json` and `report.md`: per phase the steady-state tokens/second (random rows after 2
warm-up steps), peak memory per length, NaN/inf counts, and the estimated time for one pass over single/train on one
T4 (scaled by tokens, and by steps as a cross-check). Only synthetic training rows go to Kaggle (never dev, test or
PIZZA); the upload is the training data M6 will use anyway.
"""

import argparse
import json
import random
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.train.data import DATA_VERSION, OUT, STUDENT_PROMPT_VERSION

EXPERIMENT = "train-smoke"
SEED = 20261021
JOB_DIR = ROOT / "kaggle" / EXPERIMENT
STAGE = JOB_DIR / "upload"  # gitignored
DATASET = "JReyes33/orderslm-student-data"
WARMUP_STEPS = 2  # first steps include CUDA/Triton compilation; left out of the throughput
# Same revisions as M5 (runs/student-bakeoff/20261019T182539Z/manifest.json).
MODELS = {
    "0.8b": {"repo": "Qwen/Qwen3.5-0.8B", "revision": "2fc06364715b967f1860aea9cf38778875588b17"},
    "2b": {"repo": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
}
# Versions checked on PyPI 2026-10-21 (all ≥ 2 weeks old): transformers as in M5; peft 0.21.2 (Apache-2.0);
# fla-core 0.5.2 (MIT, the `fla` package transformers looks for; installed --no-deps to keep Kaggle's torch).
PACKAGES = {
    "main": ["transformers==5.20.2", "peft==0.21.2", "accelerate"],
    "fla": ["fla-core==0.5.2"],
}
LORA = {"r": 8, "alpha": 16, "dropout": 0.0, "target_modules": "all-linear"}
LEARNING_RATE = 1e-4
PHASES = [
    {"name": "0.8b-torch-fp16", "model": "0.8b", "backend": "torch", "dtype": "float16", "steps": 20},
    {
        "name": "0.8b-fla-fp16",
        "model": "0.8b",
        "backend": "fla",
        "dtype": "float16",
        "steps": 20,
        "if": "fla_installed",
    },
    {
        "name": "0.8b-torch-fp32",
        "model": "0.8b",
        "backend": "torch",
        "dtype": "float32",
        "steps": 5,
        "if": "fp16_unstable",
        "after": "0.8b-torch-fp16",
    },
    {"name": "2b-best-fp16", "model": "2b", "backend": "best", "dtype": "float16", "steps": 10},
]


def export(args: argparse.Namespace) -> Path:
    data = OUT / DATA_VERSION
    manifest_src = json.loads((data / "manifest.json").read_text())
    n_single = sum(1 for line in (data / "single" / "train.jsonl").read_text().splitlines() if line.strip())
    random_rows = random.Random(SEED).sample(range(n_single), max(p["steps"] for p in PHASES))
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}"
    run = {
        "run_dir": out_dir.name,
        "data_version": DATA_VERSION,
        "prompt_version": STUDENT_PROMPT_VERSION,
        "models": MODELS,
        "packages": PACKAGES,
        "lora": LORA,
        "learning_rate": LEARNING_RATE,
        "random_rows": random_rows,
        "phases": PHASES,
    }
    manifest = {
        "experiment": EXPERIMENT,
        **run,
        "seed": SEED,
        "warmup_steps": WARMUP_STEPS,
        "train_sha256": {
            split: manifest_src["sets"][split]["train"]["sha256"] for split in ("single", "mixed")
        },
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "kaggle_dataset": DATASET,
        "cost_usd": 0.0,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    for split in ("single", "mixed"):  # flat: the Kaggle CLI skips subfolders by default
        shutil.copy(data / split / "train.jsonl", STAGE / f"{split}-train.jsonl")
    shutil.copy(data / "manifest.json", STAGE / "manifest.json")
    (STAGE / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    (STAGE / "dataset-metadata.json").write_text(
        json.dumps({"title": "orderslm-student-data", "id": DATASET, "licenses": [{"name": "unknown"}]})
        + "\n"
    )
    print(f"Staged single + mixed train rows ({DATA_VERSION}) in {STAGE.relative_to(ROOT)}/")
    print(f"Run dir: {out_dir.relative_to(ROOT)}/")
    return out_dir


def phase_summary(steps: list[dict], total_tokens: int, n_rows: int) -> dict[str, Any]:
    """Steady-state speed on the random rows (after warm-up) and the one-pass estimate for single/train."""
    done = [s for s in steps if "error" not in s]
    steady = [s for s in done if s["kind"] == "random"][WARMUP_STEPS:]
    out: dict[str, Any] = {
        "steps": len(steps),
        "errors": [
            {"step": s["step"], "tokens": s["tokens"], "error": s["error"][:120]}
            for s in steps
            if "error" in s
        ],
        "nonfinite_loss_steps": sum(not s["loss_finite"] for s in done),
        "nonfinite_grad_steps": sum(not s["grad_finite"] for s in done),
        "loss_first": [round(s["loss"], 4) for s in done[:3]],
        "loss_last": [round(s["loss"], 4) for s in [s for s in done if s["kind"] == "random"][-3:]],
        "longest": [
            {k: s.get(k) for k in ("split", "tokens", "seconds", "peak_memory_gb", "loss", "error")}
            for s in steps
            if s["kind"] == "longest"
        ],
    }
    if steady:
        secs, toks = sum(s["seconds"] for s in steady), sum(s["tokens"] for s in steady)
        out |= {
            "steady_steps": len(steady),
            "steady_row_tokens_mean": round(toks / len(steady)),
            "tokens_per_second": round(toks / secs, 1),
            "step_seconds_mean": round(secs / len(steady), 2),
            "peak_memory_gb_max_random": max(s["peak_memory_gb"] for s in steady),
            "single_pass_hours_by_tokens": round(total_tokens / (toks / secs) / 3600, 2),
            "single_pass_hours_by_steps": round(secs / len(steady) * n_rows / 3600, 2),
        }
    return out


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("run_dir") != run_dir.name:
        raise SystemExit(f"kernel output is for {env.get('run_dir')}, not {run_dir.name}")
    steps: dict[str, list[dict]] = {}
    for line in (output_dir / "steps.jsonl").read_text().splitlines():
        s = json.loads(line)
        steps.setdefault(s["phase"], []).append(s)
    summary: dict[str, Any] = {"env": {k: v for k, v in env.items() if k != "phases"}, "phases": {}}
    for name, info in env["phases"].items():
        tokens = info.get("single_train_tokens", {})
        summary["phases"][name] = {
            "kernels": info.get("kernels"),
            "fla_check": info.get("fla_check"),
            "model_class": info.get("model_class"),
            "parameters": info.get("parameters"),
            "trainable_parameters": info.get("trainable_parameters"),
            "memory_after_load_gb": info.get("memory_after_load_gb"),
            "single_train_tokens": tokens,
            "mixed_train_tokens": info.get("mixed_train_tokens"),
            "error": info.get("error"),
            "exit_code": info.get("exit_code"),
            **phase_summary(steps.get(name, []), tokens.get("tokens", 0), tokens.get("rows", 0)),
        }
    kernel = run_dir / "kernel"
    kernel.mkdir(exist_ok=True)
    for name in ("env.json", "steps.jsonl", "run.log"):
        if (output_dir / name).exists():
            shutil.copy(output_dir / name, kernel / name)
    manifest.update(imported_at=datetime.now(UTC).isoformat())
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    _write_report(run_dir, summary)
    print((run_dir / "report.md").read_text())
    return summary


def _write_report(run_dir: Path, summary: dict) -> None:
    env = summary["env"]
    lines = [
        f"# Kaggle LoRA smoke test `{run_dir.name}`",
        "",
        f"GPU {', '.join(env['gpus'])} (sm {'.'.join(map(str, env['capability']))}); torch {env['torch']}, "
        f"transformers {env['transformers']}, peft {env['peft']}, triton {env.get('triton')}, CUDA {env['cuda']}. "
        "One GPU per phase, batch 1, gradient checkpointing, LoRA r 8 on all linear layers, answer-only loss.",
        "",
        "| Phase | Delta rule | Steady tok/s | s/step (mean row tokens) | Peak GB (random) | Non-finite loss | "
        "Longest rows (tokens: s, GB) | One pass single/train, 1 T4 |",
        "|---|---|---:|---:|---:|---:|---|---:|",
    ]
    for name, p in summary["phases"].items():
        longest = "; ".join(
            f"{x['tokens']:,}: "
            + ("OOM" if x.get("error") else f"{x['seconds']} s, {x['peak_memory_gb']} GB")
            for x in p["longest"]
        )
        rule = (p.get("kernels") or {}).get("chunk_gated_delta_rule", "?").split(".")[0]
        if "tokens_per_second" in p:
            row = (
                f"| {name} | {rule} | {p['tokens_per_second']:,} | {p['step_seconds_mean']} "
                f"({p['steady_row_tokens_mean']:,}) | {p['peak_memory_gb_max_random']} | "
                f"{p['nonfinite_loss_steps']}/{p['steps']} | {longest} | {p['single_pass_hours_by_tokens']} h |"
            )
        else:
            row = f"| {name} | {rule} | failed: {(p.get('error') or 'no steps')[:120]} | | | | | |"
        lines.append(row)
    for name, p in summary["phases"].items():
        if p.get("fla_check"):
            lines += ["", f"fla check ({name}): `{json.dumps(p['fla_check'])}`"]
    lines += ["", "Raw: `kernel/steps.jsonl`, `kernel/env.json`, `kernel/run.log`; numbers: `summary.json`."]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("export")
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=JOB_DIR / "output")
    args = ap.parse_args(argv)
    if args.cmd == "export":
        export(args)
    else:
        import_(args.run_dir, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
