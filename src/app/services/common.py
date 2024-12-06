import logging
from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ApplicationError
from app.sql_app import Company, JobAd, Professional, Skill

logger = logging.getLogger(__name__)


def get_company_by_id(company_id: UUID, db: Session) -> Company:
    """
    Ensure that a company with the given ID exists in the database.

    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session.

    Returns:
        Company: The company object with the given ID.

    Raises:
        ApplicationError: If no company is found with the given ID.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        logger.error(f"No company found with id {company_id}")
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No company found with id {company_id}",
        )
    return company


def get_job_ad_by_id(job_ad_id: UUID, db: Session) -> JobAd:
    """
    Retrieve a job advertisement by its unique identifier.

    Args:
        job_ad_id (UUID): The unique identifier of the job advertisement.
        db (Session): The database session used to query the job advertisement.

    Returns:
        JobAd: The job advertisement if found, otherwise None.
    """
    job_ad = db.query(JobAd).get(job_ad_id)
    if job_ad is None:
        logger.error(f"Job ad with id {job_ad_id} not found")
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job ad with id {job_ad_id} not found",
        )

    return job_ad


def get_professional_by_id(professional_id: UUID, db: Session) -> Professional:
    """
    Retrieves an instance of the Professional model or None.

    Args:
        professional_id (UUID): The identifier of the Professional.
        db (Session): Database dependency.

    Returns:
        Professional: SQLAlchemy model for Professional.

    Raises:
        ApplicationError: If the professional with the given id is
            not found in the database.
    """
    professional = (
        db.query(Professional).filter(Professional.id == professional_id).first()
    )
    if professional is None:
        logger.error(f"Professional with id {professional_id} not found")
        raise ApplicationError(
            detail=f"Professional with id {professional_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    logger.info(f"Professional with id {professional_id} fetched")
    return professional


def get_skill_by_id(
    skill_id: UUID,
    db: Session,
) -> Skill:
    """
    Retrieve a skill by its unique identifier and category.

    Args:
        skill_id (UUID): The unique identifier of the skill to retrieve.
        db (Session): The database session used to query the skill.

    Returns:
        Skill: The Skill object representing the retrieved skill.

    Raises:
        ApplicationError: If no skill is found with the given ID and category.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with id {skill_id} not found",
        )

    return skill