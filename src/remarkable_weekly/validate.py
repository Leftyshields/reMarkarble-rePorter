"""Validate handwritten page dates against the target ISO week."""

from __future__ import annotations

from datetime import date

from remarkable_weekly.clients.base import VisionLLM
from remarkable_weekly.models import DateCheck, DateMismatch, PageImage


def validate_pages(
    pages: list[PageImage],
    week_dates: set[date],
    llm: VisionLLM,
) -> list[DateCheck]:
    """
    For each page, extract date via LLM and check membership in week_dates.

    Unreadable dates and out-of-week dates become mismatches.
    """
    checks: list[DateCheck] = []
    for page in pages:
        extracted = llm.extract_date(page.png_bytes)
        if extracted is None:
            mismatch = DateMismatch(
                page_index=page.index,
                extracted_date=None,
                reason="unreadable or missing handwritten date",
            )
            checks.append(
                DateCheck(
                    page_index=page.index,
                    extracted_date=None,
                    in_week=False,
                    mismatch=mismatch,
                )
            )
            continue

        if extracted in week_dates:
            checks.append(
                DateCheck(
                    page_index=page.index,
                    extracted_date=extracted,
                    in_week=True,
                    mismatch=None,
                )
            )
        else:
            mismatch = DateMismatch(
                page_index=page.index,
                extracted_date=extracted,
                reason=f"date {extracted.isoformat()} not in target week",
            )
            checks.append(
                DateCheck(
                    page_index=page.index,
                    extracted_date=extracted,
                    in_week=False,
                    mismatch=mismatch,
                )
            )
    return checks


def collect_mismatches(checks: list[DateCheck]) -> list[DateMismatch]:
    return [c.mismatch for c in checks if c.mismatch is not None]
