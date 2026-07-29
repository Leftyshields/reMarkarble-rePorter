# Closure — EPH-20260728-RJ01

## What shipped
Headless Python package `remarkable_weekly` (TDD) that:
- Pulls last N pages of configured notebook via `RemarkableClient` (fake + live remarkapy adapter)
- Validates handwritten dates via `VisionLLM` against target ISO week (`--strict` optional)
- Chops tall PNGs (`CHUNK_MAX_HEIGHT`)
- Summarizes with template-aware Claude prompt into categorized markdown
- Writes `weekly-notes/{YYYY-Www}_generated-{YYYY-MM-DDTHHMM}.md` without overwrite
- CLI: `remarkable-weekly` / `python -m remarkable_weekly` (`--week`, `--as-of`, `--pages`, `--strict`, `--dry-run`, `--use-fakes`)
- Docs: `docs/MISSION.md`, `docs/ARCHITECTURE.md`, `docs/DEV_RUNBOOK.md`; README product section; workflow “This repo”

## Deferred
- Live smoke with real reMarkable + Anthropic tokens
- Cron install on dev box
- Retry/backoff on API errors
- Batch Claude calls if image payload too large
- Confluence auto-publish / UI / third-party OCR (explicit non-goals)
- `git init` / GitHub remote / feedback PR (repo not yet a git repository)

## Ship commands
```bash
cd /home/brian/docker/reMarkarble-rePorter
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
# optional live: pip install -e ".[remarkable]"
cp .env.example .env   # fill REMARKABLE_TOKEN, ANTHROPIC_API_KEY
pytest -q
remarkable-weekly --dry-run --week 2026-W31
remarkable-weekly --week 2026-W31   # live
```

Cron example (Friday evening):
```cron
0 17 * * 5 cd /home/brian/docker/reMarkarble-rePorter && . .venv/bin/activate && remarkable-weekly >> weekly-notes/cron.log 2>&1
```

## Git (when ready)
```bash
git init
git add -A
git commit -m "feat: reMarkable weekly notes pipeline (EPH-20260728-RJ01)"
gh repo create Leftyshields/reMarkarble-rePorter --public --source=. --remote=origin --push
```

## Timestamp
2026-07-28T19:42:00-07:00
