"""End-to-end pipeline tests with fakes."""

import re
from datetime import date, datetime
from pathlib import Path

import pytest

from remarkable_weekly.clients.fake import FakeRemarkableClient, FakeVisionLLM
from remarkable_weekly.config import Config
from remarkable_weekly.pipeline import StrictValidationError, run_pipeline


def test_pipeline_end_to_end_writes_markdown(tmp_path: Path):
    week_dates = [
        date(2026, 7, 27),
        date(2026, 7, 28),
        date(2026, 7, 29),
        date(2026, 7, 30),
        date(2026, 7, 31),
    ]
    cfg = Config(notes_dir=tmp_path, page_count=5, chunk_max_height=1400)
    remarkable = FakeRemarkableClient()
    vision = FakeVisionLLM(
        dates=week_dates,
        summary="# Weekly Notes\n\n## To-Dos\n- ship it\n",
    )
    result = run_pipeline(
        cfg,
        remarkable=remarkable,
        vision=vision,
        week_str="2026-W31",
        generated_at=datetime(2026, 7, 31, 16, 0),
    )
    assert result.output_path is not None
    assert result.output_path.exists()
    assert re.match(
        r"2026-W31_generated-2026-07-31T1600\.md",
        result.output_path.name,
    )
    text = result.output_path.read_text(encoding="utf-8")
    assert "To-Dos" in text
    assert "ship it" in text
    assert remarkable.last_notebook == "Daily Journal"
    assert remarkable.last_page_count == 5
    assert not result.mismatches


def test_pipeline_strict_raises_on_mismatch(tmp_path: Path):
    cfg = Config(notes_dir=tmp_path, page_count=2)
    remarkable = FakeRemarkableClient()
    vision = FakeVisionLLM(dates=[date(2020, 1, 1), date(2020, 1, 2)])
    with pytest.raises(StrictValidationError):
        run_pipeline(
            cfg,
            remarkable=remarkable,
            vision=vision,
            week_str="2026-W31",
            strict=True,
        )


def test_pipeline_dry_run_skips_write(tmp_path: Path):
    cfg = Config(notes_dir=tmp_path, page_count=2)
    remarkable = FakeRemarkableClient()
    vision = FakeVisionLLM(
        dates=[date(2026, 7, 27), date(2026, 7, 28)],
        summary="## To-Dos\n- x\n",
    )
    result = run_pipeline(
        cfg,
        remarkable=remarkable,
        vision=vision,
        week_str="2026-W31",
        dry_run=True,
        generated_at=datetime(2026, 7, 31, 16, 0),
    )
    assert result.dry_run is True
    assert result.output_path is not None
    assert "2026-W31_generated" in result.output_path.name
    # dry-run must not create the markdown file
    assert not result.output_path.exists() or result.output_path.suffix != ".md" or (
        # ensure_unique_path may mkdir but not write
        not any(tmp_path.glob("*.md"))
    )
    assert not any(tmp_path.glob("*.md"))
