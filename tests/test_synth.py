"""M4 synthetic data: label contract, scenario cards, generator parsing, labeling checks, dedup, the CLI."""

import inspect
import json
from collections import Counter

import pytest
from pydantic import ValidationError

from orderslm.core.finalize import finalize_order
from orderslm.eval.dataset import load_eval_split
from orderslm.extractors.teacher import portable_schema
from orderslm.llm.types import ChatResponse, LLMUsage
from orderslm.menus import load_menu, load_menus
from orderslm.schema.annotation import Scenario
from orderslm.schema.conversation import Role, Split
from orderslm.schema.extraction import DecisionState, ExtractionOutput, MissingReason
from orderslm.schema.label import AmbiguityFlag, MessageIntent, ModelOrder, TeacherLabel
from orderslm.schema.routing import LABEL_DESCRIPTIONS, RouterLabel
from orderslm.schema.synthetic import GeneratedChat, PlannedItem
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate as gen
from orderslm.synth import label as lab
from orderslm.synth import run
from orderslm.synth.dedup import near_duplicates

DEV = load_eval_split(Split.dev)
DEV_ORDERS = [ac for ac in DEV if ac.gold_extraction is not None]
CARDS = synth_cards.plan_cards(500, seed=7, batch="t1")


def _key(o: ExtractionOutput) -> list[tuple[str, str, str]]:
    return sorted((m.field.value, m.reason.value, m.line_id or "") for m in o.missing_or_ambiguous)


def model_order_from_gold(gold: ExtractionOutput) -> ModelOrder:
    """What a teacher following teacher-label@0.1 would output for this gold: no missing list or question, a yes
    to an incomplete summary as plain `confirmed`, and only the two text judgments as flags."""
    data = gold.model_dump(
        mode="json", exclude={"schema_version", "missing_or_ambiguous", "clarification_question"}
    )
    if gold.customer_decision.agreed_while_incomplete:
        data["customer_decision"] = {
            **data["customer_decision"],
            "state": "confirmed",
            "agreed_while_incomplete": False,
        }
    data["ambiguity_flags"] = [
        {"field": m.field.value, "line_id": m.line_id}
        for m in gold.missing_or_ambiguous
        if m.reason is MissingReason.ambiguous and m.field.value in ("item_menu_match", "item_variant")
    ]
    return ModelOrder.model_validate(data)


# ---------------------------------------------------------------- contract


def test_label_contract_rebuilds_every_dev_gold():
    """Gold → the label contract → finalize gives back gold's missing list and decision, for every dev order."""
    for ac in DEV_ORDERS:
        gold = ac.gold_extraction
        out = finalize_order(model_order_from_gold(gold), load_menu(ac.conversation.business_id))
        assert _key(out) == _key(gold), ac.conversation.id
        assert out.customer_decision.state == gold.customer_decision.state, ac.conversation.id
        assert out.customer_decision.agreed_while_incomplete == gold.customer_decision.agreed_while_incomplete


def test_model_outputs_have_no_price_fields():
    for model in (TeacherLabel, GeneratedChat):
        text = json.dumps(portable_schema(model)).lower()
        for word in ("price", "total", "fee", 'cents":'):
            assert f'"{word}' not in text, (model.__name__, word)
    assert "missing_or_ambiguous" not in json.dumps(portable_schema(TeacherLabel))
    assert "clarification_question" not in json.dumps(portable_schema(TeacherLabel))


def test_ambiguity_flags_and_intents_are_validated():
    gold = next(ac.gold_extraction for ac in DEV_ORDERS if ac.gold_extraction.items[0].menu_item_id)
    base = model_order_from_gold(gold).model_dump(mode="json")
    line = gold.items[0].line_id
    with pytest.raises(ValidationError, match="unknown line"):
        ModelOrder.model_validate({**base, "ambiguity_flags": [{"field": "item_variant", "line_id": "L99"}]})
    with pytest.raises(ValidationError, match="unmatched_text"):
        ModelOrder.model_validate(
            {**base, "ambiguity_flags": [{"field": "item_menu_match", "line_id": line}]}
        )
    with pytest.raises(ValidationError):
        AmbiguityFlag(field="payment_method", line_id="L1")
    with pytest.raises(ValidationError, match="UNKNOWN"):
        MessageIntent(message_index=0, primary=RouterLabel.UNKNOWN, secondary=RouterLabel.SMALL_TALK)
    with pytest.raises(ValidationError, match="differ"):
        MessageIntent(message_index=0, primary=RouterLabel.PLACE_ORDER, secondary=RouterLabel.PLACE_ORDER)


def test_label_prompt_carries_the_label_descriptions_and_no_missing_list():
    text = lab.prompt_text()
    assert "{label_descriptions}" not in text
    for label, desc in LABEL_DESCRIPTIONS.items():
        assert f"`{label.value}`: {desc}" in text
    assert "missing_or_ambiguous" not in text and "clarification_question" not in text


# ---------------------------------------------------------------- cards


def test_cards_are_deterministic_and_split_exactly_across_generators():
    again = synth_cards.plan_cards(500, seed=7, batch="t1")
    assert [c.model_dump() for c in again] == [c.model_dump() for c in CARDS]
    assert Counter(c.generator for c in CARDS) == {
        "deepseek/deepseek-flash@none": 200,
        "google/gemini-3.1-flash-lite@minimal": 200,
        "anthropic/claude-haiku-5-5@off-low": 100,
    }
    # each scenario is spread over the generators, not given to one
    for scenario in {c.scenario for c in CARDS}:
        mine = [c for c in CARDS if c.scenario is scenario]
        if len(mine) >= 5:
            assert len({c.generator for c in mine}) == 3, scenario


def _check_planned(p: PlannedItem, menu) -> None:
    if p.off_menu_text:
        assert menu.item(p.off_menu_text) is None
        return
    ids = p.halves or [p.menu_item_id]
    for i in ids:
        item = menu.item(i)
        assert item is not None and item.available
        if p.variant_id:
            assert item.variant(p.variant_id) is not None
    item = menu.item(ids[0])
    allowed = item.allowed_modifier_ids
    assert set(p.remove) <= set(item.ingredient_ids)
    assert set(p.add) <= set(item.addon_ids)
    for old, new in p.substitute.items():
        assert old in item.ingredient_ids and new in allowed
    for slot_id, choice in p.combo.items():
        slot = next(s for s in item.combo_slots if s.id == slot_id)
        assert choice in slot.choices
    assert "espresso_shot" not in p.remove


def test_cards_use_only_training_menus_and_real_menu_ids():
    menus = load_menus(include_held_out=True)
    assert all(not menus[c.business_id].held_out for c in CARDS)
    for c in CARDS:
        menu = menus[c.business_id]
        for p in c.items + ([c.first_ask] if c.first_ask else []):
            _check_planned(p, menu)
        plan = synth_cards.PLANS[c.scenario]
        assert bool(c.items) == plan.order, c.id
        assert set(plan.labels) <= set(c.expected_labels)
        if plan.menus:
            assert c.business_id in plan.menus
        if not menu.delivery.available:
            assert c.fulfillment != "delivery"


def test_cards_are_built_without_source_a():
    """Source A (cards, chats, personas) is evaluation data only and never feeds synthetic generation."""
    for module in (synth_cards, gen, lab, run):
        src = inspect.getsource(module)
        assert "orderslm.data.cards" not in src and "data/dev/cards" not in src
    from orderslm.data import cards as source_a

    assert not set(synth_cards.PERSONAS) & set(source_a.PERSONAS)


def test_generator_sees_no_prices_or_ids():
    for c in CARDS[:60]:
        menu = load_menu(c.business_id)
        req = gen.build_request(c, menu)
        user = req.messages[0].content
        assert "$" not in user and not gen.PRICE.search(user)
        assert "price" not in gen.menu_view(menu).lower()
        for item in menu.items:
            assert f"{item.base_price_cents / 100:.2f}" not in user
        for item in menu.items:
            if "_" in item.id:
                assert item.id not in user


# ---------------------------------------------------------------- generator output


def _chat(*msgs: tuple[str, str]) -> str:
    return json.dumps({"messages": [{"role": r, "text": t} for r, t in msgs]})


def test_generated_chat_becomes_a_synthetic_conversation():
    card = CARDS[0]
    sc, reason = gen.to_conversation(
        card,
        "```json\n" + _chat(("customer", "hey"), ("business", "hi!"), ("customer", "2 lattes pls")) + "\n```",
    )
    assert reason is None
    conv = sc.conversation
    assert conv.split is Split.synthetic and conv.id == card.id and sc.generator == card.generator
    assert [m.role for m in conv.messages] == [Role.customer, Role.business, Role.customer]
    assert conv.messages[0].sent_at == card.start_at
    assert all(a.sent_at < b.sent_at for a, b in zip(conv.messages, conv.messages[1:], strict=False))
    again, _ = gen.to_conversation(
        card, _chat(("customer", "hey"), ("business", "hi!"), ("customer", "2 lattes pls"))
    )
    assert again.conversation == conv  # timestamps are seeded by the card


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("not json", "invalid_output"),
        (_chat(("business", "hi! what can I get you?")), "no_customer_message"),
        (
            _chat(("customer", "a coke"), ("business", "that's $2.50"), ("customer", "ok")),
            "business_states_price",
        ),
        (_chat(("customer", "a coke"), ("business", "3 bucks"), ("customer", "ok")), "business_states_price"),
        (json.dumps({"messages": [{"role": "customer", "text": "x", "price": 1}]}), "invalid_output"),
    ],
)
def test_generated_chat_drops(text, reason):
    sc, got = gen.to_conversation(CARDS[0], text)
    assert sc is None and got.startswith(reason)


def test_trailing_business_messages_are_trimmed_and_logged():
    sc, reason = gen.to_conversation(
        CARDS[0], _chat(("customer", "a coke"), ("business", "sure!"), ("business", "anything else?"))
    )
    assert reason is None
    assert [m.text for m in sc.conversation.messages] == ["a coke"]
    assert sc.repairs == ["trimmed_trailing_business_message"] * 2


def test_cards_pick_varied_addresses_and_never_repeat_an_item():
    addresses = [c.address for c in CARDS if c.address]
    assert len(addresses) > 50 and len(set(addresses)) == len(addresses)
    assert all(c.address in c.brief for c in CARDS if c.address)
    assert all(c.fulfillment == "delivery" for c in CARDS if c.address)
    for c in CARDS:
        ids = [p.menu_item_id for p in c.items if p.menu_item_id]
        assert len(ids) == len(set(ids)), c.id


# ---------------------------------------------------------------- labels


def _gold_label_json(ac) -> str:
    intents = [
        {"message_index": r.message_index, "primary": r.decision.primary.value, "secondary": None}
        for r in ac.gold_routing
    ]
    return json.dumps(
        {"intents": intents, "order": model_order_from_gold(ac.gold_extraction).model_dump(mode="json")}
    )


def test_parse_label_accepts_gold_and_drops_broken_labels():
    ac = next(a for a in DEV_ORDERS if len(a.conversation.customer_indices()) >= 2)
    conv, menu = ac.conversation, load_menu(ac.conversation.business_id)
    lc, reason = lab.parse_label(_gold_label_json(ac), conv, menu, "fake/teacher")
    assert reason is None and lc.extraction is not None
    assert _key(lc.extraction) == _key(ac.gold_extraction)

    data = json.loads(_gold_label_json(ac))
    short = {**data, "intents": data["intents"][:-1]}
    assert lab.parse_label(json.dumps(short), conv, menu, "t")[1].startswith("intents_mismatch")
    priced = {**data, "order": {**data["order"], "total_cents": 999}}
    assert lab.parse_label(json.dumps(priced), conv, menu, "t")[1].startswith("invalid_contract")
    bad_quote = json.loads(json.dumps(data))
    bad_quote["order"]["items"][0]["evidence"][0]["quote"] = "this text is not in the chat"
    assert lab.parse_label(json.dumps(bad_quote), conv, menu, "t")[1].startswith("check_failed")


def test_label_citing_a_business_message_is_dropped():
    ac = next(
        a
        for a in DEV_ORDERS
        if any(m.role is Role.business for m in a.conversation.messages) and a.gold_extraction.items
    )
    biz = next(m for m in ac.conversation.messages if m.role is Role.business)
    data = json.loads(_gold_label_json(ac))
    data["order"]["items"][0]["evidence"] = [{"message_index": biz.index, "quote": biz.text[:20]}]
    lc, reason = lab.parse_label(
        json.dumps(data), ac.conversation, load_menu(ac.conversation.business_id), "t"
    )
    assert lc is None and "EVIDENCE_NOT_CUSTOMER" in reason


def test_no_order_chat_is_stored_as_null():
    ac = next(a for a in DEV if a.gold_extraction is None)
    empty = ExtractionOutput.empty()
    order = ModelOrder.model_validate(
        empty.model_dump(
            mode="json", exclude={"schema_version", "missing_or_ambiguous", "clarification_question"}
        )
    )
    intents = [
        {"message_index": i, "primary": "SMALL_TALK", "secondary": None}
        for i in ac.conversation.customer_indices()
    ]
    text = json.dumps({"intents": intents, "order": order.model_dump(mode="json")})
    lc, reason = lab.parse_label(text, ac.conversation, load_menu(ac.conversation.business_id), "t")
    assert reason is None and lc.extraction is None


def _plain(ac) -> bool:
    return all(
        x.menu_item_id and not x.modifications and not x.combo_selections for x in ac.gold_extraction.items
    )


def test_card_agreement_flags_a_different_order():
    ac = next(a for a in DEV_ORDERS if a.conversation.business_id == "corner-patty" and _plain(a))
    menu = load_menu("corner-patty")
    card = next(c for c in CARDS if c.business_id == "corner-patty" and c.scenario is Scenario.simple_order)
    lc, reason = lab.parse_label(_gold_label_json(ac), ac.conversation, menu, "t")
    assert reason is None
    planned = [
        PlannedItem(menu_item_id=x.menu_item_id, quantity=x.quantity or 1, variant_id=x.variant_id)
        for x in lc.extraction.items
    ]
    labels = list(dict.fromkeys(i.primary for i in lc.intents))
    same = card.model_copy(update={"items": planned, "expected_labels": labels})
    assert lab.card_agreement(same, lc, menu)["flags"] == []
    other = same.model_copy(update={"items": [PlannedItem(menu_item_id="lemonade", quantity=7)]})
    assert lab.card_agreement(other, lc, menu)["flags"] == ["items"]
    more = same.model_copy(update={"expected_labels": [*labels, RouterLabel.REFUND_REQUEST]})
    assert lab.card_agreement(more, lc, menu)["missing_labels"] == ["REFUND_REQUEST"]
    if lc.extraction.customer_decision.state is not DecisionState.cancelled:
        cancel = same.model_copy(update={"scenario": Scenario.cancellation})
        assert lab.card_agreement(cancel, lc, menu)["flags"] == ["decision"]


# ---------------------------------------------------------------- dedup


def test_near_duplicates_within_batch_and_against_dev():
    a, _ = gen.to_conversation(
        CARDS[0], _chat(("customer", "can i get two cheeseburgers and a large fries for pickup"))
    )
    b, _ = gen.to_conversation(
        CARDS[1], _chat(("customer", "can i get two cheeseburgers and a large fries for pickup"))
    )
    c, _ = gen.to_conversation(CARDS[2], _chat(("customer", "one latte with oat milk please, card")))
    dev = DEV[0].conversation
    d, _ = gen.to_conversation(
        CARDS[3],
        json.dumps(
            {
                "messages": [
                    {
                        "role": "customer",
                        "text": " ".join(m.text for m in dev.messages if m.role is Role.customer),
                    }
                ]
            }
        ),
    )
    dupes = near_duplicates([x.conversation for x in (a, b, c, d)], against=[dev])
    assert set(dupes) == {b.conversation.id, d.conversation.id}
    assert dupes[b.conversation.id][0] == a.conversation.id


# ---------------------------------------------------------------- CLI, end to end with a fake model


class _FakeClient:
    """Answers generator calls with a one-message small-talk chat and label calls with a matching label."""

    def __init__(self, config_id: str):
        self.config_id = config_id

    def complete(self, request):
        if request.schema_name == "synthetic_chat":
            text = _chat(("customer", f"hi there, just saying thanks {len(request.messages[0].content)}"))
        else:
            empty = ExtractionOutput.empty().model_dump(
                mode="json", exclude={"schema_version", "missing_or_ambiguous", "clarification_question"}
            )
            text = json.dumps(
                {
                    "intents": [{"message_index": 0, "primary": "SMALL_TALK", "secondary": None}],
                    "order": {**empty, "ambiguity_flags": []},
                }
            )
        return ChatResponse(
            config_id=self.config_id, model="fake", text=text, finish_reason="stop",
            usage=LLMUsage(input_tokens=1000, output_tokens=100), latency_ms=5.0, cost_micros=150,
            at="2026-10-16T12:00:00+00:00",
        )  # fmt: skip


def test_cli_plan_generate_label_report(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(run, "batch_dir", lambda batch: tmp_path / batch)
    monkeypatch.setattr(run, "make_client", lambda cid, cache_mode=None: _FakeClient(cid))
    assert run.main(["plan", "--batch", "x", "--n", "10"]) == 0
    assert run.main(["plan", "--batch", "x", "--n", "10"]) == 2  # never overwrites silently
    assert run.main(["generate", "--batch", "x", "--limit", "1"]) == 0  # estimate only
    assert not (tmp_path / "x" / "gen").exists()
    assert run.main(["generate", "--batch", "x", "--limit", "1", "--yes"]) == 0
    convs = run.load_conversations("x")
    assert len(convs) == 3 and {c.generator for c in convs} == set(dict(synth_cards.GENERATORS))
    assert run.main(["label", "--batch", "x", "--yes"]) == 0
    labels = run._read_jsonl(tmp_path / "x" / "labels.jsonl")
    assert len(labels) == 3 and all(r["extraction"] is None for r in labels)
    assert run.main(["report", "--batch", "x"]) == 0
    summary = json.loads((tmp_path / "x" / "summary.json").read_text())
    for g, row in summary["by_generator"].items():
        assert row["kept"] == 1 and row["labeled"] == 1, g
        assert row["generation_usage"]["cost_micros"] == 150
    calls = sorted((tmp_path / "x" / "calls").iterdir())
    assert [json.loads(p.read_text())["actual_cost_micros"] for p in calls] == [450, 450]


def test_cli_refuses_over_two_dollars(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "batch_dir", lambda batch: tmp_path / batch)
    monkeypatch.setattr(run, "make_client", lambda cid, cache_mode=None: pytest.fail("no call expected"))
    monkeypatch.setattr(run, "_estimate", lambda *a: 3_000_000)
    run.main(["plan", "--batch", "x", "--n", "5"])
    assert run.main(["generate", "--batch", "x", "--yes"]) == 2
