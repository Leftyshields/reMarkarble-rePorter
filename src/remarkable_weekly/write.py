"""Write non-overwriting weekly markdown files."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def build_filename(iso_week: str, generated_at: datetime) -> str:
    """
    Build filename like ``2026-W31_generated-2026-07-31T1600.md``.

    Minute precision (no seconds) per product convention.
    """
    stamp = generated_at.strftime("%Y-%m-%dT%H%M")
    return f"{iso_week}_generated-{stamp}.md"


def ensure_unique_path(directory: Path, filename: str) -> Path:
    """
    Return a path under directory that does not yet exist.

    On collision, append ``-2``, ``-3``, ... before the ``.md`` suffix.
    """
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / filename
    if not candidate.exists():
        return candidate

    stem = filename[:-3] if filename.endswith(".md") else filename
    n = 2
    while True:
        alt = directory / f"{stem}-{n}.md"
        if not alt.exists():
            return alt
        n += 1


def write_markdown(
    directory: Path,
    iso_week: str,
    markdown: str,
    generated_at: datetime,
) -> Path:
    """Write markdown to a unique path; never overwrite."""
    filename = build_filename(iso_week, generated_at)
    path = ensure_unique_path(directory, filename)
    path.write_text(markdown, encoding="utf-8")
    return path
