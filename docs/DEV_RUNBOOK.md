# Dev Runbook — reMarkable Weekly Notes

Headless CLI beside the Genesis Node scaffold. No HTTP services.

## Terminology

| Term | Meaning |
|------|---------|
| **Local dry-run** | `remarkable-weekly --dry-run` with fake clients; no tokens |
| **Live smoke** | Real reMarkable + Anthropic tokens; writes `weekly-notes/` |
| **Scheduled job** | Cron invoking `remarkable-weekly` on Friday evening |

## Install

```bash
cd /path/to/reMarkarble-rePorter
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# optional live reMarkable adapter:
# pip install -e ".[dev,remarkable]"
```

## Environment

Copy `.env.example` → `.env` and fill secrets:

| Variable | Default | Purpose |
|----------|---------|---------|
| `REMARKABLE_TOKEN` | (empty) | reMarkable cloud device/user token |
| `ANTHROPIC_API_KEY` | (empty) | Claude vision |
| `REMARKABLE_NOTEBOOK_NAME` | `Daily Journal` | Notebook to pull |
| `REMARKABLE_PAGE_COUNT` | `5` | Trailing pages |
| `WEEKLY_CATEGORIES` | `To-Dos,Meeting Notes,Follow-ups,Other` | Summarize taxonomy |
| `WEEKLY_NOTES_DIR` | `weekly-notes` | Output directory |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-6` | Vision-capable model ID |
| `CHUNK_MAX_HEIGHT` | `1400` | Max PNG strip height |
| `WEEKLY_NOTES_TZ` | `local` | `local` or `UTC` for filename timestamps |

Never commit `.env`.

### reMarkable token (headless)

1. Browse OS/toolchain docs at [developer.remarkable.com](https://developer.remarkable.com/) if needed — **not** required for this CLI.
2. Get an 8-character code from [my.remarkable.com/device/desktop/connect](https://my.remarkable.com/device/desktop/connect).
3. `pip install -e ".[remarkable]"` then `remarkapy init` (stores tokens in `~/.rmapi`).
4. Copy `devicetoken` into `REMARKABLE_TOKEN` in `.env`.
5. Prefer a long-lived device token for cron (not a fresh one-time code each Friday).

See README **Getting a reMarkable token** for the full walkthrough.

## Start commands

| Mode | Command | Notes |
|------|---------|-------|
| Help | `remarkable-weekly --help` | |
| Module | `python -m remarkable_weekly --help` | Same CLI |
| Dry-run (fakes) | `remarkable-weekly --dry-run --week 2026-W31` | Prints planned path; no live APIs |
| Live | `remarkable-weekly --week 2026-W31` | Requires tokens |
| Strict dates | `remarkable-weekly --week 2026-W31 --strict` | Non-zero exit on mismatches |
| Tests | `pytest -q` | No tokens required |

## Cron (Friday evening example)

```cron
# Friday 16:00 local — adjust path/venv
0 16 * * 5 cd /path/to/reMarkarble-rePorter && .venv/bin/remarkable-weekly >> /var/log/remarkable-weekly.log 2>&1
```

Or pin the week explicitly if the job runs after the ISO week rolls:

```bash
remarkable-weekly --week 2026-W31
```

## Live smoke checklist

1. `pip install -e ".[dev,remarkable]"` and populate `.env`
2. `remarkable-weekly --dry-run --week YYYY-Www` (sanity)
3. `remarkable-weekly --week YYYY-Www --pages 5`
4. Confirm new file under `weekly-notes/` matching `{YYYY-Www}_generated-{YYYY-MM-DDTHHMM}.md`
5. Open markdown; paste into Confluence Data Center **Insert → Markup**
6. Re-run same minute → expect `-2` suffix (never overwrite)

## Hard requirements

| Rule | Why |
|------|-----|
| Never commit `.env` or `~/.rmapi` | Secrets / device tokens |
| Prefer `--dry-run` / fakes in CI | No live tokens |
| Cloud auth via my.remarkable.com + `remarkapy init` | Developer Portal is for tablet OS/toolchains, not this CLI’s cloud pull |

## Symptom → fix

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `REMARKABLE_TOKEN is required` | Live run without token | Set env or use `--dry-run` |
| `remarkapy is not installed` | Optional extra missing | `pip install remarkapy` or `.[remarkable]` |
| Strict exit 1 | Date outside target week | Fix pages / use non-strict / correct `--week` |
| Empty / missing notebook | Wrong name or cloud sync | Check `REMARKABLE_NOTEBOOK_NAME` |
| Anthropic model error | Retired model ID | Update `ANTHROPIC_MODEL` per Anthropic docs |

## QA gate

Before the next feature: run `/qa_checklist` → `/code_review` → `/postmortem`.
