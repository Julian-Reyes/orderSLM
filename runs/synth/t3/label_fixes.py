"""Hand fixes of t3 teacher labels (Claude, claude-opus-5-5, Claude Code session, 2026-10-25; Julian's OK).

Each fix starts from the teacher's raw output (label/<teacher>/<card>.json, left untouched), makes the smallest
edit that corrects it, and must pass the same label checks as a teacher label (parse_label). Writes
label_fixes/<card>.json: the fixed label, the reason, who fixed it. Re-run: `uv run python runs/synth/t3/label_fixes.py`.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

from orderslm.llm.types import ChatResponse
from orderslm.menus import load_menu
from orderslm.synth import label as lab
from orderslm.synth import run

BATCH = "t3"
FIXED_BY = "claude-opus-5-5 (Claude Code session, by hand)"


def _line(order, line_id):
    return next(i for i in order["items"] if i["line_id"] == line_id)


def _drop_offmenu(order, line_id, raw_text):
    """The business declined an off-menu add-on and the customer went on without it: it isn't in the order."""
    line = _line(order, line_id)
    line["modifications"] = [m for m in line["modifications"] if m["raw_text"] != raw_text]
    line["evidence"] = [e for e in line["evidence"] if raw_text.split()[-1] not in e["quote"]]


def _ambiguous_time(order):
    t = order["fulfillment"]["requested_time"]
    t["kind"] = None  # only `provided` carries a kind (schema); raw_text and evidence stay


def _intent(label, index, primary):
    next(i for i in label["intents"] if i["message_index"] == index)["primary"] = primary


def f0009(lb, o):
    o["items"] = [i for i in o["items"] if i["line_id"] != "L1"]
    _intent(lb, 1, "SMALL_TALK")  # "need coffee asap" announces an order (v0.5: SMALL_TALK)


def f0092(lb, o):
    _ambiguous_time(o)


def f0098(lb, o):
    _ambiguous_time(o)
    _drop_offmenu(o, "L1", "matcha powder")


def f0114(lb, o):
    o["customer_name"]["evidence"] = [{"message_index": 0, "quote": "It's Omar"}]


def f0154(lb, o):
    _ambiguous_time(o)
    a, b = _line(o, "L1"), _line(o, "L2")
    a["variant_id"] = b["variant_id"] = "sesame"
    a["evidence"] = [{"message_index": 2, "quote": "three sesame bagels, two plain"}]
    b["evidence"] = [
        {"message_index": 2, "quote": "three sesame bagels"},
        {"message_index": 2, "quote": "one with avocado"},
    ]


def f0166(lb, o):
    _line(o, "L1")["evidence"][1] = {"message_index": 0, "quote": "MAKE IT TWO"}


def f0169(lb, o):
    _line(o, "L3")["quantity"] = 3
    _line(o, "L4")["quantity"] = 2


def f0343(lb, o):
    o["items"] = [i for i in o["items"] if i["line_id"] != "L3"]


def _no_cheese_removal(o):
    """'no cheese' on a veggie burger: cheese isn't included, so there is nothing to remove."""
    line = _line(o, "L1")
    line["modifications"] = [m for m in line["modifications"] if m["modifier_id"] != "cheese"]
    line["evidence"] = [e for e in line["evidence"] if e["quote"] not in ("leave it off", "no cheese")]


def f0368(lb, o):
    _no_cheese_removal(o)


def f0426(lb, o):
    _line(o, "L2")["evidence"][1]["quote"] = "JUST 1 OF THOSE GETS THE THIN CRUST"


def f0428(lb, o):
    _no_cheese_removal(o)


def f0541(lb, o):
    for n, line in enumerate(o["items"], start=1):
        line["line_id"] = f"L{n}"


def f0552(lb, o):
    line = _line(o, "L2")
    line["modifications"] = []  # "one plain" next to "five with american cheese": the one without cheese


FIXES = {
    "syn-t3-0009": (
        f0009,
        "teacher added a drip coffee never ordered (from 'need coffee asap'): removed; that message is an announcement (SMALL_TALK)",
    ),
    "syn-t3-0060": (
        lambda lb, o: _drop_offmenu(o, "L3", "capers"),
        "off-menu capers declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0062": (
        lambda lb, o: _drop_offmenu(o, "L4", "arugula"),
        "off-menu arugula declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0092": (
        f0092,
        "label dropped (contract): an ambiguous time can't carry a kind; 'at 6:30' at a café open 7-15 stays ambiguous",
    ),
    "syn-t3-0098": (
        f0098,
        "label dropped (contract): ambiguous 'at 6:30' without a kind; off-menu matcha powder declined by the business: removed",
    ),
    "syn-t3-0114": (
        f0114,
        "label dropped (check): name evidence quoted 'I'm Omar', the chat says 'It's Omar'",
    ),
    "syn-t3-0154": (
        f0154,
        "label dropped (contract): ambiguous time without a kind ('around nine thirty' after 9:30); 'three sesame bagels, two plain' are sesame bagels, not the plain flavor",
    ),
    "syn-t3-0166": (
        f0166,
        "label dropped (check): 'TWO' quoted from message 2, it is in message 0 ('MAKE IT TWO')",
    ),
    "syn-t3-0169": (f0169, "teacher dropped the stated quantities: 3 garlic knots, 2 breadsticks"),
    "syn-t3-0317": (
        lambda lb, o: _drop_offmenu(o, "L2", "truffle oil"),
        "off-menu truffle oil declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0323": (
        lambda lb, o: _drop_offmenu(o, "L1", "cinnamon on top"),
        "off-menu cinnamon declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0343": (f0343, "teacher kept the 2 lattes the customer removed in the last message: removed"),
    "syn-t3-0368": (
        f0368,
        "label dropped (check): removed cheese the veggie burger doesn't come with ('leave it off' = don't add it)",
    ),
    "syn-t3-0426": (
        f0426,
        "label dropped (check): quote '1 OF THEM GETS THE THIN CRUST', the chat says '1 OF THOSE'",
    ),
    "syn-t3-0428": (
        f0428,
        "label dropped (check): removed cheese the veggie burger doesn't come with ('no cheese then' = don't add it)",
    ),
    "syn-t3-0495": (
        lambda lb, o: _drop_offmenu(o, "L1", "grilled mushrooms"),
        "off-menu grilled mushrooms declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0534": (
        lambda lb, o: _drop_offmenu(o, "L2", "grilled mushrooms"),
        "off-menu grilled mushrooms declined by the business and accepted by the customer: removed",
    ),
    "syn-t3-0541": (f0541, "label dropped (contract): two lines both L1; renumbered L1-L4"),
    "syn-t3-0552": (
        f0552,
        "teacher read 'one plain' veggie burger as removing every topping; it is the one without the added cheese",
    ),
}


def main() -> None:
    out = run.batch_dir(BATCH) / "label_fixes"
    out.mkdir(exist_ok=True)
    conv = {c.card_id: c.conversation for c in run.load_conversations(BATCH)}
    for cid, (fix, reason) in FIXES.items():
        rec = json.loads(
            (run.batch_dir(BATCH) / "label" / run._slug(lab.TEACHER) / f"{cid}.json").read_text()
        )
        label = json.loads(ChatResponse.model_validate(rec["response"]).text)
        fix(label, label["order"])
        lc, why = lab.parse_label(json.dumps(label), conv[cid], load_menu(conv[cid].business_id), lab.TEACHER)
        if lc is None:
            raise SystemExit(f"{cid}: fix fails the label checks: {why}")
        record = {
            "card_id": cid,
            "reason": reason,
            "fixed_by": FIXED_BY,
            "fixed_at": datetime.now(UTC).isoformat(),
            "label": label,
        }
        (out / f"{cid}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(FIXES)} fixes written to {out.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
