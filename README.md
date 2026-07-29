# reMarkarble rePorter

Headless Python CLI that turns your reMarkable **Daily Journal** into a paste-ready weekly markdown summary for Confluence.

Each run pulls the last N notebook pages, checks handwritten date headers against a target ISO week, chops tall scroll pages for vision, and asks Claude to summarize into configured categories (to-dos vs meeting notes and more). Output is a timestamped file under `weekly-notes/` — no UI, no third-party OCR, no Confluence auto-publish.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# No tokens needed — fake clients
remarkable-weekly --dry-run --week 2026-W31
pytest -q
```

## Live run

```bash
pip install -e ".[dev,remarkable]"
cp .env.example .env   # fill REMARKABLE_TOKEN and ANTHROPIC_API_KEY

remarkable-weekly --week 2026-W31
# or current ISO week:
remarkable-weekly
```

Paste the generated markdown into Confluence Data Center via **Insert → Markup**.

## Getting a reMarkable token

Official tablet / OS / toolchain docs: **[reMarkable Developer Portal](https://developer.remarkable.com/)** → [Browse documentation](https://developer.remarkable.com/).

This CLI does **not** use the on-device developer toolchain. It downloads notebooks from the **reMarkable cloud** (same sync service as the desktop/mobile apps) through [remarkapy](https://pypi.org/project/remarkapy/). You need a long-lived **device token**.

### Prerequisites

1. reMarkable account with cloud sync ([pair your tablet](https://support.remarkable.com/s/article/Pair-your-reMarkable-with-the-cloud)).
2. **Daily Journal** synced to the cloud (open it on Wi‑Fi so recent pages upload).

### One-time registration

1. Install the cloud client extras:

   ```bash
   source .venv/bin/activate
   pip install -e ".[remarkable]"
   ```

2. In a browser, sign in and open the connect page to get an **8-character one-time code**:  
   [https://my.remarkable.com/device/desktop/connect](https://my.remarkable.com/device/desktop/connect)

3. Register that code (stores tokens under `~/.rmapi` by default):

   ```bash
   remarkapy init
   # paste the one-time code when prompted
   ```

4. Copy the **device token** from `~/.rmapi` into this project’s `.env` (look for the `devicetoken` line):

   ```bash
   cp .env.example .env
   # set:
   # REMARKABLE_TOKEN=<devicetoken from ~/.rmapi>
   # ANTHROPIC_API_KEY=<from https://console.anthropic.com/>
   ```

5. Confirm the notebook is visible:

   ```bash
   remarkapy ls
   ```

6. Run a live weekly job:

   ```bash
   remarkable-weekly --week 2026-W31
   ```

Keep `~/.rmapi` and `.env` private — never commit them. Re-run `remarkapy init --force` if you need a new device token.

> **Developer Portal vs this app:** use [developer.remarkable.com](https://developer.remarkable.com/) for tablet OS, software internals, and toolchains. Use **my.remarkable.com connect + remarkapy** for cloud notebook access in this repo.

## CLI

| Flag | Purpose |
|------|---------|
| `--week YYYY-Www` | Target ISO week (default: week of today / `--as-of`) |
| `--as-of YYYY-MM-DD` | Reference date when `--week` is omitted |
| `--pages N` | Trailing pages to pull (default: 5) |
| `--strict` | Exit non-zero if any page date is missing or outside the week |
| `--dry-run` | Fake clients; print planned path; skip write |
| `--use-fakes` | Force fakes even when writing |

Also: `python -m remarkable_weekly …`

## Configuration

Copy `.env.example` → `.env` (never commit `.env`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `REMARKABLE_TOKEN` | — | reMarkable cloud token |
| `ANTHROPIC_API_KEY` | — | Claude vision |
| `REMARKABLE_NOTEBOOK_NAME` | `Daily Journal` | Notebook to pull |
| `REMARKABLE_PAGE_COUNT` | `5` | Trailing pages |
| `WEEKLY_CATEGORIES` | `To-Dos,Meeting Notes,Follow-ups,Other` | Summarize taxonomy |
| `WEEKLY_NOTES_DIR` | `weekly-notes` | Output directory |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-6` | Vision model (verify at ship) |
| `CHUNK_MAX_HEIGHT` | `1400` | Max PNG strip height |
| `WEEKLY_NOTES_TZ` | `local` | `local` or `UTC` for filenames |

## Output

Files are named so they sort chronologically and never overwrite:

```text
weekly-notes/2026-W31_generated-2026-07-31T1600.md
weekly-notes/2026-W31_generated-2026-07-31T1600-2.md   # same-minute rerun
```

## Pipeline

1. **Pull** — last N pages of the configured notebook  
2. **Validate dates** — Claude reads handwritten headers; mismatches are warned (or fail with `--strict`)  
3. **Chop** — tall pages split into page-sized image chunks  
4. **Summarize** — single Claude vision call with template-aware prompt  
5. **Write** — timestamped markdown under `weekly-notes/`

## Cron (Friday evening)

```cron
0 16 * * 5 cd /path/to/reMarkarble-rePorter && .venv/bin/remarkable-weekly >> weekly-notes/cron.log 2>&1
```

## Docs

- [Mission](docs/MISSION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Dev runbook](docs/DEV_RUNBOOK.md)

## License

MIT
