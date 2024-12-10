import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.schemas.common import FilterParams, SearchJobApplication, SearchParams
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
)
from app.schemas.skill import SkillBase
from app.services.common import (
    get_job_application_by_id,
    get_professional_by_id,
    get_skill_by_name,
)
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.job_application_skill.job_application_skill import JobApplicationSkill
from app.sql_app.professional.professional import Professional
from app.sql_app.skill.skill import Skill

logger = logging.getLogger(__name__)


def get_all(
    filter_params: FilterParams,
    search_params: SearchJobApplication,
    db: Session,
) -> list[JobApplicationResponse]:
    """
    Retrieve all Job Applications that match the filtering parameters and keywords.

    Args:
        filer_params (FilterParams): Pydantic schema for filtering params.
        search_params (SearchJobApplication): Pydantic schema for search params.
        db (Session): The database session.
    Returns:
        list[JobApplicationResponse]: A list of Job Applications that are visible for Companies.
    """
    job_applications_query = (
        db.query(JobApplication)
        .join(Professional, JobApplication.professional_id == Professional.id)
        .filter(
            JobApplication.status == search_params.job_application_status,
        )
    )

    if search_params.skills:
        job_applications_query = (
            job_applications_query.join(JobApplicationSkill)
            .join(Skill)
            .filter(Skill.name.in_(search_params.skills))
        )
        logger.info("Filtered job applications by skills.")

    if search_params.order == "desc":
        job_applications_query.order_by(
            getattr(JobApplication, search_params.order_by).desc()
        )
    else:
        job_applications_query.order_by(
            getattr(JobApplication, search_params.order_by).asc()
        )
    logger.info(
        f"Order job applications based on search params order {search_params.order} and order_by {search_params.order_by}"
    )

    job_applications = (
        job_applications_query.offset(filter_params.offset)
        .limit(filter_params.limit)
        .all()
    )

    logger.info("Limited job applications based on offset and limit")

    return [
        JobApplicationResponse.create(job_application)
        for job_application in job_applications
    ]


def get_by_id(job_application_id: UUID, db: Session) -> JobApplicationResponse:
    """
    Fetches a Job Application by its ID.

    Args:
        job_application_id (UUID): The identifier of the Job application.
        db (Session): Database dependency.

    Returns:
        JobApplicationResponse: JobApplication reponse model.
    """

    job_application = get_job_application_by_id(
        job_application_id=job_application_id, db=db
    )

    return JobApplicationResponse.create(job_application)


def create(
    job_application_create: JobApplicationCreate,
    db: Session,
) -> JobApplicationResponse:
    """
    Create a new job application and add it to the database.

    Args:
        job_application_create (JobApplicationCreate): The data required to create a job application.
        db (Session): The database session to use for the operation.
    Returns:
        JobApplicationResponse: The response object containing the created job application details.
    """
    professional = get_professional_by_id(
        professional_id=job_application_create.professional_id, db=db
    )
    job_application = JobApplication(
        **job_application_create.model_dump(exclude={"skills", "status"}),
        status=job_application_create.status.name,
    )

    _add_skills(
        job_application=job_application,
        skills=job_application_create.skills,
        db=db,
    )

    professional.active_application_count += 1

    db.add(job_application)
    db.commit()
    db.refresh(job_application)

    return JobApplicationResponse.create(job_application=job_application)


def update(
    job_application_id: UUID,
    job_application_data: JobApplicationUpdate,
    db: Session,
) -> JobApplicationResponse:
    """
    Update a job application with the given data.

    Args:
        job_application_id (UUID): The unique identifier of the job application to update.
        job_application_data (JobApplicationUpdate): The data to update the job application with.
        db (Session): The database session to use for the update.

    Returns:
        JobApplicationResponse: The response object containing the updated job application details.

    Raises:
        ValueError: If the job application with the given ID does not exist.
    """
    job_application = get_job_application_by_id(
        job_application_id=job_application_id, db=db
    )
    new_skills = job_application_data.skills
    job_application_data = JobApplicationUpdate(
        **job_application_data.model_dump(), exclude={"skills"}
    )

    for attr, value in vars(job_application_data).items():
        if value is not None:
            setattr(job_application, attr, value)
            logger.info(
                f"Updated job application (id: {job_application_id}) {attr} to {value}"
            )

    # TODO: Update skills

    if (
        any(value is not None for value in vars(job_application_data).values())
        or new_skills
    ):
        job_application.updated_at = datetime.now()

    db.commit()
    db.refresh(job_application)

    logger.info(f"Job Application with id {job_application.id} updated")

    return JobApplicationResponse.create(job_application=job_application)


def _add_skills(
    job_application: JobApplication,
    skills: list[SkillBase],
    db: Session,
) -> None:
    """
    Adds a list of skills to a job application.

    Args:
        job_application (JobApplication): The job application to which the skills will be added.
        skills (list[SkillBase]): A list of skills to be added to the job application.
        db (Session): The database session used for querying and adding skills.
    """
    for skill in skills:
        skill_model = get_skill_by_name(skill_name=skill.name, db=db)
        job_application_skill = JobApplicationSkill(
            job_application_id=job_application, skill_id=skill_model.id, db=db
        )
        db.add(job_application_skill)
        logger.info(f"Added skill {skill.name} to job application {job_application.id}")
