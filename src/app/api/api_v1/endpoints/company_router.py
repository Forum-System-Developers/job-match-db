from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.schemas.common import FilterParams
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services import company_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get(
    "/",
    description="Retrieve all companies.",
)
def get_all_companies(
    filter_params: FilterParams = Depends(), db: Session = Depends(get_db)
) -> JSONResponse:
    def _get_all_companies():
        return company_service.get_all(filter_params=filter_params, db=db)

    return process_request(
        get_entities_fn=_get_all_companies,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="No companies found",
    )


@router.get(
    "/by-username/{username}",
    description="Retrieve company by username.",
)
def get_company_by_username(
    username: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_company_by_username():
        return company_service.get_by_username(username=username, db=db)

    return process_request(
        get_entities_fn=_get_company_by_username,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Company with username {username} not found",
    )


@router.get(
    "/by-email/{email}",
    description="Retrieve company by email.",
)
def get_company_by_email(
    email: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_company_by_email():
        return company_service.get_by_email(email=email, db=db)

    return process_request(
        get_entities_fn=_get_company_by_email,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Company with email {email} not found",
    )


@router.get(
    "/by-phone-number/{phone_number}",
    description="Retrieve company by phone number.",
)
def get_company_by_phone(
    phone_number: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_company_by_phone():
        return company_service.get_by_phone_number(phone_number=phone_number, db=db)

    return process_request(
        get_entities_fn=_get_company_by_phone,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Company with phone number {phone_number} not found",
    )


@router.get(
    "/{company_id}",
    description="Retrieve a company by its unique identifier.",
)
def get_company_by_id(company_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    def _get_company_by_id():
        return company_service.get_by_id(company_id=company_id, db=db)

    return process_request(
        get_entities_fn=_get_company_by_id,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Company with id {company_id} not found",
    )


@router.post(
    "/",
    description="Create a new company.",
)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _create_company():
        return company_service.create(company_data=company_data, db=db)

    return process_request(
        get_entities_fn=_create_company,
        status_code=status.HTTP_201_CREATED,
        not_found_err_msg="Company not created",
    )


@router.put(
    "/{company_id}",
    description="Update the current company.",
)
def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _update_company():
        return company_service.update(
            company_id=company_id,
            company_data=company_data,
            db=db,
        )

    return process_request(
        get_entities_fn=_update_company,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Company with id {company_id} not updated",
    )


@router.post(
    "/{company_id}/logo",
    description="Upload a logo for the current company.",
)
def upload_logo(
    company_id: UUID,
    logo: UploadFile = File(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _upload_logo():
        return company_service.upload_logo(
            company_id=company_id,
            logo=logo,
            db=db,
        )

    return process_request(
        get_entities_fn=_upload_logo,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not upload logo",
    )


@router.get(
    "/{company_id}/logo",
    description="Download the logo of the current company",
)
def download_logo(
    company_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    return company_service.download_logo(company_id=company_id, db=db)


@router.delete(
    "/{company_id}/logo",
    description="Delete the logo of the current company.",
)
def delete_logo(
    company_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _delete_logo():
        return company_service.delete_logo(company_id=company_id, db=db)

    return process_request(
        get_entities_fn=_delete_logo,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not delete logo",
    )
