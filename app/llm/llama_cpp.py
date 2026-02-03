"""llama-cpp-python implementation of the LLMClient interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator, Optional, Sequence

from .base import LLMClient


@dataclass
class LlamaCppConfig:
    model_path: str
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 256
    stop: Optional[Sequence[str]] = None
    llama_kwargs: dict = field(default_factory=dict)


class LlamaCppClient(LLMClient):
    """LLMClient backed by llama-cpp-python.

    Parameters are provided via LlamaCppConfig. For unit tests, a pre-built
    llama instance or factory can be injected to avoid importing the package.
    """

    def __init__(
        self,
        config: LlamaCppConfig,
        llama_instance: Optional[object] = None,
        llama_factory: Optional[Callable[[str], object]] = None,
    ) -> None:
        self._config = config
        self._llama = llama_instance
        self._llama_factory = llama_factory

        if self._llama is None:
            self._llama = self._build_llama()

    def _build_llama(self) -> object:
        if self._llama_factory is not None:
            return self._llama_factory(self._config.model_path)

        try:
            from llama_cpp import Llama  # type: ignore
        except ImportError as exc:  # pragma: no cover - import guard
            raise ImportError(
                "llama-cpp-python is required to use LlamaCppClient."
            ) from exc

        return Llama(model_path=self._config.model_path, **self._config.llama_kwargs)

    def stream_generate(self, prompt: str) -> Iterator[str]:
        response_iter = self._llama.create_completion(
            prompt=prompt,
            temperature=self._config.temperature,
            top_p=self._config.top_p,
            max_tokens=self._config.max_tokens,
            stop=self._config.stop,
            stream=True,
        )
        for chunk in response_iter:
            yield chunk["choices"][0]["text"]
