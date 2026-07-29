"""Fake clients for tests and --dry-run without live tokens."""

from __future__ import annotations

from datetime import date
from io import BytesIO

from PIL import Image

from remarkable_weekly.clients.base import RemarkableClient, VisionLLM
from remarkable_weekly.models import PageImage


def _tiny_png(width: int = 64, height: int = 64, color: tuple[int, int, int] = (255, 255, 255)) -> bytes:
    img = Image.new("RGB", (width, height), color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class FakeRemarkableClient(RemarkableClient):
    """Returns N tiny PNG pages; optional custom pages for tests."""

    def __init__(
        self,
        pages: list[PageImage] | None = None,
        *,
        page_height: int = 64,
        page_width: int = 64,
    ) -> None:
        self._pages = pages
        self._page_height = page_height
        self._page_width = page_width
        self.last_notebook: str | None = None
        self.last_page_count: int | None = None

    def fetch_last_pages(self, notebook_name: str, page_count: int) -> list[PageImage]:
        self.last_notebook = notebook_name
        self.last_page_count = page_count
        if self._pages is not None:
            return list(self._pages)[-page_count:]
        out: list[PageImage] = []
        for i in range(page_count):
            png = _tiny_png(self._page_width, self._page_height)
            out.append(
                PageImage(index=i, png_bytes=png, width=self._page_width, height=self._page_height)
            )
        return out


class FakeVisionLLM(VisionLLM):
    """Configurable date extraction and fixed markdown summary."""

    def __init__(
        self,
        dates: list[date | None] | dict[int, date | None] | None = None,
        summary: str = "# Weekly Notes\n\n## To-Dos\n- fake item\n",
        default_date: date | None = None,
    ) -> None:
        self._dates = dates if dates is not None else {}
        self._summary = summary
        self._default_date = default_date
        self._call_index = 0
        self.extract_calls: list[bytes] = []
        self.summarize_calls: list[tuple[list[bytes], list[str]]] = []

    def extract_date(self, image_png: bytes) -> date | None:
        self.extract_calls.append(image_png)
        idx = self._call_index
        self._call_index += 1
        if isinstance(self._dates, list):
            if idx < len(self._dates):
                return self._dates[idx]
            return self._default_date
        if idx in self._dates:
            return self._dates[idx]
        return self._default_date

    def summarize(self, chunks: list[bytes], categories: list[str]) -> str:
        self.summarize_calls.append((chunks, categories))
        return self._summary
