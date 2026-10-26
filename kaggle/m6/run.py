"""Kaggle script kernel (2 × T4): M6 LoRA training and dev scoring (docs/KAGGLE.md job C).

Standalone (no orderslm import). Input: the private dataset staged by `orderslm.train.kaggle_train export`
(run.json + training rows + dev requests + checkpoints to resume + adapters to score). run.json lists jobs; jobs on
different GPUs run in parallel (one process each, `CUDA_VISIBLE_DEVICES`), jobs on the same GPU one after another.

- `train`: LoRA on fp16 base weights (fp32 adapters, GradScaler, gradient checkpointing, flash-linear-attention's
  Triton delta rule), answer-only loss (`logits_to_keep`), effective batch via gradient accumulation (each row's
  mean token loss weighs the same), warmup + cosine LR, validation loss at fixed optimizer steps (every half epoch,
  and before step 1), best adapter by validation loss in `<job>/best/`, full training state in `<job>/last/` every
  `checkpoint_every` steps. Kaggle keeps /kaggle/working only when a session ends normally, so a job stops itself
  at `deadline_hours` after the session start, saves `last/` and reports `paused`; the next session resumes from it
  exactly (same data order, optimizer, scheduler, scaler, RNG). It also pauses that way when free host RAM drops
  below MIN_FREE_GB (the host grows ~10 MB per new training row; two trainings at once ran it out in session 1).
- `score`: greedy generation for each request (dev prefixes) with base + adapter; raw text out, scored on the Mac.
  With `after_train`, the adapter is that job's best from this session, scored only if its training finished.

Before any job starts, every input file run.json names must exist (session 2 lost its resume and adapter folders in
the upload), else the session ends at once.

Output (/kaggle/working): `<job>/` (config.json, steps.jsonl, val.jsonl, status.json, best/, last/ for train;
outputs.jsonl, status.json for score), env.json, run.log, memory.jsonl (host RAM every 30 s: free, tmpfs, cgroup,
each GPU's process tree). Paths can be moved for a local test with ORDERSLM_KAGGLE_IN
/ ORDERSLM_KAGGLE_OUT; a model entry with "path" is loaded from disk instead of the Hub.
"""

import hashlib
import json
import math
import os
import random
import shlex
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

OUT = Path(os.environ.get("ORDERSLM_KAGGLE_OUT", "/kaggle/working"))
IN = Path(os.environ.get("ORDERSLM_KAGGLE_IN", "/kaggle/input"))
FLA_SITE = "/tmp/fla-site"
OUT.mkdir(parents=True, exist_ok=True)
LOG = (OUT / "run.log").open("a")


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def missing_inputs(run: dict, src: Path) -> list[str]:
    """Input files the jobs need that the dataset doesn't have (in-session adapters come later, from OUT)."""
    need = []
    for j in run["jobs"]:
        if j["kind"] == "train":
            need += [j["train_file"], j["valid_file"]]
            if j.get("resume"):
                need += [f"{j['resume']}/{f}" for f in ("state.pt", "status.json")]
        else:
            need.append(j["requests"])
            if j.get("adapter") and not j.get("after_train"):
                need += [f"{j['adapter']}/{f}" for f in ("adapter_config.json", "adapter_model.safetensors")]
    return [f for f in dict.fromkeys(need) if not (src / f).is_file()]


def find_input() -> Path:
    hits = sorted(IN.rglob("run.json"))
    if len(hits) != 1:
        raise SystemExit(f"expected one run.json under {IN}, found {hits}")
    return hits[0].parent


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2) + "\n")
    tmp.replace(path)


# ---------------------------------------------------------------- host memory
# Session 20261021T170010Z: the 0.8B job was SIGKILLed (exit -9) after step 147 with GPU memory normal, most likely
# the host running out of RAM. These readings (Linux /proc and cgroup files; empty elsewhere) show where it goes.

GB = 1e9
MEMORY_EVERY = 30  # seconds between host-memory samples in memory.jsonl
# Session 20261022T123143Z: one 2B training's process grew 4 → 25.9 GB over its first epoch (~10 MB per new row),
# then stayed flat; a training pauses (saving last/) rather than be killed when free RAM falls below this.
MIN_FREE_GB = 2.0


def _read(path: str) -> str | None:
    try:
        return Path(path).read_text()
    except OSError:
        return None


def parse_meminfo(text: str) -> dict:
    """GB values of the /proc/meminfo fields that matter here (Shmem includes files on tmpfs, which live in RAM)."""
    want = {"MemTotal", "MemAvailable", "Shmem", "Cached", "SwapFree"}
    out = {}
    for line in text.splitlines():
        k, _, v = line.partition(":")
        if k in want:
            out[k] = round(int(v.split()[0]) * 1024 / GB, 2)
    return out


def rss_gb(pid: int | str = "self") -> float | None:
    for line in (_read(f"/proc/{pid}/status") or "").splitlines():
        if line.startswith("VmRSS:"):
            return round(int(line.split()[1]) * 1024 / GB, 2)
    return None


def cgroup_memory() -> dict:
    """The container's memory use and limit in GB (cgroup v2, else v1)."""
    for cur, lim in (
        ("/sys/fs/cgroup/memory.current", "/sys/fs/cgroup/memory.max"),
        ("/sys/fs/cgroup/memory/memory.usage_in_bytes", "/sys/fs/cgroup/memory/memory.limit_in_bytes"),
    ):
        if (c := _read(cur)) is not None:
            m = (_read(lim) or "").strip()
            return {
                "current": round(int(c) / GB, 2),
                "max": round(int(m) / GB, 2) if m.isdigit() else m or None,
            }
    return {}


def descendants(pid: int) -> list[int]:
    """pid and every process below it (from /proc/*/stat)."""
    parent = {}
    for p in Path("/proc").glob("[0-9]*"):
        if stat := _read(str(p / "stat")):
            parent[int(p.name)] = int(stat.rsplit(")", 1)[1].split()[1])
    tree, todo = [], [pid]
    while todo:
        q = todo.pop()
        tree.append(q)
        todo += [c for c, pp in parent.items() if pp == q]
    return tree


def host_memory(procs: dict | None = None) -> dict:
    rec = {"meminfo": parse_meminfo(_read("/proc/meminfo") or ""), "cgroup": cgroup_memory()}
    if procs:
        rec["rss_gb"] = {
            f"gpu{g}": round(sum(rss_gb(q) or 0 for q in descendants(p.pid)), 2) for g, p in procs.items()
        }
    return rec


def mount_types(text: str, paths: tuple[str, ...] = ("/tmp", "/kaggle/working")) -> dict:
    """Filesystem type of the mount holding each path (from /proc/mounts text)."""
    table = [m for m in (x.split() for x in text.splitlines()) if len(m) > 2]
    out = {}
    for path in paths:
        hits = [m for m in table if path == m[1] or path.startswith(m[1].rstrip("/") + "/")]
        out[path] = max(hits, key=lambda m: len(m[1]))[2] if hits else None
    return out


def no_gqa_flag() -> bool:
    """As in M5: SDPA with enable_gqa=True falls back to the math kernel on a T4 (OOM at ~8k tokens)."""
    from transformers.integrations import sdpa_attention

    if not hasattr(sdpa_attention, "use_gqa_in_sdpa"):
        return False
    sdpa_attention.use_gqa_in_sdpa = lambda *a, **k: False
    return True


def implementation(fn) -> str:
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


def model_path(run: dict, key: str) -> str:
    cfg = run["models"][key]
    if "path" in cfg:
        return cfg["path"]
    from huggingface_hub import snapshot_download

    return snapshot_download(cfg["repo"], revision=cfg["revision"], local_dir=f"/tmp/models/{key}")


def encode(tok, messages: list[dict]) -> tuple[list[int], int]:
    """Full chat tokens and the prompt length (the answer starts there)."""
    ids = tok.apply_chat_template(messages, tokenize=True, return_dict=False)
    prompt = tok.apply_chat_template(
        messages[:-1], tokenize=True, add_generation_prompt=True, return_dict=False
    )
    if ids[: len(prompt)] != prompt:
        raise ValueError("prompt is not a prefix of the full chat")
    return ids, len(prompt)


def bucket(ids: list[int], multiple: int | None, pad_id: int) -> list[int]:
    """`ids` padded at the end to a multiple of `multiple` tokens (None: unchanged). Host memory grew ~10 MB per new
    row through epoch 1 and stayed flat in epoch 2 (sessions 1-4): a per-shape cache (most likely fla's Triton
    kernels, specialized per sequence length; every row had its own length). Buckets bound the number of shapes.
    The model is causal, so end padding changes no earlier position; row_loss leaves the padding out of the loss."""
    if not multiple:
        return ids
    return ids + [pad_id] * (-len(ids) % multiple)


def eval_steps(steps_per_epoch: int, epochs: int, every: float) -> list[int]:
    """Optimizer steps after which validation runs: 0 (before training), then every `every` epoch."""
    n = round(epochs / every)
    return sorted({0} | {round(k * every * steps_per_epoch) for k in range(1, n + 1)})


def epoch_order(n: int, seed: int, epoch: int) -> list[int]:
    return random.Random(seed * 1000 + epoch).sample(range(n), n)


# ---------------------------------------------------------------- train


def train_job(job: dict, run: dict, src: Path, start: float) -> None:
    import torch
    import transformers
    from peft import LoraConfig, get_peft_model
    from transformers import get_cosine_schedule_with_warmup

    cfg = run["train"]
    name = job["name"]
    out = OUT / name
    out.mkdir(exist_ok=True)
    cuda = torch.cuda.is_available()
    dev = torch.device("cuda:0" if cuda else "cpu")
    dtype = getattr(torch, job.get("dtype", "float16")) if cuda else torch.float32
    fp16 = dtype == torch.float16
    seed = job["seed"]
    random.seed(seed)
    torch.manual_seed(seed)

    info = {
        "job": job,
        "train": cfg,
        "sdpa_gqa_flag_off": no_gqa_flag(),
        "kernels": kernel_paths(),
        "device": torch.cuda.get_device_name(0) if cuda else "cpu",
        "dtype": str(dtype),
    }
    path = model_path(run, job["model"])
    tok = transformers.AutoTokenizer.from_pretrained(path)
    model = transformers.AutoModelForCausalLM.from_pretrained(path, dtype=dtype, device_map={"": dev})
    model.config.use_cache = False
    lora = cfg["lora"]
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
    targets = sorted({n.split(".")[-1] for n, m in model.named_modules() if hasattr(m, "lora_A")})
    params = [p for p in model.parameters() if p.requires_grad]
    info |= {
        "model_class": type(model.get_base_model()).__name__,
        "parameters": sum(p.numel() for p in model.parameters()),
        "trainable_parameters": sum(p.numel() for p in params),
        "lora_target_modules": targets,
    }

    train = [encode(tok, r["messages"]) for r in read_jsonl(src / job["train_file"])]
    valid = [encode(tok, r["messages"]) for r in read_jsonl(src / job["valid_file"])]
    batch = cfg["effective_batch"]
    steps_per_epoch = math.ceil(len(train) / batch)
    total_steps = steps_per_epoch * job["epochs"]
    warmup = math.ceil(cfg["warmup_share"] * total_steps)
    evals = eval_steps(steps_per_epoch, job["epochs"], cfg["eval_every_epochs"])
    info |= {
        "train_rows": len(train),
        "valid_rows": len(valid),
        "train_tokens": sum(len(x) for x, _ in train),
        "steps_per_epoch": steps_per_epoch,
        "total_steps": total_steps,
        "warmup_steps": warmup,
        "eval_steps": evals,
    }
    opt = torch.optim.AdamW(params, lr=job["lr"], weight_decay=cfg["weight_decay"])
    sched = get_cosine_schedule_with_warmup(opt, warmup, total_steps)
    scaler = torch.amp.GradScaler("cuda", enabled=fp16)
    state = {"opt_step": 0, "epoch": 0, "pos": 0, "best_val": None, "best_step": None, "skipped_updates": 0}

    resume = job.get("resume")
    if resume:
        ck = torch.load(src / resume / "state.pt", map_location=dev, weights_only=False)
        model.load_state_dict(ck["trainable"], strict=False)
        opt.load_state_dict(ck["optimizer"])
        sched.load_state_dict(ck["scheduler"])
        if fp16:
            scaler.load_state_dict(ck["scaler"])
        state = ck["state"]
        random.setstate(ck["rng"]["python"])
        # map_location moved these to the GPU; set_rng_state takes CPU ByteTensors (session 20261023T115559Z failed here)
        torch.set_rng_state(ck["rng"]["torch"].cpu())
        if cuda:
            torch.cuda.set_rng_state(ck["rng"]["cuda"].cpu())
        for f in ("steps.jsonl", "val.jsonl"):  # keep the history in this session's output
            if (src / resume / f).exists():
                shutil.copy(src / resume / f, out / f)
        if (src / resume / "best").exists() and not (out / "best").exists():
            shutil.copytree(src / resume / "best", out / "best")
        info["resumed_from"] = {"path": resume, **state}
    write_json(out / "config.json", info)
    log(
        f"{name}: {info['model_class']} {info['trainable_parameters']:,} trainable on {targets}; "
        f"{len(train)} rows, {total_steps} steps ({steps_per_epoch}/epoch), evals at {evals}; "
        f"kernels {info['kernels']}; start at step {state['opt_step']}"
    )

    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    multiple = cfg.get("pad_to_multiple")  # absent in v0.1 runs: exact lengths, as they were trained

    def row_loss(ids: list[int], offset: int):
        n = len(ids)
        x = torch.tensor([bucket(ids, multiple, pad_id)], device=dev)
        # keep the logits from the one before the answer to the end; the first n - offset predict the answer
        with torch.autocast("cuda", dtype=torch.float16, enabled=fp16):
            logits = model(input_ids=x, logits_to_keep=x.shape[1] - offset + 1).logits[0, : n - offset]
        return torch.nn.functional.cross_entropy(logits.float(), x[0, offset:n], reduction="sum"), n - offset

    def validate() -> dict:
        model.eval()
        t0, total, n = time.perf_counter(), 0.0, 0
        with torch.no_grad():
            for ids, offset in valid:
                s, k = row_loss(ids, offset)
                total, n = total + float(s), n + k
        model.train()
        return {"val_loss": total / n, "val_tokens": n, "seconds": round(time.perf_counter() - t0, 1)}

    def save_last(status: str) -> None:
        d = out / "last"
        tmp = out / "last.tmp"
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir()
        torch.save(
            {
                "trainable": {k: v for k, v in model.state_dict().items() if "lora_" in k},
                "optimizer": opt.state_dict(),
                "scheduler": sched.state_dict(),
                "scaler": scaler.state_dict() if fp16 else None,
                "state": state,
                "rng": {
                    "python": random.getstate(),
                    "torch": torch.get_rng_state(),
                    "cuda": torch.cuda.get_rng_state() if cuda else None,
                },
            },
            tmp / "state.pt",
        )
        for f in ("steps.jsonl", "val.jsonl"):
            if (out / f).exists():
                shutil.copy(out / f, tmp / f)
        if (out / "best").exists():
            shutil.copytree(out / "best", tmp / "best")
        write_json(tmp / "status.json", {"status": status, **state})
        shutil.rmtree(d, ignore_errors=True)
        tmp.replace(d)

    def maybe_eval() -> None:
        if state["opt_step"] not in evals:
            return
        done = (
            {json.loads(x)["opt_step"] for x in (out / "val.jsonl").read_text().splitlines()}
            if (out / "val.jsonl").exists()
            else set()
        )
        if state["opt_step"] in done:
            return
        # step 0 is the base model's loss: a reference, never the kept checkpoint
        v = validate() | {"opt_step": state["opt_step"], "epoch": state["opt_step"] / steps_per_epoch}
        better = state["best_val"] is None or v["val_loss"] < state["best_val"]
        if better and state["opt_step"] > 0:
            state["best_val"], state["best_step"] = v["val_loss"], state["opt_step"]
            model.save_pretrained(out / "best")
            write_json(out / "best" / "best.json", v)
        v["best"] = better and state["opt_step"] > 0
        with (out / "val.jsonl").open("a") as f:
            f.write(json.dumps(v) + "\n")
        log(
            f"{name}: val step {v['opt_step']} loss {v['val_loss']:.4f} ({v['seconds']} s){' best' if v['best'] else ''}"
        )

    if job.get("pad_check_rows") and not resume:
        # the same rows scored with exact lengths and with buckets: the losses must agree to fp16 rounding
        model.eval()
        with torch.no_grad():
            rows_ = valid[: job["pad_check_rows"]]
            saved, multiple = multiple, None
            exact = [float(row_loss(i, o)[0]) for i, o in rows_]
            multiple = saved
            padded = [float(row_loss(i, o)[0]) for i, o in rows_]
        model.train()
        diff = max(abs(a - b) / max(abs(a), 1e-9) for a, b in zip(exact, padded, strict=True))
        write_json(
            out / "pad_check.json",
            {
                "rows": len(rows_),
                "multiple": multiple,
                "exact": exact,
                "padded": padded,
                "max_rel_diff": diff,
            },
        )
        log(f"{name}: pad check on {len(rows_)} rows, max relative loss difference {diff:.2e}")
    model.train()
    maybe_eval()
    status, reason = "done", None
    deadline = start + run["deadline_hours"] * 3600
    session_steps, stop_after = 0, job.get("stop_after_steps")  # stop_after_steps: for the local resume test
    while state["opt_step"] < total_steps:
        if time.time() > deadline or (stop_after is not None and session_steps >= stop_after):
            status = "paused"
            break
        free = parse_meminfo(_read("/proc/meminfo") or "").get("MemAvailable")
        if free is not None and free < MIN_FREE_GB:
            status, reason = "paused", f"low host memory: {free} GB available"
            log(f"{name}: {reason}")
            break
        order = epoch_order(len(train), seed, state["epoch"])
        rows = order[state["pos"] : state["pos"] + batch]
        if cuda:
            torch.cuda.reset_peak_memory_stats(0)
        t0 = time.perf_counter()
        loss_sum, tokens = 0.0, 0
        try:
            for i in rows:
                ids, offset = train[i]
                s, k = row_loss(ids, offset)
                loss = s / k / len(rows)
                scaler.scale(loss).backward()
                loss_sum += float(loss.detach())
                tokens += len(ids)
            scaler.unscale_(opt)
            grad_norm = float(torch.nn.utils.clip_grad_norm_(params, cfg["max_grad_norm"]))
            scale_before = scaler.get_scale() if fp16 else 1.0
            scaler.step(opt)
            scaler.update()
            skipped = fp16 and scaler.get_scale() < scale_before
        except torch.cuda.OutOfMemoryError as e:  # recorded; the batch is skipped, training goes on
            log(f"{name}: OOM at step {state['opt_step'] + 1}: {str(e)[:200]}")
            grad_norm, skipped = float("nan"), True
            scaler = torch.amp.GradScaler("cuda", init_scale=scaler.get_scale(), enabled=fp16)
        opt.zero_grad(set_to_none=True)
        if skipped:
            state["skipped_updates"] += 1
        else:
            sched.step()
        state["pos"] += len(rows)
        if state["pos"] >= len(train):
            state["epoch"], state["pos"] = state["epoch"] + 1, 0
        state["opt_step"] += 1
        session_steps += 1
        rec = {
            "opt_step": state["opt_step"],
            "epoch": round(state["opt_step"] / steps_per_epoch, 4),
            "rows": len(rows),
            "tokens": tokens,
            "loss": loss_sum,
            "grad_norm": grad_norm,
            "lr": sched.get_last_lr()[0],
            "scale": scaler.get_scale() if fp16 else None,
            "skipped": bool(skipped),
            "seconds": round(time.perf_counter() - t0, 2),
            "peak_memory_gb": round(torch.cuda.max_memory_allocated(0) / 1e9, 2) if cuda else None,
            "rss_gb": rss_gb(),
            "mem_available_gb": parse_meminfo(_read("/proc/meminfo") or "").get("MemAvailable"),
        }
        with (out / "steps.jsonl").open("a") as f:
            f.write(json.dumps(rec) + "\n")
        if state["opt_step"] % 10 == 0:
            log(
                f"{name}: step {state['opt_step']}/{total_steps} loss {loss_sum:.4f} lr {rec['lr']:.2e} "
                f"{rec['seconds']} s/step, {rec['tokens']} tok"
            )
        maybe_eval()
        if state["opt_step"] % cfg["checkpoint_every"] == 0:
            save_last("running")
    save_last(status)
    write_json(
        out / "status.json",
        {"status": status, **state, "finished_at": datetime.now(UTC).isoformat()}
        | ({"reason": reason} if reason else {}),
    )
    log(
        f"{name}: {status} at step {state['opt_step']}/{total_steps}, best val {state['best_val']} @ {state['best_step']}"
    )


# ---------------------------------------------------------------- score


def unfinished_training(job: dict) -> str | None:
    """Why a score job with `after_train` can't run yet (its training didn't finish this session), else None."""
    if not job.get("after_train"):
        return None
    st = OUT / job["after_train"] / "status.json"
    trained = json.loads(st.read_text())["status"] if st.exists() else "missing"
    return None if trained == "done" else f"{job['after_train']} is {trained}"


def score_job(job: dict, run: dict, src: Path, start: float) -> None:
    import torch
    import transformers
    from peft import PeftModel

    name = job["name"]
    out = OUT / name
    out.mkdir(exist_ok=True)
    if reason := unfinished_training(job):
        write_json(out / "status.json", {"status": "skipped", "reason": reason})
        log(f"{name}: skipped ({reason})")
        return
    cuda = torch.cuda.is_available()
    dev = torch.device("cuda:0" if cuda else "cpu")
    dtype = torch.float16 if cuda else torch.float32
    path = model_path(run, job["model"])
    info = {"job": job, "sdpa_gqa_flag_off": no_gqa_flag(), "kernels": kernel_paths(), "dtype": str(dtype)}
    tok = transformers.AutoTokenizer.from_pretrained(path)
    model = transformers.AutoModelForCausalLM.from_pretrained(path, dtype=dtype, device_map={"": dev})
    if job.get("adapter"):
        adapter = src / job["adapter"] if (src / job["adapter"]).exists() else OUT / job["adapter"]
        info["adapter_path"] = str(adapter)
        info["adapter_sha256"] = hashlib.sha256(
            (adapter / "adapter_model.safetensors").read_bytes()
        ).hexdigest()
        model = PeftModel.from_pretrained(model, adapter).merge_and_unload()
    model.eval()
    write_json(out / "config.json", info)
    gen = run["generation"]
    requests = read_jsonl(src / job["requests"])
    done = set()
    outputs = out / "outputs.jsonl"
    if outputs.exists():  # resume: skip what this session already answered
        done = {json.loads(x)["id"] for x in outputs.read_text().splitlines()}
    deadline = start + run["deadline_hours"] * 3600
    status = "done"
    with outputs.open("a") as f:
        for k, req in enumerate(requests, 1):
            if req["id"] in done:
                continue
            if time.time() > deadline:
                status = "paused"
                break
            msgs = [{"role": "system", "content": req["system"]}, {"role": "user", "content": req["user"]}]
            ids = tok.apply_chat_template(
                msgs, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt"
            )["input_ids"].to(dev)
            t = time.perf_counter()
            rec = {"id": req["id"], "input_tokens": int(ids.shape[1])}
            try:
                with torch.inference_mode():
                    o = model.generate(
                        ids,
                        attention_mask=torch.ones_like(ids),
                        do_sample=False,
                        max_new_tokens=gen["max_new_tokens"],
                        pad_token_id=tok.pad_token_id or tok.eos_token_id,
                    )
                new = o[0, ids.shape[1] :]
                rec |= {
                    "text": tok.decode(new, skip_special_tokens=True),
                    "output_tokens": int(new.shape[0]),
                    "finish_reason": "length" if new.shape[0] >= gen["max_new_tokens"] else "stop",
                }
            except Exception as e:  # recorded per request
                rec["error"] = f"{type(e).__name__}: {e}"[:1000]
            rec["latency_ms"] = round((time.perf_counter() - t) * 1000)
            rec["at"] = datetime.now(UTC).isoformat()
            f.write(json.dumps(rec) + "\n")
            f.flush()
            if k % 20 == 0:
                log(
                    f"{name}: {k}/{len(requests)} ({rec.get('output_tokens')} tok, {rec['latency_ms'] / 1000:.1f} s)"
                )
    write_json(out / "status.json", {"status": status, "answered": len(outputs.read_text().splitlines())})
    log(f"{name}: {status}")


# ---------------------------------------------------------------- driver


def run_jobs_on_gpu(gpu: int, jobs: list[dict], start: float, child_env: dict) -> subprocess.Popen:
    """One shell process per GPU that runs its jobs one after another."""
    env = {**child_env, "CUDA_VISIBLE_DEVICES": str(gpu), "ORDERSLM_SESSION_START": str(start)}
    # ";" not "&&": a failed job (recorded in its status.json) doesn't stop the next one on that GPU
    cmd = "; ".join(shlex.join([sys.executable, __file__, "--job", json.dumps(j["name"])]) for j in jobs)
    return subprocess.Popen(["bash", "-c", cmd], env=env)


def main() -> None:
    start = time.time()
    src = find_input()
    run = json.loads((src / "run.json").read_text())
    if missing := missing_inputs(run, src):
        write_json(OUT / "env.json", {"session": run["session"], "missing_inputs": missing})
        log(f"session {run['session']}: missing inputs, nothing run: {missing}")
        raise SystemExit(1)
    pins = run["packages"]
    env: dict = {"session": run["session"], "started_at": datetime.now(UTC).isoformat(), "jobs": {}}
    if not run.get("local_test"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *pins["main"]])
        # peft 0.21.2 raises ImportError whenever torchao < 0.16 is installed (Kaggle ships 0.10); unused here.
        r = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"], capture_output=True
        )
        env["torchao_uninstall"] = r.returncode
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "--no-deps", "--target", FLA_SITE, *pins["fla"]],
            capture_output=True,
            text=True,
        )
        env["fla_install"] = {"returncode": r.returncode, "stderr": r.stderr[-1000:]}
    import peft
    import torch
    import transformers

    env |= {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "peft": peft.__version__,
        "cuda": torch.version.cuda,
        "gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        "python": sys.version.split()[0],
        "mounts": mount_types(_read("/proc/mounts") or ""),
        "host_memory_at_start": host_memory(),
    }
    log(
        f"session {run['session']}: torch {env['torch']}, transformers {env['transformers']}, GPUs {env['gpus']}"
    )
    child_env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    child_env["PYTHONPATH"] = FLA_SITE + os.pathsep + child_env.get("PYTHONPATH", "")
    by_gpu: dict[int, list[dict]] = {}
    for j in run["jobs"]:
        by_gpu.setdefault(j["gpu"], []).append(j)
    procs = {g: run_jobs_on_gpu(g, js, start, child_env) for g, js in sorted(by_gpu.items())}
    with (OUT / "memory.jsonl").open("a") as mem:
        while any(p.poll() is None for p in procs.values()):
            try:  # a failed reading must never end the session (Kaggle would kill the jobs with it)
                rec = {"t": round(time.time() - start), **host_memory(procs)}
            except Exception as e:
                rec = {"t": round(time.time() - start), "error": f"{type(e).__name__}: {e}"[:300]}
            mem.write(json.dumps(rec) + "\n")
            mem.flush()
            time.sleep(MEMORY_EVERY)
    for g, p in procs.items():
        env["jobs"][f"gpu{g}"] = {"jobs": [j["name"] for j in by_gpu[g]], "exit_code": p.returncode}
    for j in run["jobs"]:
        st = OUT / j["name"] / "status.json"
        env["jobs"][j["name"]] = json.loads(st.read_text()) if st.exists() else {"status": "failed"}
    env["finished_at"] = datetime.now(UTC).isoformat()
    write_json(OUT / "env.json", env)
    log("done")


def child(name: str) -> None:
    src = find_input()
    run = json.loads((src / "run.json").read_text())
    job = next(j for j in run["jobs"] if j["name"] == name)
    start = float(os.environ.get("ORDERSLM_SESSION_START", time.time()))
    try:
        (train_job if job["kind"] == "train" else score_job)(job, run, src, start)
    except Exception as e:
        import traceback

        (OUT / name).mkdir(exist_ok=True)
        write_json(OUT / name / "status.json", {"status": "failed", "error": traceback.format_exc()[-3000:]})
        log(f"{name}: failed: {type(e).__name__}: {str(e)[:300]}")
        raise


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--job":
        child(json.loads(sys.argv[2]))
    else:
        main()
