from typing import Literal

from app.engine.theory import ARPEGGIO_INTERVALS
from app.schemas.exercise import CamelModel, SupportedKey, SupportedScale

SupportedTechnique = Literal["alternate", "economy", "tremolo", "string_skipping", "sweep", "hybrid"]

SupportedChord = Literal["major_triad", "minor_triad", "diminished_triad"]
assert set(SupportedChord.__args__) == set(ARPEGGIO_INTERVALS)  # keep the Swagger dropdown in sync with the engine


class GeneratePickingTechniqueRequest(CamelModel):
    technique: SupportedTechnique
    key: SupportedKey = "C"
    scale: SupportedScale = "major"  # alternate, economy, string_skipping, hybrid, tremolo
    chord_type: SupportedChord = "major_triad"  # sweep only
    start_string: int = 6
    start_fret: int = 0
    num_strings: int = 6
    string: int = 1  # tremolo only
    fret: int = 0  # tremolo only
    skip: int = 2  # string_skipping only
    repeat_count: int = 8  # tremolo only
    difficulty: str = "standard"
    genre: str | None = None
