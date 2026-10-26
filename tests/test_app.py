"""Annotation tool API (orderslm.app.main) against temporary dev/test directories."""

import json

import pytest
from fastapi.testclient import TestClient

from orderslm import paths
from orderslm.app.main import create_app
from orderslm.data import splits
from orderslm.domain.clock import fixed_clock
from orderslm.paths import SAMPLES, UNSEAL_ENV
from orderslm.schema.conversation import Split


def sample_json(n: int, split: str, new_id: str | None = None) -> dict:
    data = json.loads((SAMPLES / "conversations" / f"sample-{n:03d}.json").read_text())
    data["conversation"] |= {"split": split, "id": new_id or f"{split}-{n:03d}"}
    return data


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(splits, "DEV", tmp_path / "dev")
    monkeypatch.setattr(paths, "_TEST", tmp_path / "test")
    monkeypatch.delenv(UNSEAL_ENV, raising=False)
    return tmp_path


def client(at: str = "2026-10-20T15:00:00+00:00") -> TestClient:
    return TestClient(create_app(clock=fixed_clock(at)))


def test_meta_hides_test_while_sealed(dirs):
    meta = client().get("/api/meta").json()
    assert meta["splits"] == ["dev", "fresh"]  # fresh (M6) is reviewed like dev; test stays hidden
    assert "PLACE_ORDER" in meta["labels"] and "half_and_half" in meta["scenarios"]


def test_test_split_answers_403_while_sealed(dirs):
    c = client()
    for r in (
        c.get("/api/test/conversations"),
        c.get("/api/test/menus"),
        c.post("/api/test/check", json=sample_json(1, "test")),
        c.put("/api/test/conversations/test-001", json={"annotated": sample_json(1, "test")}),
    ):
        assert r.status_code == 403, r.text


def test_dev_menus_exclude_the_held_out_menu(dirs, monkeypatch):
    assert "lucky-lime" not in client().get("/api/dev/menus").json()
    monkeypatch.setenv(UNSEAL_ENV, "annotate test")
    assert "lucky-lime" in client().get("/api/test/menus").json()


def test_check_reports_findings_and_what_the_core_derives(dirs):
    r = client().post("/api/dev/check", json=sample_json(12, "dev")).json()
    assert r["valid"] and r["findings"] == []
    assert r["derived_missing"] == [] and r["template_question"] is None
    assert r["pricing"]["ok"] is True


def test_check_returns_schema_errors_instead_of_failing(dirs):
    r = client().post("/api/dev/check", json={"conversation": {"id": "x"}}).json()
    assert r["valid"] is False and all(f["code"] == "SCHEMA" for f in r["findings"])


def test_save_list_get_round_trip(dirs):
    c = client()
    assert (
        c.put("/api/dev/conversations/dev-005", json={"annotated": sample_json(5, "dev")}).status_code == 200
    )
    (row,) = c.get("/api/dev/conversations").json()
    assert row["id"] == "dev-005" and row["business_id"] == "halfmoon-pizza"
    assert c.get("/api/dev/conversations/dev-005").json()["conversation"]["id"] == "dev-005"
    assert c.get("/api/dev/stats").json()["stats"]["conversations"] == 1


def test_save_rejects_invalid_gold_and_id_mismatch(dirs):
    c = client()
    wrong_split = c.put("/api/dev/conversations/test-001", json={"annotated": sample_json(1, "test")})
    assert wrong_split.status_code == 400 and "WRONG_SPLIT" in wrong_split.text
    mismatch = c.put("/api/dev/conversations/dev-999", json={"annotated": sample_json(1, "dev")})
    assert mismatch.status_code == 400 and "doesn't match" in mismatch.text


def test_ids_in_urls_are_validated(dirs):
    assert client().get("/api/dev/conversations/..%2Fsecret").status_code in (400, 404)
    assert client().get("/api/dev/conversations/LOCK").status_code == 400


def test_no_relabel_unless_scheduled(dirs, monkeypatch):
    monkeypatch.setenv(UNSEAL_ENV, "annotate test")
    c = client()
    c.put("/api/test/conversations/test-001", json={"annotated": sample_json(1, "test")})
    splits.lock(clock=fixed_clock())
    r = client("2027-01-01T00:00:00+00:00").get("/api/relabel")
    assert r.status_code == 409 and "no blind relabel" in r.text


def test_optional_human_relabel_waits_a_week_and_never_sends_gold(dirs, monkeypatch):
    monkeypatch.setenv(UNSEAL_ENV, "annotate test")
    c = client()
    for n in range(1, 6):
        assert c.put(
            f"/api/test/conversations/test-{n:03d}", json={"annotated": sample_json(n, "test")}
        ).is_success
    splits.lock(clock=fixed_clock("2026-10-20T15:00:00+00:00"), relabel_human=True)
    assert c.get("/api/relabel").status_code == 409  # opens 2026-10-27
    later = client("2026-10-27T09:00:00+00:00")
    listing = later.get("/api/relabel").json()
    assert len(listing["ids"]) == 5 and listing["done"] == []
    blind = later.get(f"/api/relabel/{listing['ids'][0]}").json()
    assert set(blind) == {"conversation"}  # no gold, scenarios or notes
    relabel = sample_json(int(listing["ids"][0][-3:]), "test")
    assert later.put(f"/api/relabel/{listing['ids'][0]}", json={"annotated": relabel}).is_success
    assert later.get("/api/relabel").json()["done"] == [listing["ids"][0]]
    assert splits.verify() == []  # relabels don't touch the locked files


def test_after_lock_edits_need_a_reason(dirs, monkeypatch):
    monkeypatch.setenv(UNSEAL_ENV, "annotate test")
    c = client()
    c.put("/api/test/conversations/test-001", json={"annotated": sample_json(1, "test")})
    splits.lock(clock=fixed_clock())
    edited = sample_json(1, "test") | {"annotation_notes": "clarified"}
    assert c.put("/api/test/conversations/test-001", json={"annotated": edited}).status_code == 400
    ok = c.put(
        "/api/test/conversations/test-001", json={"annotated": edited, "change_reason": "typo in note"}
    )
    assert ok.is_success
    assert splits.load_split(Split.test)[0].annotation_notes == "clarified"


def test_check_returns_the_gold_in_plain_english(dirs):
    r = client().post("/api/dev/check", json=sample_json(5, "dev")).json()
    plain = r["gold_plain"]
    assert plain[0] == "ITEMS"
    assert plain[1].startswith("L1  1 × Pizza, Large 14-inch: half Pepperoni Pizza / half Hawaiian Pizza")
    assert "Note: ring the side door   ← #4 “ring the side door”" in plain
