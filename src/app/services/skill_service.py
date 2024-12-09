import logging
from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.skill import SkillCreate, SkillResponse
from app.sql_app.pending_skill.pending_skill import PendingSkill
from app.sql_app.skill.skill import Skill

logger = logging.getLogger(__name__)


def get_all_for_category(category_id: UUID, db: Session) -> list[SkillResponse]:
    """
    Retrieve all skills for a given category.

    Args:
        category_id (UUID): The identifier of the category for which to retrieve the skills.
        db (Session): The database session used to query the skills.

    Returns:
        list[SkillResponse]: A list of SkillResponse objects representing all skills for the given category.
    """
    skills = db.query(Skill).filter(Skill.category_id == category_id).all()
    return [SkillResponse.create(skill) for skill in skills]


def get_by_id(skill_id: UUID, db: Session) -> SkillResponse:
    """
    Retrieve a skill by its unique identifier.

    Args:
        skill_id (UUID): The unique identifier of the skill to retrieve.
        db (Session): The database session used to query the skill.

    Returns:
        SkillResponse: A SkillResponse object representing the retrieved skill.

    Raises:
        ApplicationError: If no skill is found with the given ID.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with id {skill_id} not found",
        )

    return SkillResponse.create(skill)


def create(skill_data: SkillCreate, db: Session) -> SkillResponse:
    """
    Create a new skill in the database.

    Args:
        skill_data (dict): The data representing the skill to be created.
        db (Session): The database session used to create the skill.

    Returns:
        SkillResponse: A SkillResponse object representing the created skill.
    """
    skill = Skill(**skill_data.model_dump())

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return SkillResponse.create(skill)


def create_pending_skill(
    company_id: UUID,
    skill_data: SkillCreate,
    db: Session,
) -> SkillResponse:
    """
    Creates a pending skill entry in the database.

    Args:
        company_id (UUID): The ID of the company submitting the skill.
        skill_data (SkillCreate): The data of the skill to be created.
        db (Session): The database session.

    Returns:
        SkillResponse: The response containing the details of the created pending skill.

    Raises:
        ApplicationError: If the skill already exists in the database.
    """
    skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
    if skill is not None:
        raise ApplicationError(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Skill with name {skill_data.name} already exists",
        )

    pending_skill = PendingSkill(
        name=skill_data.name,
        category_id=skill_data.category_id,
        submitted_by=company_id,
    )

    db.add(pending_skill)
    db.commit()
    db.refresh(pending_skill)

    logger.info(f"Pending skill {pending_skill.name} created")

    return SkillResponse(
        id=pending_skill.id,
        name=pending_skill.name,
        category_id=pending_skill.category_id,
    )
