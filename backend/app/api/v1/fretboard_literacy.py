from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.engine import generate_fretboard_literacy_drill
from app.models import Exercise, Module
from app.schemas.exercise import GenerateFretboardLiteracyRequest, GeneratedDrillOut

router = APIRouter(prefix="/fretboard-literacy", tags=["fretboard-literacy"])


@router.post("/generate", response_model=GeneratedDrillOut)
def generate(payload: GenerateFretboardLiteracyRequest, db: Session = Depends(get_db)) -> GeneratedDrillOut:
    drill = generate_fretboard_literacy_drill(
        key=payload.key,
        string_range=payload.string_range,
        fret_range=payload.fret_range,
        count=payload.count,
    )

    reference_data = [
        {**note, "startBeat": index, "durationBeats": 1}
        for index, note in enumerate(drill.notes)
    ]

    exercise = Exercise(
        module=Module.FRETBOARD_LITERACY,
        title=drill.title,
        difficulty=payload.difficulty,
        parameters=drill.parameters,
        reference_data=reference_data,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return GeneratedDrillOut(
        id=str(exercise.id),
        title=exercise.title,
        notes=reference_data,
        generator_params=exercise.parameters,
    )
