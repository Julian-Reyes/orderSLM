"""M6 training rows: the teacher's kept labels as student targets; only synthetic chats; a fixed validation split."""

import json

import pytest

from orderslm.schema.label import MessageIntent, ModelOrder, StudentOutput, TeacherLabel
from orderslm.schema.routing import RouterLabel
from orderslm.train import data


def test_system_prompt_is_short_and_lists_every_label():
    text = data.system_prompt()
    assert "{" not in text.replace("`{", "")  # placeholder filled
    assert all(f"`{x.value}`" in text for x in RouterLabel)
    assert len(text) < 2000  # vs ~23k characters for the teacher's instructions + schema


def test_target_is_the_last_intent_and_the_teachers_order():
    order = ModelOrder.model_validate(
        {
            "fulfillment": {"method": "unknown", "requested_time": {"state": "not_mentioned"}},
            "address": {"state": "not_mentioned"},
            "payment": {"method": "unknown"},
            "customer_name": {"state": "not_mentioned"},
        }
    )
    label = TeacherLabel(
        intents=[
            MessageIntent(message_index=0, primary=RouterLabel.SMALL_TALK),
            MessageIntent(
                message_index=2, primary=RouterLabel.MENU_QUESTION, secondary=RouterLabel.PLACE_ORDER
            ),
        ],
        order=order,
    )
    out = data.target(label)
    assert (out.intent.primary, out.intent.secondary) == (RouterLabel.MENU_QUESTION, RouterLabel.PLACE_ORDER)
    assert out.order == order
    assert StudentOutput.model_validate_json(out.model_dump_json()) == out


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("student-data")
    return out, data.build(out)


def _rows(path):
    return [json.loads(x) for x in path.read_text().splitlines()]


def test_sets_are_synthetic_labels_minus_exclusions(built):
    out, m = built
    excluded = data._excluded()
    for name, batches in (("single", data.SINGLE_BATCHES), ("mixed", data.MIXED_BATCHES)):
        meta = _rows(out / name / "rows.jsonl")
        ids = {r["id"] for r in meta}
        assert all(i.startswith("syn-") for i in ids) and not ids & excluded
        assert {r["batch"] for r in meta} == set(batches)
        s = m["sets"][name]
        assert s["train"]["rows"] + s["valid"]["rows"] == len(meta)


def test_valid_split_is_disjoint_and_shared(built):
    out, m = built
    single, mixed = set(m["sets"]["single"]["valid_ids"]), set(m["sets"]["mixed"]["valid_ids"])
    assert single <= mixed and len(single) == round(1963 * data.VALID_SHARE) + round(698 * data.VALID_SHARE)
    v01 = json.loads((data.OUT / "student-data@0.1" / "manifest.json").read_text())
    assert set(v01["sets"]["mixed"]["valid_ids"]) <= mixed  # v0.2 keeps every v0.1 validation chat
    train_users = {r["messages"][1]["content"] for r in _rows(out / "mixed" / "train.jsonl")}
    valid_users = {r["messages"][1]["content"] for r in _rows(out / "mixed" / "valid.jsonl")}
    assert not train_users & valid_users


def test_rows_are_chat_messages_with_valid_targets(built):
    out, _ = built
    for r in _rows(out / "mixed" / "valid.jsonl"):
        assert list(r) == ["messages"]
        assert [x["role"] for x in r["messages"]] == ["system", "user", "assistant"]
        StudentOutput.model_validate_json(r["messages"][2]["content"])


@pytest.mark.parametrize("version", sorted(data.VERSIONS))
def test_committed_manifest_matches_a_fresh_build(version, built, tmp_path):
    """Deterministic, and every committed manifest is current (rerun `make student-data` after changing inputs);
    v0.1, which the M6 students were trained on, still rebuilds byte-identical."""
    m = built[1] if version == data.DATA_VERSION else data.build(tmp_path, version)
    committed = json.loads((data.OUT / version / "manifest.json").read_text())
    for name in ("single", "mixed"):
        for part in ("train", "valid"):
            assert committed["sets"][name][part]["sha256"] == m["sets"][name][part]["sha256"]
