from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.engine import generate_scale_fluency_drill
from app.models import Exercise, Module
from app.schemas.exercise import GenerateScaleFluencyRequest, GeneratedDrillOut

router = APIRouter(prefix="/scale-fluency", tags=["scale-fluency"])


@router.post("/generate", response_model=GeneratedDrillOut)
def generate(payload: GenerateScaleFluencyRequest, db: Session = Depends(get_db)) -> GeneratedDrillOut:
    try:
        drill = generate_scale_fluency_drill(
            key=payload.key,
            scale=payload.scale,
            start_string=payload.start_string,
            start_fret=payload.start_fret,
            num_strings=payload.num_strings,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    reference_data = [
        {**note, "startBeat": index, "durationBeats": 1}
        for index, note in enumerate(drill.notes)
    ]

    exercise = Exercise(
        module=Module.SCALE_FLUENCY,
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
        module_id="scale-fluency",
        generator_params=exercise.parameters,
    )
