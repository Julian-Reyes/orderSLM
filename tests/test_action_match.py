"""scorer@0.3 same-action match: the bot sends and asks the same, wording-level differences aside."""

from orderslm.eval.dataset import load_eval_split
from orderslm.eval.metrics import score_conversation
from orderslm.menus import load_menu
from orderslm.schema.conversation import Split
from orderslm.schema.extraction import FieldRef, MissingInfo, MissingReason

DEV = {ac.conversation.id: ac for ac in load_eval_split(Split.dev) if ac.gold_extraction is not None}
OFF_MENU_MOD = "a-dev-034"  # "with artichoke hearts": a not_on_menu add + item_modification/off_menu


def _score(ac, pred):
    return score_conversation(ac, pred, load_menu(ac.conversation.business_id))


def _with_unverified_mod(gold):
    """The 2B students' a-fresh-080 shape: the off-menu add left unclassified, flagged ambiguous."""
    items = [
        i.model_copy(
            update={
                "modifications": [
                    m.model_copy(update={"not_on_menu": False, "raw_text": m.raw_text + " instead"})
                    if m.not_on_menu
                    else m
                    for m in i.modifications
                ]
            }
        )
        for i in gold.items
    ]
    missing = [
        m.model_copy(update={"reason": MissingReason.ambiguous}) if m.reason is MissingReason.off_menu else m
        for m in gold.missing_or_ambiguous
    ]
    return gold.model_copy(update={"items": items, "missing_or_ambiguous": missing})


def test_gold_against_itself_matches_both_ways():
    for ac in DEV.values():
        s = _score(ac, ac.gold_extraction)
        assert s.exact and s.action_exact, ac.conversation.id


def test_off_menu_vs_unverified_request_is_the_same_action():
    ac = DEV[OFF_MENU_MOD]
    s = _score(ac, _with_unverified_mod(ac.gold_extraction))
    assert not s.exact and s.action_exact


def test_dropping_the_question_is_not_the_same_action():
    ac = DEV[OFF_MENU_MOD]
    pred = _with_unverified_mod(ac.gold_extraction)
    pred = pred.model_copy(
        update={
            "missing_or_ambiguous": [
                m for m in pred.missing_or_ambiguous if m.field is not FieldRef.item_modification
            ]
        }
    )
    assert not _score(ac, pred).action_exact


def test_a_different_kitchen_line_is_not_the_same_action():
    ac = DEV[OFF_MENU_MOD]
    gold = ac.gold_extraction
    first = gold.items[0]
    pred = gold.model_copy(
        update={"items": [first.model_copy(update={"quantity": (first.quantity or 1) + 1})]}
    )
    s = _score(ac, pred.model_copy(update={"items": pred.items + gold.items[1:]}))
    assert not s.exact and not s.action_exact


def test_only_an_unclear_line_equals_no_items_yet():
    """a-fresh-087's shape: gold keeps "the usual" unmatched; the student says no items yet. Both ask."""
    ac = DEV[OFF_MENU_MOD]
    gold = ac.gold_extraction
    others = [m for m in gold.missing_or_ambiguous if m.line_id is None]
    usual = gold.items[0].model_copy(
        update={
            "menu_item_id": None,
            "unmatched_text": "the usual",
            "variant_id": None,
            "modifications": [],
            "combo_selections": [],
        }
    )
    unclear = gold.model_copy(
        update={
            "items": [usual],
            "missing_or_ambiguous": [
                MissingInfo(
                    field=FieldRef.item_menu_match, reason=MissingReason.ambiguous, line_id=usual.line_id
                ),
                *others,
            ],
        }
    )
    nothing = gold.model_copy(
        update={
            "items": [],
            "missing_or_ambiguous": [
                MissingInfo(field=FieldRef.items, reason=MissingReason.missing),
                *others,
            ],
        }
    )
    s = _score(ac.model_copy(update={"gold_extraction": unclear}), nothing)
    assert not s.exact and s.action_exact
    # with a real line next to the unclear one, dropping the unclear one loses a question
    real = gold.items[0]
    both = unclear.model_copy(update={"items": [real, usual.model_copy(update={"line_id": "L9"})]})
    both = both.model_copy(
        update={
            "missing_or_ambiguous": [
                MissingInfo(field=FieldRef.item_menu_match, reason=MissingReason.ambiguous, line_id="L9"),
                *[m for m in gold.missing_or_ambiguous if m.line_id == real.line_id],
                *others,
            ]
        }
    )
    only_real = gold.model_copy(
        update={
            "items": [real],
            "missing_or_ambiguous": [
                m for m in gold.missing_or_ambiguous if m.line_id in (None, real.line_id)
            ],
        }
    )
    assert not _score(ac.model_copy(update={"gold_extraction": both}), only_real).action_exact
