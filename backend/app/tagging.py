"""Shared tag helpers used across modules' generate/create endpoints."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Tag, TagCategory


def resolve_tag_by_name(db: Session, category: TagCategory, name: str) -> Tag:
    """Case-insensitive tag lookup within a category; 400s if not found."""
    tag = db.query(Tag).filter(Tag.category == category, Tag.name.ilike(name)).first()
    if tag is None:
        raise HTTPException(status_code=400, detail=f"Unknown {category.value} tag: {name!r}")
    return tag


def split_tags(tags: list[Tag]) -> tuple[list[str], list[str]]:
    """Separate tags into (genre names, technique names).

    Position-category tags aren't surfaced here — callers that need position
    coverage use a dedicated field (e.g. Lick.scale_positions) instead of a
    browsable tag label. Kept as a plain function over in-memory Tag objects
    so it doesn't need a DB to unit test.
    """
    genre_tags = [tag.name for tag in tags if tag.category == TagCategory.GENRE]
    technique_tags = [tag.name for tag in tags if tag.category == TagCategory.TECHNIQUE]
    return genre_tags, technique_tags
