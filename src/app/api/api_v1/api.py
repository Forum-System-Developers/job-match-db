from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    category_router,
    city_router,
    professional_router,
    skill_router,
)

api_router = APIRouter()


api_router.include_router(
    category_router.router, prefix="/categories", tags=["Categories"]
)

api_router.include_router(city_router.router, prefix="/cities", tags=["Cities"])


api_router.include_router(skill_router.router, prefix="/skills", tags=["Skills"])


api_router.include_router(skill_router.router, prefix="/skills", tags=["Skills"])


api_router.include_router(
    professional_router.router, prefix="/professionals", tags=["Professionals"]
)
