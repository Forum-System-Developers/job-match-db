from unittest.mock import ANY

import pytest
from fastapi import status

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.city import CityResponse
from app.services import city_service
from app.sql_app.city.city import City
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_city(mocker):
    def _create_mock_city(id, name):
        city = mocker.Mock()
        city.id = id
        city.name = name
        return city

    return _create_mock_city


def test_getAll_returnsCities_whenCitiesExist(mock_db, mock_city):
    # Arrange
    cities = [mock_city(**td.CITY), mock_city(**td.CITY_2)]
    mock_query = mock_db.query.return_value
    mock_query.all.return_value = cities

    # Act
    result = city_service.get_all(mock_db)

    # Assert
    mock_db.query.assert_called_with(City)
    mock_query.all.assert_called_once()
    assert len(result) == 2
    assert isinstance(result, list)
    assert isinstance(result[0], CityResponse)
    assert isinstance(result[1], CityResponse)


def test_getAll_returnsEmptyList_whenNoCitiesExist(mock_db):
    # Arrange
    mock_query = mock_db.query.return_value
    mock_query.all.return_value = []

    # Act
    result = city_service.get_all(mock_db)

    # Assert
    mock_db.query.assert_called_with(City)
    mock_query.all.assert_called()
    assert result == []


def test_getById_returnsCity_whenCityIsFound(mock_db, mock_city):
    # Arrange
    city = mock_city(**td.CITY)

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = city

    expected_city_response = CityResponse(id=td.VALID_CITY_ID, name=td.VALID_CITY_NAME)

    # Act
    result = city_service.get_by_id(city_id=td.VALID_CITY_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    mock_query.filter.assert_called_once_with(ANY)
    assert_filter_called_with(mock_query, City.id == td.VALID_CITY_ID)
    assert result == expected_city_response


def test_getById_raisesApplicationError_whenCityIsNotFound(mock_db):
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc:
        city_service.get_by_id(city_id=td.VALID_CITY_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    assert_filter_called_with(mock_query, City.id == td.VALID_CITY_ID)
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"No city found with id {td.VALID_CITY_ID}"


def test_getDefault_returnsCity_whenCityIsFound(mock_db, mock_city):
    # Arrange
    city = mock_city(**td.CITY)

    mock_query = mock_db.query.return_value
    mock_query.first.return_value = city

    expected_city_response = CityResponse(id=td.VALID_CITY_ID, name=td.VALID_CITY_NAME)

    # Act
    result = city_service.get_default(db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    assert result == expected_city_response


def test_getDefault_raisesApplicationError_whenCityIsNotFound(mock_db):
    # Arrange
    mock_query = mock_db.query.return_value
    mock_query.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc:
        city_service.get_default(db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == "No default city found"


def test_getByName_returnsCity_whenCityIsFound(mock_db, mock_city):
    # Arrange
    city = mock_city(**td.CITY)

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = city

    expected_city_response = CityResponse(id=td.VALID_CITY_ID, name=td.VALID_CITY_NAME)

    # Act
    result = city_service.get_by_name(city_name=td.VALID_CITY_NAME, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    mock_query.filter.assert_called_once_with(ANY)
    assert_filter_called_with(mock_query, City.name == td.VALID_CITY_NAME)
    assert result == expected_city_response


def test_getByName_raisesApplicationError_whenCityIsNotFound(mock_db):
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc:
        city_service.get_by_name(city_name=td.VALID_CITY_NAME, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(City)
    assert_filter_called_with(mock_query, City.name == td.VALID_CITY_NAME)
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"No city found with name {td.VALID_CITY_NAME}"
