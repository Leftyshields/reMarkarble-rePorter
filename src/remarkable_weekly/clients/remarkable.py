"""Live reMarkable cloud client via remarkapy (optional dependency)."""

from __future__ import annotations

from io import BytesIO

from remarkable_weekly.clients.base import RemarkableClient
from remarkable_weekly.models import PageImage


class RemarkableCloudClient(RemarkableClient):
    """
    Fetch notebook pages from reMarkable cloud using remarkapy.

    Requires ``remarkapy`` installed (``pip install remarkable-weekly[remarkable]``)
    and a valid ``REMARKABLE_TOKEN``.
    """

    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("REMARKABLE_TOKEN is required for live reMarkable access")
        try:
            import remarkapy  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "remarkapy is not installed. Install with: "
                "pip install 'remarkable-weekly[remarkable]' "
                "or pip install remarkapy"
            ) from exc
        self._token = token

    def fetch_last_pages(self, notebook_name: str, page_count: int) -> list[PageImage]:
        try:
            from remarkapy import Client  # type: ignore[attr-defined]
        except ImportError:
            try:
                from remarkapy.client import Client  # type: ignore[attr-defined]
            except ImportError as exc:
                raise RuntimeError(
                    "Could not import remarkapy Client. "
                    "Check remarkapy version/API and reMarkable cloud credentials."
                ) from exc

        client = Client(token=self._token)
        # remarkapy APIs vary by version; try common patterns
        pdf_bytes = _download_notebook_pdf(client, notebook_name)
        return pdf_to_page_images(pdf_bytes, page_count)


def _download_notebook_pdf(client, notebook_name: str) -> bytes:
    """Best-effort download of notebook as PDF across remarkapy versions."""
    # Common patterns across remarkapy forks / versions
    if hasattr(client, "download_pdf"):
        items = _list_items(client)
        item = _find_by_name(items, notebook_name)
        return client.download_pdf(item)

    if hasattr(client, "get_document") and hasattr(client, "export"):
        items = _list_items(client)
        item = _find_by_name(items, notebook_name)
        doc_id = item.get("uuid") or item.get("id") or getattr(item, "uuid", None)
        return client.export(doc_id, format="pdf")

    raise NotImplementedError(
        "This remarkapy Client does not expose a known PDF download API. "
        "Update remarkapy or extend RemarkableCloudClient.fetch_last_pages."
    )


def _list_items(client) -> list:
    if hasattr(client, "list_items"):
        return list(client.list_items())
    if hasattr(client, "get_meta_items"):
        return list(client.get_meta_items())
    if hasattr(client, "documents"):
        return list(client.documents())
    raise NotImplementedError("remarkapy Client has no known list/documents method")


def _item_name(item) -> str | None:
    if isinstance(item, dict):
        return (
            item.get("VissibleName")
            or item.get("visibleName")
            or item.get("name")
        )
    return getattr(item, "visible_name", None) or getattr(item, "name", None)


def _find_by_name(items: list, notebook_name: str):
    target = notebook_name.strip().lower()
    for item in items:
        name = _item_name(item)
        if name and str(name).strip().lower() == target:
            return item
    raise FileNotFoundError(f"Notebook not found in reMarkable cloud: {notebook_name!r}")


def pdf_to_page_images(pdf_bytes: bytes, page_count: int) -> list[PageImage]:
    """Render the last ``page_count`` PDF pages to PNG via pypdfium2."""
    try:
        import pypdfium2 as pdfium
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pypdfium2 is required to convert PDF pages to PNG") from exc

    pdf = pdfium.PdfDocument(pdf_bytes)
    n = len(pdf)
    if n == 0:
        return []
    start = max(0, n - page_count)
    pages: list[PageImage] = []
    for i, page_index in enumerate(range(start, n)):
        page = pdf[page_index]
        bitmap = page.render(scale=2)
        pil = bitmap.to_pil()
        buf = BytesIO()
        pil.save(buf, format="PNG")
        pages.append(
            PageImage(
                index=i,
                png_bytes=buf.getvalue(),
                width=pil.width,
                height=pil.height,
            )
        )
    return pages
