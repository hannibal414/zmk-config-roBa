from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    participants_path: Path
    participant_count: Optional[int] = None
    seed: Optional[int] = None
