"""Live reMarkable cloud client via remarkapy (optional dependency)."""

from __future__ import annotations

import io
import json
import zipfile
from io import BytesIO

from remarkable_weekly.clients.base import RemarkableClient
from remarkable_weekly.models import PageImage
from remarkable_weekly.render_rm import rm_bytes_to_png


class RemarkableCloudClient(RemarkableClient):
    """
    Fetch notebook pages from reMarkable cloud using remarkapy.

    Handwritten notebooks have no original PDF — we download the raw bundle
    and render the last N ``.rm`` pages to PNG via rmscene + cairosvg.
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
            from remarkapy import Client
        except ImportError as exc:
            raise RuntimeError(
                "Could not import remarkapy Client. "
                "Check remarkapy version/API and reMarkable cloud credentials."
            ) from exc

        client = Client(device_token=self._token, interactive=False)
        bundle = client.get_document(notebook_name)
        return notebook_bundle_to_page_images(bundle, page_count)


def notebook_bundle_to_page_images(bundle_bytes: bytes, page_count: int) -> list[PageImage]:
    """Render the last ``page_count`` pages from a raw notebook zip to PNGs."""
    zf = zipfile.ZipFile(io.BytesIO(bundle_bytes))
    content_name = next((n for n in zf.namelist() if n.endswith(".content")), None)
    if not content_name:
        raise RuntimeError("Notebook bundle missing .content metadata")

    doc_id = content_name[: -len(".content")]
    content = json.loads(zf.read(content_name))
    page_ids = _page_ids_in_order(content)
    if not page_ids:
        return []

    selected = page_ids[-page_count:] if page_count > 0 else page_ids
    pages: list[PageImage] = []
    for i, page_id in enumerate(selected):
        rm_path = f"{doc_id}/{page_id}.rm"
        try:
            rm_bytes = zf.read(rm_path)
        except KeyError as exc:
            raise RuntimeError(f"Missing page file in bundle: {rm_path}") from exc
        png = rm_bytes_to_png(rm_bytes, scale=1.0)
        width, height = _png_size(png)
        pages.append(PageImage(index=i, png_bytes=png, width=width, height=height))
    return pages


def _page_ids_in_order(content: dict) -> list[str]:
    c_pages = content.get("cPages") or {}
    pages = c_pages.get("pages") or content.get("pages") or []
    ids: list[str] = []
    for entry in pages:
        if isinstance(entry, str):
            ids.append(entry)
        elif isinstance(entry, dict) and entry.get("id"):
            ids.append(entry["id"])
    return ids


def _png_size(png_bytes: bytes) -> tuple[int, int]:
    from PIL import Image

    with Image.open(BytesIO(png_bytes)) as img:
        return img.width, img.height


def pdf_to_page_images(pdf_bytes: bytes, page_count: int) -> list[PageImage]:
    """Render the last ``page_count`` PDF pages to PNG via pypdfium2 (PDF notebooks)."""
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
