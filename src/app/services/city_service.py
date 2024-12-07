from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.city import CityResponse
from app.sql_app.city.city import City


def get_all(db: Session) -> list[CityResponse]:
    """
    Retrieve all cities from the database.

    Args:
        db (Session): The database session used to query the cities.

    Returns:
        list[CityResponse]: A list of CityResponse objects containing the id and name of each city.
    """
    cities = db.query(City).all()
    return [CityResponse(id=city.id, name=city.name) for city in cities]


def get_by_id(
    city_id: UUID,
    db: Session,
) -> CityResponse:
    """
    Retrieve a city by its identifier.

    Args:
        db (Session): The database session used to query the city.
        city_id (int): The identifier of the city to retrieve.

    Returns:
        CityResponse: A CityResponse object containing the id and name of the city.

    Raises:
        ApplicationError: If no city is found with the given identifier.
    """
    city = db.query(City).filter(City.id == city_id).first()
    if city is None:
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No city found with id {city_id}",
        )
    return CityResponse(id=city.id, name=city.name)


def get_by_name(
    city_name: str,
    db: Session,
) -> CityResponse:
    """
    Retrieve a city by its name.

    Args:
        city_name (str): The name of the city to retrieve.
        db (Session): The database session used to query the city.

    Returns:
        CityResponse: A CityResponse object containing the id and name of the city.

    Raises:
        ApplicationError: If no city is found with the given name.
    """
    city = db.query(City).filter(City.name == city_name).first()
    if city is None:
        raise ApplicationError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No city found with name {city_name}",
        )
    return CityResponse(id=city.id, name=city.name)
