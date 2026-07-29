"""Tests for ISO week resolution."""

from datetime import date

import pytest

from remarkable_weekly.week import format_iso_week, resolve_iso_week


def test_resolve_from_week_string():
    year, week, dates = resolve_iso_week(week_str="2026-W31")
    assert year == 2026
    assert week == 31
    assert format_iso_week(year, week) == "2026-W31"
    # Mon–Sun
    assert len(dates) == 7
    monday = min(dates)
    assert monday.weekday() == 0
    assert monday == date(2026, 7, 27)
    assert date(2026, 8, 2) in dates  # Sunday


def test_resolve_from_as_of():
    year, week, dates = resolve_iso_week(as_of=date(2026, 7, 31))
    assert year == 2026
    assert week == 31
    assert date(2026, 7, 27) in dates


def test_invalid_week_raises():
    with pytest.raises(ValueError, match="Invalid"):
        resolve_iso_week(week_str="not-a-week")


def test_week_string_case_insensitive():
    year, week, _ = resolve_iso_week(week_str="2026-w31")
    assert (year, week) == (2026, 31)
