import json
from pathlib import Path

import httpx
import pytest

from orderslm.menus import load_menus
from orderslm.paths import SAMPLES
from orderslm.schema import AnnotatedConversation, MenuCatalog

SAMPLE_FILES = sorted((SAMPLES / "conversations").glob("*.json"))


@pytest.fixture(autouse=True)
def no_real_http(monkeypatch):
    """Tests never call real APIs: any real HTTP request fails the test (mock transports still work)."""

    def refuse(self, request):
        raise AssertionError(f"a test tried to reach the network: {request.method} {request.url}")

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", refuse)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


@pytest.fixture(scope="session")
def menus() -> dict[str, MenuCatalog]:
    """The three business menus (not the held-out one)."""
    return load_menus()


@pytest.fixture(scope="session")
def samples() -> list[AnnotatedConversation]:
    return [AnnotatedConversation.model_validate(load_json(p)) for p in SAMPLE_FILES]


@pytest.fixture
def sample_by_id(samples):
    return {s.conversation.id: s for s in samples}


@pytest.fixture
def raw_extraction() -> dict:
    """sample-001's gold extraction as plain JSON, for tests that break it on purpose."""
    return load_json(SAMPLES / "conversations" / "sample-001.json")["gold_extraction"]
