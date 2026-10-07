"""The sample conversations validate, are grounded, and cover the scenarios M0 promises."""

import pytest

from shoproute.checks import check_all, check_catalog, check_evidence
from shoproute.schema import Role, Scenario, Split
from shoproute.schema.extraction import ExtractionOutput

from .conftest import MENU_FILES, SAMPLE_FILES


def test_files_exist():
    assert len(SAMPLE_FILES) >= 10
    assert len(MENU_FILES) >= 2


def test_every_sample_is_grounded_in_its_conversation_and_menu(samples, menus):
    for s in samples:
        assert s.conversation.business_id in menus, s.conversation.id
        if s.gold_extraction is not None:
            issues = check_all(s.gold_extraction, s.conversation, menus[s.conversation.business_id])
            assert issues == [], (s.conversation.id, issues)


def test_samples_are_marked_sample_split_and_english(samples):
    for s in samples:
        assert s.conversation.split is Split.sample
        assert s.conversation.language == "en"


def test_sample_ids_unique(samples):
    ids = [s.conversation.id for s in samples]
    assert len(ids) == len(set(ids))


def test_evidence_only_cites_customer_messages(samples):
    """Gold must come from what the customer said, not from the business's summary."""
    for s in samples:
        if s.gold_extraction is None:
            continue
        roles = {m.index: m.role for m in s.conversation.messages}
        for path, ev in s.gold_extraction.iter_evidence():
            assert roles[ev.message_index] is Role.customer, (s.conversation.id, path)


REQUIRED = {
    Scenario.multi_message_order,
    Scenario.correction,
    Scenario.missing_info,
    Scenario.two_requests,
    Scenario.off_menu,
    Scenario.status_question,
    Scenario.order_problem,
    Scenario.correction_after_confirmation,
    Scenario.contextual_yes,
    Scenario.cancellation,
    Scenario.half_and_half,
    Scenario.combo,
}


def test_required_scenarios_are_covered(samples):
    covered = {sc for s in samples for sc in s.scenarios}
    assert REQUIRED <= covered, REQUIRED - covered


def test_two_request_samples_have_a_secondary_label(samples):
    for s in samples:
        if Scenario.two_requests in s.scenarios:
            assert any(r.decision.secondary for r in s.gold_routing), s.conversation.id


def test_samples_without_an_order_route_away_from_the_extractor(samples):
    for s in samples:
        if s.gold_extraction is None:
            assert not any(r.decision.goes_to_extractor for r in s.gold_routing), s.conversation.id


# ---- the grounding checks themselves catch bad annotations


def _gold(sample_by_id, cid) -> tuple:
    s = sample_by_id[cid]
    return s.gold_extraction.model_copy(deep=True), s.conversation


def test_check_catches_a_misquoted_evidence(sample_by_id):
    out, convo = _gold(sample_by_id, "sample-001")
    out.items[0].evidence[0].quote = "3 cheeseburgers"
    assert [i.code for i in check_evidence(out, convo)] == ["EVIDENCE_NOT_FOUND"]


def test_check_catches_evidence_in_the_wrong_message(sample_by_id):
    out, convo = _gold(sample_by_id, "sample-001")
    out.items[0].evidence[0].message_index = 2
    assert [i.code for i in check_evidence(out, convo)] == ["EVIDENCE_NOT_FOUND"]


def test_check_quote_matching_ignores_case_and_spacing(sample_by_id):
    out, convo = _gold(sample_by_id, "sample-001")
    out.items[0].evidence[0].quote = "2   CHEESEBURGERS"
    assert check_evidence(out, convo) == []


@pytest.mark.parametrize(
    ("change", "code"),
    [
        (lambda o: setattr(o.items[0], "menu_item_id", "chicken_sandwich"), "UNKNOWN_ITEM"),
        (lambda o: setattr(o.items[0], "variant_id", "triple"), "UNKNOWN_VARIANT"),
        (lambda o: setattr(o.items[1].modifications[0], "modifier_id", "no_olives"), "UNKNOWN_MODIFIER"),
        (
            lambda o: (
                setattr(o.items[2], "menu_item_id", "lemonade")
                or o.items[2].modifications.append(o.items[1].modifications[0])
            ),
            "MODIFIER_NOT_ALLOWED",
        ),
        (lambda o: setattr(o.items[1].modifications[0], "modifier_id", "extra_cheese"), "MODIFIER_KIND"),
    ],
)
def test_check_catches_catalog_errors(sample_by_id, menus, change, code):
    out, _ = _gold(sample_by_id, "sample-001")
    change(out)
    assert code in [i.code for i in check_catalog(out, menus["corner-patty"])]


def test_check_catches_bad_combo_choice(sample_by_id, menus):
    out, _ = _gold(sample_by_id, "sample-003")
    out.items[0].combo_selections[1].menu_item_id = "milkshake"
    assert [i.code for i in check_catalog(out, menus["corner-patty"])] == ["INVALID_COMBO_CHOICE"]


def test_check_catches_non_splittable_half(sample_by_id, menus):
    out, _ = _gold(sample_by_id, "sample-005")
    out.items[0].halves[1].menu_item_id = "garlic_knots"
    assert "NOT_SPLITTABLE" in [i.code for i in check_catalog(out, menus["halfmoon-pizza"])]


def test_gold_extractions_validate_standalone(samples):
    """What a model would emit: the gold JSON alone must pass the extraction schema."""
    for s in samples:
        if s.gold_extraction is not None:
            ExtractionOutput.model_validate_json(s.gold_extraction.model_dump_json())
