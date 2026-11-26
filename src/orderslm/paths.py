"""Where data lives, and the guard that keeps the sealed test set sealed (spec §7, §19).

Code reaches the test split only through `test_split_dir()`, which refuses
unless ORDERSLM_UNSEAL_TEST is set to a reason (e.g. "final-eval M6"). Training
and synthetic-generation code must never call it; M2 adds a test that greps
for violations.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SAMPLES = DATA / "samples"
MENUS = DATA / "menus"  # M1
DEV = DATA / "dev"  # M2
FRESH = DATA / "fresh"  # M6: fresh Source A to measure the dev-based fixes (evaluation-only, like dev)
FRESH2 = (
    DATA / "fresh2"
)  # M6 v3: a second fresh batch, written after the v3 fixes that used fresh (evaluation-only)
FRESH3 = (
    DATA / "fresh3"
)  # M6 v4: written after the v4 fixes that used dev, fresh and fresh2 (evaluation-only)
FRESH4 = (
    DATA / "fresh4"
)  # M6 v5: written after the v5 fixes that used dev, fresh, fresh2, fresh3 (evaluation-only)
FRESH5 = (
    DATA / "fresh5"
)  # M6 v6: written after the v6 fixes that used dev, fresh, fresh2, fresh3 (evaluation-only)
SIM1 = (
    DATA / "sim1"
)  # live simulated-customer test: cards with hidden target orders + the live chats (evaluation-only)
_TEST = DATA / "test"  # M2, sealed
EXTERNAL = DATA / "external"  # third-party downloads + anything derived from them, gitignored
RUNS = ROOT / "runs"  # eval outputs, committed (M3+)

UNSEAL_ENV = "ORDERSLM_UNSEAL_TEST"


class SealedSplitError(PermissionError):
    pass


def test_split_dir() -> Path:
    reason = os.environ.get(UNSEAL_ENV, "").strip()
    if not reason:
        raise SealedSplitError(
            f"The test split is sealed. Set {UNSEAL_ENV}=<reason> only for final evaluation runs; "
            "never for training, prompt tuning or data generation."
        )
    return _TEST


test_split_dir.__test__ = False  # not a pytest test, despite the name
