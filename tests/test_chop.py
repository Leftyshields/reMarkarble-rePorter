"""Tests for PNG chopping."""

from io import BytesIO

from PIL import Image

from remarkable_weekly.chop import chop_png


def _png(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), (200, 200, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_chop_leaves_short_alone():
    png = _png(100, 500)
    chunks = chop_png(png, max_height=1400)
    assert len(chunks) == 1
    with Image.open(BytesIO(chunks[0])) as img:
        assert img.size == (100, 500)


def test_chop_splits_tall_image():
    png = _png(80, 3000)
    chunks = chop_png(png, max_height=1400)
    assert len(chunks) == 3  # 1400 + 1400 + 200
    heights = []
    for c in chunks:
        with Image.open(BytesIO(c)) as img:
            assert img.width == 80
            heights.append(img.height)
    assert heights == [1400, 1400, 200]
