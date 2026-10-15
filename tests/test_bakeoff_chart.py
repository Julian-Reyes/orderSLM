"""The committed case-study data is reproducible from the saved run outputs."""

import json

from orderslm.eval.bakeoff_chart import OUT_JSON, build


def test_chart_data_matches_saved_outputs():
    assert json.loads(OUT_JSON.read_text()) == json.loads(json.dumps(build()))


def test_before_view_reproduces_the_first_reported_scores():
    """'Before' = raw output with scorer@0.1: the numbers first reported for the 12-way bake-off (2026-10-15)."""
    data = json.loads(OUT_JSON.read_text())
    by_id = {v["id"]: v for v in data["bakeoff"]["variants"]}
    assert round(by_id["openai/gpt-6-luna@low"]["before"]["item_f1"], 3) == 0.983
    assert by_id["openai/gpt-6-luna@low"]["before"]["exact"] == 32
    assert round(by_id["google/gemini-3.1-flash-lite@minimal"]["before"]["item_f1"], 3) == 0.741
    assert by_id["anthropic/claude-haiku-5-5@on-medium"]["before"]["exact"] == 33
