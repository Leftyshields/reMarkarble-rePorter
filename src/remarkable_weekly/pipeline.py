"""Orchestrate pull → validate → chop → summarize → write."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from remarkable_weekly.chop import chop_pages
from remarkable_weekly.clients.base import RemarkableClient, VisionLLM
from remarkable_weekly.config import Config
from remarkable_weekly.models import PipelineResult
from remarkable_weekly.pull import pull_pages
from remarkable_weekly.summarize import summarize_pages
from remarkable_weekly.validate import collect_mismatches, validate_pages
from remarkable_weekly.week import format_iso_week, resolve_iso_week
from remarkable_weekly.write import build_filename, ensure_unique_path, write_markdown


class StrictValidationError(Exception):
    """Raised when --strict is set and date mismatches are found."""

    def __init__(self, mismatches):
        self.mismatches = mismatches
        super().__init__(f"{len(mismatches)} date mismatch(es) in strict mode")


def _now(notes_tz: str) -> datetime:
    if notes_tz == "utc":
        return datetime.now(timezone.utc)
    return datetime.now().astimezone()


def planned_output_path(
    notes_dir: Path,
    iso_week: str,
    generated_at: datetime | None = None,
    notes_tz: str = "local",
) -> Path:
    """Compute the path that would be written (honoring collision uniqueness)."""
    when = generated_at or _now(notes_tz)
    filename = build_filename(iso_week, when)
    return ensure_unique_path(notes_dir, filename)


def run_pipeline(
    config: Config,
    *,
    remarkable: RemarkableClient,
    vision: VisionLLM,
    week_str: str | None = None,
    as_of=None,
    pages: int | None = None,
    strict: bool = False,
    dry_run: bool = False,
    generated_at: datetime | None = None,
) -> PipelineResult:
    """
    Run the full weekly notes pipeline with injected clients.

    When dry_run=True, still runs pull/validate/chop/summarize with the injected
    clients but skips writing; returns the planned output path.
    """
    year, week, week_dates = resolve_iso_week(as_of=as_of, week_str=week_str)
    iso_week = format_iso_week(year, week)
    page_count = pages if pages is not None else config.page_count
    when = generated_at or _now(config.notes_tz)

    page_images = pull_pages(remarkable, config.notebook_name, page_count)
    checks = validate_pages(page_images, week_dates, vision)
    mismatches = collect_mismatches(checks)

    if strict and mismatches:
        raise StrictValidationError(mismatches)

    chunks = chop_pages(
        [p.png_bytes for p in page_images],
        max_height=config.chunk_max_height,
    )
    markdown = summarize_pages(
        chunks,
        list(config.categories),
        vision,
        mismatches=mismatches,
    )

    planned = planned_output_path(config.notes_dir, iso_week, when, config.notes_tz)

    if dry_run:
        return PipelineResult(
            output_path=planned,
            markdown=markdown,
            mismatches=mismatches,
            iso_week=iso_week,
            dry_run=True,
        )

    path = write_markdown(config.notes_dir, iso_week, markdown, when)
    return PipelineResult(
        output_path=path,
        markdown=markdown,
        mismatches=mismatches,
        iso_week=iso_week,
        dry_run=False,
    )
