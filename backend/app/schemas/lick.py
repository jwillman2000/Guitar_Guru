from typing import Literal

from app.schemas.exercise import CamelModel, NoteEventOut


class LickOut(CamelModel):
    id: str
    title: str
    artist: str | None = None
    song: str
    key: str
    difficulty: str
    description: str | None = None
    notes: list[NoteEventOut]
    genre_tags: list[str] = []
    technique_tags: list[str] = []
    scale_positions: list[int] = []
    source: Literal["canonical"] = "canonical"
    module_id: Literal["lick-library"] = "lick-library"


class LickCreate(CamelModel):
    title: str
    artist: str | None = None
    song: str
    key: str
    difficulty: str = "standard"
    description: str | None = None
    notes: list[NoteEventOut]
    tag_ids: list[int] = []
    scale_positions: list[int] = []
