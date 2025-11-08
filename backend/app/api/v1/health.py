from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Health check", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
