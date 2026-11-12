"""Orders for another day (extraction@0.5, menu@0.7, schedule@0.1): the model names the day, code finds the date."""

from datetime import UTC, date, datetime, time, timedelta

import pytest
from pydantic import ValidationError

from orderslm.core import replies
from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.schedule import resolve_day, resolve_schedule
from orderslm.core.ticket import ticket_lines
from orderslm.eval.metrics import field_values
from orderslm.menus import load_menu
from orderslm.schema.common import Weekday
from orderslm.schema.conversation import Conversation, Message
from orderslm.schema.extraction import ExtractionOutput, RequestedDay, RequestedTime
from orderslm.schema.menu import DayHours, ScheduledOrders
from orderslm.schema.order import Schedule, ToolErr, ToolOk

from .builders import line, order

CP = load_menu("corner-patty")  # 11:00-22:00 America/New_York
P = DeterministicPricing()
WED = date(2026, 11, 11)  # a Wednesday
EV = [{"message_index": 0, "quote": "x"}]


def day(kind: str, **kw) -> dict:
    return {"kind": kind, "raw_text": kw.pop("raw_text", "x"), "evidence": EV, **kw}


def at(hhmm: str, d: dict | None = None) -> dict:
    return {"state": "provided", "kind": "clock_time", "raw_text": "at x", "normalized_local": hhmm,
            "evidence": EV, **({"day": d} if d else {})}  # fmt: skip


def chat(local: datetime, business: str = "corner-patty") -> Conversation:
    return Conversation(
        id="t-1",
        business_id=business,
        split="dev",
        source="human",
        messages=[Message(index=0, role="customer", text="x", sent_at=local)],
    )


NY_WED_1PM = datetime(2026, 11, 11, 18, 0, tzinfo=UTC)  # 13:00 in New York
SCHEDULING = CP  # takes orders up to 7 days ahead (data/menus)
TODAY_ONLY = CP.model_copy(update={"scheduled_orders": None})


def resolve(menu, time_: dict, when: datetime = NY_WED_1PM):
    return resolve_schedule(menu, order(line("L1", "cheeseburger"), time_=time_), chat(when))


# ---------------------------------------------------------------- the contract


def test_day_needs_its_fields_and_a_clock_time_or_an_open_time():
    RequestedDay.model_validate(day("weekday", weekday="sat"))
    RequestedDay.model_validate(day("date", month=11, day_of_month=20))
    RequestedDay.model_validate(day("date", day_of_month=15))  # "the 15th"
    for bad in (day("weekday"), day("tomorrow", weekday="sat"), day("date"), day("tomorrow", month=3)):
        with pytest.raises(ValidationError):
            RequestedDay.model_validate(bad)
    RequestedTime.model_validate(at("18:30", day("tomorrow")))
    RequestedTime.model_validate(
        {"state": "ambiguous", "raw_text": "tmrw", "evidence": EV, "day": day("tomorrow")}
    )
    for bad in (
        {"state": "not_mentioned", "day": day("tomorrow")},
        {"state": "provided", "kind": "asap", "raw_text": "asap", "evidence": EV, "day": day("tomorrow")},
    ):
        with pytest.raises(ValidationError):
            RequestedTime.model_validate(bad)


def test_no_day_is_left_out_of_the_json_so_older_data_is_unchanged():
    o = order(line("L1", "cheeseburger"))
    assert '"day"' not in o.model_dump_json()
    assert ExtractionOutput.model_validate_json(o.model_dump_json()) == o
    o2 = order(line("L1", "cheeseburger"), time_=at("18:30", day("tomorrow")))
    assert ExtractionOutput.model_validate_json(o2.model_dump_json()) == o2


def test_extractor_never_sees_hours_or_scheduling_policy():
    menu = SCHEDULING.model_copy(update={"weekly_hours": {Weekday.sun: None}})
    assert menu.has_reply_only_fields()
    view = menu.extractor_view()
    assert view.weekly_hours is None and view.scheduled_orders is None and not view.has_reply_only_fields()
    assert view.model_dump_json(exclude_none=True) == TODAY_ONLY.extractor_view().model_dump_json(
        exclude_none=True
    )


def test_the_scorer_counts_a_wrong_day_as_a_wrong_time():
    today = field_values(order(line("L1", "cheeseburger"), time_=at("18:30")))["time"]
    tmrw = field_values(order(line("L1", "cheeseburger"), time_=at("18:30", day("tomorrow"))))["time"]
    other_words = field_values(
        order(line("L1", "cheeseburger"), time_=at("18:30", day("tomorrow", raw_text="tomorrow")))
    )["time"]
    assert today != tmrw and tmrw == other_words


# ---------------------------------------------------------------- the date, in code


@pytest.mark.parametrize(
    ("named", "expected"),
    [
        (day("tomorrow"), date(2026, 11, 12)),
        (day("weekday", weekday="sat"), date(2026, 11, 14)),
        (day("weekday", weekday="wed"), WED),  # said on a Wednesday: today
        (day("weekday", weekday="tue"), date(2026, 11, 17)),
        (day("date", month=11, day_of_month=20), date(2026, 11, 20)),
        (day("date", month=1, day_of_month=5), date(2027, 1, 5)),  # past this year: next year
        (day("date", day_of_month=15), date(2026, 11, 15)),
        (day("date", day_of_month=3), date(2026, 12, 3)),  # past this month: next month
        (day("date", day_of_month=31), date(2026, 12, 31)),  # November has no 31st
        (day("date", month=2, day_of_month=30), None),
    ],
)
def test_resolve_day(named, expected):
    assert resolve_day(RequestedDay.model_validate(named), WED) == expected


def test_tomorrow_at_a_time_is_scheduled():
    r = resolve(SCHEDULING, at("18:30", day("tomorrow")))
    assert isinstance(r, ToolOk)
    assert (r.data.local_date, r.data.days_ahead, r.data.local_time, r.data.asap) == (
        date(2026, 11, 12), 1, time(18, 30), False,
    )  # fmt: skip


def test_the_day_counts_from_the_business_local_day_of_the_message():
    # 02:00 UTC Thursday is 21:00 Wednesday in New York: "tomorrow" is Thursday.
    r = resolve(SCHEDULING, at("12:00", day("tomorrow")), datetime(2026, 11, 12, 2, 0, tzinfo=UTC))
    assert r.data.local_date == date(2026, 11, 12)


def test_today_stays_today_and_asap():
    r = resolve(CP, {"state": "not_mentioned"})
    assert (r.data.local_date, r.data.days_ahead, r.data.asap) == (WED, 0, True)


@pytest.mark.parametrize(
    ("menu", "time_", "code"),
    [
        (TODAY_ONLY, at("18:30", day("tomorrow")), "SCHEDULE_NOT_ACCEPTED"),
        (
            CP.model_copy(update={"scheduled_orders": ScheduledOrders(accepted=False)}),
            at("18:30", day("tomorrow")),
            "SCHEDULE_NOT_ACCEPTED",
        ),
        (SCHEDULING, at("18:30", day("date", month=12, day_of_month=1)), "SCHEDULE_TOO_FAR_AHEAD"),
        (SCHEDULING, at("18:30", day("date", month=2, day_of_month=30)), "SCHEDULE_INVALID_DATE"),
        (SCHEDULING, at("23:00", day("tomorrow")), "SCHEDULE_OUTSIDE_HOURS"),
        (SCHEDULING, at("22:00"), "SCHEDULE_OUTSIDE_HOURS"),  # closing time is not open
        (SCHEDULING, at("12:30"), "SCHEDULE_IN_PAST"),  # 13:00 now
        (
            SCHEDULING.model_copy(update={"weekly_hours": {Weekday.thu: None}}),
            at("18:30", day("tomorrow")),
            "SCHEDULE_CLOSED_DAY",
        ),
    ],
)
def test_schedule_problems(menu, time_, code):
    r = resolve(menu, time_)
    assert isinstance(r, ToolErr) and r.error.code == code


def test_a_weekday_with_its_own_hours():
    menu = SCHEDULING.model_copy(
        update={"weekly_hours": {Weekday.sat: DayHours(opens_at=time(9), closes_at=time(14))}}
    )
    assert isinstance(resolve(menu, at("12:00", day("weekday", weekday="sat"))), ToolOk)
    assert resolve(menu, at("18:30", day("weekday", weekday="sat"))).error.code == "SCHEDULE_OUTSIDE_HOURS"
    assert isinstance(resolve(menu, at("18:30", day("weekday", weekday="fri"))), ToolOk)  # Friday keeps 11-22


# ---------------------------------------------------------------- what the customer and the kitchen see


def _complete(time_: dict):
    return order(line("L1", "cheeseburger"), time_=time_)


def test_summary_names_the_day_so_a_yes_confirms_a_date():
    o = _complete(at("18:30", day("tomorrow")))
    text, kind = replies.next_reply(
        SCHEDULING, o, P.quote(SCHEDULING, o), resolve(SCHEDULING, o.fulfillment.requested_time.model_dump())
    )
    assert kind == "summary"
    assert "Pickup tomorrow, Thu, Nov 12, at 6:30 PM." in text
    o = _complete(at("18:30", day("weekday", weekday="sat")))
    s = resolve(SCHEDULING, o.fulfillment.requested_time.model_dump()).data
    assert "Pickup on Sat, Nov 14 at 6:30 PM." in replies.summary(
        SCHEDULING, P.quote(SCHEDULING, o).data, o, s
    )
    o = _complete(at("18:30"))
    s = resolve(SCHEDULING, o.fulfillment.requested_time.model_dump()).data
    assert "Pickup today at 6:30 PM." in replies.summary(SCHEDULING, P.quote(SCHEDULING, o).data, o, s)


def test_ticket_says_scheduled_first_for_a_later_day():
    o = _complete(at("18:30", day("tomorrow")))
    s = resolve(SCHEDULING, o.fulfillment.requested_time.model_dump()).data
    lines = ticket_lines(SCHEDULING, P.quote(SCHEDULING, o).data, o, s)
    assert lines[0] == "SCHEDULED for tomorrow, Thu, Nov 12, at 6:30 PM, not today"
    o = _complete(at("18:30"))
    s = resolve(SCHEDULING, o.fulfillment.requested_time.model_dump()).data
    assert not ticket_lines(SCHEDULING, P.quote(SCHEDULING, o).data, o, s)[0].startswith("SCHEDULED")


def test_a_day_without_a_time_asks_the_time_on_that_day():
    o = _complete({"state": "ambiguous", "raw_text": "tmrw", "evidence": EV, "day": day("tomorrow")})
    missing = required_missing(o, SCHEDULING)
    assert [m.field.value for m in missing] == ["requested_time"]
    assert replies.template_question(missing, o, SCHEDULING) == "What time tomorrow would you like it?"
    o = _complete(
        {"state": "ambiguous", "raw_text": "sat", "evidence": EV, "day": day("weekday", weekday="sat")}
    )
    assert replies.template_question(missing, o, SCHEDULING) == "What time on Saturday would you like it?"
    o = _complete(
        {"state": "ambiguous", "raw_text": "15th", "evidence": EV, "day": day("date", day_of_month=15)}
    )
    assert replies.template_question(missing, o, SCHEDULING) == "What time on the 15th would you like it?"


def test_a_problem_with_the_day_comes_before_any_question():
    o = _complete({"state": "ambiguous", "raw_text": "tmrw", "evidence": EV, "day": day("tomorrow")})
    r = resolve(TODAY_ONLY, o.fulfillment.requested_time.model_dump())
    text, kind = replies.next_reply(TODAY_ONLY, o, P.quote(TODAY_ONLY, o), r)
    assert kind == "schedule_problem"
    assert text == "Sorry, we can only take orders for today. Would you like it today instead?"


@pytest.mark.parametrize(
    ("menu", "time_", "expected"),
    [
        (SCHEDULING, at("18:30", day("date", month=12, day_of_month=1)),
         "Sorry, we take orders up to 7 days ahead, and Tue, Dec 1 is further out. Could you pick an earlier day?"),
        (SCHEDULING.model_copy(update={"weekly_hours": {Weekday.thu: None}}), at("18:30", day("tomorrow")),
         "Sorry, we're closed tomorrow, Thu, Nov 12. Would another day work?"),
        (SCHEDULING, at("23:00", day("weekday", weekday="sat")),
         "We're open 11:00 AM to 10:00 PM on Sat, Nov 14. What time in that window works for you?"),
        (SCHEDULING, at("12:30"), "12:30 PM has already passed today. What time would you like it instead?"),
        (SCHEDULING, at("18:30", day("date", month=2, day_of_month=30, raw_text="feb 30")),
         "Sorry, I couldn't find that date (feb 30). Which day would you like it for?"),
    ],
)  # fmt: skip
def test_schedule_problem_replies(menu, time_, expected):
    o = _complete(time_)
    r = resolve(menu, time_)
    assert replies.next_reply(menu, o, P.quote(menu, o), r) == (expected, "schedule_problem")


def test_every_menu_takes_orders_up_to_a_week_ahead():
    for business in ("corner-patty", "halfmoon-pizza", "morning-crumb"):
        policy = load_menu(business).scheduled_orders
        assert policy == ScheduledOrders(accepted=True, max_days_ahead=7), business


def test_relative_time_and_asap_are_today_only():
    with pytest.raises(ValidationError):
        Schedule(
            business_id="x", local_date=WED + timedelta(days=1), days_ahead=1, asap=True, verified_by="s"
        )
