from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.schemas.common import FilterParams, SearchParams
from app.schemas.job_application import JobSearchStatus
from app.schemas.professional import (
    PrivateMatches,
    ProfessionalCreate,
    ProfessionalUpdate,
)
from app.services import professional_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get(
    "/",
    description="Retrieve all professionals.",
)
def get_all_professionals(
    filter_params: FilterParams = Depends(),
    search_params: SearchParams = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_all_professionals():
        return professional_service.get_all(
            filter_params=filter_params, search_params=search_params, db=db
        )

    return process_request(
        get_entities_fn=_get_all_professionals,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="No professionals found",
    )


@router.get(
    "/{professional_id}",
    description="Retrieve a professional by its unique identifier.",
)
def get_professional_by_id(
    professional_id: UUID, db: Session = Depends(get_db)
) -> JSONResponse:
    def _get_professional_by_id():
        return professional_service.get_by_id(professional_id=professional_id, db=db)

    return process_request(
        get_entities_fn=_get_professional_by_id,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Professional with id {professional_id} not found",
    )


@router.get(
    "/by-username/{username}",
    description="Retrieve professional by username.",
)
def get_professional_by_username(
    username: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_professional_by_username():
        return professional_service.get_by_username(username=username, db=db)

    return process_request(
        get_entities_fn=_get_professional_by_username,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Professional with username {username} not found",
    )


@router.post(
    "/",
    description="Create a new professional.",
)
def create_professional(
    professional_data: ProfessionalCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _create_professional():
        return professional_service.create(professional_data=professional_data, db=db)

    return process_request(
        get_entities_fn=_create_professional,
        status_code=status.HTTP_201_CREATED,
        not_found_err_msg="Professional not created",
    )


@router.put(
    "/{professional_id}",
    description="Update a professional by its unique identifier.",
)
def update_professional(
    professional_id: UUID,
    professional_data: ProfessionalUpdate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _update_professional():
        return professional_service.update(
            professional_id=professional_id, professional_data=professional_data, db=db
        )

    return process_request(
        get_entities_fn=_update_professional,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Professional with id {professional_id} not found",
    )


@router.get(
    "/{professional_id}/photo",
    description="Retrieve a photo for a professional.",
)
def get_professional_photo(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    return professional_service.download_photo(professional_id=professional_id, db=db)


@router.post(
    "/{professional_id}/photo",
    description="Upload a photo for a professional.",
)
def upload_professional_photo(
    professional_id: UUID,
    photo: UploadFile = File(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _upload_professional_photo():
        return professional_service.upload_photo(
            professional_id=professional_id, photo=photo, db=db
        )

    return process_request(
        get_entities_fn=_upload_professional_photo,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Photo for professional with id {professional_id} not uploaded",
    )


@router.get(
    "/{professional_id}/cv",
    description="Retrieve a CV for a professional.",
)
def get_professional_cv(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    return professional_service.download_cv(professional_id=professional_id, db=db)


@router.post(
    "/{professional_id}/cv",
    description="Upload a CV for a professional.",
)
def upload_professional_cv(
    professional_id: UUID,
    cv: UploadFile = File(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _upload_professional_cv():
        return professional_service.upload_cv(
            professional_id=professional_id, cv=cv, db=db
        )

    return process_request(
        get_entities_fn=_upload_professional_cv,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"CV for professional with id {professional_id} not uploaded",
    )


@router.delete(
    "/{professional_id}/cv",
    description="Delete the CV of a professional.",
)
def delete_professional_cv(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _delete_professional_cv():
        return professional_service.delete_cv(professional_id=professional_id, db=db)

    return process_request(
        get_entities_fn=_delete_professional_cv,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"CV for professional with id {professional_id} not deleted",
    )


@router.patch(
    "/{professional_id}/private-matches",
    description="Toggle private matches for a professional.",
)
def toggle_private_matches(
    professional_id: UUID,
    private_matches: PrivateMatches,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _toggle_private_matches():
        return professional_service.set_matches_status(
            professional_id=professional_id, private_matches=private_matches, db=db
        )

    return process_request(
        get_entities_fn=_toggle_private_matches,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Private matches for professional with id {professional_id} not toggled",
    )


@router.get(
    "/{professional_id}/job-applications",
    description="Retrieve all applications of a professional.",
)
def get_professional_applications(
    professional_id: UUID,
    application_status: JobSearchStatus = Query(),
    filter_params: FilterParams = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_professional_applications():
        return professional_service.get_applications(
            professional_id=professional_id,
            application_status=application_status,
            filter_params=filter_params,
            db=db,
        )

    return process_request(
        get_entities_fn=_get_professional_applications,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Applications for professional with id {professional_id} not found",
    )


@router.get(
    "/{professional_id}/skills",
    description="Retrieve all skills of a professional.",
)
def get_professional_skills(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_professional_skills():
        return professional_service.get_skills(professional_id=professional_id, db=db)

    return process_request(
        get_entities_fn=_get_professional_skills,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Skills for professional with id {professional_id} not found",
    )


@router.get(
    "/{professional_id}/match-requests",
    description="Retrieve all match requests of a professional.",
)
def get_professional_match_requests(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_professional_match_requests():
        return professional_service.get_match_requests(
            professional_id=professional_id, db=db
        )

    return process_request(
        get_entities_fn=_get_professional_match_requests,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"Match requests for professional with id {professional_id} not found",
    )
