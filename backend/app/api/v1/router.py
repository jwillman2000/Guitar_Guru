from fastapi import APIRouter

from app.api.v1.fretboard_literacy import router as fretboard_literacy_router
from app.api.v1.licks import router as licks_router
from app.api.v1.picking_technique import router as picking_technique_router
from app.api.v1.scale_fluency import router as scale_fluency_router
from app.api.v1.tags import router as tags_router

router = APIRouter(prefix="/api/v1")
router.include_router(fretboard_literacy_router)
router.include_router(scale_fluency_router)
router.include_router(picking_technique_router)
router.include_router(licks_router)
router.include_router(tags_router)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
