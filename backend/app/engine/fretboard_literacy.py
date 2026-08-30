"""Module 1 (Fretboard Literacy) drill generator.

Builds on app.engine.theory's deterministic note-identity math. Randomness
here only selects *which* fretboard positions appear in a drill — the pitch
computed for each position is always rule-based, never freehanded.
"""

import random
from dataclasses import dataclass, field

from app.engine.theory import SUPPORTED_KEYS, fret_to_midi, midi_to_pitch_name

MAX_FRET = 15  # matches the frontend Fretboard.tsx FRET_COUNT constant
MIN_STRING, MAX_STRING = 1, 6


@dataclass
class FretboardDrill:
    title: str
    parameters: dict
    notes: list[dict] = field(default_factory=list)  # [{"position": {"string", "fret"}, "pitch"}]


def generate_drill(
    key: str = "C",
    string_range: tuple[int, int] = (1, 6),
    fret_range: tuple[int, int] = (0, 15),
    count: int = 8,
    rng: random.Random | None = None,
) -> FretboardDrill:
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}. Supported keys: {sorted(SUPPORTED_KEYS)}")

    string_min, string_max = string_range
    fret_min, fret_max = fret_range
    if not (MIN_STRING <= string_min <= string_max <= MAX_STRING):
        raise ValueError(f"string_range must be within {MIN_STRING}-{MAX_STRING}, got {string_range}")
    if not (0 <= fret_min <= fret_max <= MAX_FRET):
        raise ValueError(f"fret_range must be within 0-{MAX_FRET}, got {fret_range}")

    positions = [
        (string, fret)
        for string in range(string_min, string_max + 1)
        for fret in range(fret_min, fret_max + 1)
    ]
    if count > len(positions):
        raise ValueError(f"count ({count}) exceeds available positions ({len(positions)}) in range")

    rng = rng or random.Random()
    chosen = rng.sample(positions, count)

    notes = [
        {
            "position": {"string": string, "fret": fret},
            "pitch": midi_to_pitch_name(fret_to_midi(string, fret), key),
        }
        for string, fret in chosen
    ]

    return FretboardDrill(
        title=f"Fretboard Literacy — Key of {key}",
        parameters={
            "key": key,
            "string_range": list(string_range),
            "fret_range": list(fret_range),
            "count": count,
        },
        notes=notes,
    )
