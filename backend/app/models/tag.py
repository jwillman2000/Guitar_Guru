import enum

from sqlalchemy import Column, Enum, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TagCategory(str, enum.Enum):
    """The fixed dimensions tags are organized under. Tag *names* within a
    category (e.g. which genres exist) stay free-form and extensible."""

    GENRE = "genre"
    TECHNIQUE = "technique"
    POSITION = "position"


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("category", "slug", name="uq_tags_category_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[TagCategory] = mapped_column(Enum(TagCategory, name="tag_category"))
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100))


exercise_tags = Table(
    "exercise_tags",
    Base.metadata,
    Column("exercise_id", ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

lick_tags = Table(
    "lick_tags",
    Base.metadata,
    Column("lick_id", ForeignKey("licks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
