"""ISO week resolution helpers."""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from typing import Iterable

_WEEK_RE = re.compile(r"^(\d{4})-W(\d{1,2})$", re.IGNORECASE)


def iso_week_dates(year: int, week: int) -> set[date]:
    """Return Mon–Sun dates for the given ISO week."""
    # ISO: week 1 is the week with the year's first Thursday
    monday = date.fromisocalendar(year, week, 1)
    return {monday + timedelta(days=i) for i in range(7)}


def format_iso_week(year: int, week: int) -> str:
    return f"{year}-W{week:02d}"


def resolve_iso_week(
    as_of: date | datetime | None = None,
    week_str: str | None = None,
) -> tuple[int, int, set[date]]:
    """
    Resolve target ISO week.

    - If week_str like '2026-W31' is given, use that week.
    - Else use the ISO week of as_of (default: today).
    Returns (year, week, set of Mon–Sun dates).
    """
    if week_str:
        m = _WEEK_RE.match(week_str.strip())
        if not m:
            raise ValueError(f"Invalid --week value: {week_str!r} (expected YYYY-Www)")
        year, week = int(m.group(1)), int(m.group(2))
        if not 1 <= week <= 53:
            raise ValueError(f"ISO week out of range: {week}")
        # Validate the week exists for that year
        try:
            date.fromisocalendar(year, week, 1)
        except ValueError as exc:
            raise ValueError(f"Invalid ISO week: {week_str}") from exc
        return year, week, iso_week_dates(year, week)

    if as_of is None:
        as_of = date.today()
    elif isinstance(as_of, datetime):
        as_of = as_of.date()

    year, week, _ = as_of.isocalendar()
    return year, week, iso_week_dates(year, week)


def dates_sorted(dates: Iterable[date]) -> list[date]:
    return sorted(dates)
