from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pytest import Session

from app.schemas.common import FilterParams
from app.schemas.match import MatchRequestCreate, MatchRequestUpdate
from app.services import match_request_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get(
    "/job-ads/{job_ad_id}/job-applications/{job_application_id}",
    description="Retrieve a match request by job ad and job application.",
)
def get_match_request(
    job_ad_id: UUID,
    job_application_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_match_request():
        return match_request_service.get_by_id(
            job_ad_id=job_ad_id, job_application_id=job_application_id, db=db
        )

    return process_request(
        get_entities_fn=_get_match_request,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch match request",
    )


@router.patch(
    "/job-ads/{job_ad_id}/job-applications/{job_application_id}",
    description="Update a match request status.",
)
def update_match_status(
    job_ad_id: UUID,
    job_application_id: UUID,
    match_request_data: MatchRequestUpdate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _update_match_status():
        return match_request_service.update_status(
            job_ad_id=job_ad_id,
            job_application_id=job_application_id,
            match_request_data=match_request_data,
            db=db,
        )

    return process_request(
        get_entities_fn=_update_match_status,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not update match request",
    )


@router.post(
    "/",
    description="Create a match request.",
)
def create_match_request(
    match_request_data: MatchRequestCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _create_match_request():
        return match_request_service.create(
            match_request_data=match_request_data, db=db
        )

    return process_request(
        get_entities_fn=_create_match_request,
        status_code=status.HTTP_201_CREATED,
        not_found_err_msg="Could not create match request",
    )


@router.put(
    "/job-ads/{job_ad_id}/job-applications/{job_application_id}",
    description="Accept a match request.",
)
def accept_match_request(
    job_ad_id: UUID,
    job_application_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _accept_match_request():
        return match_request_service.accept_match_request(
            job_ad_id=job_ad_id, job_application_id=job_application_id, db=db
        )

    return process_request(
        get_entities_fn=_accept_match_request,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not accept match request",
    )


@router.get(
    "/job-applications/{job_application_id}",
    description="Retrieve match requests for a job ad.",
)
def get_match_requests_for_job_application(
    job_application_id: UUID,
    filter_params: FilterParams = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_match_requests_for_job_application():
        return match_request_service.get_match_requests_for_job_application(
            job_application_id=job_application_id,
            filter_params=filter_params,
            db=db,
        )

    return process_request(
        get_entities_fn=_get_match_requests_for_job_application,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch match requests for job ad",
    )


@router.get(
    "/professionals/{professional_id}",
    description="Retrieve all match requests for a professional.",
)
def get_match_requests_for_professional(
    professional_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_match_requests_for_professional():
        return match_request_service.get_match_requests_for_professional(
            professional_id=professional_id, db=db
        )

    return process_request(
        get_entities_fn=_get_match_requests_for_professional,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch match requests for professional",
    )


@router.get(
    "/companies/{company_id}",
    description="Retrieve all match requests for a company.",
)
def get_match_requests_for_company(
    company_id: UUID,
    filter_params: FilterParams = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_match_requests_for_company():
        return match_request_service.get_match_requests_for_company(
            company_id=company_id, filter_params=filter_params, db=db
        )

    return process_request(
        get_entities_fn=_get_match_requests_for_company,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch match requests for company",
    )


@router.get(
    "/job-ads/{job_ad_id}/received-matches",
    description="Retrieve all match requests for a job ad.",
)
def get_job_ad_received_matches(
    job_ad_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_job_ad_received_matches():
        return match_request_service.get_job_ad_received_matches(
            job_ad_id=job_ad_id, db=db
        )

    return process_request(
        get_entities_fn=_get_job_ad_received_matches,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch received match requests for job ad",
    )


@router.get(
    "/job-ads/{job_ad_id}/sent-matches",
    description="Retrieve all match requests sent by a job ad.",
)
def get_job_ad_sent_matches(
    job_ad_id: UUID,
    db: Session = Depends(get_db),
) -> JSONResponse:
    def _get_job_ad_sent_matches():
        return match_request_service.get_job_ad_sent_matches(job_ad_id=job_ad_id, db=db)

    return process_request(
        get_entities_fn=_get_job_ad_sent_matches,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Could not fetch sent match requests for job ad",
    )
