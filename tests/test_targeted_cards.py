"""Targeted synthetic cards (M6 error review): each pattern is really in the card, old batches still reproduce."""

import json
import re
from collections import Counter

import pytest

from orderslm.menus import load_menus
from orderslm.paths import RUNS
from orderslm.schema.routing import RouterLabel
from orderslm.synth import cards as sc

GENS = (
    ("deepseek/deepseek-flash@none", 4),
    ("google/gemini-3.1-flash-lite@minimal", 1),
    ("anthropic/claude-haiku-5-5@off-low", 1),
)


@pytest.fixture(scope="module")
def planned():
    return sc.plan_targeted_cards(600, seed=20261016, batch="t-test", generators=GENS)


def _target(card):
    return next(x.removeprefix("target:") for x in card.extras if x.startswith("target:"))


def _by(planned, target):
    return [c for c in planned if _target(c) == target]


def test_targets_and_writers_come_out_exactly(planned):
    total = sum(sc.TARGET_WEIGHTS.values())
    assert Counter(_target(c) for c in planned) == {t: w * 600 // total for t, w in sc.TARGET_WEIGHTS.items()}
    assert Counter(c.generator for c in planned) == {g: w * 100 for g, w in GENS}
    menus = load_menus()
    assert {c.business_id for c in planned} == {b for b, m in menus.items() if not m.held_out}


def test_same_seed_same_cards(planned):
    again = sc.plan_targeted_cards(600, seed=20261016, batch="t-test", generators=GENS)
    assert [c.model_dump() for c in again] == [c.model_dump() for c in planned]


def test_split_lines_are_one_dish_on_two_lines_one_changed(planned):
    for c in _by(planned, "split_lines"):
        a, b = c.items[:2]
        assert a.menu_item_id == b.menu_item_id and a.variant_id == b.variant_id
        assert not (a.remove or a.add or a.substitute) and len(b.remove) + len(b.add) == 1
        assert "same item" in c.brief


def test_big_orders_have_four_to_six_lines(planned):
    assert all(4 <= len(c.items) <= 6 for c in _by(planned, "big_order"))


def test_modify_last_expects_a_modify_and_says_the_change_comes_last(planned):
    for c in _by(planned, "modify_last"):
        assert RouterLabel.MODIFY_ORDER in c.expected_labels
        assert "very last customer message" in c.brief


def test_size_unstated_leaves_a_size_open(planned):
    menus = load_menus()
    for c in _by(planned, "size_unstated"):
        m = menus[c.business_id]
        open_size = [
            p for p in c.items if p.menu_item_id and p.variant_id is None and m.item(p.menu_item_id).variants
        ]
        assert open_size and "Never says the size" in c.brief


def test_off_menu_addons_are_not_on_any_training_menu(planned):
    for b, addons in sc.OFF_MENU_ADDONS.items():
        menu = load_menus()[b]
        names = {x.casefold() for mod in menu.modifiers for x in [mod.name, *mod.aliases]}
        for a in addons:
            word = a.removeprefix("a ").casefold()
            assert word not in names and not any(word in n or n in word for n in names), (b, a)
    assert all("isn't on the menu" in c.brief for c in _by(planned, "offmenu_addon"))


def test_bare_times_have_no_am_pm_and_mean_the_coming_hour(planned):
    for c in _by(planned, "bare_time"):
        said, hh, mm = re.search(
            r"'at (\d{1,2}(?::\d\d)?)' \(meaning (\d\d):(\d\d) today\)", c.brief
        ).groups()
        h, m = int(hh), int(mm)
        assert said == (f"{(h - 1) % 12 + 1}:{m:02d}" if m else f"{(h - 1) % 12 + 1}")
        menu = load_menus()[c.business_id]
        local = c.start_at.astimezone(__import__("zoneinfo").ZoneInfo(menu.timezone))
        minutes = h * 60 + m - (local.hour * 60 + local.minute)
        assert 0 < minutes <= 90 and h * 60 + m <= menu.closes_at.hour * 60 + menu.closes_at.minute


def test_trivia_and_unclear_are_non_order_cards(planned):
    assert all(not c.items and "trivia" in c.brief for c in _by(planned, "trivia"))
    assert all(not c.items and c.expected_labels == [RouterLabel.UNKNOWN] for c in _by(planned, "unclear"))


def test_m4_batches_still_plan_identically():
    """Targets are an opt-in argument: without one, the card builder draws the same random numbers as in M4."""
    meta = json.loads((RUNS / "synth" / "m1" / "plan.json").read_text())
    saved = [json.loads(x) for x in (RUNS / "synth" / "m1" / "cards.jsonl").read_text().splitlines()]
    again = sc.plan_cards(
        meta["n"],
        seed=meta["seed"],
        batch="m1",
        generators=tuple(meta["generators"].items()),
        business_ids=tuple(sorted(meta["menu_versions"])),
    )
    assert [c.model_dump(mode="json") for c in again] == saved


def test_adding_an_item_is_a_change_only_after_confirmation(planned):
    """'Customer changes something already stated': a new item before any confirmation is just more ordering."""
    mods = _by(planned, "modify_last")
    adds = [c for c in mods if "(not asked for before)" in c.brief]
    assert adds and all(c.scenario.value == "correction_after_confirmation" for c in adds)
    assert len(adds) == sc.MODIFY_KIND_WEIGHTS["add_item"]


def test_change_kinds_follow_the_weights_and_each_is_really_in_the_card(planned):
    """Size changes and option swaps (what all three students missed on dev) get their set share."""
    mods = _by(planned, "modify_last")
    change = {c.id: c.brief.split("very last customer message, ")[1] for c in mods}

    def count(text):
        return sum(change[c.id].startswith(text) for c in mods)

    assert count("changes the size of the") == sc.MODIFY_KIND_WEIGHTS["size"]
    assert count("moves the time to") == sc.MODIFY_KIND_WEIGHTS["time"]
    assert count("removes the") == sc.MODIFY_KIND_WEIGHTS["remove_item"]
    assert count("swaps the") == sc.MODIFY_KIND_WEIGHTS["swap_item"]
    payment = [c for c in mods if change[c.id].startswith("switches the payment to")]
    assert len(payment) == sc.MODIFY_KIND_WEIGHTS["payment"]
    assert all("Pays " not in c.brief for c in payment)  # the change sentence says both payments
    menus = load_menus()
    options = [
        c for c in mods if change[c.id].startswith("asks for the") and " with " in change[c.id].split(".")[0]
    ]
    assert len(options) == sc.MODIFY_KIND_WEIGHTS["option_swap"]
    for c in options:
        assert menus[c.business_id].exclusive_groups
        assert any(
            p.substitute
            or any(
                menus[c.business_id].modifier(a).group in menus[c.business_id].exclusive_groups for a in p.add
            )
            for p in c.items
        )


def test_topup_plans_only_the_two_targets_and_open_requests_say_so():
    cards = sc.plan_targeted_cards(
        100,
        seed=20261016,
        batch="t-top",
        generators=(("claude-session/claude-opus-5-5", 1),),
        weights=sc.TOPUP_WEIGHTS,
    )
    assert Counter(_target(c) for c in cards) == sc.TOPUP_WEIGHTS
    for c in (c for c in cards if _target(c) == "offmenu_open"):
        assert "isn't on the menu" in c.brief and "hasn't answered it yet" in c.brief


def _hand_batch(tmp_path, monkeypatch):
    from orderslm.synth import run

    monkeypatch.setattr(run, "batch_dir", lambda b: tmp_path / b)
    cards = sc.plan_targeted_cards(
        6, seed=1, batch="h", generators=((run.HAND_WRITER, 1),), weights={"trivia": 1, "offmenu_open": 1}
    )
    (tmp_path / "h").mkdir()
    run._jsonl(tmp_path / "h" / "cards.jsonl", [c.model_dump(mode="json") for c in cards])
    return run, cards


def test_hand_written_chats_go_through_the_writer_checks(tmp_path, monkeypatch):
    run, cards = _hand_batch(tmp_path, monkeypatch)
    rows = [
        {"card_id": cards[0].id, "messages": [{"role": "customer", "text": "who won the 1998 world cup?"}]},
        {
            "card_id": cards[1].id,
            "messages": [
                {"role": "customer", "text": "is that $4.50?"},
                {"role": "business", "text": "It's $4.50"},
                {"role": "customer", "text": "ok"},
            ],
        },
        {
            "card_id": cards[2].id,
            "messages": [{"role": "customer", "text": "hi"}, {"role": "business", "text": "hey!"}],
        },
    ]
    run._jsonl(tmp_path / "chats.jsonl", rows)
    run.main(["import", "--batch", "h", "--file", str(tmp_path / "chats.jsonl")])
    kept = run.load_conversations("h")
    assert [k.card_id for k in kept] == [cards[0].id, cards[2].id]
    assert kept[1].repairs == ["trimmed_trailing_business_message"]
    assert all(
        k.generator == run.HAND_WRITER and k.generator_prompt_version == run.HAND_PROMPT_VERSION for k in kept
    )
    drops = run._read_jsonl(tmp_path / "h" / "gen_drops.jsonl")
    assert drops == [
        {"card_id": cards[1].id, "generator": run.HAND_WRITER, "reason": "business_states_price"}
    ]


def test_import_refuses_cards_planned_for_a_model(tmp_path, monkeypatch):
    run, cards = _hand_batch(tmp_path, monkeypatch)
    model_card = cards[0].model_copy(update={"generator": "deepseek/deepseek-flash@none"})
    run._jsonl(tmp_path / "h" / "cards.jsonl", [model_card.model_dump(mode="json")])
    run._jsonl(
        tmp_path / "chats.jsonl",
        [{"card_id": model_card.id, "messages": [{"role": "customer", "text": "hi"}]}],
    )
    with pytest.raises(SystemExit):
        run.main(["import", "--batch", "h", "--file", str(tmp_path / "chats.jsonl")])


def test_rewrite_copies_only_dropped_cards_with_new_ids(tmp_path, monkeypatch):
    run, cards = _hand_batch(tmp_path, monkeypatch)
    run._jsonl(
        tmp_path / "h" / "gen_drops.jsonl",
        [{"card_id": cards[3].id, "generator": "x", "reason": "invalid_output"}],
    )
    out = run.rewrite_cards("h", "h2", start=101, generator=run.HAND_WRITER)
    assert [c.id for c in out] == ["syn-h2-0101"]
    assert out[0].extras[0] == f"rewrite_of:{cards[3].id}" and out[0].extras[1:] == cards[3].extras
    assert out[0].brief == cards[3].brief and out[0].generator == run.HAND_WRITER


def test_label_fix_replaces_the_teacher_output_but_keeps_it(tmp_path, monkeypatch):
    from orderslm.llm.types import ChatResponse, LLMUsage

    run, _ = _hand_batch(tmp_path, monkeypatch)
    raw = {"intents": [], "order": None}
    resp = ChatResponse(
        config_id="t",
        model="t",
        text=json.dumps(raw),
        finish_reason="stop",
        usage=LLMUsage(),
        latency_ms=0,
        cost_micros=0,
        at="x",
    )
    path = tmp_path / "h" / "label" / run._slug(run.lab.TEACHER) / "syn-h-0001.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"versions": {"label_prompt": "v"}, "response": resp.model_dump(mode="json")}))
    assert run.label_record("h", "syn-h-0001") == (json.dumps(raw), "v", None)
    fix = {"label": {"intents": [1]}, "reason": "r", "fixed_by": "me"}
    (tmp_path / "h" / "label_fixes").mkdir()
    (tmp_path / "h" / "label_fixes" / "syn-h-0001.json").write_text(json.dumps(fix))
    text, version, got = run.label_record("h", "syn-h-0001")
    assert json.loads(text) == {"intents": [1]} and version == "v" and got == fix
    assert json.loads(ChatResponse.model_validate(json.loads(path.read_text())["response"]).text) == raw
