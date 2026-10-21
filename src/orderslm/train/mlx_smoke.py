"""M6 MLX smoke test on the Mac mini (Apple Silicon): does LoRA training run, how fast, and do the longest rows fit?

Two short phases on the M6 training rows (`make student-data`), each from a fresh base model:

1. `throughput`: `--steps` seeded random rows of `<data>/train.jsonl`, batch 1, one step per row; validation loss on
   `--val-rows` rows of `valid.jsonl` before and after. Gives step time, tokens/s, peak memory and the loss trend.
2. `longest`: the `--longest` longest rows of `<longest-from>/train.jsonl` (default `mixed`: the food-court menu
   makes the longest rows), one step each. Shows whether they fit in memory.

The full-run estimate scales phase 1's seconds per prompt+answer token to the whole training set (time per token
grows a little with length, so it is an estimate, not a measurement).

    make mlx-smoke ARGS="--model models/qwen3.5-0.8b"     # → runs/mlx-smoke/<time>-<model>/

Needs the `mlx` dependency group (`uv run --group mlx`, Apple Silicon only); `make check` never imports this file.
Writes `config.json`, `steps.jsonl` (one record per step / validation), `summary.json` and the LoRA adapter (gitignored
safetensors) to the run directory. Free: local compute only. Only synthetic training rows: never dev, test or PIZZA.
"""

import argparse
import json
import platform
import random
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.train.data import DATA_VERSION, OUT, STUDENT_PROMPT_VERSION

SEED = 20261021
RUN_DIR = RUNS / "mlx-smoke"
# LoRA settings for the smoke test: mlx-lm's defaults except the learning rate (its 1e-5 barely moves in 30 steps)
# and a sequence limit above our longest row (mixed: 9,805 tokens), so nothing is truncated.
LORA = {"rank": 8, "dropout": 0.0, "scale": 20.0}
LEARNING_RATE = 1e-4
NUM_LAYERS = 16
MAX_SEQ_LENGTH = 10240


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def pick_rows(lengths: list[int], n: int, seed: int) -> list[int]:
    """`n` seeded random row indices (sorted)."""
    return sorted(random.Random(seed).sample(range(len(lengths)), min(n, len(lengths))))


def longest_rows(lengths: list[int], n: int) -> list[int]:
    return sorted(range(len(lengths)), key=lambda i: (-lengths[i], i))[:n]


def token_lengths(tokenizer, rows: list[dict[str, Any]]) -> list[int]:
    return [len(tokenizer.apply_chat_template(r["messages"], return_dict=False)) for r in rows]


def estimate(seconds: float, tokens: int, total_tokens: int, n_rows: int, steps: int) -> dict[str, float]:
    """Full-epoch time from the throughput phase: per token (main) and per step (cross-check)."""
    return {
        "seconds_per_1k_tokens": round(1000 * seconds / tokens, 4),
        "epoch_hours_by_tokens": round(seconds / tokens * total_tokens / 3600, 2),
        "epoch_hours_by_steps": round(seconds / steps * n_rows / 3600, 2),
    }


class Recorder:
    """mlx-lm TrainingCallback that keeps every report (mlx-lm calls it with plain dicts)."""

    def __init__(self, phase: str, out):
        self.phase, self.out, self.train, self.val = phase, out, [], []

    def on_train_loss_report(self, info: dict) -> None:
        self.train.append(info)
        self.out.write(json.dumps({"phase": self.phase, "kind": "train", **info}) + "\n")
        self.out.flush()

    def on_val_loss_report(self, info: dict) -> None:
        self.val.append(info)
        self.out.write(json.dumps({"phase": self.phase, "kind": "val", **info}) + "\n")
        self.out.flush()


def train_args(
    model_path: str, data_name: str, adapter_path: Path, iters: int, val_rows: int
) -> SimpleNamespace:
    from mlx_lm.lora import CONFIG_DEFAULTS

    cfg = dict(CONFIG_DEFAULTS)
    cfg.update(
        fine_tune_type="lora",
        num_layers=NUM_LAYERS,
        lora_parameters=dict(LORA),
        learning_rate=LEARNING_RATE,
        batch_size=1,
        iters=iters,
        val_batches=val_rows,
        steps_per_report=1,
        steps_per_eval=iters,  # validation before step 1 and after the last step only
        save_every=iters,
        model=model_path,
        data=data_name,
        adapter_path=str(adapter_path),
        max_seq_length=MAX_SEQ_LENGTH,
        grad_checkpoint=True,
        mask_prompt=True,
        seed=SEED,
    )
    return SimpleNamespace(**cfg)


def run_phase(
    name: str, model_path: str, data_name: str, train_rows, valid_rows, run_dir: Path, steps_out
) -> dict[str, Any]:
    import mlx.core as mx
    from mlx_lm.lora import train_model
    from mlx_lm.tuner.datasets import ChatDataset
    from mlx_lm.utils import load

    model, tokenizer = load(model_path)
    mx.reset_peak_memory()
    args = train_args(model_path, data_name, run_dir / f"adapter-{name}", len(train_rows), len(valid_rows))
    rec = Recorder(name, steps_out)
    t0 = time.perf_counter()
    train_model(
        args,
        model,
        ChatDataset(train_rows, tokenizer, mask_prompt=True),
        ChatDataset(valid_rows, tokenizer, mask_prompt=True),
        training_callback=rec,
    )
    wall = time.perf_counter() - t0
    step_seconds = [1 / r["iterations_per_second"] for r in rec.train]
    return {
        "rows": len(train_rows),
        "wall_seconds": round(wall, 1),
        "train_seconds": round(sum(step_seconds), 1),
        "step_seconds_mean": round(sum(step_seconds) / len(step_seconds), 3),
        "step_seconds_max": round(max(step_seconds), 3),
        "answer_tokens_per_second_mean": round(
            sum(r["tokens_per_second"] for r in rec.train) / len(rec.train), 1
        ),
        "peak_memory_gb": round(mx.get_peak_memory() / 1e9, 2),
        "train_loss_first5": [round(r["train_loss"], 4) for r in rec.train[:5]],
        "train_loss_last5": [round(r["train_loss"], 4) for r in rec.train[-5:]],
        "val_loss": [round(v["val_loss"], 4) for v in rec.val],
    }


def probe(model_path: str, lengths: list[int], out: Path) -> list[dict[str, Any]]:
    """One LoRA step (smoke settings) on random tokens per length, shortest first; stops at the first failure.

    The last `min(400, n // 2)` tokens are the answer (our answers: p50 ~400 tokens), the rest is masked prompt.
    """
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    from mlx_lm.tuner.trainer import default_loss, grad_checkpoint
    from mlx_lm.tuner.utils import linear_to_lora_layers
    from mlx_lm.utils import load

    model, _ = load(model_path)
    model.freeze()
    linear_to_lora_layers(model, NUM_LAYERS, dict(LORA))
    grad_checkpoint(model.layers[0])
    model.train()
    opt = optim.Adam(learning_rate=LEARNING_RATE)
    loss_and_grad = nn.value_and_grad(model, default_loss)
    results = []
    for n in sorted(lengths):
        mx.clear_cache()
        mx.reset_peak_memory()
        tokens = mx.random.randint(0, 1000, (1, n), key=mx.random.key(SEED))
        t0 = time.perf_counter()
        try:
            (loss, _), grad = loss_and_grad(model, tokens, mx.array([[n - min(400, n // 2), n]]))
            opt.update(model, grad)
            mx.eval(model.parameters(), opt.state, loss)
            r = {"tokens": n, "ok": True, "seconds": round(time.perf_counter() - t0, 2)}
        except RuntimeError as e:
            r = {
                "tokens": n,
                "ok": False,
                "seconds": round(time.perf_counter() - t0, 2),
                "error": str(e)[:200],
            }
        r["peak_memory_gb"] = round(mx.get_peak_memory() / 1e9, 2)
        results.append(r)
        print(json.dumps(r), flush=True)
        out.write_text(json.dumps(results, indent=2) + "\n")
        if not r["ok"]:
            break
    return results


def machine() -> dict[str, Any]:
    def sysctl(key: str) -> str:
        return subprocess.run(["sysctl", "-n", key], capture_output=True, text=True).stdout.strip()

    import mlx.core as mx
    import mlx_lm

    return {
        "chip": sysctl("machdep.cpu.brand_string"),
        "memory_gb": round(int(sysctl("hw.memsize") or 0) / 2**30),
        "macos": platform.mac_ver()[0],
        "python": platform.python_version(),
        "mlx": mx.__version__,
        "mlx_lm": mlx_lm.__version__,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True, help="local HF-format model dir, e.g. models/qwen3.5-0.8b")
    ap.add_argument("--data", default="single", choices=["single", "mixed"])
    ap.add_argument("--longest-from", default="mixed", choices=["single", "mixed"])
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--longest", type=int, default=5)
    ap.add_argument("--val-rows", type=int, default=10)
    ap.add_argument(
        "--probe", help="comma-separated token lengths: one train step each instead of the phases"
    )
    a = ap.parse_args(argv)

    data_dir = OUT / DATA_VERSION
    train = read_rows(data_dir / a.data / "train.jsonl")
    valid = read_rows(data_dir / a.data / "valid.jsonl")
    long_pool = read_rows(data_dir / a.longest_from / "train.jsonl")
    model_name = Path(a.model).name
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUN_DIR / f"{stamp}-{model_name}"
    run_dir.mkdir(parents=True)
    if a.probe:
        info = {"experiment": "mlx-smoke probe", "model": a.model, "lora": LORA, "num_layers": NUM_LAYERS}
        info |= {"grad_checkpoint": True, "seed": SEED, "machine": machine(), "git_commit": git_commit()}
        (run_dir / "config.json").write_text(json.dumps(info, indent=2) + "\n")
        probe(a.model, [int(x) for x in a.probe.split(",")], run_dir / "probe.json")
        print(f"→ {run_dir.relative_to(ROOT)}")
        return 0

    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(a.model)
    train_len = token_lengths(tok, train)
    long_len = token_lengths(tok, long_pool)
    picked = pick_rows(train_len, a.steps, SEED)
    longest = longest_rows(long_len, a.longest)
    val_picked = pick_rows([0] * len(valid), a.val_rows, SEED)
    config = {
        "experiment": "mlx-smoke",
        "model": a.model,
        "model_config": json.loads((Path(a.model) / "config.json").read_text()).get("architectures"),
        "data_version": DATA_VERSION,
        "prompt_version": STUDENT_PROMPT_VERSION,
        "data": a.data,
        "longest_from": a.longest_from,
        "seed": SEED,
        "lora": LORA,
        "learning_rate": LEARNING_RATE,
        "num_layers": NUM_LAYERS,
        "batch_size": 1,
        "grad_checkpoint": True,
        "mask_prompt": True,
        "max_seq_length": MAX_SEQ_LENGTH,
        "throughput_rows": picked,
        "throughput_row_tokens": [train_len[i] for i in picked],
        "longest_rows": longest,
        "longest_row_tokens": [long_len[i] for i in longest],
        "valid_rows": val_picked,
        "machine": machine(),
        "git_commit": git_commit(),
        "started_at": datetime.now(UTC).isoformat(),
        "cost_usd": 0.0,
    }
    (run_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n")

    with (run_dir / "steps.jsonl").open("w") as steps_out:
        p1 = run_phase(
            "throughput",
            a.model,
            a.data,
            [train[i] for i in picked],
            [valid[i] for i in val_picked],
            run_dir,
            steps_out,
        )
        p2 = run_phase(
            "longest", a.model, a.longest_from, [long_pool[i] for i in longest], [], run_dir, steps_out
        )

    sampled = sum(config["throughput_row_tokens"])
    summary = {
        "throughput": {**p1, "row_tokens_sum": sampled},
        "longest": {**p2, "row_tokens": config["longest_row_tokens"]},
        "estimate_per_epoch": {
            name: {
                "rows": len(lens),
                "tokens": sum(lens),
                **estimate(p1["train_seconds"], sampled, sum(lens), len(lens), len(picked)),
            }
            for name, lens in {a.data: train_len, a.longest_from: long_len}.items()
        },
        "finished_at": datetime.now(UTC).isoformat(),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"→ {run_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
