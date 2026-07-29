"""Chop tall PNG pages into horizontal strips."""

from __future__ import annotations

from io import BytesIO

from PIL import Image


def chop_png(png_bytes: bytes, max_height: int = 1400) -> list[bytes]:
    """
    If image height exceeds max_height, split into horizontal strips of at most
    max_height pixels. Short images are returned unchanged as a single-element list.
    """
    if max_height <= 0:
        raise ValueError("max_height must be positive")

    img = Image.open(BytesIO(png_bytes))
    img = img.convert("RGB")
    width, height = img.size

    if height <= max_height:
        return [png_bytes]

    chunks: list[bytes] = []
    top = 0
    while top < height:
        bottom = min(top + max_height, height)
        strip = img.crop((0, top, width, bottom))
        buf = BytesIO()
        strip.save(buf, format="PNG")
        chunks.append(buf.getvalue())
        top = bottom
    return chunks


def chop_pages(png_pages: list[bytes], max_height: int = 1400) -> list[bytes]:
    """Chop each page and flatten into a single chunk list (page order preserved)."""
    out: list[bytes] = []
    for page in png_pages:
        out.extend(chop_png(page, max_height=max_height))
    return out
