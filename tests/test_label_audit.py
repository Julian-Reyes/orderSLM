"""Label audit (spec §11d): what the providers see, and scoring of intents, false alarms and planted catches."""

from orderslm.eval import label_audit as la
from orderslm.interfaces.decision import Answer, DecisionResponse, QuestionType


def _resp(request, intent=None, order_ok=True):
    answers = {}
    for q in request.questions:
        if q.type is QuestionType.choice:
            answers[q.name] = Answer(name=q.name, type=q.type, choice=intent or q.options[0].id)
        else:
            answers[q.name] = Answer(
                name=q.name, type=q.type, boolean=order_ok, probabilities={"true": float(order_ok)}
            )
    return {
        "response": DecisionResponse(provider="fake", model="m", answers=answers, latency_ms=1).model_dump(
            mode="json"
        )
    }


def test_requests_show_the_order_in_words_and_ask_every_customer_message():
    jobs = la.dev_jobs()
    gold = next(j for j in jobs if j["id"] == "a-dev-020")
    req = gold["request"]
    assert (
        "2 × Cheeseburger: no Pickles" in req.input
        and "Fulfillment: delivery to 200 park ave 5th fl" in req.input
    )
    assert [q.name for q in req.questions][-1] == "order_ok"
    assert len(req.questions) - 1 == len(gold["intents"])
    planted = [j for j in jobs if j["kind"] == "planted"]
    assert planted and all([q.name for q in j["request"].questions] == ["order_ok"] for j in planted)
    assert all(
        "price" not in j["request"].input.lower() and "$" not in j["request"].input.split("recorded")[1]
        for j in planted
    )


def test_score_counts_agreement_false_alarms_and_catches():
    jobs = [j for j in la.dev_jobs() if j["id"].startswith("a-dev-020")]
    gold = jobs[0]
    responses = {"fake": {}}
    for j in jobs:
        if j["kind"] == "gold":
            responses["fake"][j["id"]] = _resp(j["request"], intent="PLACE_ORDER", order_ok=True)
        else:  # catch every planted mistake except one
            responses["fake"][j["id"]] = _resp(j["request"], order_ok=j is jobs[1])
    m = la.score(jobs, responses)["fake"]
    expected = sum(p == "PLACE_ORDER" for p, _ in gold["intents"].values())
    assert m["intent_agree_primary"] == expected and m["intent_messages"] == len(gold["intents"])
    assert m["order_flagged"] == 0 and m["orders_expected_ok"] == 1
    planted = len(jobs) - 1
    assert sum(v["caught"] for v in m["planted"].values()) == planted - 1
