import io
import logging
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.common import FilterParams, MessageResponse, SearchParams
from app.schemas.job_ad import JobAdPreview
from app.schemas.job_application import JobApplicationResponse, JobSearchStatus
from app.schemas.match import MatchRequestAd
from app.schemas.professional import (
    PrivateMatches,
    ProfessionalCreate,
    ProfessionalResponse,
    ProfessionalUpdate,
)
from app.schemas.skill import SkillResponse
from app.services import match_service
from app.services.common import get_professional_by_id
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.match.match import Match
from app.sql_app.professional.professional import Professional
from app.sql_app.professional.professional_status import ProfessionalStatus

logger = logging.getLogger(__name__)


def get_all(
    db: Session,
    filter_params: FilterParams,
    search_params: SearchParams,
) -> list[ProfessionalResponse]:
    """
    Retrieve all active professionals from the database with optional filtering and sorting.

    Args:
        db (Session): The database session to use for the query.
        filter_params (FilterParams): Parameters for filtering the results, including offset and limit.
        search_params (SearchParams): Parameters for sorting the results, including order and order_by fields.

    Returns:
        list[ProfessionalResponse]: A list of ProfessionalResponse objects representing the active professionals.
    """
    professionals = (
        db.query(Professional)
        .filter(Professional.status == ProfessionalStatus.ACTIVE)
        .offset(filter_params.offset)
        .limit(filter_params.limit)
    )
    logger.info(
        f"Retrieved all professionals with status ACTIVE and filtered by offset {filter_params.offset} and limit {filter_params.limit}"
    )

    if search_params.order == "desc":
        professionals.order_by(getattr(Professional, search_params.order_by).desc())
    else:
        professionals.order_by(getattr(Professional, search_params.order_by).asc())
    logger.info(
        f"Order Professionals based on search params order {search_params.order} and order_by {search_params.order_by}"
    )

    return [
        ProfessionalResponse.create(professional=professional)
        for professional in professionals.all()
    ]


def get_by_id(professional_id: UUID, db: Session) -> ProfessionalResponse:
    """
    Retrieve a Professional profile by its ID.

    Args:
        professional_id (UUID): The identifier of the professional.
        db (Session): Database session dependency.

    Returns:
        ProfessionalResponse: The created professional profile response.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)

    matched_ads = (
        _get_matches(professional_id=professional_id, db=db)
        if not professional.has_private_matches
        else None
    )

    return ProfessionalResponse.create(
        professional=professional, matched_ads=matched_ads
    )


def create(
    professional_data: ProfessionalCreate,
    db: Session,
) -> ProfessionalResponse:
    """
    Create a new instance of the Professional model.

    Args:
        professional_data (ProfessionalCreate): Pydantic schema for collecting data.
        db (Session): Database dependency.

    Returns:
        Professional: Pydantic response model for Professional.
    """
    professional = Professional(
        **professional_data.model_dump(),
    )

    db.add(professional)
    db.commit()
    db.refresh(professional)
    logger.info(f"Professional with id {professional.id} created")

    return ProfessionalResponse.create(professional=professional)


def update(
    professional_id: UUID,
    professional_data: ProfessionalUpdate,
    db: Session,
) -> ProfessionalResponse:
    professional = get_professional_by_id(professional_id=professional_id, db=db)

    for attr, value in vars(professional_data).items():
        if value is not None:
            setattr(professional, attr, value)
            logger.info(
                f"Updated professional (id: {professional.id}) {attr} to {value}"
            )

    if any(value is not None for value in vars(professional_data).values()):
        professional.updated_at = datetime.now()

    db.commit()
    db.refresh(professional)

    return ProfessionalResponse.create(professional=professional)


def upload_photo(
    professional_id: UUID, photo: UploadFile, db: Session
) -> MessageResponse:
    """
    Uploads a photo for a professional and updates the professional's record in the database.
    Args:
        professional_id (UUID): The unique identifier of the professional.
        photo (UploadFile): The photo file to be uploaded.
        db (Session): The database session.
    Returns:
        MessageResponse: A response message indicating the result of the upload operation.
    """
    profesional = get_professional_by_id(professional_id=professional_id, db=db)
    profesional.photo = photo.file.read()
    profesional.updated_at = datetime.now()

    db.commit()
    logger.info(f"Uploaded photo for Professional with id {professional_id}")

    return MessageResponse(message="Photo successfully uploaded")


def download_photo(
    professional_id: UUID,
    db: Session,
) -> StreamingResponse:
    """
    Downloads the photo of a professional by their ID.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session to use for querying.

    Returns:
        StreamingResponse: A streaming response containing the photo in PNG format.

    Raises:
        HTTPException: If the professional does not have a photo, a 404 error is raised.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    photo = professional.photo
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Professional with id {professional_id} does not have a photo",
        )
    logger.info(f"Downloaded photo of Professional with id {professional_id}")

    return StreamingResponse(io.BytesIO(photo), media_type="image/png")


def upload_cv(professional_id: UUID, cv: UploadFile, db: Session) -> MessageResponse:
    """
    Uploads a CV for a professional and updates the professional's record in the database.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        cv (UploadFile): The CV file to be uploaded.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the operation.
    """
    profesional = get_professional_by_id(professional_id=professional_id, db=db)
    profesional.cv = cv.file.read()
    profesional.updated_at = datetime.now()

    db.commit()
    logger.info(f"Uploaded CV for Professional with id {professional_id}")

    return MessageResponse(message="CV successfully uploaded")


def download_cv(professional_id: UUID, db: Session) -> StreamingResponse:
    """
    Downloads the CV for a given professional.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session to use for querying.

    Returns:
        StreamingResponse: A streaming response containing the CV file.

    Raises:
        HTTPException: If the CV for the given professional ID is not found.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    cv = professional.cv
    if cv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV for Job Application with id {professional_id} not found",
        )

    return _generate_cv_response(professional=professional, cv=cv)


def delete_cv(professional_id: UUID, db: Session) -> MessageResponse:
    """
    Deletes the CV of a professional by setting the CV attribute to None and updating the updated_at timestamp.

    Args:
        professional_id (UUID): The unique identifier of the professional whose CV is to be deleted.
        db (Session): The database session used to interact with the database.

    Returns:
        MessageResponse: A response object containing a success message.

    Raises:
        ApplicationError: If the professional's CV is not found.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    if professional.cv is None:
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV for Job Application with id {professional_id} not found",
        )
    professional.cv = None
    professional.updated_at = datetime.now()

    db.commit()
    logger.info(f"Deleted CV of professional with id {professional_id}")

    return MessageResponse(message="CV deleted successfully")


def set_matches_status(
    professional_id: UUID,
    private_matches: PrivateMatches,
    db: Session,
) -> MessageResponse:
    """
    Set the match status for a professional.
    Args:
        professional_id (UUID): The unique identifier of the professional.
        private_matches (PrivateMatches): An object containing the status of the matches (private or public).
        db (Session): The database session.
    Returns:
        MessageResponse: A response message indicating the new status of the matches.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    professional.has_private_matches = private_matches.status

    db.commit()
    logger.info(
        f"Professional with id {professional_id} set matches as {'private' if private_matches.status else 'public'}"
    )

    return MessageResponse(
        message=f"Matches set as {'private' if private_matches.status else 'public'}"
    )


def get_by_username(username: str, db: Session) -> ProfessionalResponse:
    """
    Retrieve a professional by their username.

    Args:
        username (str): The username of the professional to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        ProfessionalResponse: The response object containing the professional's details.

    Raises:
        ApplicationError: If no professional with the given username is found.
    """
    professional = (
        db.query(Professional).filter(Professional.username == username).first()
    )
    if professional is None:
        raise ApplicationError(
            detail=f"User with username {username} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ProfessionalResponse.create(professional)


def get_applications(
    professional_id: UUID,
    application_status: JobSearchStatus,
    filter_params: FilterParams,
    db: Session,
) -> list[JobApplicationResponse]:
    """
    Retrieve job applications for a given professional based on the application status and filter parameters.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        application_status (JobSearchStatus): The status of the job applications to filter by.
        filter_params (FilterParams): Parameters to filter the job applications (e.g., offset, limit).
        db (Session): The database session to use for querying.

    Returns:
        list[JobApplicationResponse]: A list of job application responses matching the criteria.

    Raises:
        ApplicationError: If the professional has set their matches to private and the application status is 'MATCHED'.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    if (
        professional.has_private_matches
        and application_status.value == JobSearchStatus.MATCHED
    ):
        raise ApplicationError(
            detail="Professional has set their Matches to Private",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    search_status = JobStatus(application_status.value)

    applications = (
        db.query(JobApplication)
        .filter(
            JobApplication.professional_id == professional_id,
            JobApplication.status == search_status,
        )
        .offset(filter_params.offset)
        .limit(filter_params.limit)
        .all()
    )

    return [
        JobApplicationResponse.create(
            professional=professional, job_application=application, db=db
        )
        for application in applications
    ]


def get_skills(professional_id: UUID, db: Session) -> list[SkillResponse]:
    """
    Retrieve the skills associated with a professional's job applications.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session used to query the data.

    Returns:
        list[SkillResponse]: A list of SkillResponse objects representing the skills.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)
    professional_job_applications = professional.job_applications
    skills = {
        skill.skill
        for application in professional_job_applications
        for skill in application.skills
    }

    return [
        SkillResponse(id=skill.id, name=skill.name, category_id=skill.category_id)
        for skill in skills
    ]


def get_match_requests(professional_id: UUID, db: Session) -> list[MatchRequestAd]:
    """
    Fetches Match Requests for the given Professional.

    Args:
        professional_id (UUID): The identifier of the Professional.
        db (Session): Database dependency.

    Returns:
        list[MatchRequest]: List of Pydantic models containing basic information about the match request.
    """
    professional = get_professional_by_id(professional_id=professional_id, db=db)

    match_requests = match_service.get_match_requests_for_professional(
        professional_id=professional.id, db=db
    )

    return match_requests


def _get_matches(professional_id: UUID, db: Session) -> list[JobAdPreview]:
    """
    Retrieve a list of job advertisements that match a given professional.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session used for querying.

    Returns:
        list[JobAdPreview]: A list of job advertisement previews that match the professional.
    """
    ads: list[JobAd] = (
        db.query(JobAd)
        .join(Match, Match.job_ad_id == JobAd.id)
        .join(JobApplication, Match.job_application_id == JobApplication.id)
        .filter(
            JobApplication.professional_id == professional_id,
            JobApplication.status == JobStatus.MATCHED,
        )
        .all()
    )

    return [JobAdPreview.create(ad) for ad in ads]


def _generate_cv_response(professional: Professional, cv: bytes) -> StreamingResponse:
    """
    Generates a streaming response for downloading a CV as a PDF file.

    Args:
        professional (Professional): An instance of the Professional class containing the professional's details.
        cv (bytes): The CV content in bytes.

    Returns:
        StreamingResponse: A response object that streams the CV as a PDF file with appropriate headers.
    """
    filename = f"{professional.first_name}_{professional.last_name}_CV.pdf"
    response = StreamingResponse(io.BytesIO(cv), media_type="application/pdf")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    return response
