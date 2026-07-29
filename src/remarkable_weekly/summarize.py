"""Build prompts and summarize page chunks via VisionLLM."""

from __future__ import annotations

from remarkable_weekly.clients.base import VisionLLM
from remarkable_weekly.models import DateMismatch

TEMPLATE_INSTRUCTIONS = """\
You are summarizing handwritten reMarkable journal pages for a weekly notes digest.

Template awareness:
- Quadrant / four-box layouts are typically daily to-dos — put those under To-Dos.
- Lined / ruled pages are typically meeting notes — put those under Meeting Notes.

Rules:
- Produce clean markdown suitable for Confluence Insert > Markup.
- Sort content into the provided categories only.
- Do not invent content that is not visible on the pages.
- Prefer concise bullets; preserve names, decisions, and action items.
"""


def build_summarize_prompt(categories: list[str]) -> str:
    cats = ", ".join(categories)
    return (
        f"{TEMPLATE_INSTRUCTIONS}\n"
        f"Categories (use these section headings): {cats}\n"
        "Return markdown with a ## heading for each category that has content."
    )


def format_warnings(mismatches: list[DateMismatch]) -> str:
    if not mismatches:
        return ""
    lines = ["## Validation Warnings", ""]
    for m in mismatches:
        date_part = m.extracted_date.isoformat() if m.extracted_date else "unknown"
        lines.append(f"- Page {m.page_index}: {date_part} — {m.reason}")
    lines.append("")
    return "\n".join(lines)


def summarize_pages(
    chunks: list[bytes],
    categories: list[str],
    llm: VisionLLM,
    mismatches: list[DateMismatch] | None = None,
) -> str:
    """Call LLM summarize; prepend warnings section when mismatches exist."""
    body = llm.summarize(chunks, list(categories))
    warnings = format_warnings(mismatches or [])
    if warnings:
        return f"{warnings}\n{body.lstrip()}"
    return body
