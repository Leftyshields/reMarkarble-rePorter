"""Client interfaces for reMarkable cloud and vision LLM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from remarkable_weekly.models import PageImage


class RemarkableClient(ABC):
    """Pull notebook page images from reMarkable cloud."""

    @abstractmethod
    def fetch_last_pages(self, notebook_name: str, page_count: int) -> list[PageImage]:
        """Return the last ``page_count`` pages as PNG PageImage objects (oldest→newest or as stored)."""


class VisionLLM(ABC):
    """Vision model for handwritten date extraction and page summarization."""

    @abstractmethod
    def extract_date(self, image_png: bytes) -> date | None:
        """Extract handwritten ISO date from a page image, or None if unreadable."""

    @abstractmethod
    def summarize(self, chunks: list[bytes], categories: list[str]) -> str:
        """Summarize page chunks into categorized markdown."""
