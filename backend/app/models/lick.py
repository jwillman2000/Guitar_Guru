from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.tag import Tag, lick_tags


class Lick(Base, TimestampMixin):
    """A hand-curated, canonical lick — entered one at a time, never
    scraped or freehanded by an LLM. `reference_data` holds the structured
    note/timing/fret sequence (not just a rendering string), so it can drive
    both playback and the Module 2 tie-back (e.g. showing why a lick crosses
    scale positions).
    """

    __tablename__ = "licks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    artist: Mapped[str | None] = mapped_column(String(200), default=None)
    song: Mapped[str] = mapped_column(String(200))
    key: Mapped[str] = mapped_column(String(20))
    difficulty: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    reference_data: Mapped[dict] = mapped_column(JSONB)
    scale_positions: Mapped[list[int]] = mapped_column(JSONB, default=list)

    tags: Mapped[list[Tag]] = relationship(secondary=lick_tags)
