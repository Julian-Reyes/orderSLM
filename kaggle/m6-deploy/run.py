"""Kaggle script kernel (2 × T4): package the picked M6 student for local use and check it (docs/KAGGLE.md job D).

Standalone (no orderslm import). Input: the private dataset staged by `orderslm.train.kaggle_deploy export`
(run.json, the student's LoRA adapter, dev + fresh requests). Steps, in order:

1. **merge**: base model (Hub, pinned revision) in fp16 + the adapter, merged (`merge_and_unload`), saved as a
   full HF model; the base's own tokenizer files are copied next to it unchanged. Same dtype and merge as the M6
   scoring runs (kaggle/m6/run.py `score_job`), in a child process so its GPU memory is freed after.
2. **convert**: llama.cpp's `convert_hf_to_gguf.py` (source at the pinned tag) → F16 GGUF; `llama-quantize` →
   each quantized format. GGUF files stay in /kaggle/working/gguf/ (kernel output on Kaggle; `make kaggle-pull`
   skips them).
3. **prompts**: every request rendered with the base tokenizer's chat template (as `score_job` does) to token ids;
   llama-server gets the ids (no BOS added for an id array), so every format sees the identical input.
4. **gpu**: one llama-server per GPU (prebuilt CUDA build, all layers on the GPU, one slot, no prompt cache),
   greedy (`samplers: ["top_k"]`, `top_k: 1`), every dev + fresh request per format; jobs on the same GPU run one
   after another, the two GPUs in parallel.
5. **cpu**: after the GPU jobs, the CPU build (no GPU visible, all cores) on a fixed sample of dev requests, for
   CPU latency.

Stop rules (run 1, 2026-11-04, ran 11 h on the CPU because the prebuilt CUDA backend silently did not load):
- before anything else, llama-server must list a CUDA device (`--list-devices`); if the prebuilt build lists none,
  llama.cpp is built from source for the T4 (sm_75); if that lists none either, nothing else runs.
- after each GPU job's first answer, the GPU must hold the model (run.json `guard.min_gpu_mib`) and generate faster
  than a CPU (`guard.min_output_tok_s`); 3 failed requests in a row also count. Any of these stops every job.
- the deadline (run.json `deadline_hours`) is checked before every request.

Each job writes `<job>/outputs.jsonl` (id, input_tokens, text, output_tokens, finish_reason, latency_ms, timings),
`<job>/status.json` and `<job>/memory.json` (peak GPU memory and server RSS). env.json records versions, hardware,
GGUF sizes + sha256 and each step's result. A step that fails is recorded and the next steps that need it are
skipped. Paths can be moved for a local test with ORDERSLM_KAGGLE_IN / ORDERSLM_KAGGLE_OUT.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

OUT = Path(os.environ.get("ORDERSLM_KAGGLE_OUT", "/kaggle/working"))
IN = Path(os.environ.get("ORDERSLM_KAGGLE_IN", "/kaggle/input"))
WORK = Path(os.environ.get("ORDERSLM_KAGGLE_TMP", "/tmp/deploy"))
MERGED = WORK / "merged"
GGUF = OUT / "gguf"
OUT.mkdir(parents=True, exist_ok=True)
LOG = (OUT / "run.log").open("a")
GB = 1e9
STOP = threading.Event()  # set by a stop rule: every queue ends before its next request
STOP_REASON: list[str] = []


def stop_all(reason: str) -> None:
    if not STOP.is_set():
        STOP_REASON.append(reason)
        STOP.set()
        log(f"STOP: {reason}")


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def find_input() -> Path:
    hits = sorted(IN.rglob("run.json"))
    if len(hits) != 1:
        raise SystemExit(f"expected one run.json under {IN}, found {hits}")
    return hits[0].parent


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2) + "\n")
    tmp.replace(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def missing_inputs(run: dict, src: Path) -> list[str]:
    need = [f"{run['adapter']}/{f}" for f in ("adapter_config.json", "adapter_model.safetensors")]
    need += sorted({j["requests"] for j in run["jobs"]})
    return [f for f in need if not (src / f).is_file()]


def gguf_name(fmt: str) -> str:
    return f"{fmt.lower()}.gguf"


# ---------------------------------------------------------------- llama-server requests


def completion_payload(ids: list[int], gen: dict) -> dict:
    """Greedy, the same limit as the transformers scoring runs; no prompt cache, so every request is timed cold."""
    return {
        "prompt": ids,
        "n_predict": gen["max_new_tokens"],
        "samplers": ["top_k"],
        "top_k": 1,
        "temperature": 0.0,
        "cache_prompt": False,
    }


def record(req_id: str, ids: list[int], resp: dict, latency_ms: int) -> dict:
    """One outputs.jsonl line in the shape of the transformers scoring runs (+ llama.cpp's own timings)."""
    return {
        "id": req_id,
        "input_tokens": len(ids),
        "text": resp.get("content", ""),
        "output_tokens": resp.get("tokens_predicted"),
        "finish_reason": "length" if resp.get("stop_type") == "limit" else "stop",
        "stop_type": resp.get("stop_type"),
        "truncated": resp.get("truncated"),
        "tokens_evaluated": resp.get("tokens_evaluated"),
        "timings": resp.get("timings"),
        "latency_ms": latency_ms,
        "at": datetime.now(UTC).isoformat(),
    }


def gpu_problem(used_mib: int | None, rec: dict, guard: dict) -> str | None:
    """Why the first answer of a GPU job shows the model is not running on the GPU (None: it is)."""
    if "error" in rec:
        return f"the first request failed: {rec['error'][:300]}"
    if used_mib is None or used_mib < guard["min_gpu_mib"]:
        return f"the GPU holds {used_mib} MiB after the first answer (< {guard['min_gpu_mib']}): model not on the GPU"
    tps = (rec.get("timings") or {}).get("predicted_per_second")
    if tps is not None and tps < guard["min_output_tok_s"]:
        return f"{tps:.1f} output tok/s on the first answer (< {guard['min_output_tok_s']}): not GPU speed"
    return None


def post(url: str, payload: dict, timeout: float = 900) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def wait_ready(port: int, proc: subprocess.Popen, timeout: float = 600) -> None:
    end = time.time() + timeout
    while time.time() < end:
        if proc.poll() is not None:
            raise RuntimeError(f"llama-server exited with {proc.returncode}")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as r:
                if r.status == 200:
                    return
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2)
    raise RuntimeError("llama-server not ready in time")


# ---------------------------------------------------------------- memory


def rss_gb(pid: int) -> float | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return round(int(line.split()[1]) * 1024 / GB, 3)
    except OSError:
        return None
    return None


def gpu_used_mib(gpu: int) -> int | None:
    try:
        r = subprocess.run(
            ["nvidia-smi", f"--id={gpu}", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        return int(r.stdout.strip().splitlines()[0])
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return None


class PeakMemory(threading.Thread):
    """Peak server RSS and (on a GPU) peak memory used on that GPU, sampled every few seconds."""

    def __init__(self, pid: int, gpu: int | None, every: float = 3.0):
        super().__init__(daemon=True)
        self.pid, self.gpu, self.every = pid, gpu, every
        self.peak_rss_gb = 0.0
        self.peak_gpu_mib = 0
        self.samples = 0
        self._stop = threading.Event()

    def run(self) -> None:
        while not self._stop.is_set():
            try:  # a failed reading must never end the job
                if (r := rss_gb(self.pid)) is not None:
                    self.peak_rss_gb = max(self.peak_rss_gb, r)
                if self.gpu is not None and (g := gpu_used_mib(self.gpu)) is not None:
                    self.peak_gpu_mib = max(self.peak_gpu_mib, g)
                self.samples += 1
            except Exception:
                pass
            self._stop.wait(self.every)

    def stop(self) -> dict:
        self._stop.set()
        self.join(timeout=30)
        return {
            "peak_server_rss_gb": self.peak_rss_gb,
            "peak_gpu_used_mib": self.peak_gpu_mib if self.gpu is not None else None,
            "samples": self.samples,
        }


# ---------------------------------------------------------------- setup


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        log(f"download {url}")
        urllib.request.urlretrieve(url, dest)
    return dest


def extract(archive: Path, into: Path) -> Path:
    if not into.exists():
        into.mkdir(parents=True)
        with tarfile.open(archive) as t:
            t.extractall(into, filter="data")
    return into


def find_file(root: Path, name: str) -> Path:
    hits = sorted(p for p in root.rglob(name) if p.is_file())
    if not hits:
        raise FileNotFoundError(f"{name} not found under {root}")
    return hits[0]


DRIVER_DIRS = [
    "/usr/local/nvidia/lib64",
    "/usr/local/nvidia/lib",
    "/usr/lib64-nvidia",
    "/usr/lib/x86_64-linux-gnu",
]


def driver_lib() -> Path | None:
    """The NVIDIA driver library (libcuda.so.1) as the system loader finds it (ctypes: no CUDA context, so no GPU
    memory used), else the first one in a usual place. Run 2 (2026-11-05): the CUDA backend could not find it once
    LD_LIBRARY_PATH held only the llama.cpp folders."""
    try:
        import ctypes

        ctypes.CDLL("libcuda.so.1")
        for line in Path("/proc/self/maps").read_text().splitlines():
            path = line.split()[-1]
            if "/libcuda.so" in path and Path(path).exists():
                return Path(path)
    except Exception:
        pass
    return next((Path(d) / "libcuda.so.1" for d in DRIVER_DIRS if (Path(d) / "libcuda.so.1").exists()), None)


def lib_dirs(*roots: Path) -> str:
    """Every folder holding a shared library in the extracted builds (the binaries load their ggml backends), then
    the driver's folder and the machine's own LD_LIBRARY_PATH (added to, never replaced)."""
    dirs = sorted({str(p.parent) for r in roots for p in r.rglob("*.so*")})
    if (drv := driver_lib()) is not None:
        dirs.append(str(drv.parent))
    dirs += [d for d in os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep) if d]
    return os.pathsep.join(dict.fromkeys(dirs))


def probe(build: dict) -> dict:
    """The devices llama-server sees, and for a build with a CUDA backend library, any library it cannot find."""
    env = {**os.environ, "LD_LIBRARY_PATH": build["ld_library_path"]}
    try:
        r = subprocess.run(
            [build["server"], "--list-devices"], capture_output=True, text=True, timeout=120, env=env
        )
        out = (r.stdout + r.stderr)[-3000:]
    except (OSError, subprocess.SubprocessError) as e:
        out = f"{type(e).__name__}: {e}"
    info: dict = {"list_devices": out, "cuda": "CUDA0" in out, "driver_lib": str(driver_lib())}
    lib = next(iter(sorted(Path(build["server"]).parent.glob("libggml-cuda.so*"))), None)
    if lib:
        r = subprocess.run(["ldd", str(lib)], capture_output=True, text=True, env=env)
        info["ldd_libggml_cuda_not_found"] = [x.strip() for x in r.stdout.splitlines() if "not found" in x]
    return info


def build_cuda(source: Path) -> dict:
    """llama-server built from the pinned source with CUDA for the T4 (sm_75), when the prebuilt one sees no GPU."""
    nvcc = shutil.which("nvcc") or next(
        (str(p) for p in sorted(Path("/usr/local").glob("cuda*/bin/nvcc"))), None
    )
    if not nvcc:
        raise RuntimeError("no nvcc on this machine: cannot build llama.cpp with CUDA")
    cmake = shutil.which("cmake")
    if not cmake:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "cmake"])
        cmake = shutil.which("cmake") or str(Path(sys.executable).parent / "cmake")
    build = WORK / "llama.cpp" / "cuda-src"
    configure = [cmake, "-S", str(source), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release", "-DGGML_CUDA=ON"]
    configure += ["-DCMAKE_CUDA_ARCHITECTURES=75", f"-DCMAKE_CUDA_COMPILER={nvcc}", "-DGGML_NATIVE=OFF"]
    configure += ["-DLLAMA_CURL=OFF", "-DLLAMA_BUILD_TESTS=OFF"]
    if (drv := driver_lib()) is not None:  # run 2: CMake found no CUDA::cuda_driver (no toolkit stub)
        configure.append(f"-DCUDA_cuda_driver_LIBRARY={drv}")
    compile_ = [cmake, "--build", str(build), "--target", "llama-server", "-j", str(os.cpu_count())]
    for cmd, limit in ((configure, 600), (compile_, 3000)):
        log(f"build: {' '.join(cmd[:4])} ...")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=limit)
        if r.returncode != 0:
            raise RuntimeError(f"{cmd[1]} {cmd[2]} failed: {(r.stdout + r.stderr)[-1500:]}")
    server = find_file(build, "llama-server")
    return {"server": str(server), "ld_library_path": lib_dirs(build / "bin"), "nvcc": nvcc}


def setup_llama(run: dict) -> dict:
    """Source (converter + gguf-py) and the prebuilt CUDA and CPU builds at the pinned tag."""
    lc = run["llama_cpp"]
    base = WORK / "llama.cpp"
    paths = {}
    for key in ("source", "cuda", "cudart", "cpu"):
        url = lc["urls"][key]
        archive = download(url, base / "archives" / url.rsplit("/", 1)[1])
        paths[key] = extract(archive, base / key)
    builds = {}
    for key, extra in (("cuda", (paths["cuda"], paths["cudart"])), ("cpu", (paths["cpu"],))):
        builds[key] = {
            "server": str(find_file(paths[key], "llama-server")),
            "ld_library_path": lib_dirs(*extra),
        }
    builds["quantize"] = str(find_file(paths["cpu"], "llama-quantize"))
    builds["convert"] = str(find_file(paths["source"], "convert_hf_to_gguf.py"))
    for b in (builds["cuda"]["server"], builds["cpu"]["server"], builds["quantize"]):
        os.chmod(b, 0o755)
    builds["cuda"]["probe"] = probe(builds["cuda"])
    builds["cuda_build"] = "prebuilt CUDA 12.8"
    if not builds["cuda"]["probe"]["cuda"]:
        log(f"the prebuilt CUDA build sees no GPU: {builds['cuda']['probe']}; building from source")
        write_json(OUT / "llama-probe.json", builds)
        own = build_cuda(Path(builds["convert"]).parent)
        own["probe"] = probe(own)
        builds["cuda_prebuilt"], builds["cuda"] = builds["cuda"], own
        builds["cuda_build"] = "built from source at the tag, CUDA sm_75"
    write_json(OUT / "llama-probe.json", builds)
    if not builds["cuda"]["probe"]["cuda"]:
        raise RuntimeError(
            f"llama-server sees no CUDA device: {builds['cuda']['probe']['list_devices'][-500:]}"
        )
    log(f"llama-server ({builds['cuda_build']}): {builds['cuda']['probe']['list_devices'].strip()[-300:]}")
    return builds


# ---------------------------------------------------------------- steps


def merge_step(run: dict, src: Path) -> dict:
    """Child process: base fp16 + adapter merged on GPU 0, saved with the base's tokenizer files."""
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from peft import PeftModel

    m = run["model"]
    snap = Path(snapshot_download(m["repo"], revision=m["revision"]))
    dev = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = transformers.AutoModelForCausalLM.from_pretrained(snap, dtype=torch.float16, device_map={"": dev})
    adapter = src / run["adapter"]
    model = PeftModel.from_pretrained(model, adapter).merge_and_unload()
    if MERGED.exists():
        shutil.rmtree(MERGED)
    model.save_pretrained(MERGED, safe_serialization=True)
    copied = []
    for f in sorted(snap.iterdir()):  # the base's own tokenizer and chat-template files, unchanged
        weights = f.suffix == ".safetensors" or f.name.endswith(".index.json")
        if f.is_file() and not weights and not (MERGED / f.name).exists():
            shutil.copy(f, MERGED / f.name)
            copied.append(f.name)
    cfg = json.loads((MERGED / "config.json").read_text())
    return {
        "model_class": type(model).__name__,
        "architectures": cfg.get("architectures"),
        "model_type": cfg.get("model_type"),
        "adapter_sha256": sha256(adapter / "adapter_model.safetensors"),
        "copied_from_base": copied,
        "merged_gb": round(sum(p.stat().st_size for p in MERGED.iterdir()) / GB, 3),
    }


def convert_step(run: dict, builds: dict) -> dict:
    GGUF.mkdir(parents=True, exist_ok=True)
    f16 = GGUF / gguf_name("F16")
    r = subprocess.run(
        [sys.executable, builds["convert"], str(MERGED), "--outtype", "f16", "--outfile", str(f16)],
        capture_output=True,
        text=True,
    )
    info: dict = {"convert": {"returncode": r.returncode, "stderr_tail": r.stderr[-3000:]}}
    if r.returncode != 0:
        raise RuntimeError(f"convert failed: {r.stderr[-800:]}")
    env = {**os.environ, "LD_LIBRARY_PATH": builds["cpu"]["ld_library_path"]}
    for fmt in run["formats"]:
        if fmt == "F16":
            continue
        q = subprocess.run(
            [builds["quantize"], str(f16), str(GGUF / gguf_name(fmt)), fmt],
            capture_output=True,
            text=True,
            env=env,
        )
        info[f"quantize_{fmt}"] = {"returncode": q.returncode, "stderr_tail": q.stderr[-1500:]}
        if q.returncode != 0:
            raise RuntimeError(f"quantize {fmt} failed: {q.stderr[-800:]}")
    info["files"] = {
        fmt: {
            "file": gguf_name(fmt),
            "bytes": (GGUF / gguf_name(fmt)).stat().st_size,
            "sha256": sha256(GGUF / gguf_name(fmt)),
        }
        for fmt in run["formats"]
    }
    return info


def prompts_step(run: dict, src: Path) -> dict:
    """Token ids for every request, with the chat template exactly as the transformers scoring runs apply it."""
    import transformers

    tok = transformers.AutoTokenizer.from_pretrained(MERGED)
    counts = {}
    for f in sorted({j["requests"] for j in run["jobs"]}):
        lines = []
        for req in read_jsonl(src / f):
            msgs = [{"role": "system", "content": req["system"]}, {"role": "user", "content": req["user"]}]
            ids = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True, return_dict=False)
            if isinstance(ids, dict):
                ids = ids["input_ids"]
            lines.append(json.dumps({"id": req["id"], "ids": [int(i) for i in ids]}))
        (WORK / f"ids-{f}").write_text("\n".join(lines) + "\n")
        counts[f] = len(lines)
    return counts


def serve_job(job: dict, run: dict, builds: dict, port: int, deadline: float) -> None:
    name = job["name"]
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    gguf = GGUF / gguf_name(job["format"])
    if not gguf.exists():
        write_json(out / "status.json", {"status": "skipped", "reason": f"{gguf.name} missing"})
        return
    build = builds[job["device"]]
    env = {**os.environ, "LD_LIBRARY_PATH": build["ld_library_path"]}
    srv = run["server"]
    cmd = [build["server"], "-m", str(gguf), "--host", "127.0.0.1", "--port", str(port)]
    cmd += ["-c", str(srv["ctx_size"]), "-np", "1", "--no-webui"]
    if job["device"] == "cuda":
        env["CUDA_VISIBLE_DEVICES"] = str(job["gpu"])
        cmd += ["-ngl", "999"]
    else:
        env["CUDA_VISIBLE_DEVICES"] = ""
        cmd += ["-ngl", "0", "-t", str(os.cpu_count())]
    ids = {r["id"]: r["ids"] for r in read_jsonl(WORK / f"ids-{job['requests']}")}
    order = job.get("request_ids") or list(ids)
    server_log = (out / "server.log").open("w")
    proc = subprocess.Popen(cmd, env=env, stdout=server_log, stderr=subprocess.STDOUT)
    mem = PeakMemory(proc.pid, job["gpu"] if job["device"] == "cuda" else None)
    status, answered, failed_in_a_row = "done", 0, 0
    try:
        wait_ready(port, proc)
        mem.start()
        url = f"http://127.0.0.1:{port}/completion"
        with (out / "outputs.jsonl").open("w") as f:
            for k, rid in enumerate(order, 1):
                if STOP.is_set():
                    status = "stopped"
                    break
                if time.time() > deadline:
                    status = "paused"
                    break
                t = time.perf_counter()
                try:
                    resp = post(url, completion_payload(ids[rid], run["generation"]))
                    rec = record(rid, ids[rid], resp, round((time.perf_counter() - t) * 1000))
                except Exception as e:  # recorded per request
                    rec = {
                        "id": rid,
                        "input_tokens": len(ids[rid]),
                        "error": f"{type(e).__name__}: {e}"[:1000],
                        "latency_ms": round((time.perf_counter() - t) * 1000),
                    }
                f.write(json.dumps(rec) + "\n")
                f.flush()
                answered += 1
                failed_in_a_row = failed_in_a_row + 1 if "error" in rec else 0
                if failed_in_a_row >= 3:
                    stop_all(f"{name}: 3 failed requests in a row ({rec['error'][:200]})")
                if k == 1 and job["device"] == "cuda":
                    used = gpu_used_mib(job["gpu"])
                    log(
                        f"{name}: first answer, GPU {job['gpu']} holds {used} MiB, {rec.get('latency_ms')} ms"
                    )
                    if problem := gpu_problem(used, rec, run["guard"]):
                        stop_all(f"{name}: {problem}")
                if k % 25 == 0:
                    log(
                        f"{name}: {k}/{len(order)} ({rec.get('output_tokens')} tok, {rec['latency_ms'] / 1000:.1f} s)"
                    )
    except Exception as e:
        status = "failed"
        write_json(out / "error.json", {"error": f"{type(e).__name__}: {e}"[:3000]})
        log(f"{name}: failed: {type(e).__name__}: {str(e)[:300]}")
    finally:
        memory = mem.stop() if mem.is_alive() else {"samples": 0}
        proc.terminate()
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
        server_log.close()
    write_json(out / "memory.json", memory)
    write_json(out / "status.json", {"status": status, "answered": answered, "of": len(order), "cmd": cmd})
    log(f"{name}: {status} ({answered}/{len(order)})")


def run_queue(jobs: list[dict], run: dict, builds: dict, port: int, deadline: float) -> None:
    for j in jobs:
        if STOP.is_set():
            write_json(OUT / j["name"] / "status.json", {"status": "not started", "reason": STOP_REASON[:1]})
            continue
        try:
            serve_job(j, run, builds, port, deadline)
        except Exception as e:  # never let one job stop the rest
            write_json(OUT / j["name"] / "status.json", {"status": "failed", "error": str(e)[:2000]})


def hardware() -> dict:
    info: dict = {"cpu_count": os.cpu_count()}
    try:
        names = [
            x.split(":", 1)[1].strip()
            for x in Path("/proc/cpuinfo").read_text().splitlines()
            if x.startswith("model name")
        ]
        info["cpu_model"] = names[0] if names else None
    except OSError:
        info["cpu_model"] = None
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        info["gpus"] = [x.strip() for x in r.stdout.splitlines() if x.strip()]
    except (OSError, subprocess.SubprocessError):
        info["gpus"] = []
    try:
        mem = Path("/proc/meminfo").read_text().splitlines()[0]
        info["host_memory_gb"] = round(int(mem.split()[1]) * 1024 / GB, 1)
    except (OSError, ValueError, IndexError):
        info["host_memory_gb"] = None
    return info


def main() -> None:
    start = time.time()
    src = find_input()
    run = json.loads((src / "run.json").read_text())
    env: dict = {"session": run["session"], "started_at": datetime.now(UTC).isoformat(), "steps": {}}
    if missing := missing_inputs(run, src):
        env["missing_inputs"] = missing
        write_json(OUT / "env.json", env)
        log(f"missing inputs, nothing run: {missing}")
        raise SystemExit(1)
    WORK.mkdir(parents=True, exist_ok=True)
    deadline = start + run["deadline_hours"] * 3600

    def step(name: str, fn, *args):
        t = time.time()
        try:
            env["steps"][name] = {"status": "done", **(fn(*args) or {})}
        except Exception as e:
            import traceback

            env["steps"][name] = {"status": "failed", "error": traceback.format_exc()[-3000:]}
            log(f"{name}: failed: {type(e).__name__}: {str(e)[:300]}")
        env["steps"][name]["seconds"] = round(time.time() - t, 1)
        write_json(OUT / "env.json", env)
        return env["steps"][name]["status"] == "done"

    def install() -> dict:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *run["packages"]["main"]])
        # peft 0.21.2 raises ImportError whenever torchao < 0.16 is installed (Kaggle ships 0.10); unused here.
        r = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"], capture_output=True
        )
        return {"torchao_uninstall": r.returncode}

    def merge() -> dict:
        r = subprocess.run([sys.executable, __file__, "--merge"], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-2500:])
        return json.loads((WORK / "merge.json").read_text())

    builds: dict = {}

    def llama() -> dict:
        builds.update(setup_llama(run))
        return {"builds": builds, "cuda_build": builds["cuda_build"]}

    ok = step("install", install) if not run.get("local_test") else True
    import torch
    import transformers

    env |= {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda": torch.version.cuda,
        "python": sys.version.split()[0],
        "hardware": hardware(),
        "llama_cpp": run["llama_cpp"]["tag"],
    }
    log(
        f"session {run['session']}: torch {env['torch']}, transformers {env['transformers']}, {env['hardware']}"
    )
    ok = ok and step("llama_cpp", llama)
    ok = ok and step("merge", merge)
    ok = ok and step("convert", convert_step, run, builds)
    ok = ok and step("prompts", prompts_step, run, src)
    if ok:
        t = time.time()
        gpu_jobs = [j for j in run["jobs"] if j["device"] == "cuda"]
        threads = []
        for g in sorted({j["gpu"] for j in gpu_jobs}):
            js = [j for j in gpu_jobs if j["gpu"] == g]
            th = threading.Thread(target=run_queue, args=(js, run, builds, 8080 + g, deadline))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
        env["steps"]["gpu"] = {"seconds": round(time.time() - t, 1)}
        t = time.time()  # CPU timing only once the GPUs are idle (no other work competes for the cores)
        run_queue([j for j in run["jobs"] if j["device"] == "cpu"], run, builds, 8090, deadline)
        env["steps"]["cpu"] = {"seconds": round(time.time() - t, 1)}
    env["jobs"] = {}
    for j in run["jobs"]:
        st = OUT / j["name"] / "status.json"
        env["jobs"][j["name"]] = json.loads(st.read_text()) if st.exists() else {"status": "not run"}
    env["stopped"] = STOP_REASON[0] if STOP_REASON else None
    env["finished_at"] = datetime.now(UTC).isoformat()
    write_json(OUT / "env.json", env)
    log("done")


if __name__ == "__main__":
    if sys.argv[1:] == ["--merge"]:
        src = find_input()
        run = json.loads((src / "run.json").read_text())
        WORK.mkdir(parents=True, exist_ok=True)
        write_json(WORK / "merge.json", merge_step(run, src))
    else:
        main()
