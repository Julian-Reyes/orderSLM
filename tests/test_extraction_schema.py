"""The extraction contract: what a model may and may not say."""

import copy
import re

import pytest
from pydantic import ValidationError

from shoproute.schema import ExtractionOutput
from shoproute.schema.common import Strict


def mutate(raw: dict, fn) -> dict:
    d = copy.deepcopy(raw)
    fn(d)
    return d


def test_gold_sample_validates(raw_extraction):
    out = ExtractionOutput.model_validate(raw_extraction)
    assert [i.line_id for i in out.items] == ["L1", "L2", "L3"]


def test_round_trips_through_json(raw_extraction):
    out = ExtractionOutput.model_validate(raw_extraction)
    assert ExtractionOutput.model_validate_json(out.model_dump_json()) == out


# ---- prices are never produced by a model


PRICE_WORDS = re.compile(r"price|total|subtotal|fee|amount|cost", re.I)


def _all_property_names(schema: dict) -> set[str]:
    names: set[str] = set()
    for sub in [schema, *schema.get("$defs", {}).values()]:
        names |= set(sub.get("properties", {}))
    return names


def test_extraction_schema_has_no_price_fields():
    names = _all_property_names(ExtractionOutput.model_json_schema())
    assert names, "schema should have properties"
    assert not [n for n in names if PRICE_WORDS.search(n)]


@pytest.mark.parametrize("field", ["total_cents", "price", "subtotal"])
def test_model_inventing_a_price_field_is_rejected(raw_extraction, field):
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ExtractionOutput.model_validate(mutate(raw_extraction, lambda d: d.__setitem__(field, 2000)))


def test_item_price_field_is_rejected(raw_extraction):
    with pytest.raises(ValidationError, match="Extra inputs"):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d["items"][0].__setitem__("unit_price", 899))
        )


def test_every_contract_forbids_unknown_fields():
    def subclasses(cls):
        for c in cls.__subclasses__():
            yield c
            yield from subclasses(c)

    for cls in subclasses(Strict):
        assert cls.model_config.get("extra") == "forbid", cls.__name__


# ---- items


def test_item_needs_exactly_one_identity(raw_extraction):
    both = mutate(raw_extraction, lambda d: d["items"][0].__setitem__("unmatched_text", "cheeseburgers"))
    with pytest.raises(ValidationError, match="exactly one of"):
        ExtractionOutput.model_validate(both)
    neither = mutate(raw_extraction, lambda d: d["items"][0].pop("menu_item_id"))
    with pytest.raises(ValidationError, match="exactly one of"):
        ExtractionOutput.model_validate(neither)


def test_off_menu_item_must_be_flagged_for_clarification(raw_extraction):
    def off_menu(d):
        d["items"][0].pop("menu_item_id")
        d["items"][0]["unmatched_text"] = "chicken sandwich"

    with pytest.raises(ValidationError, match="off-menu item must be listed"):
        ExtractionOutput.model_validate(mutate(raw_extraction, off_menu))


@pytest.mark.parametrize("qty", [0, -1, 100])
def test_quantity_bounds(raw_extraction, qty):
    with pytest.raises(ValidationError):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d["items"][0].__setitem__("quantity", qty))
        )


def test_unclear_quantity_is_null_not_guessed(raw_extraction):
    def unclear(d):
        d["items"][0]["quantity"] = None
        d["missing_or_ambiguous"] = [{"field": "item_quantity", "reason": "ambiguous", "line_id": "L1"}]
        d["clarification_question"] = "How many cheeseburgers?"

    assert ExtractionOutput.model_validate(mutate(raw_extraction, unclear)).items[0].quantity is None


def test_items_need_evidence(raw_extraction):
    with pytest.raises(ValidationError):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d["items"][0].__setitem__("evidence", []))
        )


def test_duplicate_line_ids_rejected(raw_extraction):
    with pytest.raises(ValidationError, match="duplicate line_id"):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d["items"][1].__setitem__("line_id", "L1"))
        )


def test_half_and_half_needs_two_halves(raw_extraction):
    def one_half(d):
        d["items"][0].pop("menu_item_id")
        d["items"][0]["halves"] = [{"menu_item_id": "pepperoni"}]

    with pytest.raises(ValidationError):
        ExtractionOutput.model_validate(mutate(raw_extraction, one_half))


# ---- unknown vs absent vs not applicable


def test_provided_slot_needs_value_and_evidence(raw_extraction):
    with pytest.raises(ValidationError, match="needs a value"):
        ExtractionOutput.model_validate(
            mutate(
                raw_extraction,
                lambda d: d.__setitem__("customer_name", {"state": "provided", "evidence": []}),
            )
        )
    with pytest.raises(ValidationError, match="needs evidence"):
        ExtractionOutput.model_validate(
            mutate(
                raw_extraction, lambda d: d.__setitem__("customer_name", {"state": "provided", "value": "Al"})
            )
        )


def test_not_mentioned_slot_cannot_carry_a_value(raw_extraction):
    with pytest.raises(ValidationError, match="only state 'provided'"):
        ExtractionOutput.model_validate(
            mutate(
                raw_extraction,
                lambda d: d.__setitem__("customer_name", {"state": "not_mentioned", "value": "Al"}),
            )
        )


def test_ambiguous_time_keeps_raw_text_but_no_normalized_value(raw_extraction):
    amb = {
        "state": "ambiguous",
        "raw_text": "around 7 or 8",
        "evidence": [{"message_index": 3, "quote": "pickup at 7"}],
    }

    def set_amb(d, extra=None):
        d["fulfillment"]["requested_time"] = {**amb, **(extra or {})}
        d["missing_or_ambiguous"] = [{"field": "requested_time", "reason": "ambiguous"}]
        d["clarification_question"] = "What time would you like to pick up?"

    ExtractionOutput.model_validate(mutate(raw_extraction, set_amb))
    with pytest.raises(ValidationError, match="normalized_local only when provided"):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: set_amb(d, {"normalized_local": "19:00"}))
        )


def test_pickup_means_address_not_applicable(raw_extraction):
    with pytest.raises(ValidationError, match="not_applicable for pickup"):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d.__setitem__("address", {"state": "not_mentioned"}))
        )


def test_delivery_address_cannot_be_not_applicable(raw_extraction):
    def to_delivery(d):
        d["fulfillment"]["method"] = "delivery"

    with pytest.raises(ValidationError, match="only not_applicable for pickup"):
        ExtractionOutput.model_validate(mutate(raw_extraction, to_delivery))


@pytest.mark.parametrize("bad", ["7pm", "19:60", "24:00", "7:00"])
def test_normalized_time_is_strict_hhmm(raw_extraction, bad):
    with pytest.raises(ValidationError):
        ExtractionOutput.model_validate(
            mutate(
                raw_extraction,
                lambda d: d["fulfillment"]["requested_time"].__setitem__("normalized_local", bad),
            )
        )


# ---- payment claims and decisions


def test_payment_claim_is_a_claim_with_evidence(raw_extraction):
    out = ExtractionOutput.model_validate(
        mutate(raw_extraction, lambda d: d["payment"].__setitem__("customer_claims_paid", True))
    )
    assert out.payment.customer_claims_paid
    # A model can only record the claim: confirming payment is a field on the verified OrderRecord.
    assert "payment_confirmed" not in type(out.payment).model_fields


def test_change_only_for_cash(raw_extraction):
    def card_with_change(d):
        d["payment"]["method"] = "card"
        d["payment"]["change_for_cents"] = 5000

    with pytest.raises(ValidationError, match="change_for_cents only for cash"):
        ExtractionOutput.model_validate(mutate(raw_extraction, card_with_change))


def test_change_for_must_be_integer_cents(raw_extraction):
    with pytest.raises(ValidationError):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d["payment"].__setitem__("change_for_cents", 50.0))
        )


def test_cancelled_order_has_nothing_to_clarify(raw_extraction):
    def cancel_with_question(d):
        d["customer_decision"] = {"state": "cancelled", "evidence": [{"message_index": 3, "quote": "pickup"}]}
        d["missing_or_ambiguous"] = [{"field": "customer_name", "reason": "missing"}]
        d["clarification_question"] = "Name?"

    with pytest.raises(ValidationError, match="nothing left to clarify"):
        ExtractionOutput.model_validate(mutate(raw_extraction, cancel_with_question))


# ---- clarification


def test_question_required_exactly_when_something_is_missing(raw_extraction):
    with pytest.raises(ValidationError, match="clarification_question is required"):
        ExtractionOutput.model_validate(
            mutate(raw_extraction, lambda d: d.__setitem__("clarification_question", "Anything else?"))
        )
    with pytest.raises(ValidationError, match="clarification_question is required"):
        ExtractionOutput.model_validate(
            mutate(
                raw_extraction,
                lambda d: d.__setitem__(
                    "missing_or_ambiguous", [{"field": "customer_name", "reason": "missing"}]
                ),
            )
        )


def test_item_level_missing_info_needs_existing_line(raw_extraction):
    def bad_ref(d):
        d["missing_or_ambiguous"] = [{"field": "item_variant", "reason": "missing", "line_id": "L9"}]
        d["clarification_question"] = "Which size?"

    with pytest.raises(ValidationError, match="unknown line L9"):
        ExtractionOutput.model_validate(mutate(raw_extraction, bad_ref))

    def no_line(d):
        d["missing_or_ambiguous"] = [{"field": "item_variant", "reason": "missing"}]
        d["clarification_question"] = "Which size?"

    with pytest.raises(ValidationError, match="line_id is required"):
        ExtractionOutput.model_validate(mutate(raw_extraction, no_line))


# ---- language neutrality


def test_enum_values_are_language_neutral_codes():
    schema = ExtractionOutput.model_json_schema()
    for name, sub in schema["$defs"].items():
        for value in sub.get("enum", []):
            assert re.fullmatch(r"[a-z][a-z_]*", value), f"{name}: {value!r}"
