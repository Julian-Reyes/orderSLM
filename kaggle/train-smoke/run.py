"""Kaggle script kernel (GPU): M6 LoRA training smoke test on a T4 (docs/KAGGLE.md job C).

Standalone (no orderslm import). Input: the private dataset staged by `orderslm.train.kaggle_smoke export`
(single-train.jsonl, mixed-train.jsonl, manifest.json, run.json with the phases). Questions it answers:

1. Do the fast Gated DeltaNet kernels run on a T4, or does transformers fall back to its PyTorch version? Phases
   run without `flash-linear-attention` (fla) installed (transformers' PyTorch chunked path) and with it (Triton
   kernels), after a numeric check of fla against the PyTorch version on the T4. `causal-conv1d` ships only as a
   source tarball (CUDA build), so it isn't installed; the short depthwise conv stays on PyTorch either way.
2. Is fp16 training stable (base weights fp16, LoRA weights fp32, autocast + GradScaler)? Loss, grad norm, scale,
   NaN/inf per step.
3. Tokens/second and peak memory at our real lengths: seeded random rows of single/train (typical ~3k tokens), then
   the longest single row (6.3k) and the longest mixed row (9.8k).

Each phase runs in its own process (clean GPU, and fla is only importable in the fla phases). One GPU per phase.
Logits are computed only for the answer tokens (`logits_to_keep`): the same loss as masking the prompt, without a
9.8k × 248k logits tensor. Output in /kaggle/working: steps.jsonl (one line per step), env.json, run.log.
"""

import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

OUT = Path("/kaggle/working")
LOG = (OUT / "run.log").open("a")
PART = Path("/tmp/smoke")
FLA_SITE = "/tmp/fla-site"


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def find_input() -> Path:
    hits = sorted(Path("/kaggle/input").rglob("run.json"))
    if len(hits) != 1:
        raise SystemExit(f"expected one run.json under /kaggle/input, found {hits}")
    return hits[0].parent


def read_rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def no_gqa_flag() -> bool:
    """As in M5: transformers passes enable_gqa=True to SDPA, which on a T4 falls back to the math kernel (full
    seq × seq scores: out of memory at ~8k tokens). Off, K/V heads are repeated first. Same attention."""
    from transformers.integrations import sdpa_attention

    if not hasattr(sdpa_attention, "use_gqa_in_sdpa"):
        return False
    sdpa_attention.use_gqa_in_sdpa = lambda *a, **k: False
    return True


def implementation(fn) -> str:
    """Which function a transformers hub-kernel wrapper calls (closure variable `implementation`)."""
    f = fn
    while f is not None:
        code = getattr(f, "__code__", None)
        if code and "implementation" in code.co_freevars:
            impl = f.__closure__[code.co_freevars.index("implementation")].cell_contents
            return f"{impl.__module__}.{impl.__qualname__}"
        f = getattr(f, "__wrapped__", None)
    return "unknown"


def kernel_paths() -> dict:
    from transformers.models.qwen3_5 import modeling_qwen3_5 as mq

    return {
        "chunk_gated_delta_rule": implementation(mq.torch_chunk_gated_delta_rule),
        "causal_conv1d_fn": implementation(mq.causal_conv1d_fn),
    }


def fla_check() -> dict:
    """fla's chunk_gated_delta_rule vs transformers' PyTorch version on the T4, fp16 inputs, forward + backward."""
    import inspect

    import torch
    import torch.nn.functional as F
    from fla.ops.gated_delta_rule import chunk_gated_delta_rule
    from transformers.models.qwen3_5 import modeling_qwen3_5 as mq

    reference = inspect.unwrap(mq.torch_chunk_gated_delta_rule)
    torch.manual_seed(0)
    B, T, H, D = 1, 2048, 16, 128  # Qwen3.5-0.8B linear-attention shape (16 value heads, head dim 128)
    dev = "cuda:0"
    base = {
        "q": torch.randn(B, T, H, D, device=dev, dtype=torch.float16),
        "k": torch.randn(B, T, H, D, device=dev, dtype=torch.float16),
        "v": torch.randn(B, T, H, D, device=dev, dtype=torch.float16),
    }
    a = torch.randn(B, T, H, device=dev)
    g = -torch.exp(torch.zeros(H, device=dev)) * F.softplus(a)  # log decay, fp32, as the model computes it
    beta = torch.rand(B, T, H, device=dev, dtype=torch.float16)
    w = torch.randn(B, T, H, D, device=dev)
    res = {}
    for name, fn in (("torch", reference), ("fla", chunk_gated_delta_rule)):
        x = {k: t.clone().requires_grad_(True) for k, t in base.items()}
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        y, _ = fn(x["q"], x["k"], x["v"], g=g, beta=beta, use_qk_l2norm_in_kernel=True)
        (y.float() * w).sum().backward()
        torch.cuda.synchronize()
        res[name] = {
            "y": y.detach().float(),
            "grads": [x[k].grad.float() for k in ("q", "k", "v")],
            "seconds_first_call": round(time.perf_counter() - t0, 3),
        }

    def rel(a, b):
        return float((a - b).norm() / b.norm())

    return {
        "shape": [B, T, H, D],
        "y_rel_l2": rel(res["fla"]["y"], res["torch"]["y"]),
        "grad_rel_l2": [rel(x, y) for x, y in zip(res["fla"]["grads"], res["torch"]["grads"], strict=True)],
        "finite": bool(torch.isfinite(res["fla"]["y"]).all()),
        "seconds_first_call": {k: v["seconds_first_call"] for k, v in res.items()},
    }


def encode(tok, row: dict) -> tuple[list[int], int]:
    msgs = row["messages"]
    ids = tok.apply_chat_template(msgs, tokenize=True, return_dict=False)
    prompt = tok.apply_chat_template(msgs[:-1], tokenize=True, add_generation_prompt=True, return_dict=False)
    if ids[: len(prompt)] != prompt:
        raise ValueError("prompt is not a prefix of the full chat")
    return ids, len(prompt)


def train_phase(phase: dict) -> None:
    """Child process: LoRA steps for one model/backend/dtype → /tmp/smoke/<name>.jsonl + <name>.json."""
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from peft import LoraConfig, get_peft_model

    src = find_input()
    run = json.loads((src / "run.json").read_text())
    name, model_cfg = phase["name"], run["models"][phase["model"]]
    info: dict = {"phase": phase, "sdpa_gqa_flag_off": no_gqa_flag(), "kernels": kernel_paths()}
    PART.mkdir(exist_ok=True)
    out = (PART / f"{name}.jsonl").open("w")

    def save_info() -> None:
        (PART / f"{name}.json").write_text(json.dumps(info))

    try:
        if phase["backend"] == "fla":
            info["fla_check"] = fla_check()
            log(f"{name}: fla check {json.dumps(info['fla_check'])}")
        path = snapshot_download(
            model_cfg["repo"], revision=model_cfg["revision"], local_dir=f"/tmp/models/{phase['model']}"
        )
        dtype = getattr(torch, phase["dtype"])
        tok = transformers.AutoTokenizer.from_pretrained(path)
        t0 = time.time()
        model = transformers.AutoModelForCausalLM.from_pretrained(path, dtype=dtype, device_map={"": 0})
        info["load_seconds"] = round(time.time() - t0, 1)
        info["model_class"] = type(model).__name__
        info["parameters"] = sum(p.numel() for p in model.parameters())
        model.config.use_cache = False
        lora = run["lora"]
        model = get_peft_model(
            model,
            LoraConfig(
                r=lora["r"],
                lora_alpha=lora["alpha"],
                lora_dropout=lora["dropout"],
                target_modules=lora["target_modules"],
                task_type="CAUSAL_LM",
            ),
        )
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
        params = [p for p in model.parameters() if p.requires_grad]
        info["trainable_parameters"] = sum(p.numel() for p in params)
        info["trainable_dtypes"] = sorted({str(p.dtype) for p in params})
        info["memory_after_load_gb"] = round(torch.cuda.memory_allocated(0) / 1e9, 2)
        log(
            f"{name}: {info['model_class']} {info['parameters']:,} params, {info['trainable_parameters']:,} trainable, kernels {info['kernels']}"
        )
        opt = torch.optim.AdamW(params, lr=run["learning_rate"])
        fp16 = dtype == torch.float16
        scaler = torch.amp.GradScaler("cuda", enabled=fp16)
        model.train()

        rows = {s: read_rows(src / f"{s}-train.jsonl") for s in ("single", "mixed")}
        lengths = {s: [len(encode(tok, r)[0]) for r in rs] for s, rs in rows.items()}
        for s, ls in lengths.items():
            info[f"{s}_train_tokens"] = {"rows": len(ls), "tokens": sum(ls), "max": max(ls)}
        picks = [("single", i, "random") for i in run["random_rows"][: phase["steps"]]]
        picks += [(s, max(range(len(ls)), key=ls.__getitem__), "longest") for s, ls in lengths.items()]
        for step, (split, idx, kind) in enumerate(picks, 1):
            ids, offset = encode(tok, rows[split][idx])
            x = torch.tensor([ids], device="cuda:0")
            # logits at positions offset-1 .. end-1 (the last one predicts nothing): the answer tokens only
            keep = len(ids) - offset + 1
            rec = {"phase": name, "step": step, "split": split, "row": idx, "kind": kind}
            rec |= {"tokens": len(ids), "answer_tokens": len(ids) - offset}
            torch.cuda.reset_peak_memory_stats(0)
            torch.cuda.synchronize()
            t = time.perf_counter()
            try:
                with torch.autocast("cuda", dtype=torch.float16, enabled=fp16):
                    logits = model(input_ids=x, logits_to_keep=keep).logits[0, :-1]
                loss = torch.nn.functional.cross_entropy(logits.float(), x[0, offset:])
                scaler.scale(loss).backward()
                scaler.unscale_(opt)
                grad_norm = torch.nn.utils.clip_grad_norm_(params, 1.0)
                scaler.step(opt)
                scaler.update()
                torch.cuda.synchronize()
                rec |= {
                    "seconds": round(time.perf_counter() - t, 3),
                    "loss": float(loss),
                    "loss_finite": bool(torch.isfinite(loss)),
                    "grad_norm": float(grad_norm),
                    "grad_finite": bool(torch.isfinite(grad_norm)),
                    "scale": float(scaler.get_scale()) if fp16 else None,
                }
            except torch.cuda.OutOfMemoryError as e:
                rec |= {"seconds": round(time.perf_counter() - t, 3), "error": f"OOM: {str(e)[:300]}"}
                scaler = torch.amp.GradScaler("cuda", init_scale=scaler.get_scale(), enabled=fp16)
            opt.zero_grad(set_to_none=True)
            rec["peak_memory_gb"] = round(torch.cuda.max_memory_allocated(0) / 1e9, 2)
            rec["peak_reserved_gb"] = round(torch.cuda.max_memory_reserved(0) / 1e9, 2)
            logits = loss = None
            torch.cuda.empty_cache()
            out.write(json.dumps(rec) + "\n")
            out.flush()
            log(
                f"{name} {step}/{len(picks)} {split}#{idx} {rec['tokens']} tok: "
                + (
                    rec.get("error")
                    or f"{rec['seconds']}s loss {rec['loss']:.4f} gn {rec['grad_norm']:.3g} peak {rec['peak_memory_gb']} GB"
                )
            )
    except Exception as e:  # a phase that can't run is a result (e.g. fla failing on sm75), not a crash
        info["error"] = f"{type(e).__name__}: {e}"[:3000]
        log(f"{name}: failed: {info['error'][:500]}")
    save_info()
    out.close()


def run_child(phase: dict, env: dict) -> dict:
    child_env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    if phase["backend"] == "fla":
        child_env["PYTHONPATH"] = FLA_SITE + os.pathsep + child_env.get("PYTHONPATH", "")
    r = subprocess.run([sys.executable, __file__, "--phase", json.dumps(phase)], env=child_env)
    info_path = PART / f"{phase['name']}.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {"phase": phase}
    if r.returncode:
        info["exit_code"] = r.returncode
        log(f"{phase['name']}: process exited with {r.returncode}")
    env["phases"][phase["name"]] = info
    return info


def steps_of(name: str) -> list[dict]:
    p = PART / f"{name}.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []


def main() -> None:
    src = find_input()
    run = json.loads((src / "run.json").read_text())
    pins = run["packages"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *pins["main"]])
    # peft 0.21.2 raises ImportError whenever torchao < 0.16 is installed (Kaggle ships 0.10, attempt 1); we don't use
    # it (it is for quantized LoRA), so remove it.
    torchao = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"], capture_output=True, text=True
    )
    fla = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--no-deps", "--target", FLA_SITE, *pins["fla"]],
        capture_output=True,
        text=True,
    )
    import accelerate
    import peft
    import torch
    import transformers

    gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    env = {
        "run_dir": run["run_dir"],
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "peft": peft.__version__,
        "accelerate": accelerate.__version__,
        "cuda": torch.version.cuda,
        "capability": list(torch.cuda.get_device_capability(0)),
        "gpus": gpus,
        "python": sys.version.split()[0],
        "fla_install": {"returncode": fla.returncode, "stderr": fla.stderr[-2000:]},
        "torchao_uninstall": {"returncode": torchao.returncode, "stderr": torchao.stderr[-500:]},
        "started_at": datetime.now(UTC).isoformat(),
        "phases": {},
    }
    try:
        import triton

        env["triton"] = triton.__version__
    except ImportError:
        env["triton"] = None
    log(
        f"run {run['run_dir']}: torch {torch.__version__}, transformers {transformers.__version__}, GPUs {gpus}"
    )
    PART.mkdir(exist_ok=True)

    def ok(name: str) -> bool:
        st = steps_of(name)
        return (
            bool(st)
            and "error" not in env["phases"].get(name, {})
            and all(s.get("loss_finite") for s in st if "error" not in s)
        )

    for phase in run["phases"]:
        cond = phase.get("if")
        if cond == "fla_installed" and fla.returncode:
            log(f"{phase['name']}: skipped (fla install failed)")
            continue
        if cond == "fp16_unstable" and ok(phase["after"]):
            log(f"{phase['name']}: skipped ({phase['after']} was stable)")
            continue
        p = dict(phase)
        if p["backend"] == "best":  # fla if its 0.8B phase ran clean and faster, else torch
            fast = [
                s["seconds"] for s in steps_of("0.8b-fla-fp16") if s["kind"] == "random" and "error" not in s
            ][2:]
            slow = [
                s["seconds"]
                for s in steps_of("0.8b-torch-fp16")
                if s["kind"] == "random" and "error" not in s
            ][2:]
            p["backend"] = (
                "fla" if ok("0.8b-fla-fp16") and fast and slow and sum(fast) < sum(slow) else "torch"
            )
            p["name"] = p["name"].replace("best", p["backend"])
        log(f"phase {p['name']}")
        run_child(p, env)
        with (OUT / "steps.jsonl").open("a") as f:
            for s in steps_of(p["name"]):
                f.write(json.dumps(s) + "\n")
        (OUT / "env.json").write_text(json.dumps(env, indent=2) + "\n")
    env["finished_at"] = datetime.now(UTC).isoformat()
    (OUT / "env.json").write_text(json.dumps(env, indent=2) + "\n")
    log("done")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--phase":
        train_phase(json.loads(sys.argv[2]))
    else:
        main()
