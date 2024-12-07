from uuid import UUID

from fastapi import APIRouter, Body, Depends
from fastapi import status as status_code
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.common import FilterParams, SearchParams
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate
from app.services import job_application_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.post(
    "/all",
    description="Retrieve all Job Applications.",
)
def get_all(
    filter_params: FilterParams = Depends(),
    search_params: SearchParams = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_all():
        return job_application_service.get_all(
            filter_params=filter_params,
            search_params=search_params,
            db=db,
        )

    return process_request(
        get_entities_fn=_get_all,
        status_code=status_code.HTTP_200_OK,
        not_found_err_msg="Could not fetch Job Applications",
    )


@router.get(
    "/{job_application_id}",
    description="Retrieve a Job Application by its unique identifier.",
)
def get_by_id(
    job_application_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_by_id():
        return job_application_service.get_by_id(
            job_application_id=job_application_id, db=db
        )

    return process_request(
        get_entities_fn=_get_by_id,
        status_code=status_code.HTTP_200_OK,
        not_found_err_msg="Could not fetch Job Application",
    )


@router.post(
    "/{professional_id}",
    description="Create a new Job Application.",
)
def create(
    job_application_create: JobApplicationCreate = Body(
        description="Job Application creation form"
    ),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _create():
        return job_application_service.create(
            professional_id=job_application_create.professional_id,
            job_application_create=job_application_create,
            db=db,
        )

    return process_request(
        get_entities_fn=_create,
        status_code=status_code.HTTP_201_CREATED,
        not_found_err_msg="Job application could not be created",
    )


@router.put(
    "/{job_application_id}/{professional_id}",
    description="Update a Job Application.",
)
def update(
    job_application_id: UUID,
    professional_id: UUID,
    application_update: JobApplicationUpdate = Body(
        description="Job Application update form"
    ),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _update():
        return job_application_service.update(
            professional_id=professional_id,
            job_application_id=job_application_id,
            job_application_update=application_update,
            db=db,
        )

    return process_request(
        get_entities_fn=_update,
        status_code=status_code.HTTP_200_OK,
        not_found_err_msg="Job application could not be updated",
    )
