from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    category_router,
    city_router,
    company_router,
    job_ad_router,
    job_application_router,
    match_router,
    professional_router,
    skill_router,
)

api_router = APIRouter()


api_router.include_router(
    category_router.router, prefix="/categories", tags=["Categories"]
)

api_router.include_router(city_router.router, prefix="/cities", tags=["Cities"])


api_router.include_router(skill_router.router, prefix="/skills", tags=["Skills"])


api_router.include_router(
    company_router.router, prefix="/companies", tags=["Companies"]
)


api_router.include_router(
    professional_router.router, prefix="/professionals", tags=["Professionals"]
)

api_router.include_router(job_ad_router.router, prefix="/job-ads", tags=["Job Ads"])


api_router.include_router(
    job_application_router.router, prefix="/job-applications", tags=["Job Applications"]
)


api_router.include_router(
    match_router.router, prefix="/match-requests", tags=["Match Requests"]
)
