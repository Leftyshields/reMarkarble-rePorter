"""Tests for markdown write / unique paths."""

from datetime import datetime
from pathlib import Path

from remarkable_weekly.write import build_filename, ensure_unique_path, write_markdown


def test_build_filename():
    name = build_filename("2026-W31", datetime(2026, 7, 31, 16, 0))
    assert name == "2026-W31_generated-2026-07-31T1600.md"


def test_write_never_overwrites(tmp_path: Path):
    when = datetime(2026, 7, 31, 16, 0)
    p1 = write_markdown(tmp_path, "2026-W31", "first\n", when)
    p2 = write_markdown(tmp_path, "2026-W31", "second\n", when)
    assert p1.name == "2026-W31_generated-2026-07-31T1600.md"
    assert p2.name == "2026-W31_generated-2026-07-31T1600-2.md"
    assert p1.read_text(encoding="utf-8") == "first\n"
    assert p2.read_text(encoding="utf-8") == "second\n"
    assert p1 != p2


def test_ensure_unique_path_suffix_chain(tmp_path: Path):
    base = "2026-W31_generated-2026-07-31T1600.md"
    (tmp_path / base).write_text("a")
    (tmp_path / "2026-W31_generated-2026-07-31T1600-2.md").write_text("b")
    path = ensure_unique_path(tmp_path, base)
    assert path.name == "2026-W31_generated-2026-07-31T1600-3.md"
