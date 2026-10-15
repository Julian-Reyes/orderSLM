"""Scores for extraction outputs against gold (spec §8 step 2, §12).

- JSON validity: the output parsed and validated as ExtractionOutput.
- Item-level F1 (micro, over item lines): a predicted line counts only if menu item (or halves) + quantity +
  size + modifications (+ combo picks) all match a gold line. Line ids and evidence are ignored. Off-menu
  lines match on being off-menu with the same quantity (their wording is free text).
- Order exact match: the item multiset and every order-level field equal (method, time, address state,
  payment, name, decision, the missing set by field + reason). A conversation with no gold order
  (gold_extraction null) is an exact match when the prediction has no items.
- Field accuracy on conversations with a gold order and a valid prediction.
- Correction handling: exact match and item F1 on conversations tagged correction / cancellation.
- Grounding issues (hallucinations): evidence quotes not in the cited message, evidence citing a business
  message, ids not in the menu, items predicted when there is no order; plus unclassified requests.
"""

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from orderslm.checks import check_catalog, check_evidence, check_requests
from orderslm.schema.annotation import AnnotatedConversation, Scenario
from orderslm.schema.conversation import Role
from orderslm.schema.extraction import ExtractionOutput, ItemProposal, Modification
from orderslm.schema.menu import MenuCatalog

CORRECTION_SCENARIOS = {Scenario.correction, Scenario.correction_after_confirmation, Scenario.cancellation}


def _mod_key(m: Modification) -> tuple:
    return (
        m.kind.value,
        m.modifier_id,
        m.replacement_modifier_id,
        m.amount.value,
        m.not_on_menu,
        m.kitchen_note,
    )


def item_key(item: ItemProposal) -> tuple:
    if item.unmatched_text is not None:
        return ("off_menu", item.quantity)
    if item.halves is not None:
        identity: Any = (
            "halves",
            tuple(
                sorted(
                    (h.menu_item_id, tuple(sorted(_mod_key(m) for m in h.modifications))) for h in item.halves
                )
            ),
        )
    else:
        identity = item.menu_item_id
    return (
        identity,
        item.quantity,
        item.variant_id,
        tuple(sorted(_mod_key(m) for m in item.modifications)),
        tuple(sorted((c.slot_id, c.menu_item_id, c.variant_id) for c in item.combo_selections)),
    )


FIELDS = ("method", "time", "address", "payment", "name", "decision", "missing")


def field_values(o: ExtractionOutput) -> dict[str, Any]:
    t = o.fulfillment.requested_time
    return {
        "method": o.fulfillment.method.value,
        "time": (t.state.value, t.kind.value if t.kind else None, t.normalized_local),
        "address": o.address.state.value,
        "payment": (o.payment.method.value, o.payment.change_for_cents, o.payment.customer_claims_paid),
        "name": (
            o.customer_name.state.value,
            o.customer_name.value.strip().casefold() if o.customer_name.value else None,
        ),
        "decision": (o.customer_decision.state.value, o.customer_decision.agreed_while_incomplete),
        "missing": tuple(
            sorted(Counter((m.field.value, m.reason.value) for m in o.missing_or_ambiguous).items())
        ),
    }


@dataclass
class ConversationScore:
    conversation_id: str
    has_gold_order: bool
    correction: bool
    valid: bool
    tp: int
    fp: int
    fn: int
    exact: bool
    fields: dict[str, bool] = field(default_factory=dict)
    grounding_issues: list[str] = field(default_factory=list)
    unclassified_requests: int = 0


def score_conversation(
    gold: AnnotatedConversation, predicted: ExtractionOutput | None, menu: MenuCatalog
) -> ConversationScore:
    conv = gold.conversation
    gold_items = (
        Counter(item_key(i) for i in gold.gold_extraction.items) if gold.gold_extraction else Counter()
    )
    pred_items = Counter(item_key(i) for i in predicted.items) if predicted else Counter()
    tp = sum((gold_items & pred_items).values())
    score = ConversationScore(
        conversation_id=conv.id,
        has_gold_order=gold.gold_extraction is not None,
        correction=bool(set(gold.scenarios) & CORRECTION_SCENARIOS),
        valid=predicted is not None,
        tp=tp,
        fp=sum(pred_items.values()) - tp,
        fn=sum(gold_items.values()) - tp,
        exact=False,
    )
    if predicted is None:
        return score
    roles = {m.index: m.role for m in conv.messages}
    issues = [i.code for i in check_evidence(predicted, conv) + check_catalog(predicted, menu)]
    issues += [
        "EVIDENCE_BUSINESS_MESSAGE"
        for _, ev in predicted.iter_evidence()
        if roles.get(ev.message_index) is Role.business
    ]
    if gold.gold_extraction is None and predicted.items:
        issues.append("ITEMS_WITHOUT_ORDER")
    score.grounding_issues = issues
    score.unclassified_requests = len(check_requests(predicted))
    if gold.gold_extraction is None:
        score.exact = not predicted.items
        return score
    gold_fields, pred_fields = field_values(gold.gold_extraction), field_values(predicted)
    score.fields = {f: gold_fields[f] == pred_fields[f] for f in FIELDS}
    score.exact = gold_items == pred_items and all(score.fields.values())
    return score


def _f1(tp: int, fp: int, fn: int) -> dict[str, float | None]:
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f1 = 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else None
    return {"precision": p, "recall": r, "f1": f1}


def _rate(n: int, d: int) -> float | None:
    return n / d if d else None


def aggregate(scores: list[ConversationScore]) -> dict[str, Any]:
    n = len(scores)
    valid = [s for s in scores if s.valid]
    with_order = [s for s in valid if s.has_gold_order]
    corrections = [s for s in scores if s.correction]
    tp, fp, fn = (sum(getattr(s, k) for s in scores) for k in ("tp", "fp", "fn"))
    issue_counts = Counter(code for s in valid for code in s.grounding_issues)
    return {
        "conversations": n,
        "json_valid": len(valid),
        "json_validity_rate": _rate(len(valid), n),
        "item": {"tp": tp, "fp": fp, "fn": fn, **_f1(tp, fp, fn)},
        "exact_match_rate": _rate(sum(s.exact for s in scores), n),
        "field_accuracy": {f: _rate(sum(s.fields[f] for s in with_order), len(with_order)) for f in FIELDS},
        "correction": {
            "conversations": len(corrections),
            "exact_match_rate": _rate(sum(s.exact for s in corrections), len(corrections)),
            **_f1(*(sum(getattr(s, k) for s in corrections) for k in ("tp", "fp", "fn"))),
        },
        "grounding": {
            "conversations_with_issues": sum(bool(s.grounding_issues) for s in valid),
            "rate": _rate(sum(bool(s.grounding_issues) for s in valid), len(valid)),
            "issues": dict(sorted(issue_counts.items())),
        },
        "unclassified_requests": sum(s.unclassified_requests for s in valid),
    }
