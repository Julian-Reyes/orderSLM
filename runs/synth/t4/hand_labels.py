"""Hand labels for t4 (Claude, claude-opus-5-5, Claude Code session, 2026-10-25; Julian: "you label the rest").

28 chats whose teacher call failed (OpenAI credit used up: `credit_balance_exhausted`) get a whole label written by
hand under the teacher's rules (teacher-label@0.7, followed as written; conventions checked against the teacher's
own labels: "around 9pm" = provided clock time, a payment change after a yes = MODIFY_ORDER + pending, landmarks in
`reference`). Four teacher labels are fixed like t3's: syn-t4-0084 (dropped: an ambiguous time with a kind) and the three the\ncard check flagged (0005, 0020, 0031).
Every label must pass the same checks as the teacher's (parse_label). Writes label_fixes/<card>.json.
Re-run: `uv run python runs/synth/t4/hand_labels.py`.
"""

import json
from datetime import UTC, datetime

from orderslm.llm.types import ChatResponse
from orderslm.menus import load_menu
from orderslm.synth import label as lab
from orderslm.synth import run

BATCH = "t4"
FIXED_BY = "claude-opus-5-5 (Claude Code session, by hand)"


def ev(i, q):
    return [{"message_index": i, "quote": q}]


def mod(kind, mid, raw, repl=None, off=False):
    return {
        "kind": kind,
        "modifier_id": None if off else mid,
        "replacement_modifier_id": repl,
        "amount": "normal",
        "raw_text": raw,
        "not_on_menu": off,
        "kitchen_note": False,
    }


def offmenu(raw):
    return mod("add", None, raw, off=True)


def item(n, mid, qty, var, evidence, mods=()):
    return {
        "line_id": f"L{n}",
        "menu_item_id": mid,
        "unmatched_text": None,
        "halves": None,
        "quantity": qty,
        "variant_id": var,
        "unmatched_variant_text": None,
        "modifications": list(mods),
        "combo_selections": [],
        "notes": None,
        "evidence": evidence,
    }


def time(kind=None, raw=None, at=None, evidence=()):
    if raw is None:
        return {
            "state": "not_mentioned",
            "kind": None,
            "raw_text": None,
            "normalized_local": None,
            "evidence": [],
        }
    return {
        "state": "provided",
        "kind": kind,
        "raw_text": raw,
        "normalized_local": at,
        "evidence": list(evidence),
    }


def address(number=None, street=None, unit=None, reference=None, raw=None, evidence=(), pickup=False):
    if pickup:
        state = "not_applicable"
    else:
        state = "provided" if raw else "not_mentioned"
    return {
        "state": state,
        "street": street,
        "number": number,
        "unit": unit,
        "reference": reference,
        "raw_text": raw,
        "evidence": list(evidence),
    }


def order(
    items=(),
    method="unknown",
    method_ev=(),
    when=None,
    addr=None,
    pay="unknown",
    pay_ev=(),
    change=None,
    name=None,
    name_ev=(),
    decision="pending",
    decision_ev=(),
):
    return {
        "items": list(items),
        "fulfillment": {
            "method": method,
            "method_evidence": list(method_ev),
            "requested_time": when or time(),
        },
        "address": addr or address(pickup=method == "pickup"),
        "payment": {
            "method": pay,
            "change_for_cents": change,
            "customer_claims_paid": False,
            "evidence": list(pay_ev),
        },
        "customer_name": {
            "state": "provided" if name else "not_mentioned",
            "value": name,
            "evidence": list(name_ev),
        },
        "customer_decision": {
            "state": decision,
            "agreed_while_incomplete": False,
            "evidence": list(decision_ev),
        },
        "notes": [],
        "ambiguity_flags": [],
    }


def intents(*pairs):
    return [
        {"message_index": i, "primary": p, "secondary": s}
        for i, p, s in (x if len(x) == 3 else (*x, None) for x in pairs)
    ]


S, P, M, C, Q, U, OOS = (
    "SMALL_TALK",
    "PLACE_ORDER",
    "MODIFY_ORDER",
    "CONFIRM_ORDER",
    "MENU_QUESTION",
    "UNKNOWN",
    "OUT_OF_SCOPE",
)

LABELS = {
    "syn-t4-0085": (
        intents((0, P), (2, P), (3, P)),
        order(
            [
                item(
                    1,
                    "bagel",
                    3,
                    "plain",
                    ev(0, "3 plain bagels") + ev(3, "matcha powder on the bagels"),
                    [offmenu("matcha powder")],
                )
            ],
            "pickup",
            ev(2, "pick them up"),
            time("relative", "in 20 min", None, ev(2, "in 20 min")),
            pay="card",
            pay_ev=ev(2, "card"),
            name="Nico",
            name_ev=ev(2, "Nico"),
        ),
    ),
    "syn-t4-0086": (
        intents((0, P), (2, P), (3, P)),
        order(
            [
                item(
                    1,
                    "bagel",
                    4,
                    "sesame",
                    ev(0, "four sesame bagels") + ev(3, "cinnamon on the bagels"),
                    [offmenu("cinnamon")],
                ),
                item(2, "muffin", 1, "banana_nut", ev(0, "a banana nut muffin")),
            ],
            "pickup",
            ev(2, "pick them up"),
            pay="cash",
            pay_ev=ev(2, "pay cash"),
            name="Luis",
            name_ev=ev(2, "Luis"),
        ),
    ),
    "syn-t4-0089": (intents((0, U)), order()),
    "syn-t4-0090": (
        intents((0, P), (2, P)),
        order(
            [
                item(
                    1,
                    "hot_chocolate",
                    1,
                    "medium",
                    ev(0, "a medium hot chocolate") + ev(2, "cinnamon on the hot chocolate"),
                    [
                        mod("add", "hazelnut_syrup", "hazelnut syrup"),
                        mod("substitute", "whole_milk", "skim milk instead of whole", repl="skim_milk"),
                        offmenu("cinnamon"),
                    ],
                ),
                item(2, "cappuccino", 3, "medium", ev(0, "three medium cappuccinos")),
            ],
            "pickup",
            ev(0, "pick them up"),
            pay="card",
            pay_ev=ev(0, "pay by card"),
            name="Sam",
            name_ev=ev(0, "Sam"),
        ),
    ),
    "syn-t4-0092": (
        intents((0, S), (2, P), (3, P), (4, P), (5, P)),
        order(
            [
                item(
                    1,
                    "veggie_burger",
                    1,
                    None,
                    ev(2, "veggie burger") + ev(5, "chili on the veggie burger"),
                    [offmenu("chili")],
                ),
                item(2, "onion_rings", 1, None, ev(3, "onion rings")),
            ],
            "pickup",
            ev(4, "pick it up"),
        ),
    ),
    "syn-t4-0093": (
        intents((0, S), (2, P), (3, P)),
        order(
            [
                item(
                    1,
                    "hawaiian_pizza",
                    1,
                    "small",
                    ev(2, "A small Hawaiian") + ev(3, "add arugula to the Hawaiian"),
                    [mod("remove", "ham", "no ham"), offmenu("arugula")],
                ),
                item(2, "sprite", 1, None, ev(2, "a Sprite")),
                item(3, "water", 2, None, ev(2, "two bottled waters")),
            ],
        ),
    ),
    "syn-t4-0094": (intents((0, S), (1, S), (2, U)), order()),
    "syn-t4-0096": (intents((0, S), (1, U)), order()),
    "syn-t4-0097": (intents((0, S), (1, S), (2, U)), order()),
    "syn-t4-0098": (intents((0, S), (1, U), (2, U)), order()),
    "syn-t4-0101": (
        intents((0, S), (2, P), (3, P), (4, P), (5, Q), (7, P), (8, M)),
        order(
            [
                item(
                    1,
                    "bacon_burger",
                    1,
                    None,
                    ev(2, "bacon burger no pickles"),
                    [mod("remove", "pickle", "no pickles")],
                ),
                item(
                    2,
                    "veggie_burger",
                    1,
                    None,
                    ev(3, "veggie burger no onions"),
                    [mod("remove", "onion", "no onions")],
                ),
            ],
            pay="card",
            pay_ev=ev(7, "paying w card"),
        ),
    ),
    "syn-t4-0102": (
        intents((0, P), (1, P), (3, P)),
        order(
            [
                item(
                    1,
                    "hot_chocolate",
                    1,
                    None,
                    ev(0, "a hot choc") + ev(3, "honey in the hot choc"),
                    [
                        mod("substitute", "whole_milk", "almond milk instead of whole", repl="almond_milk"),
                        offmenu("honey"),
                    ],
                ),
                item(2, "breakfast_sandwich", 3, None, ev(1, "3 breakfast sandwiches")),
                item(
                    3,
                    "croissant",
                    2,
                    "chocolate",
                    ev(1, "2 choc croissants w butter"),
                    [mod("add", "butter", "w butter")],
                ),
            ],
            pay="card",
            pay_ev=ev(1, "card"),
        ),
    ),
    "syn-t4-0104": (
        intents((0, S), (1, P), (2, P), (3, P), (4, P), (5, P), (7, C), (8, M)),
        order(
            [
                item(2, "coke", 1, None, ev(2, "a coke")),
                item(3, "dr_pepper", 1, "two_liter", ev(3, "a 2 liter dr pepper")),
            ],
            "delivery",
            ev(4, "deliver"),
            addr=address(
                "8524", "union terrace", raw="8524 union terrace", evidence=ev(4, "8524 union terrace")
            ),
            pay="card",
            pay_ev=ev(5, "card"),
        ),
    ),
    "syn-t4-0106": (
        intents((0, P), (1, P), (3, P)),
        order(
            [
                item(1, "bbq_chicken_pizza", 2, "large", ev(0, "4 large bbq chicken pizzas")),
                item(
                    2,
                    "bbq_chicken_pizza",
                    2,
                    "large",
                    ev(0, "4 large bbq chicken pizzas") + ev(0, "2 of them w black olives"),
                    [mod("add", "olives", "w black olives")],
                ),
                item(3, "breadsticks", 2, None, ev(1, "2 orders of breadstiks")),
                item(4, "veggie_pizza", 1, "small", ev(1, "a small veggie")),
                item(5, "hawaiian_pizza", 1, "medium", ev(1, "a medium hawaiian")),
            ],
            "delivery",
            ev(3, "delivery"),
            addr=address(
                "975",
                "brookside terrace",
                reference="across from the park",
                raw="975 brookside terrace, across from the park",
                evidence=ev(3, "975 brookside terrace, across from the park"),
            ),
        ),
    ),
    "syn-t4-0107": (
        intents((0, S), (1, P), (2, P), (3, P), (4, P)),
        order(
            [item(1, "diet_coke", 2, None, ev(1, "2 diet cokes"))],
            "delivery",
            ev(2, "deliver"),
            time("clock_time", "at 8:45", "20:45", ev(4, "at 8:45")),
            addr=address(
                "807",
                "riverside ave",
                reference="next to the laundromat",
                raw="807 riverside ave, next to the laundromat",
                evidence=ev(2, "807 riverside ave") + ev(3, "next to the laundromat"),
            ),
            pay="card",
            pay_ev=ev(4, "card"),
        ),
    ),
    "syn-t4-0108": (
        intents((0, S), (1, P), (2, P), (3, P), (4, P), (5, P)),
        order(
            [
                item(
                    1,
                    "bagel",
                    1,
                    "plain",
                    ev(1, "plain bagel") + ev(5, "matcha powder on the bagel"),
                    [offmenu("matcha powder")],
                ),
                item(2, "drip_coffee", 2, None, ev(2, "2 drip coffees")),
            ],
            "pickup",
            ev(3, "pickup"),
            pay="card",
            pay_ev=ev(4, "card"),
            name="Nico",
            name_ev=ev(4, "nico"),
        ),
    ),
    "syn-t4-0110": (
        intents((0, P), (2, P), (3, P), (4, Q), (6, P)),
        order(
            [
                item(
                    2,
                    "veggie_burger",
                    2,
                    None,
                    ev(2, "the veggie burger, two of them no onions"),
                    [mod("remove", "onion", "no onions")],
                ),
                item(3, "onion_rings", 1, None, ev(3, "onion rings")),
                item(4, "lemonade", 4, None, ev(3, "four lemonades")),
                item(5, "sprite", 1, None, ev(3, "a sprite")),
            ],
            "delivery",
            ev(6, "deliver"),
            addr=address(
                "6",
                "harbor way",
                unit="5b",
                raw="6 harbor way unit 5b",
                evidence=ev(6, "6 harbor way unit 5b"),
            ),
            pay="card",
            pay_ev=ev(6, "card"),
        ),
    ),
    "syn-t4-0111": (
        intents((0, S), (1, S), (3, P), (4, P), (5, P), (6, P), (7, P), (8, P), (9, P)),
        order(
            [
                item(1, "bacon_burger", 4, None, ev(3, "4 bacon burgers")),
                item(2, "cheeseburger", 1, None, ev(4, "a cheeseburger")),
                item(3, "onion_rings", 1, None, ev(5, "onion rings")),
                item(4, "milkshake", 1, "chocolate", ev(6, "chocolate shake")),
                item(5, "lemonade", 1, None, ev(7, "a lemonade")),
            ],
            "delivery",
            ev(8, "deliver"),
            addr=address(
                "838", "cedar hill ln", raw="838 cedar hill ln", evidence=ev(8, "838 cedar hill ln")
            ),
            pay="card",
            pay_ev=ev(9, "card"),
        ),
    ),
    "syn-t4-0112": (
        intents((0, S), (2, P), (3, P), (4, P), (6, C), (7, M)),
        order(
            [
                item(
                    1,
                    "meat_lovers_pizza",
                    2,
                    "medium",
                    ev(2, "2 medium meat lovers, no bacon") + ev(7, "add banana peppers to the meat lovers"),
                    [mod("remove", "bacon", "no bacon"), mod("add", "banana_peppers", "banana peppers")],
                ),
                item(2, "coke", 2, None, ev(3, "2 cokes")),
                item(3, "diet_coke", 2, None, ev(3, "2 diet cokes")),
            ],
            "pickup",
            ev(4, "pickup"),
            pay="cash",
            pay_ev=ev(4, "cash"),
            name="Maya",
            name_ev=ev(4, "maya"),
        ),
    ),
    "syn-t4-0113": (intents((0, OOS)), order()),
    "syn-t4-0114": (
        intents((0, Q), (2, P), (4, C), (5, M)),
        order(
            [
                item(
                    1,
                    "breakfast_sandwich",
                    4,
                    "english_muffin",
                    ev(2, "4 on english muffins no bacon"),
                    [mod("remove", "bacon", "no bacon")],
                ),
                item(3, "croissant", 1, "almond", ev(5, "an almond croissant")),
            ],
            "pickup",
            ev(2, "pickup"),
            pay="card",
            pay_ev=ev(2, "card"),
            name="Nico",
            name_ev=ev(2, "nico"),
        ),
    ),
    "syn-t4-0115": (
        intents((0, P), (2, P), (3, P), (4, P)),
        order(
            [
                item(
                    2,
                    "cheese_pizza",
                    2,
                    "small",
                    ev(2, "2 small cheese pizzas no cheese"),
                    [mod("remove", "cheese", "no cheese")],
                ),
                item(
                    3,
                    "supreme_pizza",
                    1,
                    "small",
                    ev(2, "a small supreme w red onions"),
                    [mod("add", "red_onions", "w red onions")],
                ),
                item(4, "dr_pepper", 3, "bottle_20oz", ev(3, "3 dr peppers, the 20 oz bottles")),
                item(5, "coke", 2, None, ev(3, "2 cokes")),
            ],
            "pickup",
            ev(4, "pickup"),
            name="Marcus",
            name_ev=ev(4, "marcus"),
        ),
    ),
    "syn-t4-0116": (
        intents((0, S), (2, P), (3, P), (4, P), (5, P), (6, P)),
        order(
            [
                item(1, "bbq_chicken_pizza", 2, "medium", ev(2, "4 medium bbq chicken pizzas")),
                item(
                    2,
                    "bbq_chicken_pizza",
                    2,
                    "medium",
                    ev(2, "4 medium bbq chicken pizzas") + ev(2, "2 of those without the chicken"),
                    [mod("remove", "grilled_chicken", "without the chicken")],
                ),
                item(
                    3,
                    "supreme_pizza",
                    1,
                    "small",
                    ev(3, "a small supreme") + ev(4, "add grilled chicken on the supreme"),
                    [mod("add", "grilled_chicken", "add grilled chicken")],
                ),
                item(4, "dr_pepper", 1, None, ev(5, "a dr pepper")),
            ],
            "delivery",
            ev(6, "delivery"),
            addr=address(
                "70",
                "vine blvd",
                reference="across from the park",
                raw="70 vine blvd, across from the park",
                evidence=ev(6, "70 vine blvd, across from the park"),
            ),
        ),
    ),
    "syn-t4-0118": (
        intents((0, P), (2, P), (3, Q), (5, P)),
        order(
            [
                item(1, "cappuccino", 2, "large", ev(0, "2 large capuccinos")),
                item(
                    2,
                    "americano",
                    1,
                    "large",
                    ev(2, "large americano w hazelnut"),
                    [mod("add", "hazelnut_syrup", "w hazelnut")],
                ),
                item(3, "drip_coffee", 1, "large", ev(2, "a large drip")),
                item(4, "muffin", 2, "banana_nut", ev(5, "2 banana nut")),
            ],
            "pickup",
            ev(5, "pickup"),
            name="Dev",
            name_ev=ev(5, "dev"),
        ),
    ),
    "syn-t4-0119": (
        intents((0, S), (1, P), (2, P), (3, P), (4, P)),
        order(
            [
                item(1, "bagel", 5, "plain", ev(1, "6 plain bagels")),
                item(
                    2,
                    "bagel",
                    1,
                    "plain",
                    ev(1, "6 plain bagels") + ev(1, "1 of them w cream cheese"),
                    [mod("add", "cream_cheese", "w cream cheese")],
                ),
                item(3, "croissant", 1, None, ev(2, "a croissant")),
            ],
            "pickup",
            ev(3, "pickup"),
            time("clock_time", "at 10:30am", "10:30", ev(3, "at 10:30am")),
            name="Rosa",
            name_ev=ev(4, "rosa"),
        ),
    ),
    "syn-t4-0120": (
        intents((0, P), (1, P), (3, P)),
        order(
            [
                item(
                    1,
                    "breakfast_sandwich",
                    1,
                    "english_muffin",
                    ev(0, "a breakfast sandwich on an english muffin") + ev(1, "no egg"),
                    [mod("remove", "egg", "no egg")],
                )
            ],
            when=time("clock_time", "at 12:45", "12:45", ev(3, "at 12:45")),
            pay="card",
            pay_ev=ev(3, "paying w card"),
        ),
    ),
    "syn-t4-0121": (
        intents((0, Q), (2, P), (3, Q), (5, P), (7, C), (8, M)),
        order(
            [item(1, "margherita_pizza", 1, "extra_large", ev(0, "margherita") + ev(2, "extra large"))],
            "pickup",
            ev(5, "pick it up"),
            pay="cash",
            pay_ev=ev(8, "pay cash instead"),
        ),
    ),
    "syn-t4-0122": (
        intents((0, P), (1, P), (3, P)),
        order(
            [
                item(
                    1,
                    "bbq_chicken_pizza",
                    4,
                    "personal",
                    ev(0, "4 personal bbq chicken pizzas w parmesan"),
                    [mod("add", "parmesan", "w parmesan")],
                ),
                item(
                    2,
                    "margherita_pizza",
                    1,
                    "large",
                    ev(1, "a large margherita no tomato sauce"),
                    [mod("remove", "tomato_sauce", "no tomato sauce")],
                ),
                item(3, "breadsticks", 2, None, ev(1, "2 orders of breadsticks")),
                item(4, "diet_coke", 4, None, ev(1, "4 diet cokes")),
                item(5, "iced_tea", 1, "bottle_20oz", ev(1, "a 20oz iced tea")),
            ],
            "delivery",
            ev(3, "delivery"),
            addr=address("98", "elm dr", raw="98 elm dr", evidence=ev(3, "98 elm dr")),
        ),
    ),
}


def fix_0084(label):
    """Teacher label dropped (contract): 'around 9pm' marked ambiguous with a kind. The teacher's own convention
    for a single 'around' time is a provided clock time."""
    t = label["order"]["fulfillment"]["requested_time"]
    t.update(state="provided", kind="clock_time", raw_text="around 9pm", normalized_local="21:00")
    return label


def _no_order(label):
    o = label["order"]
    o["items"], o["ambiguity_flags"] = [], []


def fix_0005(label):
    label["intents"][2]["primary"] = U  # "the usu": cut off mid-word, orders nothing
    _no_order(label)
    return label


def fix_0020(label):
    label["intents"][0]["primary"] = U
    return label


def fix_0031(label):
    label["intents"][3]["primary"] = (
        P  # a request about an item being ordered (the teacher's own 36 other cases)
    )
    line = label["order"]["items"][0]
    line["modifications"].append(offmenu("capers"))
    line["evidence"].append({"message_index": 3, "quote": "capers on the pepperoni"})
    return label


TEACHER_FIXES = {
    "syn-t4-0084": (
        fix_0084,
        "label dropped (contract): 'around 9pm' marked ambiguous with a kind; the teacher's convention is a provided clock time (21:00)",
    ),
    "syn-t4-0005": (
        fix_0005,
        "card check: 'the usu' is cut off mid-word: UNKNOWN, no item (teacher-label@0.7 rule)",
    ),
    "syn-t4-0020": (
        fix_0020,
        "card check: a garbled message is UNKNOWN, not SMALL_TALK (teacher-label@0.7 rule)",
    ),
    "syn-t4-0031": (
        fix_0031,
        "card check: the off-menu capers request was dropped and called MENU_QUESTION; kept as not_on_menu + PLACE_ORDER like the teacher's 36 other offmenu_open labels ('3 breadsticks' stays quantity null: 3 pieces at 4 per order)",
    ),
}


def main() -> None:
    out = run.batch_dir(BATCH) / "label_fixes"
    out.mkdir(exist_ok=True)
    conv = {c.card_id: c.conversation for c in run.load_conversations(BATCH)}
    now = datetime.now(UTC).isoformat()
    records = {}
    for cid, (ints, order_) in LABELS.items():
        records[cid] = {
            "card_id": cid,
            "kind": "hand_label",
            "reason": "teacher call failed (OpenAI credit used up); whole label written by hand under teacher-label@0.7",
            "fixed_by": FIXED_BY,
            "fixed_at": now,
            "label_prompt_version": run.HAND_LABEL_VERSION,
            "label": {"schema_version": "label@0.1", "intents": ints, "order": order_},
        }
    for cid, (fix, reason) in TEACHER_FIXES.items():
        rec = json.loads(
            (run.batch_dir(BATCH) / "label" / run._slug(lab.TEACHER) / f"{cid}.json").read_text()
        )
        label = fix(json.loads(ChatResponse.model_validate(rec["response"]).text))
        records[cid] = {
            "card_id": cid,
            "reason": reason,
            "fixed_by": FIXED_BY,
            "fixed_at": now,
            "label": label,
        }
    for cid, record in records.items():
        c = conv[cid]
        lc, why = lab.parse_label(json.dumps(record["label"]), c, load_menu(c.business_id), FIXED_BY)
        if lc is None:
            raise SystemExit(f"{cid}: fails the label checks: {why}")
        (out / f"{cid}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(records)} labels written to runs/synth/{BATCH}/label_fixes/")


if __name__ == "__main__":
    main()
