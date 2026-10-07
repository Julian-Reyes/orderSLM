"""The patch shown to the business: compare the previous order snapshot with the new one.

The extractor outputs full snapshots (decision 2026-10-07); this is where "what
changed this turn" comes from. Lines are matched by line_id. Evidence and
raw_text are ignored: re-quoting the same order is not a change.
"""

from pydantic import Field

from orderslm.schema.common import Strict
from orderslm.schema.extraction import ExtractionOutput, ItemProposal

LINE_FIELDS = ("menu_item_id", "unmatched_text", "halves", "quantity", "variant_id", "modifications",
               "combo_selections", "notes")  # fmt: skip


class LineChange(Strict):
    line_id: str
    fields: list[str] = Field(min_length=1)


class OrderPatch(Strict):
    lines_added: list[str] = Field(default_factory=list)
    lines_removed: list[str] = Field(default_factory=list)
    lines_changed: list[LineChange] = Field(default_factory=list)
    fields_changed: list[str] = Field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.lines_added or self.lines_removed or self.lines_changed or self.fields_changed)

    @property
    def items_changed(self) -> bool:
        return bool(self.lines_added or self.lines_removed or self.lines_changed)


def _line_view(line: ItemProposal) -> dict[str, object]:
    d = line.model_dump(mode="json", include=set(LINE_FIELDS))
    for mods in [d.get("modifications") or []] + [
        h.get("modifications") or [] for h in d.get("halves") or []
    ]:
        for m in mods:
            m.pop("raw_text", None)
    return d


def _order_fields(o: ExtractionOutput) -> dict[str, object]:
    t = o.fulfillment.requested_time
    return {
        "fulfillment.method": o.fulfillment.method.value,
        "fulfillment.requested_time": (t.state.value, t.kind, t.normalized_local, t.raw_text),
        "address": o.address.model_dump(mode="json", exclude={"evidence"}),
        "payment": o.payment.model_dump(mode="json", exclude={"evidence"}),
        "customer_name": (o.customer_name.state.value, o.customer_name.value),
        "customer_decision": o.customer_decision.state.value,
        "notes": sorted(n.text for n in o.notes),
    }


def diff_orders(previous: ExtractionOutput | None, current: ExtractionOutput) -> OrderPatch:
    prev_lines = {line.line_id: line for line in (previous.items if previous else [])}
    cur_lines = {line.line_id: line for line in current.items}
    changed = []
    for lid in cur_lines.keys() & prev_lines.keys():
        before, after = _line_view(prev_lines[lid]), _line_view(cur_lines[lid])
        fields = [f for f in LINE_FIELDS if before.get(f) != after.get(f)]
        if fields:
            changed.append(LineChange(line_id=lid, fields=fields))
    before_fields = _order_fields(previous or ExtractionOutput.empty())
    after_fields = _order_fields(current)
    fields_changed = [k for k in after_fields if before_fields[k] != after_fields[k]]
    order = list(cur_lines)
    return OrderPatch(
        lines_added=[lid for lid in order if lid not in prev_lines],
        lines_removed=[lid for lid in prev_lines if lid not in cur_lines],
        lines_changed=sorted(changed, key=lambda c: order.index(c.line_id)),
        fields_changed=fields_changed,
    )
