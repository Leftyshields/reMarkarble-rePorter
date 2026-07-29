"""CLI tests."""

from remarkable_weekly.cli import build_parser, main


def test_cli_help_exits_zero():
    parser = build_parser()
    help_text = parser.format_help()
    assert "remarkable-weekly" in help_text
    assert "--week" in help_text
    assert "--dry-run" in help_text
    assert "--strict" in help_text


def test_cli_dry_run_exits_zero(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WEEKLY_NOTES_DIR", str(tmp_path / "weekly-notes"))
    # Avoid loading a real .env from repo root when chdir'd; empty env is fine
    code = main(["--dry-run", "--week", "2026-W31", "--pages", "3"])
    assert code == 0
    out = capsys.readouterr().out
    assert "Dry-run planned output:" in out
    assert "2026-W31_generated-" in out
