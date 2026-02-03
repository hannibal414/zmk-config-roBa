from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
from typing import Iterable, Optional

import yaml

from app.config import AppConfig


_FIRST_NAMES = [
    "Alex",
    "Blake",
    "Casey",
    "Dana",
    "Elliot",
    "Finley",
    "Gray",
    "Harper",
    "Jordan",
    "Kai",
]

_LAST_NAMES = [
    "Adams",
    "Bennett",
    "Carter",
    "Diaz",
    "Evans",
    "Foster",
    "Garcia",
    "Hughes",
    "Irwin",
    "Johnson",
]

_ROLES = [
    "Facilitator",
    "Observer",
    "Participant",
    "Recorder",
    "Reviewer",
]


@dataclass(frozen=True)
class Participant:
    name: str
    email: str
    age: int
    role: str
    participant_id: int

    @classmethod
    def from_dict(cls, data: dict, rng: random.Random) -> "Participant":
        name = _value_or_random(data.get("name"), _random_name(rng))
        email = _value_or_random(data.get("email"), _random_email(name, rng))
        age = _value_or_random(data.get("age"), rng.randint(18, 75))
        role = _value_or_random(data.get("role"), rng.choice(_ROLES))
        participant_id = _value_or_random(data.get("participant_id"), rng.randint(1000, 9999))
        return cls(
            name=str(name),
            email=str(email),
            age=int(age),
            role=str(role),
            participant_id=int(participant_id),
        )


def load_participants(config: AppConfig) -> list[Participant]:
    rng = random.Random(config.seed)
    raw_entries = _load_yaml_entries(config.participants_path)
    participants = [Participant.from_dict(entry, rng) for entry in raw_entries]

    if config.participant_count is None:
        return participants

    requested = config.participant_count
    if requested <= 0:
        return []

    if len(participants) < requested:
        participants.extend(_generate_random_participants(requested - len(participants), rng))
    elif len(participants) > requested:
        participants = participants[:requested]

    return participants


def _load_yaml_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)

    if payload is None:
        return []

    if not isinstance(payload, Iterable) or isinstance(payload, (str, bytes, dict)):
        raise ValueError("participants.yaml must contain a list of participants")

    entries: list[dict] = []
    for item in payload:
        if item is None:
            entries.append({})
        elif isinstance(item, dict):
            entries.append(item)
        else:
            raise ValueError("Each participant must be a mapping of fields")

    return entries


def _generate_random_participants(count: int, rng: random.Random) -> list[Participant]:
    return [Participant.from_dict({}, rng) for _ in range(count)]


def _value_or_random(value: Optional[object], fallback: object) -> object:
    if value is None:
        return fallback
    if isinstance(value, str) and not value.strip():
        return fallback
    return value


def _random_name(rng: random.Random) -> str:
    first = rng.choice(_FIRST_NAMES)
    last = rng.choice(_LAST_NAMES)
    return f"{first} {last}"


def _random_email(name: str, rng: random.Random) -> str:
    safe = name.lower().replace(" ", ".")
    return f"{safe}{rng.randint(1, 999)}@example.com"
