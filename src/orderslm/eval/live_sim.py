"""Simulated-customer test (live-sim@0.1): the shipped student + the bot code, talking to a customer who reacts to
the bot's real replies, scored on the order the customer confirms.

Julian, 2026-11-26: "do a simulated customer test", "just you write it" (no API spend). The customer is played by
Claude in the session, in rounds, from a scenario card with a hidden target order (`data/sim1/cards.jsonl`):

    make live-sim ARGS="customer 0"     # data/sim1/turns/0.jsonl: first messages → data/sim1/chats/<id>.json
    make live-sim ARGS="export"         # requests for every chat waiting on the bot → kaggle/m6-deploy/upload/
    make kaggle-push JOB=m6-deploy      # v6 as Q8_0 GGUF on Kaggle (free), exactly as shipped
    make kaggle-pull JOB=m6-deploy
    make live-sim ARGS="import runs/live-sim/<session>"   # student answers → bot_turn → bot replies in the chats
    make live-sim ARGS="show"           # what each open chat's customer sees, to write the next round
    make live-sim ARGS="customer 1"     # ... repeat until every chat has ended
    make live-sim ARGS="score"          # → runs/live-sim/score-<time>/

Outcomes per chat: **placed correct** (the confirmed order matches the target), **placed wrong** (the customer said
yes to an order that differs from what they wanted: the number that matters), handed to staff, cancelled, or no
order (the customer gave up, or MAX_CUSTOMER_TURNS ran out). Turns = customer messages.

The order is compared as the kitchen would get it: items by scorer@0.5's item_key (defaults filled), the method,
the day and time from code's schedule, the address numbers, payment method (+ change), and the name when the target
has one. Caveats for the write-up: the customer is played by the same writer as the training and fresh chats, and
it knows the bot is a bot; sim1 is evaluation-only and never training or generation input.
"""

import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pydantic import Field

from orderslm.bot.turn import BOT_VERSION, BotState, bot_turn
from orderslm.core.finalize import fill_default_variants
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.schedule import resolve_schedule
from orderslm.eval.metrics import SCORER_VERSION, item_key
from orderslm.eval.stats import wilson
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS, SIM1
from orderslm.runinfo import git_commit
from orderslm.schema.common import Strict
from orderslm.schema.conversation import Conversation, Message, Role, Source, Split
from orderslm.schema.extraction import ComboSelection, ExtractionOutput, ItemProposal, Modification
from orderslm.schema.order import OrderStatus, ToolOk
from orderslm.train import data
from orderslm.train import kaggle_deploy as kd

SIM_VERSION = "live-sim@0.1"
EXPERIMENT = "live-sim"
CARDS = SIM1 / "cards.jsonl"
CHATS = SIM1 / "chats"
TURNS = SIM1 / "turns"
MAX_CUSTOMER_TURNS = 12
CUSTOMER_GAP = timedelta(seconds=45)  # a customer reply this long after the bot's
BOT_GAP = timedelta(seconds=4)


class TargetItem(Strict):
    menu_item_id: str
    variant_id: str | None = None
    quantity: int = Field(ge=1, le=99)
    modifications: list[dict[str, Any]] = Field(default_factory=list)  # Modification fields minus raw_text
    combo_selections: list[ComboSelection] = Field(default_factory=list)


class Target(Strict):
    items: list[TargetItem] = Field(min_length=1)
    method: str  # pickup | delivery
    days_ahead: int = 0
    time: str | None = None  # "HH:MM" local; None = as soon as possible
    address: str | None = None  # delivery only
    payment: str  # card | cash
    change_for_cents: int | None = None
    name: str | None = None  # checked only when set


class SimCard(Strict):
    id: str = Field(pattern=r"^sim1-\d{3}$")
    business_id: str
    start_at: datetime  # the first customer message, timezone-aware
    persona: str
    style: str
    plan: str  # how this customer behaves: what they say up front, what they leave out, what they change
    checks_summary: bool = True  # False: says yes to the first summary without reading it
    target: Target


def load_cards() -> dict[str, SimCard]:
    cards = [SimCard.model_validate_json(x) for x in CARDS.read_text().splitlines() if x.strip()]
    return {c.id: c for c in cards}


def target_items(card: SimCard) -> list[ItemProposal]:
    ev = [{"message_index": 0, "quote": "target"}]
    return [
        ItemProposal(
            line_id=f"L{k}",
            menu_item_id=t.menu_item_id,
            variant_id=t.variant_id,
            quantity=t.quantity,
            modifications=[Modification.model_validate({"raw_text": "target", **m}) for m in t.modifications],
            combo_selections=t.combo_selections,
            evidence=ev,
        )
        for k, t in enumerate(card.target.items, 1)
    ]


def check_card(card: SimCard) -> list[str]:
    """A target the code can't price or schedule is a bad card (written by hand), not a bot mistake."""
    menu = load_menu(card.business_id)
    problems = []
    blank = _blank_order(target_items(card), card)
    quote = DeterministicPricing().quote(menu, blank)
    if not isinstance(quote, ToolOk):
        problems.append(f"target doesn't price: {quote.error.code} {quote.error.message}")
    if card.start_at.tzinfo is None:
        problems.append("start_at needs a timezone")
    hours = menu.hours_on(_weekday(card.start_at.astimezone(_tz(menu))))
    local = card.start_at.astimezone(_tz(menu)).time()
    if hours is None or not hours.opens_at <= local < hours.closes_at:
        problems.append(f"chat starts outside opening hours ({local})")
    if card.target.method == "delivery" and not card.target.address:
        problems.append("delivery target without an address")
    return problems


def _tz(menu):
    from zoneinfo import ZoneInfo

    return ZoneInfo(menu.timezone)


def _weekday(dt: datetime):
    from orderslm.core.schedule import weekday_of

    return weekday_of(dt.date())


def _blank_order(items: list[ItemProposal], card: SimCard) -> ExtractionOutput:
    return ExtractionOutput.model_validate(
        {
            "items": [i.model_dump(mode="json") for i in items],
            "fulfillment": {
                "method": card.target.method,
                "method_evidence": [{"message_index": 0, "quote": "target"}],
                "requested_time": {"state": "not_mentioned"},
            },
            "address": {"state": "not_applicable" if card.target.method == "pickup" else "not_mentioned"},
            "payment": {"method": "unknown"},
            "customer_name": {"state": "not_mentioned"},
        }
    )


# ---------------------------------------------------------------- chats


def chat_path(cid: str) -> Path:
    return CHATS / f"{cid}.json"


def load_chat(cid: str) -> dict[str, Any]:
    return json.loads(chat_path(cid).read_text())


def save_chat(chat: dict[str, Any]) -> None:
    CHATS.mkdir(parents=True, exist_ok=True)
    chat_path(chat["id"]).write_text(json.dumps(chat, indent=2, ensure_ascii=False) + "\n")


def all_chats() -> list[dict[str, Any]]:
    return [json.loads(p.read_text()) for p in sorted(CHATS.glob("sim1-*.json"))]


def conversation(chat: dict[str, Any]) -> Conversation:
    return Conversation(
        id=chat["id"],
        business_id=chat["business_id"],
        split=Split.sim1,
        source=Source.claude_written,
        messages=[Message.model_validate(m) for m in chat["messages"]],
    )


def bot_state(chat: dict[str, Any]) -> BotState:
    b = chat["bot"]
    return BotState(
        status=OrderStatus(b["status"]),
        proposal=ExtractionOutput.model_validate(b["proposal"]) if b["proposal"] else None,
        ended=b["ended"],
    )


def _set_state(chat: dict[str, Any], s: BotState) -> None:
    chat["bot"] = {
        "status": s.status.value,
        "proposal": s.proposal.model_dump(mode="json") if s.proposal else None,
        "ended": s.ended,
    }


def ended(chat: dict[str, Any]) -> str | None:
    return chat["bot"]["ended"] or chat.get("customer_end")


def waiting_on(chat: dict[str, Any]) -> str | None:
    """Who speaks next: 'bot', 'customer', or None (ended)."""
    if ended(chat):
        return None
    return "bot" if chat["messages"][-1]["role"] == Role.customer.value else "customer"


def customer_turns(chat: dict[str, Any]) -> int:
    return sum(m["role"] == Role.customer.value for m in chat["messages"])


def add_customer_turns(round_no: int) -> dict[str, int]:
    """data/sim1/turns/<round>.jsonl: {"id", "text"} or {"id", "gives_up": true}. Round 0 starts the chats."""
    cards = load_cards()
    rows = [json.loads(x) for x in (TURNS / f"{round_no}.jsonl").read_text().splitlines() if x.strip()]
    counts = Counter()
    for r in rows:
        card = cards[r["id"]]
        if round_no == 0:
            if chat_path(card.id).exists():
                raise SystemExit(f"{card.id} already started")
            if bad := check_card(card):
                raise SystemExit(f"{card.id}: {bad}")
            chat = {
                "id": card.id,
                "business_id": card.business_id,
                "sim_version": SIM_VERSION,
                "bot_version": BOT_VERSION,
                "messages": [],
                "turns": [],
                "customer_end": None,
            }
            _set_state(chat, BotState())
            at = card.start_at
        else:
            chat = load_chat(card.id)
            if waiting_on(chat) != "customer":
                raise SystemExit(f"{card.id}: not waiting for the customer ({waiting_on(chat)})")
            at = datetime.fromisoformat(chat["messages"][-1]["sent_at"]) + CUSTOMER_GAP
        if r.get("gives_up"):
            chat["customer_end"] = "gave_up"
            counts["gave_up"] += 1
        else:
            chat["messages"].append(
                {
                    "index": len(chat["messages"]),
                    "role": "customer",
                    "text": r["text"],
                    "sent_at": at.isoformat(),
                }
            )
            counts["messages"] += 1
            if customer_turns(chat) > MAX_CUSTOMER_TURNS:
                raise SystemExit(f"{card.id}: more than {MAX_CUSTOMER_TURNS} customer turns")
        save_chat(chat)
    return dict(counts)


def requests() -> list[dict[str, Any]]:
    system = data.system_prompt()
    out = []
    for chat in all_chats():
        if waiting_on(chat) != "bot":
            continue
        conv = conversation(chat)
        menu = load_menu(chat["business_id"])
        k = conv.messages[-1].index
        out.append({"id": f"{chat['id']}#{k}", "system": system, "user": data.user_prompt(conv, menu)})
    return out


def export() -> Path:
    reqs = requests()
    session = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    run = kd.export_sim(reqs, session)
    out = RUNS / EXPERIMENT / session
    out.mkdir(parents=True)
    (out / "requests.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in reqs))
    manifest = {
        "experiment": EXPERIMENT,
        "sim_version": SIM_VERSION,
        "bot_version": BOT_VERSION,
        **run,
        "requests": len(reqs),
        "git_commit": git_commit(),
        "exported_at": datetime.now(UTC).isoformat(),
        "kaggle_dataset": kd.DATASET,
        "cost_usd": 0.0,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"{len(reqs)} requests staged; run dir {out.relative_to(ROOT)}/")
    return out


def import_(run_dir: Path, output_dir: Path) -> dict[str, int]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("session") != manifest["session"]:
        raise SystemExit(f"kernel output is for session {env.get('session')}, not {manifest['session']}")
    records = {}
    for job in manifest["jobs"]:
        src = output_dir / job["name"] / "outputs.jsonl"
        lines = src.read_text().splitlines() if src.exists() else []
        (run_dir / f"{job['name']}-outputs.jsonl").write_text("\n".join(lines) + ("\n" if lines else ""))
        records |= {(r := json.loads(x))["id"]: r for x in lines if x.strip()}
    counts = Counter()
    wanted = [json.loads(x)["id"] for x in (run_dir / "requests.jsonl").read_text().splitlines()]
    for rid in wanted:
        cid, k = rid.split("#")
        chat = load_chat(cid)
        rec = records.get(rid)
        if waiting_on(chat) != "bot" or chat["messages"][-1]["index"] != int(k):
            raise SystemExit(f"{rid}: the chat moved on since export")
        if not rec or "text" not in rec:
            counts["unanswered"] += 1  # left waiting on the bot: the next export retries it
            continue
        conv = conversation(chat)
        result = bot_turn(load_menu(chat["business_id"]), conv, bot_state(chat), rec["text"])
        at = conv.messages[-1].sent_at + BOT_GAP
        chat["messages"].append(
            {
                "index": len(chat["messages"]),
                "role": "business",
                "text": result.reply,
                "sent_at": at.isoformat(),
            }
        )
        chat["turns"].append(
            {
                "run": str(run_dir.relative_to(ROOT)),
                "request_id": rid,
                "student_text": rec["text"],
                "latency_ms": rec.get("latency_ms"),
                "valid": result.valid,
                "intent": result.intent,
                "kind": result.kind,
            }
        )
        _set_state(chat, result.state)
        if not result.state.ended and customer_turns(chat) >= MAX_CUSTOMER_TURNS:
            chat["customer_end"] = "turn_limit"
        save_chat(chat)
        counts[result.kind] += 1
    manifest["imported_at"] = datetime.now(UTC).isoformat()
    manifest["import_counts"] = dict(counts)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return dict(counts)


def show(cid: str | None = None) -> str:
    cards = load_cards()
    out = []
    for chat in all_chats():
        if cid and chat["id"] != cid:
            continue
        if not cid and waiting_on(chat) != "customer":
            continue
        card = cards[chat["id"]]
        out.append(f"## {chat['id']} · {card.business_id} · {card.persona} · {card.style}")
        out.append(
            f"plan: {card.plan}" + ("" if card.checks_summary else " [SAYS YES WITHOUT READING THE SUMMARY]")
        )
        out.append(f"target: {card.target.model_dump_json(exclude_defaults=True)}")
        for m in chat["messages"]:
            out.append(f"  [{m['index']}] {m['role']}: {m['text']}")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- score


def compare(card: SimCard, placed: ExtractionOutput, conv: Conversation) -> list[str]:
    """What differs between the placed order and the target (empty = correct)."""
    menu = load_menu(card.business_id)
    t = card.target
    got = fill_default_variants(placed, menu)
    want = fill_default_variants(_blank_order(target_items(card), card), menu)
    diffs = []
    g, w = Counter(item_key(i) for i in got.items), Counter(item_key(i) for i in want.items)
    if g != w:
        diffs.append(
            f"items: missing {sorted(map(repr, (w - g).elements()))} extra {sorted(map(repr, (g - w).elements()))}"
        )
    if got.fulfillment.method.value != t.method:
        diffs.append(f"method: {got.fulfillment.method.value} vs {t.method}")
    sched = resolve_schedule(menu, placed, conv)
    if isinstance(sched, ToolOk):
        s = sched.data
        got_time = None if s.asap else (s.local_time.strftime("%H:%M") if s.local_time else s.time_text)
        if s.days_ahead != t.days_ahead or got_time != t.time:
            diffs.append(f"when: +{s.days_ahead}d {got_time} vs +{t.days_ahead}d {t.time}")
    else:
        diffs.append(f"when: {sched.error.code}")
    if t.method == "delivery":
        import re

        want_n = sorted(re.findall(r"\d+", t.address or ""))
        got_n = sorted(re.findall(r"\d+", placed.address.raw_text or ""))
        if want_n != got_n:
            diffs.append(f"address: {placed.address.raw_text!r} vs {t.address!r}")
    if placed.payment.method.value != t.payment or (
        t.change_for_cents is not None and placed.payment.change_for_cents != t.change_for_cents
    ):
        diffs.append(
            f"payment: {placed.payment.method.value}/{placed.payment.change_for_cents} vs {t.payment}"
        )
    if t.name and (placed.customer_name.value or "").strip().casefold() != t.name.casefold():
        diffs.append(f"name: {placed.customer_name.value!r} vs {t.name!r}")
    return diffs


def score() -> Path:
    cards = load_cards()
    rows = []
    for chat in all_chats():
        card = cards[chat["id"]]
        how = ended(chat)
        row = {
            "id": chat["id"],
            "business_id": card.business_id,
            "outcome": how or "open",
            "customer_turns": customer_turns(chat),
            "bot_questions": sum(t["kind"] == "question" for t in chat["turns"]),
            "summaries": sum(t["kind"] == "summary" for t in chat["turns"]),
            "invalid_answers": sum(not t["valid"] for t in chat["turns"]),
            "checks_summary": card.checks_summary,
            "diffs": None,
        }
        if how == "placed":
            row["diffs"] = compare(card, bot_state(chat).proposal, conversation(chat))
            row["outcome"] = "placed_correct" if not row["diffs"] else "placed_wrong"
        rows.append(row)
    n = len(rows)
    outcomes = Counter(r["outcome"] for r in rows)
    summary = {
        "sim_version": SIM_VERSION,
        "bot_version": BOT_VERSION,
        "scorer": SCORER_VERSION,
        "student": kd.STUDENT,
        "chats": n,
        "outcomes": dict(outcomes),
        "rates": {
            k: {"n": outcomes[k], "rate": outcomes[k] / n if n else None, "ci95": wilson(outcomes[k], n)}
            for k in ("placed_correct", "placed_wrong")
        },
        "by_customer": {
            k: dict(Counter(r["outcome"] for r in rows if r["checks_summary"] is v))
            for k, v in (("reads_summary", True), ("says_yes_without_reading", False))
        },
        "customer_turns_mean": sum(r["customer_turns"] for r in rows) / n if n else None,
        "bot_questions_mean": sum(r["bot_questions"] for r in rows) / n if n else None,
        "invalid_answers": sum(r["invalid_answers"] for r in rows),
        "git_commit": git_commit(),
    }
    out = RUNS / EXPERIMENT / f"score-{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    out.mkdir(parents=True)
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# Simulated-customer test ({SIM_VERSION}, {BOT_VERSION}, `{kd.STUDENT}` Q8_0)", ""]
    lines += [f"- {k}: {v} of {n}" for k, v in sorted(outcomes.items())]
    lines += ["", "Placed wrong:", ""] + [
        f"- {r['id']}: {'; '.join(r['diffs'])}" for r in rows if r["outcome"] == "placed_wrong"
    ]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print((out / "report.md").read_text())
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    c = sub.add_parser("customer")
    c.add_argument("round", type=int)
    sub.add_parser("export")
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=kd.JOB_DIR / "output")
    s = sub.add_parser("show")
    s.add_argument("id", nargs="?")
    sub.add_parser("score")
    args = ap.parse_args(argv)
    if args.cmd == "check":
        bad = {c.id: p for c in load_cards().values() if (p := check_card(c))}
        print(json.dumps(bad, indent=2) if bad else f"{len(load_cards())} cards ok")
        return 1 if bad else 0
    if args.cmd == "customer":
        print(add_customer_turns(args.round))
    elif args.cmd == "export":
        export()
    elif args.cmd == "import":
        print(import_(args.run_dir.resolve(), args.output.resolve()))
    elif args.cmd == "show":
        print(show(args.id))
    else:
        score()
    return 0


if __name__ == "__main__":
    sys.exit(main())
