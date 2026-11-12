"""When an order is for: the day and time the customer asked for, worked out and checked in code (extraction@0.5).

The model only says what was named ("tmrw", "on saturday", "at 6:30" read as 18:30 from the opening hours). The
date comes from here, counted from the business-local day of the message the customer said it in, never from a
model, and is checked against the menu (`weekly_hours`, `scheduled_orders`, docs/MENUS.md):

- tomorrow = the next day; a weekday = the first such day from the message's day, that day included (said on a
  Saturday, "saturday" is today; "next friday" is read the same way, and the summary states the date, so a
  customer who meant the week after can say so); a date = its next occurrence from that day (this month or
  year if not past, else the next); "the 31st" skips months without one; Feb 30 is no date.
- A later day needs `scheduled_orders.accepted` and at most `max_days_ahead` days.
- The day must be open (`hours_on`) and a clock time inside its hours, closing time excluded; today, not
  before the message.

ASAP and relative times ("in 20 min") are today. Tools never raise for business outcomes: a problem is a ToolErr
whose code the reply layer turns into a question (core/replies.schedule_problem).
"""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from orderslm.schema.common import Weekday
from orderslm.schema.conversation import Conversation
from orderslm.schema.extraction import DayKind, ExtractionOutput, RequestedDay, SlotState, TimeKind
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.order import Schedule, ToolErr, ToolError, ToolOk, ToolResult

SCHEDULE_VERSION = "schedule@0.1"
WEEKDAYS = list(Weekday)  # date.weekday() order: Monday first

DAY_PROBLEMS = frozenset(
    {"SCHEDULE_INVALID_DATE", "SCHEDULE_NOT_ACCEPTED", "SCHEDULE_TOO_FAR_AHEAD", "SCHEDULE_CLOSED_DAY"}
)
"""Problems with the day itself: told before asking anything else, since no time on that day can work."""


def _err(code: str, message: str, **details: object) -> ToolErr:
    return ToolErr(error=ToolError(code=code, message=message, details=details), verified_by=SCHEDULE_VERSION)


def weekday_of(d: date) -> Weekday:
    return WEEKDAYS[d.weekday()]


def resolve_day(day: RequestedDay, today: date) -> date | None:
    """The date a named day means, counted from `today` (the message's local day); None if it doesn't exist."""
    if day.kind is DayKind.tomorrow:
        return today + timedelta(days=1)
    if day.kind is DayKind.weekday:
        return today + timedelta(days=(WEEKDAYS.index(day.weekday) - today.weekday()) % 7)
    dom = day.day_of_month
    if day.month is not None:
        for year in (today.year, today.year + 1):
            try:
                d = date(year, day.month, dom)
            except ValueError:  # Feb 29 in a common year, Apr 31
                continue
            if d >= today:
                return d
        return None
    year, month = today.year, today.month
    for _ in range(12):  # "the 31st": the next month that has one
        try:
            d = date(year, month, dom)
        except ValueError:
            d = None
        if d is not None and d >= today:
            return d
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return None


def reference_time(proposal: ExtractionOutput, conversation: Conversation, tz: ZoneInfo) -> datetime:
    """Business-local time of the message the day (or else the time) was said in; else the latest customer
    message. "tmrw" is counted from when it was said."""
    rt = proposal.fulfillment.requested_time
    evidence = (rt.day.evidence if rt.day else []) or rt.evidence
    sent = {m.index: m.sent_at for m in conversation.messages}
    if evidence and evidence[0].message_index in sent:
        at = sent[evidence[0].message_index]
    else:
        at = sent[conversation.customer_indices()[-1]]
    return at.astimezone(tz)


def resolve_schedule(
    menu: MenuCatalog, proposal: ExtractionOutput, conversation: Conversation
) -> ToolResult[Schedule]:
    rt = proposal.fulfillment.requested_time
    ref = reference_time(proposal, conversation, ZoneInfo(menu.timezone))
    today = ref.date()
    day = resolve_day(rt.day, today) if rt.day else today
    if day is None:
        return _err("SCHEDULE_INVALID_DATE", f"no such date: {rt.day.raw_text}", raw_text=rt.day.raw_text)
    ahead = (day - today).days
    if ahead:
        policy = menu.scheduled_orders
        if policy is None or not policy.accepted:
            return _err("SCHEDULE_NOT_ACCEPTED", "orders for a later day aren't taken", date=day.isoformat())
        if ahead > policy.max_days_ahead:
            return _err(
                "SCHEDULE_TOO_FAR_AHEAD",
                f"orders are taken up to {policy.max_days_ahead} days ahead",
                date=day.isoformat(),
                max_days_ahead=policy.max_days_ahead,
            )
    hours = menu.hours_on(weekday_of(day))
    if hours is None:
        return _err("SCHEDULE_CLOSED_DAY", "closed that day", date=day.isoformat(), days_ahead=ahead)

    def ok(**fields: object) -> ToolOk[Schedule]:
        schedule = Schedule(
            business_id=menu.business_id,
            local_date=day,
            days_ahead=ahead,
            verified_by=SCHEDULE_VERSION,
            **fields,
        )
        return ToolOk(data=schedule, verified_by=SCHEDULE_VERSION)

    if rt.state is SlotState.provided and rt.kind is TimeKind.clock_time and rt.normalized_local:
        at = time.fromisoformat(rt.normalized_local)
        if not hours.opens_at <= at < hours.closes_at:
            return _err(
                "SCHEDULE_OUTSIDE_HOURS",
                "the time is outside that day's opening hours",
                date=day.isoformat(),
                days_ahead=ahead,
                time=at.isoformat("minutes"),
                opens_at=hours.opens_at.isoformat("minutes"),
                closes_at=hours.closes_at.isoformat("minutes"),
            )
        if not ahead and at < ref.time().replace(second=0, microsecond=0):
            return _err(
                "SCHEDULE_IN_PAST", "that time has already passed today", time=at.isoformat("minutes")
            )
        return ok(asap=False, local_time=at)
    if rt.state is SlotState.provided and rt.kind is TimeKind.relative:
        return ok(asap=False, time_text=rt.raw_text)
    if rt.state is SlotState.ambiguous or (rt.state is SlotState.provided and rt.kind is TimeKind.clock_time):
        return ok(asap=False)  # the time is still to ask (core/missing.py); the day is checked
    return ok(asap=not ahead)
