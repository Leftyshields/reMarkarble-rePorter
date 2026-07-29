"""Pull last N pages via RemarkableClient."""

from __future__ import annotations

from remarkable_weekly.clients.base import RemarkableClient
from remarkable_weekly.models import PageImage


def pull_pages(
    client: RemarkableClient,
    notebook_name: str,
    page_count: int,
) -> list[PageImage]:
    if page_count < 1:
        raise ValueError("page_count must be >= 1")
    return client.fetch_last_pages(notebook_name, page_count)
