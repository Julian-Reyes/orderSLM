"""Website case-study data: every number comes from the saved runs it names (no network)."""

import json

import pytest

from orderslm.eval import site_data
from orderslm.paths import ROOT


@pytest.fixture(scope="module")
def data():
    if not (site_data.DEPLOY / "summary.json").exists():
        pytest.skip("deploy run not present")
    return site_data.build()


def test_student_rows_are_the_runs_metrics(data):
    for row in data["students"]:
        for split in ("dev", "fresh"):
            m = json.loads((ROOT / row[split]["run"] / "metrics.json").read_text())
            assert row[split]["exact"] == m["order"]["exact_match"]
            assert row[split]["intents_right"] == m["intent"]["all"]["primary_correct"]
            assert row[split]["finalize"] == "finalize@0.2"  # all re-scored with the current rules


def test_packaging_and_example(data):
    rows = {r["format"]: r for r in data["packaging"]["rows"]}
    assert data["packaging"]["picked"] == "Q8_0"
    for split in ("dev", "fresh"):  # what the page claims: Q8_0 = the fp16 model's accuracy
        assert rows["Q8_0"][split]["exact"] == rows["fp16 (transformers)"][split]["exact"]
    ex = data["example"]
    assert ex["exact_match_with_gold"] is True
    assert ex["priced_by_code"]["total_cents"] == sum(x["total_cents"] for x in ex["priced_by_code"]["lines"])


def test_written_file_is_current(data):
    """docs/site/case-study.json (copied to the website) must match the runs: rerun `make site-data` after a change."""
    assert json.loads(site_data.OUT.read_text()) == json.loads(json.dumps(data))
