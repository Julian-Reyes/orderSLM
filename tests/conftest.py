import json
from pathlib import Path

import pytest

from shoproute.paths import SAMPLES
from shoproute.schema import AnnotatedConversation, MenuCatalog

SAMPLE_FILES = sorted((SAMPLES / "conversations").glob("*.json"))
MENU_FILES = sorted((SAMPLES / "menus").glob("*.json"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


@pytest.fixture(scope="session")
def menus() -> dict[str, MenuCatalog]:
    out = {}
    for p in MENU_FILES:
        m = MenuCatalog.model_validate(load_json(p))
        out[m.business_id] = m
    return out


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
