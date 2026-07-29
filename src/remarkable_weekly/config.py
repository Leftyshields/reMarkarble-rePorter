"""Configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_NOTEBOOK_NAME = "Daily Journal"
DEFAULT_PAGE_COUNT = 5
DEFAULT_CATEGORIES = ("To-Dos", "Meeting Notes", "Follow-ups", "Other")
DEFAULT_NOTES_DIR = "weekly-notes"
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_CHUNK_MAX_HEIGHT = 1400
DEFAULT_TZ = "local"


@dataclass(frozen=True)
class Config:
    remarkable_token: str | None = None
    anthropic_api_key: str | None = None
    notebook_name: str = DEFAULT_NOTEBOOK_NAME
    page_count: int = DEFAULT_PAGE_COUNT
    categories: tuple[str, ...] = field(default_factory=lambda: DEFAULT_CATEGORIES)
    notes_dir: Path = field(default_factory=lambda: Path(DEFAULT_NOTES_DIR))
    anthropic_model: str = DEFAULT_MODEL
    chunk_max_height: int = DEFAULT_CHUNK_MAX_HEIGHT
    notes_tz: str = DEFAULT_TZ


def _parse_categories(raw: str | None) -> tuple[str, ...]:
    if raw is None or not raw.strip():
        return DEFAULT_CATEGORIES
    parts = [p.strip() for p in raw.split(",")]
    return tuple(p for p in parts if p) or DEFAULT_CATEGORIES


def _parse_int(raw: str | None, default: int) -> int:
    if raw is None or not str(raw).strip():
        return default
    return int(raw)


def load_config(*, env_file: str | Path | None = ".env", environ: dict[str, str] | None = None) -> Config:
    """Load config from env. Optionally load dotenv file first (skipped if environ is injected)."""
    if environ is None:
        if env_file:
            load_dotenv(env_file)
        env = os.environ
    else:
        env = environ

    token = env.get("REMARKABLE_TOKEN") or None
    if token is not None and not token.strip():
        token = None
    api_key = env.get("ANTHROPIC_API_KEY") or None
    if api_key is not None and not api_key.strip():
        api_key = None

    notes_dir_raw = env.get("WEEKLY_NOTES_DIR", DEFAULT_NOTES_DIR).strip() or DEFAULT_NOTES_DIR
    tz = (env.get("WEEKLY_NOTES_TZ") or DEFAULT_TZ).strip().lower()
    if tz not in ("local", "utc"):
        tz = DEFAULT_TZ

    return Config(
        remarkable_token=token,
        anthropic_api_key=api_key,
        notebook_name=(env.get("REMARKABLE_NOTEBOOK_NAME") or DEFAULT_NOTEBOOK_NAME).strip()
        or DEFAULT_NOTEBOOK_NAME,
        page_count=_parse_int(env.get("REMARKABLE_PAGE_COUNT"), DEFAULT_PAGE_COUNT),
        categories=_parse_categories(env.get("WEEKLY_CATEGORIES")),
        notes_dir=Path(notes_dir_raw),
        anthropic_model=(env.get("ANTHROPIC_MODEL") or DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        chunk_max_height=_parse_int(env.get("CHUNK_MAX_HEIGHT"), DEFAULT_CHUNK_MAX_HEIGHT),
        notes_tz=tz,
    )
