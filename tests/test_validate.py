"""Tests for date validation."""

from datetime import date
from io import BytesIO

from PIL import Image

from remarkable_weekly.clients.fake import FakeVisionLLM
from remarkable_weekly.models import PageImage
from remarkable_weekly.validate import collect_mismatches, validate_pages


def _page(index: int) -> PageImage:
    img = Image.new("RGB", (32, 32), (255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return PageImage(index=index, png_bytes=buf.getvalue(), width=32, height=32)


def test_validate_flags_out_of_week_dates():
    week = {date(2026, 7, 27), date(2026, 7, 28), date(2026, 7, 29)}
    pages = [_page(0), _page(1), _page(2)]
    llm = FakeVisionLLM(
        dates=[
            date(2026, 7, 27),  # ok
            date(2026, 7, 20),  # out of week
            None,  # unreadable
        ]
    )
    checks = validate_pages(pages, week, llm)
    assert checks[0].in_week is True
    assert checks[0].mismatch is None
    assert checks[1].in_week is False
    assert checks[1].mismatch is not None
    assert checks[2].in_week is False
    mismatches = collect_mismatches(checks)
    assert len(mismatches) == 2
    assert mismatches[0].extracted_date == date(2026, 7, 20)
    assert mismatches[1].extracted_date is None
