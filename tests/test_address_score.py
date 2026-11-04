"""scorer@0.4: the address compares the numbers in its text (what the ticket prints), not its wording."""

from orderslm.eval.dataset import load_eval_split
from orderslm.eval.metrics import address_key, score_conversation
from orderslm.menus import load_menu
from orderslm.schema.conversation import Split

DEV = {ac.conversation.id: ac for ac in load_eval_split(Split.dev)}
CORRECTED = "a-dev-023"  # "wait sry its 104 river rd not 140"


def _with_address(gold, raw_text: str):
    return gold.model_copy(update={"address": gold.address.model_copy(update={"raw_text": raw_text})})


def _score(ac, pred):
    return score_conversation(ac, pred, load_menu(ac.conversation.business_id))


def test_the_uncorrected_house_number_is_a_wrong_address():
    ac = DEV[CORRECTED]
    s = _score(ac, _with_address(ac.gold_extraction, "140 river rd"))
    assert not s.fields["address"] and not s.exact and not s.action_exact


def test_wording_around_the_numbers_does_not_count():
    ac = DEV[CORRECTED]
    for raw in ("104 River Road", "104 river rd, the blue house"):
        s = _score(ac, _with_address(ac.gold_extraction, raw))
        assert s.fields["address"] and s.exact, raw


def test_unit_numbers_count_in_any_order():
    gold = DEV[CORRECTED].gold_extraction.address
    key = lambda raw: address_key(gold.model_copy(update={"raw_text": raw}))  # noqa: E731
    assert key("12 water st, room 214") == key("room 214, 12 water st")
    assert key("12 water st, room 214") != key("12 water st, room 241")
