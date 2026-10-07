"""Docs that restate contracts must match the code, so providers, annotators and readers see the same wording."""

from orderslm.paths import ROOT
from orderslm.schema.routing import LABEL_DESCRIPTIONS, REFERENCE_DESCRIPTIONS, URGENCY_DESCRIPTIONS

TAXONOMY = (ROOT / "docs" / "TAXONOMY.md").read_text()


def test_taxonomy_doc_has_every_label_description_verbatim():
    for label, desc in LABEL_DESCRIPTIONS.items():
        assert f"| `{label.value}` | {desc} |" in TAXONOMY, label


def test_taxonomy_doc_has_urgency_and_reference_descriptions_verbatim():
    for u, desc in URGENCY_DESCRIPTIONS.items():
        assert f"| `{u.value}` | {desc} |" in TAXONOMY, u
    for r, desc in REFERENCE_DESCRIPTIONS.items():
        assert f"`{r.value}` | {desc} |" in TAXONOMY, r


def test_required_docs_exist():
    for name in ["SCHEMA", "TAXONOMY", "ARCHITECTURE", "ANNOTATION_GUIDE", "COSTS", "AGENTDESK_REUSE"]:
        assert (ROOT / "docs" / f"{name}.md").stat().st_size > 500, name
    assert (ROOT / "PROGRESS.md").exists()
