"""Domain models for the weekly notes pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class PageImage:
    index: int
    png_bytes: bytes
    width: int
    height: int


@dataclass(frozen=True)
class DateMismatch:
    page_index: int
    extracted_date: date | None
    reason: str


@dataclass(frozen=True)
class DateCheck:
    page_index: int
    extracted_date: date | None
    in_week: bool
    mismatch: DateMismatch | None = None


@dataclass
class PipelineResult:
    output_path: Path | None
    markdown: str
    mismatches: list[DateMismatch] = field(default_factory=list)
    iso_week: str = ""
    dry_run: bool = False
