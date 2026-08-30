from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.engine.theory import MAX_FRET, SCALE_INTERVALS, SUPPORTED_KEYS

SupportedKey = Literal["C", "G", "D", "A", "E", "B", "F#", "F", "Bb", "Eb", "Ab", "Db"]
assert set(SupportedKey.__args__) == SUPPORTED_KEYS  # keep the Swagger dropdown in sync with the engine

SupportedScale = Literal[
    "major", "natural_minor", "harmonic_minor", "melodic_minor", "major_pentatonic", "minor_pentatonic"
]
assert set(SupportedScale.__args__) == set(SCALE_INTERVALS)  # keep the Swagger dropdown in sync with the engine


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FretPositionOut(CamelModel):
    string: int
    fret: int


class NoteEventOut(CamelModel):
    position: FretPositionOut
    pitch: str
    start_beat: float
    duration_beats: float
    pick_direction: Literal["down", "up"] | None = None
    pluck_method: Literal["pick", "finger"] | None = None


class GeneratedDrillOut(CamelModel):
    id: str
    title: str
    genre_tags: list[str] = []
    technique_tags: list[str] = []
    notes: list[NoteEventOut]
    source: Literal["generated"] = "generated"
    module_id: Literal["fretboard-literacy", "scale-fluency", "picking-technique"] = "fretboard-literacy"
    generator_params: dict


class GenerateFretboardLiteracyRequest(CamelModel):
    key: SupportedKey = "C"
    string_range: tuple[int, int] = (1, 6)
    fret_range: tuple[int, int] = (0, MAX_FRET)
    count: int = 8
    difficulty: str = "standard"


class GenerateScaleFluencyRequest(CamelModel):
    key: SupportedKey = "C"
    scale: SupportedScale = "major"
    start_string: int = 6
    start_fret: int = 0
    num_strings: int = 6
    difficulty: str = "standard"
