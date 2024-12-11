from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services import city_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get("/", description="Retrieve all cities.")
def get_all_cities(db: Session = Depends(get_db)) -> JSONResponse:
    def _get_all_cities():
        return city_service.get_all(db)

    return process_request(
        get_entities_fn=_get_all_cities,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="No cities found",
    )


@router.get(
    "/default",
    description="Retrieve the default city.",
)
def get_default_city(db: Session = Depends(get_db)) -> JSONResponse:
    def _get_default_city():
        return city_service.get_default(db)

    return process_request(
        get_entities_fn=_get_default_city,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="Default city not found",
    )


@router.get("/{city_id}", description="Retrieve a city by its identifier.")
def get_city_by_id(city_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    def _get_city_by_id():
        return city_service.get_by_id(city_id=city_id, db=db)

    return process_request(
        get_entities_fn=_get_city_by_id,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"No city found with id {city_id}",
    )


@router.get("/by-name/{city_name}", description="Retrieve a city by its name.")
def get_city_by_name(city_name: str, db: Session = Depends(get_db)) -> JSONResponse:
    def _get_city_by_name():
        return city_service.get_by_name(city_name=city_name, db=db)

    return process_request(
        get_entities_fn=_get_city_by_name,
        status_code=status.HTTP_200_OK,
        not_found_err_msg=f"No city found with name {city_name}",
    )
