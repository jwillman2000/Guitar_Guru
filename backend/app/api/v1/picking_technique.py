from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.engine import (
    generate_alternate_picking_drill,
    generate_economy_picking_drill,
    generate_hybrid_picking_drill,
    generate_string_skipping_drill,
    generate_sweep_picking_drill,
    generate_tremolo_drill,
)
from app.engine.theory import Drill
from app.models import Exercise, Module, TagCategory
from app.schemas.exercise import GeneratedDrillOut
from app.schemas.picking_technique import GeneratePickingTechniqueRequest
from app.tagging import resolve_tag_by_name, split_tags

router = APIRouter(prefix="/picking-technique", tags=["picking-technique"])

# The engine's technique values don't match the seeded tag names exactly.
TECHNIQUE_TAG_NAMES = {
    "alternate": "Alternate Picking",
    "economy": "Economy Picking",
    "tremolo": "Tremolo Picking",
    "string_skipping": "String Skipping",
    "sweep": "Sweep Picking",
    "hybrid": "Hybrid Picking",
}


def _generate(payload: GeneratePickingTechniqueRequest) -> Drill:
    if payload.technique == "alternate":
        return generate_alternate_picking_drill(
            key=payload.key, scale=payload.scale, start_string=payload.start_string,
            start_fret=payload.start_fret, num_strings=payload.num_strings,
        )
    if payload.technique == "economy":
        return generate_economy_picking_drill(
            key=payload.key, scale=payload.scale, start_string=payload.start_string,
            start_fret=payload.start_fret, num_strings=payload.num_strings,
        )
    if payload.technique == "tremolo":
        return generate_tremolo_drill(
            key=payload.key, scale=payload.scale, string=payload.string, fret=payload.fret,
            repeat_count=payload.repeat_count,
        )
    if payload.technique == "string_skipping":
        return generate_string_skipping_drill(
            key=payload.key, scale=payload.scale, start_string=payload.start_string,
            start_fret=payload.start_fret, num_strings=payload.num_strings, skip=payload.skip,
        )
    if payload.technique == "sweep":
        return generate_sweep_picking_drill(
            key=payload.key, chord_type=payload.chord_type, start_string=payload.start_string,
            start_fret=payload.start_fret, num_strings=payload.num_strings,
        )
    return generate_hybrid_picking_drill(
        key=payload.key, scale=payload.scale, start_string=payload.start_string,
        start_fret=payload.start_fret, num_strings=payload.num_strings,
    )


@router.post("/generate", response_model=GeneratedDrillOut)
def generate(payload: GeneratePickingTechniqueRequest, db: Session = Depends(get_db)) -> GeneratedDrillOut:
    try:
        drill = _generate(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    reference_data = [
        {**note, "startBeat": index, "durationBeats": 1}
        for index, note in enumerate(drill.notes)
    ]

    tags = [resolve_tag_by_name(db, TagCategory.TECHNIQUE, TECHNIQUE_TAG_NAMES[payload.technique])]
    if payload.genre:
        tags.append(resolve_tag_by_name(db, TagCategory.GENRE, payload.genre))

    exercise = Exercise(
        module=Module.PICKING_TECHNIQUE,
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
        module_id="picking-technique",
        generator_params=exercise.parameters,
        genre_tags=genre_tags,
        technique_tags=technique_tags,
    )
