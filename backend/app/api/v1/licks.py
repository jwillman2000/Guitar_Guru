from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Lick, Tag, TagCategory
from app.schemas.lick import LickCreate, LickOut

router = APIRouter(prefix="/licks", tags=["licks"])


def _split_tags(tags: list[Tag]) -> tuple[list[str], list[str]]:
    """Separate a lick's tags into (genre names, technique names).

    Position-category tags aren't surfaced here — a lick's actual position
    coverage is the more precise `scale_positions` field, not a browsable tag
    label. Kept as a plain function over in-memory Tag objects so it doesn't
    need a DB to unit test.
    """
    genre_tags = [tag.name for tag in tags if tag.category == TagCategory.GENRE]
    technique_tags = [tag.name for tag in tags if tag.category == TagCategory.TECHNIQUE]
    return genre_tags, technique_tags


def _to_lick_out(lick: Lick) -> LickOut:
    genre_tags, technique_tags = _split_tags(lick.tags)
    return LickOut(
        id=str(lick.id),
        title=lick.title,
        artist=lick.artist,
        song=lick.song,
        key=lick.key,
        difficulty=lick.difficulty,
        description=lick.description,
        notes=lick.reference_data,
        genre_tags=genre_tags,
        technique_tags=technique_tags,
        scale_positions=lick.scale_positions,
    )


@router.get("/", response_model=list[LickOut])
def list_licks(db: Session = Depends(get_db)) -> list[LickOut]:
    licks = db.query(Lick).order_by(Lick.title).all()
    return [_to_lick_out(lick) for lick in licks]


@router.get("/{lick_id}", response_model=LickOut)
def get_lick(lick_id: int, db: Session = Depends(get_db)) -> LickOut:
    lick = db.get(Lick, lick_id)
    if lick is None:
        raise HTTPException(status_code=404, detail=f"Lick {lick_id} not found")
    return _to_lick_out(lick)


def _resolve_tags(db: Session, tag_ids: list[int]) -> list[Tag]:
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    missing_ids = set(tag_ids) - {tag.id for tag in tags}
    if missing_ids:
        raise HTTPException(status_code=400, detail=f"Unknown tag_ids: {sorted(missing_ids)}")
    return tags


@router.post("/", response_model=LickOut)
def create_lick(payload: LickCreate, db: Session = Depends(get_db)) -> LickOut:
    tags = _resolve_tags(db, payload.tag_ids)

    lick = Lick(
        title=payload.title,
        artist=payload.artist,
        song=payload.song,
        key=payload.key,
        difficulty=payload.difficulty,
        description=payload.description,
        reference_data=[note.model_dump(by_alias=True) for note in payload.notes],
        scale_positions=payload.scale_positions,
        tags=tags,
    )
    db.add(lick)
    db.commit()
    db.refresh(lick)

    return _to_lick_out(lick)


@router.put("/{lick_id}", response_model=LickOut)
def update_lick(lick_id: int, payload: LickCreate, db: Session = Depends(get_db)) -> LickOut:
    lick = db.get(Lick, lick_id)
    if lick is None:
        raise HTTPException(status_code=404, detail=f"Lick {lick_id} not found")

    tags = _resolve_tags(db, payload.tag_ids)

    lick.title = payload.title
    lick.artist = payload.artist
    lick.song = payload.song
    lick.key = payload.key
    lick.difficulty = payload.difficulty
    lick.description = payload.description
    lick.reference_data = [note.model_dump(by_alias=True) for note in payload.notes]
    lick.scale_positions = payload.scale_positions
    lick.tags = tags

    db.commit()
    db.refresh(lick)

    return _to_lick_out(lick)


@router.delete("/{lick_id}", status_code=204)
def delete_lick(lick_id: int, db: Session = Depends(get_db)) -> None:
    lick = db.get(Lick, lick_id)
    if lick is None:
        raise HTTPException(status_code=404, detail=f"Lick {lick_id} not found")
    db.delete(lick)
    db.commit()
