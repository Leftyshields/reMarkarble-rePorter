"""Tests for config loading."""

from pathlib import Path

from remarkable_weekly.config import (
    DEFAULT_CATEGORIES,
    DEFAULT_CHUNK_MAX_HEIGHT,
    DEFAULT_MODEL,
    DEFAULT_NOTEBOOK_NAME,
    DEFAULT_PAGE_COUNT,
    load_config,
)


def test_config_defaults():
    cfg = load_config(environ={})
    assert cfg.remarkable_token is None
    assert cfg.anthropic_api_key is None
    assert cfg.notebook_name == DEFAULT_NOTEBOOK_NAME
    assert cfg.page_count == DEFAULT_PAGE_COUNT
    assert cfg.categories == DEFAULT_CATEGORIES
    assert cfg.notes_dir == Path("weekly-notes")
    assert cfg.anthropic_model == DEFAULT_MODEL
    assert cfg.chunk_max_height == DEFAULT_CHUNK_MAX_HEIGHT
    assert cfg.notes_tz == "local"


def test_config_env_override():
    env = {
        "REMARKABLE_TOKEN": "tok",
        "ANTHROPIC_API_KEY": "key",
        "REMARKABLE_NOTEBOOK_NAME": "My Journal",
        "REMARKABLE_PAGE_COUNT": "7",
        "WEEKLY_CATEGORIES": "A, B, C",
        "WEEKLY_NOTES_DIR": "/tmp/notes",
        "ANTHROPIC_MODEL": "claude-test",
        "CHUNK_MAX_HEIGHT": "900",
        "WEEKLY_NOTES_TZ": "UTC",
    }
    cfg = load_config(environ=env)
    assert cfg.remarkable_token == "tok"
    assert cfg.anthropic_api_key == "key"
    assert cfg.notebook_name == "My Journal"
    assert cfg.page_count == 7
    assert cfg.categories == ("A", "B", "C")
    assert cfg.notes_dir == Path("/tmp/notes")
    assert cfg.anthropic_model == "claude-test"
    assert cfg.chunk_max_height == 900
    assert cfg.notes_tz == "utc"


def test_empty_token_treated_as_none():
    cfg = load_config(environ={"REMARKABLE_TOKEN": "  ", "ANTHROPIC_API_KEY": ""})
    assert cfg.remarkable_token is None
    assert cfg.anthropic_api_key is None
