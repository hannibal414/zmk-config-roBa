"""LLM client abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator


class LLMClient(ABC):
    """Interface for streaming text generation."""

    @abstractmethod
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """Yield generated text chunks for the given prompt."""
        raise NotImplementedError
