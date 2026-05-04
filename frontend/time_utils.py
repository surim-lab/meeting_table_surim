from __future__ import annotations

import calendar
from datetime import date


HOUR_OPTIONS = list(range(0, 24))
MINUTE_OPTIONS = list(range(0, 60, 10))
MAX_TIME_MINUTES = 23 * 60 + 50


def get_day_options(year: int, month: int) -> list[int]:
    _, last_day = calendar.monthrange(year, month)
    return list(range(1, last_day + 1))


def make_slots(year: int, month: int, days: list[int], start_time: str, end_time: str) -> list[dict[str, str]]:
    slots = []
    for day in sorted(days):
        slot_date = date(year, month, day).isoformat()
        slots.append(
            {
                "date": slot_date,
                "start_time": start_time,
                "end_time": end_time,
            }
        )
    return slots


def format_slot(slot: dict) -> str:
    month = int(slot["date"].split("-")[1])
    day = int(slot["date"].split("-")[2])
    return f"{month}월 {day}일 {slot['start_time']} - {slot['end_time']}"


def to_minutes(hour: int, minute: int) -> int:
    return hour * 60 + minute


def format_hm(hour: int, minute: int) -> str:
    return f"{hour:02d}:{minute:02d}"
