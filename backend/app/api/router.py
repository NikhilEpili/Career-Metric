from fastapi import APIRouter

from app.api.v1 import assessments, auth, health, profiles

api_router = APIRouter()
api_router.include_router(health.router, prefix="/v1/health", tags=["health"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(profiles.router, prefix="/v1/profiles", tags=["profiles"])
api_router.include_router(assessments.router, prefix="/v1/assessments", tags=["assessments"])
