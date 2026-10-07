"""Mocks satisfy the interfaces, model output goes through one parse path, the test split stays sealed."""

import pytest

from orderslm.domain.clock import fixed_clock
from orderslm.interfaces.decision import DecisionProvider
from orderslm.interfaces.extractor import ExtractionRequest, OrderExtractor
from orderslm.interfaces.tools import BusinessTools
from orderslm.mocks.decision import ScriptedDecisionProvider, router_answers
from orderslm.mocks.extractor import ScriptedExtractor
from orderslm.mocks.tools import InMemoryBusinessTools
from orderslm.paths import UNSEAL_ENV, SealedSplitError, test_split_dir


def test_mocks_implement_the_protocols():
    assert isinstance(ScriptedDecisionProvider(), DecisionProvider)
    assert isinstance(ScriptedExtractor({}), OrderExtractor)
    assert isinstance(InMemoryBusinessTools(fixed_clock()), BusinessTools)


@pytest.fixture
def request_for(menus, sample_by_id):
    def make(cid: str) -> ExtractionRequest:
        s = sample_by_id[cid]
        return ExtractionRequest(
            menu=menus[s.conversation.business_id], conversation=s.conversation, prompt_version="test"
        )

    return make


def test_extractor_returns_validated_output(sample_by_id, request_for):
    gold = sample_by_id["sample-002"].gold_extraction
    ext = ScriptedExtractor({"sample-002": gold})
    res = ext.extract(request_for("sample-002"))
    assert res.output == gold and res.error is None
    assert ext.requests[0].conversation.id == "sample-002"


@pytest.mark.parametrize(
    "raw",
    [
        "Sure! Here is your order: 2 cheeseburgers",  # prose, not JSON
        '{"items": []}',  # JSON, but missing required fields
        '{"items": [], "total_cents": 100}',  # invents a price
    ],
)
def test_invalid_model_output_is_kept_not_raised(raw, request_for):
    res = ScriptedExtractor({"sample-001": raw}).extract(request_for("sample-001"))
    assert res.output is None and res.error and res.raw_text == raw


def test_scripted_provider_records_and_exhausts():
    p = ScriptedDecisionProvider([router_answers("SMALL_TALK"), RuntimeError("provider down")])
    from orderslm.interfaces.decision import DecisionRequest

    req = DecisionRequest(
        request_id="r1",
        input="hi",
        prompt_version="p",
        questions=[{"name": "q", "type": "boolean", "prompt": "?"}],
    )
    assert p.decide(req).answers["primary"].choice == "SMALL_TALK"
    with pytest.raises(RuntimeError, match="provider down"):
        p.decide(req)
    with pytest.raises(RuntimeError, match="exhausted"):
        p.decide(req)
    assert len(p.requests) == 3


def test_test_split_is_sealed_by_default(monkeypatch):
    monkeypatch.delenv(UNSEAL_ENV, raising=False)
    with pytest.raises(SealedSplitError):
        test_split_dir()
    monkeypatch.setenv(UNSEAL_ENV, "   ")
    with pytest.raises(SealedSplitError):
        test_split_dir()
    monkeypatch.setenv(UNSEAL_ENV, "final-eval test")
    assert test_split_dir().name == "test"


def test_name_required_for_pickup_is_an_optional_menu_setting(menus):
    required = [b for b, m in menus.items() if m.name_required_for_pickup]
    assert required == ["morning-crumb"]  # exactly one business, so missing-name clarifications get tested
    data = menus["corner-patty"].model_dump(mode="json") | {"name_required_for_pickup": True}
    assert type(menus["corner-patty"]).model_validate(data).name_required_for_pickup


def test_no_third_party_dataset_is_tracked_by_git():
    """PIZZA is CC-BY-NC-4.0 (no redistribution): only scripts may be committed, never data/external/."""
    import subprocess

    from orderslm.paths import ROOT

    tracked = subprocess.run(
        ["git", "ls-files", "data/external"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert tracked == ""
    assert "data/external/" in (ROOT / ".gitignore").read_text()


def test_secrets_and_local_files_are_ignored_but_env_example_is_tracked():
    import subprocess

    from orderslm.paths import ROOT

    def ignored(path: str) -> bool:
        return subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT).returncode == 0

    for path in (".env", ".env.local", ".env.production", ".venv/bin/python", "data/external/pizza/x.json"):
        assert ignored(path), path
    assert not ignored(".env.example")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert ".env.example" in tracked.split()
    assert not [f for f in tracked.split() if f.startswith(".env") and f != ".env.example"]
