import io
import logging
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.common import FilterParams, MessageResponse
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.common import get_company_by_id
from app.sql_app.company.company import Company

logger = logging.getLogger(__name__)


def get_all(filter_params: FilterParams, db: Session) -> list[CompanyResponse]:
    """
    Retrieve a list of companies from the database based on the provided filter parameters.

    Args:
        filter_params (FilterParams): The parameters to filter the companies, including offset and limit.
        db (Session): The database session used to query the companies.

    Returns:
        list[CompanyResponse]: A list of CompanyResponse objects representing the retrieved companies.
    """
    companies = (
        db.query(Company).offset(filter_params.offset).limit(filter_params.limit).all()
    )
    logger.info(f"Retrieved {len(companies)} companies")

    return [CompanyResponse.create(company) for company in companies]


def get_by_id(company_id: UUID, db: Session) -> CompanyResponse:
    """
    Retrieve a company by its ID.

    Args:
        db (Session): The database session to use for the query.
        company_id (int): The ID of the company to retrieve.

    Returns:
        CompanyResponse: The response object containing the company details.

    Raises:
        ApplicationError: If no company is found with the given ID.
    """
    company = get_company_by_id(company_id=company_id, db=db)
    logger.info(f"Retrieved company with id {company_id}")

    return CompanyResponse.create(company)


def get_by_username(username: str, db: Session) -> CompanyResponse:
    """
    Retrieve a company by its username.

    Args:
        username (str): The username of the company to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        User: A User object representing the retrieved company.

    Raises:
        ApplicationError: If no company with the given username is found.
    """
    company = db.query(Company).filter(Company.username == username).first()
    if company is None:
        logger.error(f"Company with username {username} not found")
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with username {username} not found",
        )
    logger.info(f"Retrieved company with username {username}")

    return CompanyResponse.create(company)


def get_by_email(email: str, db: Session) -> CompanyResponse:
    """
    Retrieve a company by its email.

    Args:
        email (str): The email of the company to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        User: A User object representing the retrieved company.

    Raises:
        ApplicationError: If no company with the given email is found.
    """
    company = db.query(Company).filter(Company.email == email).first()
    if company is None:
        logger.error(f"Company with email {email} not found")
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with email {email} not found",
        )
    logger.info(f"Retrieved company with email {email}")

    return CompanyResponse.create(company)


def get_by_phone_number(phone_number: str, db: Session) -> CompanyResponse:
    """
    Retrieve a company by its phone number.

    Args:
        phone_number (str): The phone number of the company to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        User: A User object representing the retrieved company.

    Raises:
        ApplicationError: If no company with the given phone number is found.
    """
    company = db.query(Company).filter(Company.phone_number == phone_number).first()
    if company is None:
        logger.error(f"Company with phone number {phone_number} not found")
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with phone number {phone_number} not found",
        )
    logger.info(f"Retrieved company with phone number {phone_number}")

    return CompanyResponse.create(company)


def create(company_data: CompanyCreate, db: Session) -> CompanyResponse:
    """
    Create a new company record in the database.

    Args:
        company_data (CompanyCreate): The data required to create a new company.
        db (Session): The database session to use for the operation.

    Returns:
        CompanyResponse: The response object containing the created company details.
    """
    company = Company(
        **company_data.model_dump(),
    )

    db.add(company)
    db.commit()
    db.refresh(company)
    logger.info(f"Created company with id {company.id}")

    return CompanyResponse.create(company)


def update(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session,
) -> CompanyResponse:
    """
    Update an existing company in the database.

    Args:
        company_id (UUID): The unique identifier of the company to update.
        company_data (CompanyCreate): The data to update the company with.
        db (Session): The database session to use for the operation.

    Returns:
        CompanyResponse: The response object containing the updated company's details.
    """
    company = get_company_by_id(company_id=company_id, db=db)
    for attr, value in vars(company_data).items():
        if value is not None:
            setattr(company, attr, value)
            logger.info(f"Updated company (id: {company.id}) {attr} to {value}")

    if any(value is not None for value in vars(company_data).values()):
        company.updated_at = datetime.now()

    db.commit()
    db.refresh(company)

    return CompanyResponse.create(company)


def upload_logo(company_id: UUID, logo: UploadFile, db: Session) -> MessageResponse:
    """
    Uploads a logo for a specified company.

    Args:
        company_id (UUID): The unique identifier of the company.
        logo (UploadFile): The logo file to be uploaded.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the upload operation.
    """
    company = get_company_by_id(company_id=company_id, db=db)
    company.logo = logo.file.read()
    company.updated_at = datetime.now()
    db.commit()
    logger.info(f"Uploaded logo for company with id {company_id}")

    return MessageResponse(message="Logo uploaded successfully")


def download_logo(company_id: UUID, db: Session) -> StreamingResponse:
    """
    Downloads the logo of a company.
    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session.
    Returns:
        StreamingResponse: A streaming response containing the company's logo.
    Raises:
        ApplicationError: If the company does not have a logo or does not exist.
    """
    company = get_company_by_id(company_id=company_id, db=db)
    logo = company.logo
    if logo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} does not have a logo",
        )
    logger.info(f"Downloaded logo of company with id {company_id}")

    return StreamingResponse(io.BytesIO(logo), media_type="image/png")


def delete_logo(company_id: UUID, db: Session) -> MessageResponse:
    """
    Deletes the logo of a company.

    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session.

    Returns:
        MessageResponse: A response message indicating the result of the deletion operation.
    """
    company = get_company_by_id(company_id=company_id, db=db)
    company.logo = None
    company.updated_at = datetime.now()

    db.commit()
    logger.info(f"Deleted logo of company with id {company_id}")

    return MessageResponse(message="Logo deleted successfully")
