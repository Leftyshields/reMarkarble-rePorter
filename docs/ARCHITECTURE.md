# Architecture — reMarkable Weekly Notes

## Overview

`remarkable_weekly` is a **headless Python CLI** that pulls the last N pages of a reMarkable notebook (default: "Daily Journal"), validates handwritten dates against a target ISO week via Claude vision, chops tall page images into chunks, summarizes into categorized markdown, and writes a non-overwriting timestamped file under `weekly-notes/`. There is **no HTTP server** in v1.

## Module layout

```
src/remarkable_weekly/
  cli.py              # argparse entry (remarkable-weekly / python -m)
  config.py           # env-based Config
  models.py           # PageImage, DateCheck, DateMismatch, PipelineResult
  week.py             # ISO week resolution (Mon–Sun)
  pull.py             # fetch last N pages
  validate.py         # date extraction checks
  chop.py             # tall PNG → horizontal strips (Pillow)
  summarize.py        # prompt + VisionLLM summarize
  write.py            # unique weekly-notes/{YYYY-Www}_generated-….md
  pipeline.py         # orchestrate stages (DI clients)
  clients/
    base.py           # RemarkableClient, VisionLLM interfaces
    fake.py           # fakes for tests / --dry-run
    remarkable.py     # remarkapy + pypdfium2 PDF→PNG (optional live)
    anthropic_llm.py  # Anthropic Messages vision adapter
weekly-notes/         # output markdown (gitkept)
```

## Entry points (CLI only — no HTTP)

| Environment | Entry | How to run | Output |
|-------------|-------|------------|--------|
| Local / cron | `remarkable_weekly.cli:main` | `remarkable-weekly` or `python -m remarkable_weekly` | `weekly-notes/*.md` |
| Dry-run / CI | same + `--dry-run` | uses Fake clients; prints planned path | no write |

**Flags:** `--week YYYY-Www`, `--as-of YYYY-MM-DD`, `--pages N`, `--strict`, `--dry-run`, `--use-fakes`.

## Pipeline stages

1. **Pull** — `RemarkableClient.fetch_last_pages(notebook, N)`
2. **Validate** — per-page `VisionLLM.extract_date`; mismatches warn (or fail with `--strict`)
3. **Chop** — split PNGs taller than `CHUNK_MAX_HEIGHT` (default 1400)
4. **Summarize** — single `VisionLLM.summarize(chunks, categories)` with template (quadrants→to-dos, lined→meeting notes)
5. **Write** — `{ISO_WEEK}_generated-{YYYY-MM-DDTHHMM}.md`; collision suffixes `-2`, `-3`, …

## Security

- Secrets only via env / `.env` (never committed): `REMARKABLE_TOKEN`, `ANTHROPIC_API_KEY`
- No network in unit tests; fakes satisfy pytest without tokens

## External services

| Service | Usage |
|---------|--------|
| reMarkable cloud (remarkapy) | Notebook download / PDF export |
| Anthropic Messages API | Handwritten date extract + vision summarize |
| Pillow / pypdfium2 | Image chop / PDF→PNG |
