import logging
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.schemas.common import FilterParams, MessageResponse
from app.schemas.match import (
    MatchRequestAd,
    MatchRequestApplication,
    MatchRequestCreate,
    MatchRequestUpdate,
    MatchResponse,
)
from app.services.common import get_match_by_id
from app.sql_app import Match
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_ad.job_ad_status import JobAdStatus
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.match.match_status import MatchStatus
from app.sql_app.professional.professional_status import ProfessionalStatus

logger = logging.getLogger(__name__)


def create(
    match_request_data: MatchRequestCreate,
    db: Session,
) -> MessageResponse:
    """
    Create a match request for a professional.

    Args:
        match_request_data (MatchRequestCreate): The match request data to create a match request from.
        db (Session): The database session.

    Returns:
        MatchResponse: The created match request.
    """
    job_ad_id = match_request_data.job_ad_id
    job_application_id = match_request_data.job_application_id
    status = match_request_data.status

    match_request = Match(
        job_ad_id=job_ad_id,
        job_application_id=job_application_id,
        status=status,
    )
    logger.info(
        f"Match created for JobApplication id{job_application_id} and JobAd id {job_ad_id} with status {status}"
    )
    db.add(match_request)
    db.commit()
    db.refresh(match_request)

    return MessageResponse(message="Match request created successfully")


def get_by_id(
    job_ad_id: UUID,
    job_application_id: UUID,
    db: Session,
) -> MatchResponse:
    """
    Retrieve a match request by job ad and job application.

    Args:
        job_ad_id (UUID): The ID of the job ad.
        job_application_id (UUID): The ID of the job application.
        db (Session): The database session.

    Returns:
        MatchResponse: The retrieved match request.
    """
    match = get_match_by_id(
        job_ad_id=job_ad_id,
        job_application_id=job_application_id,
        db=db,
    )

    return MatchResponse.create(match)


def update_status(
    job_ad_id: UUID,
    job_application_id: UUID,
    match_request_data: MatchRequestUpdate,
    db: Session,
) -> MessageResponse:
    """
    Update the status of a match request.

    Args:
        job_ad_id (UUID): The ID of the job advertisement.
        job_application_id (UUID): The ID of the job application.
        match_request_data (MatchRequestUpdate): The data containing the new status for the match request.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the update operation.
    """
    match = get_match_by_id(
        job_ad_id=job_ad_id,
        job_application_id=job_application_id,
        db=db,
    )

    match.status = match_request_data.status
    db.commit()

    return MessageResponse(message="Match request updated successfully")


def accept_match_request(
    job_ad_id: UUID,
    job_application_id: UUID,
    db: Session,
) -> MessageResponse:
    """
    Accept a match request.

    Args:
        job_ad_id (UUID): The ID of the job advertisement.
        job_application_id (UUID): The ID of the job application.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the operation.
    """

    match = get_match_by_id(
        job_ad_id=job_ad_id,
        job_application_id=job_application_id,
        db=db,
    )

    job_application = match.job_application
    job_ad = match.job_ad
    professional = job_application.professional
    company = job_ad.company

    match.status = MatchStatus.ACCEPTED
    professional.status = ProfessionalStatus.BUSY
    job_application.status = JobStatus.MATCHED
    job_ad.status = JobAdStatus.ARCHIVED

    professional.active_application_count -= 1
    company.successfull_matches_count += 1

    db.commit()
    logger.info(
        f"Updated statuses for JobAplication with id {job_application_id}, JobAd id {job_ad_id}, Professional with id {professional.id}"
    )

    return MessageResponse(message="Match request accepted successfully")


def get_match_requests_for_job_application(
    job_application_id: UUID,
    filter_params: FilterParams,
    db: Session,
) -> list[MatchRequestAd]:
    """
    Retrieve match requests for a job advertisement.

    Args:
        job_ad_id (UUID): The ID of the job advertisement.
        db (Session): The database session.

    Returns:
        list[MatchResponse]: A list of match requests for the job advertisement.
    """
    requests = (
        db.query(Match, JobAd)
        .join(JobAd, Match.job_ad_id == JobAd.id)
        .filter(
            and_(
                Match.job_application_id == job_application_id,
                Match.status == MatchStatus.REQUESTED_BY_JOB_AD,
            )
        )
        .offset(filter_params.offset)
        .limit(filter_params.limit)
        .all()
    )

    return [
        MatchRequestAd.create_response(match=match, job_ad=job_ad)
        for (match, job_ad) in requests
    ]


def get_match_requests_for_professional(
    professional_id: UUID,
    db: Session,
) -> list[MatchRequestAd]:
    """
    Retrieve match requests for a given professional.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session used for querying.

    Returns:
        list[MatchRequestAd]: A list of MatchRequestAd objects representing
        the match requests for the professional.
    """
    result = (
        db.query(Match, JobAd)
        .join(JobApplication, Match.job_application_id == JobApplication.id)
        .join(JobAd, Match.job_ad_id == JobAd.id)
        .filter(
            JobApplication.professional_id == professional_id,
            JobApplication.status == JobStatus.ACTIVE,
            Match.status == MatchStatus.REQUESTED_BY_JOB_AD,
        )
        .all()
    )

    return [
        MatchRequestAd.create_response(match=match, job_ad=ad) for (match, ad) in result
    ]


def get_match_requests_for_company(
    company_id: UUID,
    filter_params: FilterParams,
    db: Session,
) -> list[MatchRequestApplication]:
    """
    Retrieve match requests for a given company.

    Args:
        company_id (UUID): The unique identifier of the company.
        filter_params (FilterParams): The filter parameters to apply to the query.
        db (Session): The database session used for querying.

    Returns:
        list[MatchRequestApplication]: A list of MatchRequestApplication objects representing
        the match requests for the company.
    """
    requests = (
        db.query(Match, JobApplication)
        .join(Match.job_application)
        .join(Match.job_ad)
        .filter(
            and_(
                JobAd.company_id == company_id,
                Match.status == MatchStatus.REQUESTED_BY_JOB_APP,
            )
        )
        .offset(filter_params.offset)
        .limit(filter_params.limit)
        .all()
    )

    logger.info(f"Retrieved {len(requests)} requests for company with id {company_id}")

    return [
        MatchRequestApplication.create_response(match, job_application)
        for (match, job_application) in requests
    ]


def get_job_ad_received_matches(
    job_ad_id: UUID,
    db: Session,
) -> list[MatchResponse]:
    """
    Retrieve match requests for a given job advertisement.

    Args:
        job_ad_id (UUID): The unique identifier of the job advertisement.
        db (Session): The database session used for querying.

    Returns:
        list[MatchResponse]: A list of MatchResponse objects representing
        the match requests for the job advertisement
    """
    requests = requests = (
        db.query(Match)
        .join(Match.job_ad)
        .filter(
            and_(
                JobAd.id == job_ad_id, Match.status == MatchStatus.REQUESTED_BY_JOB_APP
            )
        )
        .all()
    )
    logger.info(f"Retrieved {len(requests)} requests for job ad with id {job_ad_id}")

    return [MatchResponse.create(request) for request in requests]


def get_job_ad_sent_matches(
    job_ad_id: UUID,
    db: Session,
) -> list[MatchResponse]:
    """
    Retrieve match requests sent by a given job advertisement.

    Args:
        job_ad_id (UUID): The unique identifier of the job advertisement.
        db (Session): The database session used for querying.

    Returns:
        list[MatchResponse]: A list of MatchResponse objects representing
        the match requests sent by the job advertisement
    """
    requests = (
        db.query(Match)
        .filter(
            and_(
                Match.job_ad_id == job_ad_id,
                Match.status == MatchStatus.REQUESTED_BY_JOB_AD,
            )
        )
        .all()
    )

    logger.info(
        f"Retrieved {len(requests)} sent requests for job ad with id {job_ad_id}"
    )

    return [MatchResponse.create(request) for request in requests]
