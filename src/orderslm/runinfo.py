"""What every run records about the code it ran with (spec §19)."""

import subprocess

from orderslm.paths import ROOT


def git_commit() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    return (out.stdout.strip() or "unknown") + ("-dirty" if dirty.stdout.strip() else "")
