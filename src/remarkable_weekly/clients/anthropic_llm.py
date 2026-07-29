"""Anthropic Messages API vision adapter."""

from __future__ import annotations

import base64
import re
from datetime import date

from remarkable_weekly.clients.base import VisionLLM
from remarkable_weekly.summarize import build_summarize_prompt

_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


class AnthropicVisionLLM(VisionLLM):
    """Vision LLM backed by Anthropic Messages API."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "anthropic package is required for live vision calls. "
                "Install with: pip install anthropic"
            ) from exc
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def _image_block(self, png_bytes: bytes) -> dict:
        b64 = base64.standard_b64encode(png_bytes).decode("ascii")
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": b64,
            },
        }

    def extract_date(self, image_png: bytes) -> date | None:
        content = [
            self._image_block(image_png),
            {
                "type": "text",
                "text": (
                    "Read the handwritten date header on this journal page. "
                    "Reply with ONLY an ISO date YYYY-MM-DD, or NONE if unreadable."
                ),
            },
        ]
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=64,
            messages=[{"role": "user", "content": content}],
        )
        text = _first_text(msg).strip().upper()
        if not text or text == "NONE" or "NONE" in text.split():
            # still try to parse if mixed
            m = _DATE_RE.search(_first_text(msg))
            if m:
                try:
                    return date.fromisoformat(m.group(1))
                except ValueError:
                    return None
            return None
        m = _DATE_RE.search(_first_text(msg))
        if not m:
            return None
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            return None

    def summarize(self, chunks: list[bytes], categories: list[str]) -> str:
        content: list[dict] = []
        for chunk in chunks:
            content.append(self._image_block(chunk))
        content.append({"type": "text", "text": build_summarize_prompt(categories)})
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            messages=[{"role": "user", "content": content}],
        )
        return _first_text(msg)


def _first_text(msg) -> str:
    parts: list[str] = []
    for block in msg.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts)
