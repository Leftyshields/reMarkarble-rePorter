"""CLI entry: remarkable-weekly / python -m remarkable_weekly."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from remarkable_weekly.clients.fake import FakeRemarkableClient, FakeVisionLLM
from remarkable_weekly.config import load_config
from remarkable_weekly.pipeline import StrictValidationError, run_pipeline
from remarkable_weekly.week import format_iso_week, resolve_iso_week


def _parse_as_of(raw: str | None) -> date | None:
    if not raw:
        return None
    return date.fromisoformat(raw)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="remarkable-weekly",
        description=(
            "Pull reMarkable Daily Journal pages, validate dates, chop tall pages, "
            "summarize via Claude vision, write timestamped weekly markdown."
        ),
    )
    p.add_argument(
        "--week",
        metavar="YYYY-Www",
        help="Target ISO week (e.g. 2026-W31). Default: week of --as-of / today.",
    )
    p.add_argument(
        "--as-of",
        metavar="YYYY-MM-DD",
        help="Reference date for ISO week when --week is omitted.",
    )
    p.add_argument(
        "--pages",
        type=int,
        default=None,
        help="Number of trailing notebook pages to pull (default from env/config).",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any page date is missing or outside the target week.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Run pipeline with fake clients (no live tokens); print planned "
            "output path and skip writing the markdown file."
        ),
    )
    p.add_argument(
        "--use-fakes",
        action="store_true",
        help="Force fake reMarkable + vision clients (useful for local demos).",
    )
    return p


def _build_live_clients(config):
    from remarkable_weekly.clients.anthropic_llm import AnthropicVisionLLM
    from remarkable_weekly.clients.remarkable import RemarkableCloudClient

    if not config.remarkable_token:
        raise SystemExit("REMARKABLE_TOKEN is required for live runs (or pass --dry-run / --use-fakes)")
    if not config.anthropic_api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required for live runs (or pass --dry-run / --use-fakes)")

    remarkable = RemarkableCloudClient(config.remarkable_token)
    vision = AnthropicVisionLLM(config.anthropic_api_key, model=config.anthropic_model)
    return remarkable, vision


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config()

    as_of = _parse_as_of(args.as_of)
    use_fakes = args.dry_run or args.use_fakes

    if use_fakes:
        year, week, week_dates = resolve_iso_week(as_of=as_of, week_str=args.week)
        # Seed fake dates inside the target week so dry-run validates cleanly
        week_list = sorted(week_dates)
        remarkable = FakeRemarkableClient()
        vision = FakeVisionLLM(
            dates=week_list[: max(args.pages or config.page_count, 1)],
            default_date=week_list[0] if week_list else None,
            summary=(
                f"# Weekly Notes ({format_iso_week(year, week)})\n\n"
                "## To-Dos\n- (fake dry-run)\n\n"
                "## Meeting Notes\n- (fake dry-run)\n"
            ),
        )
    else:
        remarkable, vision = _build_live_clients(config)

    try:
        result = run_pipeline(
            config,
            remarkable=remarkable,
            vision=vision,
            week_str=args.week,
            as_of=as_of,
            pages=args.pages,
            strict=args.strict,
            dry_run=args.dry_run,
        )
    except StrictValidationError as exc:
        print(f"Strict validation failed: {exc}", file=sys.stderr)
        for m in exc.mismatches:
            print(f"  page {m.page_index}: {m.reason}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    for m in result.mismatches:
        print(f"Warning: page {m.page_index}: {m.reason}", file=sys.stderr)

    if result.dry_run:
        print(f"Dry-run planned output: {result.output_path}")
    else:
        print(f"Wrote: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
