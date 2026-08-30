from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.engine import generate_fretboard_literacy_drill
from app.models import Exercise, Module, TagCategory
from app.schemas.exercise import GenerateFretboardLiteracyRequest, GeneratedDrillOut
from app.tagging import resolve_tag_by_name, split_tags

router = APIRouter(prefix="/fretboard-literacy", tags=["fretboard-literacy"])


@router.post("/generate", response_model=GeneratedDrillOut)
def generate(payload: GenerateFretboardLiteracyRequest, db: Session = Depends(get_db)) -> GeneratedDrillOut:
    try:
        drill = generate_fretboard_literacy_drill(
            key=payload.key,
            string_range=payload.string_range,
            fret_range=payload.fret_range,
            count=payload.count,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    reference_data = [
        {**note, "startBeat": index, "durationBeats": 1}
        for index, note in enumerate(drill.notes)
    ]

    tags = [resolve_tag_by_name(db, TagCategory.GENRE, payload.genre)] if payload.genre else []

    exercise = Exercise(
        module=Module.FRETBOARD_LITERACY,
        title=drill.title,
        difficulty=payload.difficulty,
        parameters=drill.parameters,
        reference_data=reference_data,
        tags=tags,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    genre_tags, technique_tags = split_tags(exercise.tags)
    return GeneratedDrillOut(
        id=str(exercise.id),
        title=exercise.title,
        notes=reference_data,
        generator_params=exercise.parameters,
        genre_tags=genre_tags,
        technique_tags=technique_tags,
    )
