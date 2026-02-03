"""Stub LLM client for tests."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Iterable, List, Optional

from .base import LLMClient


class StubLLMClient(LLMClient):
    """Test double that returns predefined text chunks."""

    def __init__(self, chunks: Optional[Iterable[str]] = None) -> None:
        self._chunks: List[str] = list(chunks) if chunks is not None else ["stub"]
        self.last_prompt: Optional[str] = None

    def stream_generate(self, prompt: str) -> Iterator[str]:
        self.last_prompt = prompt
        yield from self._chunks
