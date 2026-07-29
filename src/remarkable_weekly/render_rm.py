"""Render reMarkable v6 `.rm` pages to PNG for Claude vision."""

from __future__ import annotations

# Standard reMarkable page (rM1/2 / Paper Pro normalized space)
REMARKABLE_WIDTH = 1404.0
REMARKABLE_HEIGHT = 1872.0

HIGHLIGHTER_PENS = {5, 18}
ERASER_PENS = {6, 8}
COLOR_MAP = {
    0: "black",
    1: "#808080",
    2: "white",
    3: "#FFD700",
    4: "#00A000",
    5: "#FF69B4",
    6: "#4169E1",
    7: "#E00000",
    8: "#A0A0A0",
    9: "#FFD700",
    10: "#00C000",
    11: "#00CED1",
    12: "#FF00FF",
    13: "#FFD700",
}


def _read_v6_blocks(rm_bytes: bytes) -> list | None:
    try:
        from rmscene import read_blocks
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "rmscene is required to render handwritten notebooks. "
            "Install with: pip install 'rmscene>=0.8.0'"
        ) from exc

    import io

    bio = io.BytesIO(rm_bytes)
    header = bio.read(43)
    if b"version=6" not in header:
        return None
    bio.seek(0)
    try:
        return list(read_blocks(bio))
    except Exception:
        return None


def _paper_size(blocks: list) -> tuple[float, float]:
    for b in blocks:
        ps = getattr(b, "paper_size", None)
        if ps and len(ps) == 2 and ps[0] and ps[1]:
            try:
                return float(ps[0]), float(ps[1])
            except (TypeError, ValueError):
                continue
    return REMARKABLE_WIDTH, REMARKABLE_HEIGHT


def _paths_from_lines(lines: list) -> list[str]:
    paths: list[str] = []
    for line in lines:
        if not hasattr(line, "points") or not line.points:
            continue

        tool = line.tool if hasattr(line, "tool") else None
        color = line.color if hasattr(line, "color") else 0
        tool = tool.value if hasattr(tool, "value") else tool
        color = color.value if hasattr(color, "value") else color

        if tool in ERASER_PENS:
            continue

        is_highlighter = tool in HIGHLIGHTER_PENS
        stroke_color = COLOR_MAP.get(color, "black")
        if is_highlighter:
            avg_width = (
                sum(p.width for p in line.points) / len(line.points)
                if all(hasattr(p, "width") for p in line.points)
                else 20.0
            )
            stroke_width = max(10.0, min(avg_width * 2.0, 40.0))
            opacity = ' opacity="0.35"'
        else:
            avg_width = (
                sum(p.width for p in line.points) / len(line.points)
                if all(hasattr(p, "width") for p in line.points)
                else 2.0
            )
            stroke_width = max(0.5, min(avg_width * 0.8, 5.0))
            opacity = ""

        d = f"M {line.points[0].x:.1f} {line.points[0].y:.1f}"
        d += "".join(f" L {p.x:.1f} {p.y:.1f}" for p in line.points[1:])
        paths.append(
            f'<path d="{d}" stroke="{stroke_color}" '
            f'stroke-width="{stroke_width:.1f}" '
            f'fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round"{opacity}/>'
        )
    return paths


def _lines_from_blocks(blocks: list) -> list:
    lines = []
    for block in blocks:
        if not hasattr(block, "item") or not hasattr(block.item, "value"):
            continue
        line = block.item.value
        if hasattr(line, "points"):
            lines.append(line)
    return lines


def _lines_via_tree(rm_bytes: bytes) -> list:
    import io

    try:
        from rmscene import read_tree
        from rmscene.scene_items import Line
    except ImportError:
        return []

    try:
        tree = read_tree(io.BytesIO(rm_bytes))
    except Exception:
        return []

    lines: list = []

    def walk(node) -> None:
        if isinstance(node, Line):
            lines.append(node)
            return
        children = getattr(node, "children", None)
        if children is None and hasattr(node, "items"):
            children = node.items
        if children is None:
            return
        try:
            iterable = children.values() if hasattr(children, "values") else children
            for child in iterable:
                if isinstance(child, tuple) and len(child) == 2:
                    walk(child[1])
                else:
                    walk(getattr(child, "value", child))
        except Exception:
            return

    walk(getattr(tree, "root", tree))
    if not lines and hasattr(tree, "walk"):
        try:
            for item in tree.walk():
                if isinstance(item, Line):
                    lines.append(item)
        except Exception:
            pass
    return lines


def _svg_full_page(paths: list[str], paper_w: float, paper_h: float) -> str:
    min_x = -paper_w / 2.0
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{min_x:.0f} 0 {paper_w:.0f} {paper_h:.0f}" '
        f'width="{paper_w:.0f}" height="{paper_h:.0f}">'
        f'<rect x="{min_x:.0f}" y="0" width="{paper_w:.0f}" height="{paper_h:.0f}" '
        f'fill="#F7F5F0"/>'
        f"{''.join(paths)}</svg>"
    )


def rm_bytes_to_png(rm_bytes: bytes, *, scale: float = 1.0) -> bytes:
    """Convert a v6 `.rm` page to PNG bytes."""
    blocks = _read_v6_blocks(rm_bytes)
    paper_w, paper_h = REMARKABLE_WIDTH, REMARKABLE_HEIGHT
    if blocks is not None:
        paper_w, paper_h = _paper_size(blocks)
        lines = _lines_from_blocks(blocks)
    else:
        lines = _lines_via_tree(rm_bytes)

    paths = _paths_from_lines(lines)
    svg = _svg_full_page(paths, paper_w, paper_h)

    try:
        import cairosvg
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "cairosvg is required to rasterize notebook pages. "
            "Install with: pip install cairosvg"
        ) from exc

    out_w = max(1, int(paper_w * scale))
    out_h = max(1, int(paper_h * scale))
    png = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=out_w,
        output_height=out_h,
    )
    if not png:
        raise RuntimeError("cairosvg returned empty PNG")
    return png
