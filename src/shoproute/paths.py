"""Where data lives, and the guard that keeps the sealed test set sealed (spec §7, §19).

Code reaches the test split only through `test_split_dir()`, which refuses
unless SHOPROUTE_UNSEAL_TEST is set to a reason (e.g. "final-eval M6"). Training
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
_TEST = DATA / "test"  # M2, sealed
RUNS = ROOT / "runs"  # eval outputs, committed (M3+)

UNSEAL_ENV = "SHOPROUTE_UNSEAL_TEST"


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
