from fastapi import APIRouter

from app.api.v1.fretboard_literacy import router as fretboard_literacy_router

router = APIRouter(prefix="/api/v1")
router.include_router(fretboard_literacy_router)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
