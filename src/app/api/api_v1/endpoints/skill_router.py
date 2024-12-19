from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.skill import SkillCreate
from app.services import skill_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get(
    "/categories/{category_id}/",
    description="Retrieve all skills for a category.",
)
def get_all_skills_for_category(
    category_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_all_skills_for_category():
        return skill_service.get_all_for_category(category_id=category_id, db=db)

    return process_request(
        get_entities_fn=_get_all_skills_for_category,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"No skills found for category with id {category_id}",
        db=db,
    )


@router.get(
    "/{skill_id}",
    description="Retrieve a skill by its unique identifier.",
)
def get_skill_by_id(
    skill_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_skill_by_id():
        return skill_service.get_by_id(skill_id=skill_id, db=db)

    return process_request(
        get_entities_fn=_get_skill_by_id,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Skill with id {skill_id} not found",
        db=db,
    )


@router.post(
    "/",
    description="Create a new skill.",
)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _create_skill():
        return skill_service.create(skill_data=skill_data, db=db)

    return process_request(
        get_entities_fn=_create_skill,
        status_code=status.HTTP_201_CREATED,
        not_found_err_msg="Error creating skill",
        db=db,
    )
