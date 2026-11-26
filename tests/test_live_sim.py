"""The bot turn (bot@0.1) and the simulated-customer loop (live-sim@0.1), offline: v6's saved answers stand in
for the model, so nothing here needs a GPU."""

import inspect
import json

import pytest

from orderslm.bot.turn import TEXT, BotState, bot_turn
from orderslm.eval import live_sim as ls
from orderslm.eval.dataset import load_eval_split
from orderslm.menus import load_menu
from orderslm.paths import RUNS
from orderslm.schema.conversation import Split
from orderslm.schema.order import OrderStatus
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data

V6_DEV = RUNS / "student-dev" / "20261125T130650Z-qwen3.5-0.8b-single-v6-cd" / "outputs.jsonl"


def _replay(cid: str):
    if not V6_DEV.exists():
        pytest.skip("v6 dev run not present")
    outs = {json.loads(x)["id"]: json.loads(x) for x in V6_DEV.read_text().splitlines()}
    conv = next(a.conversation for a in load_eval_split(Split.dev) if a.conversation.id == cid)
    menu, state, kinds = load_menu(conv.business_id), BotState(), []
    for k in conv.customer_indices():
        r = bot_turn(
            menu,
            conv.model_copy(update={"messages": conv.messages[: k + 1]}),
            state,
            outs[f"{cid}#{k}"]["text"],
        )
        state = r.state
        kinds.append(r.kind)
        if state.ended:
            break
    return kinds, state


def test_questions_then_a_summary_then_yes_places_the_order():
    kinds, state = _replay("a-dev-023")
    assert kinds == ["question", "question", "question", "summary", "placed"]
    assert state.ended == "placed" and state.status is OrderStatus.new


def test_a_yes_before_any_summary_places_nothing():
    kinds, state = _replay("a-dev-065")  # ends on "CARD": the summary goes out, no yes yet
    assert kinds[-1] == "summary" and state.status is OrderStatus.awaiting_confirmation and not state.ended


def _one(text: str, intent: str):
    conv = next(a.conversation for a in load_eval_split(Split.dev) if a.conversation.id == "a-dev-023")
    conv = conv.model_copy(update={"messages": conv.messages[:1]})
    student = {
        "schema_version": "student@0.2",
        "intent": {"primary": intent, "secondary": None},
        "order": json.loads(json.loads(V6_DEV.read_text().splitlines()[0])["text"])["order"]
        if V6_DEV.exists()
        else pytest.skip("v6 dev run not present"),
    }
    return bot_turn(load_menu(conv.business_id), conv, BotState(), text or json.dumps(student))


def test_invalid_answer_asks_again_and_keeps_the_state():
    r = _one("not json", "PLACE_ORDER")
    assert r.kind == "repeat" and r.reply == TEXT["repeat"] and not r.valid and r.state == BotState()


def test_staff_intents_end_the_chat_with_a_handoff():
    r = _one("", "HUMAN_REQUEST")
    assert r.kind == "handoff" and r.state.ended == "handoff"


def _card(**target) -> ls.SimCard:
    base = {
        "items": [{"menu_item_id": "pepperoni_pizza", "variant_id": "large", "quantity": 2}],
        "method": "pickup",
        "payment": "card",
    }
    return ls.SimCard.model_validate(
        {
            "id": "sim1-999",
            "business_id": "halfmoon-pizza",
            "start_at": "2026-12-01T18:30:00-06:00",
            "persona": "p",
            "style": "s",
            "plan": "p",
            "target": base | target,
        }
    )


def test_card_check_catches_targets_the_code_cant_price_or_times_outside_hours():
    assert ls.check_card(_card()) == []
    bad = _card(items=[{"menu_item_id": "pepperoni_pizza", "variant_id": "huge", "quantity": 1}])
    assert any("doesn't price" in p for p in ls.check_card(bad))
    early = _card().model_copy(update={"start_at": ls.datetime.fromisoformat("2026-12-01T08:00:00-06:00")})
    assert any("opening hours" in p for p in ls.check_card(early))


def test_the_customer_turns_and_bot_replies_round_trip(tmp_path, monkeypatch):
    """customer 0 → requests → (fake kernel output) → import: the bot's reply lands in the chat."""
    if not V6_DEV.exists():
        pytest.skip("v6 dev run not present")
    card = _card()
    monkeypatch.setattr(ls, "CARDS", tmp_path / "cards.jsonl")
    monkeypatch.setattr(ls, "CHATS", tmp_path / "chats")
    monkeypatch.setattr(ls, "TURNS", tmp_path / "turns")
    monkeypatch.setattr(ls, "ROOT", tmp_path)
    (tmp_path / "cards.jsonl").write_text(card.model_dump_json() + "\n")
    (tmp_path / "turns").mkdir()
    (tmp_path / "turns" / "0.jsonl").write_text(
        json.dumps({"id": card.id, "text": "2 large pepperoni pls"}) + "\n"
    )
    assert ls.add_customer_turns(0) == {"messages": 1}
    reqs = ls.requests()
    assert [r["id"] for r in reqs] == ["sim1-999#0"] and "2 large pepperoni pls" in reqs[0]["user"]
    run_dir, out = tmp_path / "run", tmp_path / "out"
    run_dir.mkdir()
    (out / "sim-a").mkdir(parents=True)
    (run_dir / "requests.jsonl").write_text(json.dumps(reqs[0]) + "\n")
    (run_dir / "manifest.json").write_text(json.dumps({"session": "S", "jobs": [{"name": "sim-a"}]}))
    (out / "env.json").write_text(json.dumps({"session": "S"}))
    (out / "sim-a" / "outputs.jsonl").write_text(json.dumps({"id": "sim1-999#0", "text": "garbage"}) + "\n")
    assert ls.import_(run_dir, out) == {"repeat": 1}
    chat = ls.load_chat(card.id)
    assert chat["messages"][-1] == {**chat["messages"][-1], "role": "business", "text": TEXT["repeat"]}
    assert ls.waiting_on(chat) == "customer" and ls.requests() == []


def test_sim1_is_never_training_or_generation_input():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "SIM1" not in src and "Split.sim1" not in src and "data/sim1" not in src, module.__name__
