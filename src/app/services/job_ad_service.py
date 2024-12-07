import logging
from datetime import datetime
from uuid import UUID

from fastapi import status
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Query, Session, aliased

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.common import FilterParams, JobAdSearchParams, MessageResponse
from app.schemas.job_ad import JobAdCreate, JobAdResponse, JobAdUpdate
from app.services import company_service
from app.services.common import get_company_by_id, get_job_ad_by_id, get_skill_by_id
from app.sql_app import JobAd, JobAdSkill, Skill
from app.sql_app.job_ad.job_ad_status import JobAdStatus

logger = logging.getLogger(__name__)


def get_all(
    filter_params: FilterParams,
    search_params: JobAdSearchParams,
    db: Session,
) -> list[JobAdResponse]:
    """
    Retrieve all job advertisements.

    Args:
        db (Session): The database session used to query the job advertisements.
        skip (int): The number of job advertisements to skip.
        limit (int): The maximum number of job advertisements to retrieve.

    Returns:
        list[JobAdResponse]: The list of job advertisements.
    """
    job_ads = _search_job_ads(search_params=search_params, db=db)
    job_ads = job_ads.offset(filter_params.offset).limit(filter_params.limit)
    job_ads_list = job_ads.all()
    logger.info(f"Retrieved {len(job_ads_list)} job ads")

    return [JobAdResponse.create(job_ad) for job_ad in job_ads_list]


def get_by_id(id: UUID, db: Session) -> JobAdResponse:
    """
    Retrieve a job advertisement by its unique identifier.

    Args:
        id (UUID): The unique identifier of the job advertisement.
        db (Session): The database session used to query the job advertisement.

    Returns:
        JobAdResponse: The job advertisement if found, otherwise None.
    """
    job_ad = get_job_ad_by_id(job_ad_id=id, db=db)
    logger.info(f"Retrieved job ad with id {id}")

    return JobAdResponse.create(job_ad)


def create(
    job_ad_data: JobAdCreate,
    db: Session,
) -> JobAdResponse:
    """
    Create a new job advertisement.

    Args:
        job_ad_data (JobAdCreate): The data required to create a new job advertisement.
        db (Session): The database session used to create the job advertisement.

    Returns:
        JobAdResponse: The created job advertisement.

    Raises:
        ApplicationError: If the company or city is not found.
    """
    company = get_company_by_id(company_id=job_ad_data.company_id, db=db)
    job_ad = JobAd(**job_ad_data.model_dump(), status=JobAdStatus.ACTIVE)

    company.active_job_count += 1

    db.add(job_ad)
    db.commit()
    db.refresh(job_ad)
    logger.info(f"Created job ad with id {job_ad.id}")

    return JobAdResponse.create(job_ad)


def update(
    job_ad_id: UUID,
    job_ad_data: JobAdUpdate,
    db: Session,
) -> JobAdResponse:
    """
    Update a job advertisement with the given data.

    Args:
        job_ad_id (UUID): The unique identifier of the job advertisement to update.
        job_ad_data (JobAdUpdate): The data to update the job advertisement with.
        db (Session): The database session to use for the update.

    Returns:
        JobAdResponse: The response object containing the updated job advertisement data.
    """
    job_ad = get_job_ad_by_id(job_ad_id=job_ad_id, db=db)

    for attr, value in vars(job_ad_data).items():
        if value is not None:
            setattr(job_ad, attr, value)
            logger.info(f"Updated job ad (id: {job_ad_id}) {attr} to {value}")

    if any(value is not None for value in vars(job_ad_data).values()):
        job_ad.updated_at = datetime.now()

    db.commit()
    db.refresh(job_ad)

    return JobAdResponse.create(job_ad)


def add_skill_requirement(
    job_ad_id: UUID,
    skill_id: UUID,
    db: Session,
) -> MessageResponse:
    """
    Adds a skill requirement to a job advertisement.

    Args:
        job_ad_id (UUID): The unique identifier of the job advertisement.
        skill_id (UUID): The unique identifier of the skill to be added.
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the operation.

    Raises:
        ApplicationError: If the skill is already added to the job advertisement.
    """
    job_ad = get_job_ad_by_id(job_ad_id=job_ad_id, db=db)
    skill = get_skill_by_id(skill_id=skill_id, db=db)

    if skill in job_ad.skills:
        logger.error(
            f"Skill with id {skill_id} already added to job ad with id {job_ad_id}"
        )
        raise ApplicationError(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Skill with id {skill_id} already added to job ad with id {job_ad_id}",
        )

    job_ad_skill = JobAdSkill(
        job_ad_id=job_ad_id,
        skill_id=skill_id,
    )

    db.add(job_ad_skill)
    db.commit()
    db.refresh(job_ad_skill)
    logger.info(f"Added skill with id {skill_id} to job ad with id {job_ad_id}")

    return MessageResponse(message="Skill added to job ad")


def _search_job_ads(search_params: JobAdSearchParams, db: Session) -> Query[JobAd]:
    """
    Searches for job advertisements based on the provided search parameters.
    Args:
        search_params (JobAdSearchParams): The parameters to filter job advertisements.
        db (Session): The database session to use for querying.
    Returns:
        list[JobAd]: A list of job advertisements that match the search criteria.
    """
    job_ads = db.query(JobAd)

    if search_params.company_id:
        job_ads = job_ads.filter(JobAd.company_id == search_params.company_id)
        logger.info(
            f"Searching for job ads with company_id: {search_params.company_id}"
        )

    if search_params.title:
        job_ads = job_ads.filter(JobAd.title.ilike(f"%{search_params.title}%"))
        logger.info(f"Searching for job ads with title: {search_params.title}")

    if search_params.location_id:
        job_ads = job_ads.filter(JobAd.location_id == search_params.location_id)
        logger.info(
            f"Searching for job ads with location_id: {search_params.location_id}"
        )

    if search_params.job_ad_status:
        job_ads = job_ads.filter(JobAd.status == search_params.job_ad_status)
        logger.info(f"Searching for job ads with status: {search_params.job_ad_status}")

    job_ads = _filter_by_salary(job_ads=job_ads, search_params=search_params)
    job_ads = _filter_by_skills(job_ads=job_ads, search_params=search_params, db=db)
    job_ads = _order_by(job_ads=job_ads, search_params=search_params)

    return job_ads


def _filter_by_salary(
    job_ads: Query[JobAd],
    search_params: JobAdSearchParams,
) -> Query[JobAd]:
    """
    Filters job advertisements by salary range.

    Args:
        job_ads (Query[JobAd]): The query object containing the job advertisements.
        search_params (JobAdSearchParams): The search parameters to filter the job advertisements.

    Returns:
        Query[JobAd]: The filtered query object containing the job advertisements.
    """
    min_salary = search_params.min_salary or 0
    max_salary = search_params.max_salary or float("inf")
    logger.info(
        f"Filtering job ads with salary range: {search_params.min_salary} - {search_params.max_salary} \
            and threshold: {search_params.salary_threshold}"
    )

    job_ads = job_ads.filter(
        (JobAd.min_salary - search_params.salary_threshold) <= max_salary
    )
    logger.info(f"Filtering job ads with max_salary: {max_salary}")

    job_ads = job_ads.filter(
        (JobAd.max_salary + search_params.salary_threshold) >= min_salary
    )
    logger.info(f"Filtering job ads with min_salary: {min_salary}")

    return job_ads


def _filter_by_skills(
    job_ads: Query[JobAd],
    search_params: JobAdSearchParams,
    db: Session,
) -> Query[JobAd]:
    """
    Filters job advertisements based on the provided skills in the search parameters.

    Args:
        job_ads (Query[JobAd]): The initial query of job advertisements.
        search_params (JobAdSearchParams): The search parameters containing the skills and threshold.
        db (Session): The database session.

    Returns:
        Query[JobAd]: The filtered query of job advertisements.

    Notes:
        - If the number of skills in the search parameters is equal to the threshold, skill filtering is skipped.
        - The function filters job advertisements that have at least the required number of matching skills from the provided skill list.
    """
    if search_params.skills:
        num_skills = len(search_params.skills)
        threshold = search_params.skills_threshold
        required_matches = max(num_skills - threshold, 0)

        if required_matches == 0:
            logger.info(
                f"Threshold equals to the number of skills({num_skills}), skipping skill filtering."
            )
            return job_ads

        skill_alias = aliased(Skill)

        skill_match_count = (
            db.query(JobAd.id.label("job_ad_id"))
            .join(JobAd.skills)
            .filter(
                func.lower(skill_alias.name).in_(
                    [skill.lower() for skill in search_params.skills]
                )
            )
            .group_by(JobAd.id)
            .having(func.count(func.distinct(skill_alias.id)) >= required_matches)
            .subquery()
        )

        job_ads = job_ads.join(
            skill_match_count, JobAd.id == skill_match_count.c.job_ad_id
        )
        logger.info(
            f"Searching for job ads with at least {required_matches} skills from the provided skill list: {search_params.skills}"
        )

    return job_ads


def _order_by(
    job_ads: Query[JobAd],
    search_params: JobAdSearchParams,
) -> Query[JobAd]:
    """
    Orders job advertisements based on the provided search parameters.

    Args:
        job_ads (Query[JobAd]): The query object containing the job advertisements.
        search_params (JobAdSearchParams): The search parameters to order the job advertisements.

    Returns:
        Query[JobAd]: The ordered query object containing the job advertisements.
    """
    order_by_column = getattr(JobAd, search_params.order_by, None)

    if order_by_column is not None:
        if search_params.order == "asc":
            job_ads = job_ads.order_by(asc(order_by_column))
            logger.info(
                f"Ordering job ads by {search_params.order_by} in ascending order"
            )
        else:
            job_ads = job_ads.order_by(desc(order_by_column))
            logger.info(
                f"Ordering job ads by {search_params.order_by} in descending order"
            )

    return job_ads
