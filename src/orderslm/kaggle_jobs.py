"""Drive Kaggle script kernels from this repo (docs/KAGGLE.md). Uses the `kaggle` CLI (uv tool, outside the project).

    make kaggle-push JOB=julia-audit    # upload kaggle/<job>/upload/ as the job's private dataset, start the kernel
    make kaggle-status JOB=julia-audit
    make kaggle-pull JOB=julia-audit    # when complete: kernel output → kaggle/<job>/output/ (gitignored)

Each job folder holds `run.py` + `kernel-metadata.json` (private, its dataset in `dataset_sources`). The dataset is
whatever the job's own export staged in `upload/` (never test or PIZZA data, never secrets).
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from orderslm.paths import ROOT

KAGGLE_DIR = ROOT / "kaggle"


def _kaggle(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["kaggle", *args], capture_output=True, text=True, check=check)


def _meta(job: str) -> dict:
    return json.loads((KAGGLE_DIR / job / "kernel-metadata.json").read_text())


def _dataset_status(dataset: str) -> str:
    r = _kaggle("datasets", "status", dataset, check=False)
    return (r.stdout + r.stderr).strip().lower()


def push(job: str) -> None:
    job_dir = KAGGLE_DIR / job
    stage = job_dir / "upload"
    meta = _meta(job)
    if not meta.get("is_private", False):
        raise SystemExit(f"{job}: kernel-metadata.json must have is_private: true")
    dataset = json.loads((stage / "dataset-metadata.json").read_text())["id"]
    if meta["id"] == dataset:  # Kaggle answers 409 Conflict on kernels push
        raise SystemExit(f"{job}: kernel and dataset need different slugs ({dataset})")
    if dataset not in meta["dataset_sources"]:
        raise SystemExit(f"{job}: kernel does not read the staged dataset {dataset}")
    status = _dataset_status(dataset)
    if "ready" in status:
        print(f"New version of {dataset}")
        _kaggle("datasets", "version", "-p", str(stage), "-m", f"staged {time.strftime('%Y-%m-%dT%H:%M:%S')}")
    else:
        print(f"Creating private dataset {dataset}")
        _kaggle("datasets", "create", "-p", str(stage))
    time.sleep(10)  # the status call can lag behind the upload
    for _ in range(60):
        if "ready" in (status := _dataset_status(dataset)):
            break
        time.sleep(10)
    else:
        raise SystemExit(f"{dataset} not ready after 10 min: {status}")
    r = _kaggle("kernels", "push", "-p", str(job_dir))
    print(r.stdout.strip())


def status(job: str) -> str:
    out = _kaggle("kernels", "status", _meta(job)["id"]).stdout.strip()
    print(out)
    return out


def pull(job: str) -> Path:
    s = status(job).lower()
    if "complete" not in s and "error" not in s:
        raise SystemExit("kernel not finished yet")
    out = KAGGLE_DIR / job / "output"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    r = _kaggle("kernels", "output", _meta(job)["id"], "-p", str(out))
    print(r.stdout.strip())
    print(f"Saved {out.relative_to(ROOT)}/: {sorted(p.name for p in out.iterdir())}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["push", "status", "pull"])
    ap.add_argument("job")
    args = ap.parse_args(argv)
    {"push": push, "status": status, "pull": pull}[args.cmd](args.job)
    return 0


if __name__ == "__main__":
    sys.exit(main())
