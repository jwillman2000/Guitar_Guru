import enum

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.tag import Tag, exercise_tags


class Module(str, enum.Enum):
    """The three modules whose exercises are rules-engine generated, not
    hand-curated. Lick Library (canonical licks) has its own model."""

    FRETBOARD_LITERACY = "fretboard_literacy"
    SCALE_FLUENCY = "scale_fluency"
    PICKING_TECHNIQUE = "picking_technique"


class Exercise(Base, TimestampMixin):
    """A drill instance produced by the deterministic rules engine.

    `parameters` captures the engine inputs (scale, key, position, genre
    preset, ...) that generated this exercise; `reference_data` captures the
    engine's structured output (target notes/frets/timing) so playback and
    future scoring don't have to re-derive it from a tab string.
    """

    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    module: Mapped[Module] = mapped_column(Enum(Module, name="module"))
    title: Mapped[str] = mapped_column(String(200))
    difficulty: Mapped[str] = mapped_column(String(50))
    parameters: Mapped[dict] = mapped_column(JSONB)
    reference_data: Mapped[dict] = mapped_column(JSONB)

    tags: Mapped[list[Tag]] = relationship(secondary=exercise_tags)
