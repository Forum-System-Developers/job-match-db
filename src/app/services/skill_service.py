from uuid import UUID

from sqlalchemy.orm import Session

from app.schemas.skill import SkillCreate, SkillResponse
from app.sql_app.skill.skill import Skill


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
