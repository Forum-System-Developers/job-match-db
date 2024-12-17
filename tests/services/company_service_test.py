from datetime import datetime
from unittest.mock import ANY

import pytest
from fastapi import HTTPException, status

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.common import MessageResponse
from app.schemas.company import CompanyUpdate
from app.services import company_service
from app.sql_app.company.company import Company
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_company(mocker):
    mock_company = mocker.Mock(**td.COMPANY)
    mock_company.name = td.COMPANY["name"]
    mock_company.city = mocker.Mock()
    mock_company.city.name = td.VALID_CITY_NAME
    mock_company.website_url = td.VALID_COMPANY_WEBSITE_URL
    mock_company.youtube_video_id = td.VALID_COMPANY_YOUTUBE_VIDEO_ID
    mock_company.active_job_count = 0
    mock_company.successfull_matches_count = 0
    return mock_company


def test_getAll_returnsCompanies_whenCompaniesAreFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_filter_params = mocker.Mock(offset=0, limit=10)
    mock_companies = [mocker.Mock(), mocker.Mock()]
    mock_company_response = [mocker.Mock(), mocker.Mock()]

    mock_query = mock_db.query.return_value
    mock_offset = mock_query.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_companies

    mock_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        side_effect=mock_company_response,
    )

    # Act
    result = company_service.get_all(filter_params=mock_filter_params, db=mock_db)

    # Assert
    mock_db.query.assert_called_with(Company)
    mock_query.offset.assert_called_with(mock_filter_params.offset)
    mock_offset.limit.assert_called_with(mock_filter_params.limit)
    mock_create.assert_any_call(mock_companies[0])
    mock_create.assert_any_call(mock_companies[1])
    assert len(result) == 2
    assert result[0] == mock_company_response[0]
    assert result[1] == mock_company_response[1]


def test_getAll_returnsEmptyList_whenNoCompaniesAreFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_filter_params = mocker.Mock(offset=0, limit=10)

    mock_query = mock_db.query.return_value
    mock_offset = mock_query.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = []

    # Act
    result = company_service.get_all(filter_params=mock_filter_params, db=mock_db)

    # Assert
    mock_db.query.assert_called_with(Company)
    mock_query.offset.assert_called_with(mock_filter_params.offset)
    mock_offset.limit.assert_called_with(mock_filter_params.limit)
    assert len(result) == 0


def test_getById_returnsCompany_whenCompanyIsFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_response = mocker.Mock()
    mock_company = mocker.Mock()
    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )
    mock_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        return_value=mock_response,
    )

    # Act
    result = company_service.get_by_id(company_id=td.VALID_COMPANY_ID, db=mock_db)

    # Assert
    mock_get_company_by_id.assert_called_with(
        company_id=td.VALID_COMPANY_ID, db=mock_db
    )
    mock_create.assert_called_with(mock_company)
    assert result == mock_response


def test_getByUsername_returnsCompany_whenCompanyIsFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company = mocker.Mock(
        id=td.VALID_COMPANY_ID,
        username=td.VALID_COMPANY_USERNAME,
        password_hash=td.VALID_PASSWORD,
    )

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_company

    # Act
    result = company_service.get_by_username(
        username=td.VALID_COMPANY_USERNAME, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_with(Company)
    assert_filter_called_with(mock_query, Company.username == td.VALID_COMPANY_USERNAME)
    mock_filter.first.assert_called_once()
    assert result.id == td.VALID_COMPANY_ID
    assert result.username == td.VALID_COMPANY_USERNAME
    assert result.password == td.VALID_PASSWORD


def test_getByUsername_raisesApplicationError_whenCompanyIsNotFound(mock_db) -> None:
    # Arrange
    mock_username = td.NON_EXISTENT_USERNAME
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        company_service.get_by_username(username=mock_username, db=mock_db)

    assert_filter_called_with(mock_query, Company.username == mock_username)
    mock_query.filter.return_value.first.assert_called_once()
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"Company with username {mock_username} not found"


def test_getByEmail_returnsCompany_whenCompanyIsFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company = mocker.Mock()
    mock_response = mocker.Mock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_company

    mock_company_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        return_value=mock_response,
    )

    # Act
    result = company_service.get_by_email(email=td.VALID_COMPANY_EMAIL, db=mock_db)

    # Assert
    mock_db.query.assert_called_with(Company)
    assert_filter_called_with(mock_query, Company.email == td.VALID_COMPANY_EMAIL)
    mock_filter.first.assert_called_once()
    assert result == mock_response


def test_getByEmail_raisesApplicationError_whenCompanyIsNotFound(mock_db) -> None:
    # Arrange
    mock_email = "non existent email"
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        company_service.get_by_email(email=mock_email, db=mock_db)

    assert_filter_called_with(mock_query, Company.email == mock_email)
    mock_query.filter.return_value.first.assert_called_once()
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"Company with email {mock_email} not found"


def test_getByPhoneNumber_returnsCompany_whenCompanyIsFound(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company = mocker.Mock()
    mock_response = mocker.Mock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_company

    mock_company_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        return_value=mock_response,
    )

    # Act
    result = company_service.get_by_phone_number(
        phone_number=td.VALID_COMPANY_PHONE_NUMBER, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_with(Company)
    assert_filter_called_with(
        mock_query, Company.phone_number == td.VALID_COMPANY_PHONE_NUMBER
    )
    mock_filter.first.assert_called_once()
    assert result == mock_response


def test_getByPhoneNumber_raisesApplicationError_whenCompanyIsNotFound(mock_db) -> None:
    # Arrange
    mock_phone_number = "non existent phone number"
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        company_service.get_by_phone_number(phone_number=mock_phone_number, db=mock_db)

    assert_filter_called_with(mock_query, Company.phone_number == mock_phone_number)
    mock_query.filter.return_value.first.assert_called_once()
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.data.detail
        == f"Company with phone number {mock_phone_number} not found"
    )


def test_create_createsCompany_whenDataIsValid(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company_data = mocker.Mock()
    mock_company_data.model_dump.return_value = {}
    mock_response = mocker.Mock()

    mock_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        return_value=mock_response,
    )

    # Act
    result = company_service.create(company_data=mock_company_data, db=mock_db)

    # Assert
    mock_db.add.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(ANY)
    mock_create.assert_called_with(ANY)
    assert result == mock_response


def test_update_updatesCompany_whenDataIsValid(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company_data = mocker.Mock(id=td.VALID_COMPANY_ID)
    mock_company = mocker.Mock(id=td.VALID_COMPANY_ID)
    mock_response = mocker.Mock()

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )
    mock_create = mocker.patch(
        "app.schemas.company.CompanyResponse.create",
        return_value=mock_response,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id, company_data=mock_company_data, db=mock_db
    )

    # Assert
    mock_get_company_by_id.assert_called_with(
        company_id=td.VALID_COMPANY_ID, db=mock_db
    )
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_company)
    mock_create.assert_called_with(mock_company)
    assert result == mock_response


def test_updateCompany_updatesName_whenNameIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(name=td.VALID_COMPANY_NAME_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id, company_data=company_update_data, db=mock_db
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.name == company_update_data.name
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.description == mock_company.description
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesDescription_whenDescriptionIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(description=td.VALID_COMPANY_DESCRIPTION_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.description == company_update_data.description
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesAddressLine_whenAddressLineIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(address_line=td.VALID_COMPANY_ADDRESS_LINE_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.address_line == company_update_data.address_line
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesCity_whenCityIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(city_id=td.VALID_CITY_ID_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.city == mock_company.city.name
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.description == mock_company.description
    assert result.address_line == mock_company.address_line
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesEmail_whenEmailIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(email=td.VALID_COMPANY_EMAIL_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.email == company_update_data.email
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.description == mock_company.description
    assert result.address_line == mock_company.address_line
    assert result.city == mock_company.city.name
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesPhoneNumber_whenPhoneNumberIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(phone_number=td.VALID_COMPANY_PHONE_NUMBER_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.phone_number == company_update_data.phone_number
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.description == mock_company.description
    assert result.address_line == mock_company.address_line
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email


def test_updateCompany_updatesWebsiteUrl_whenWebsiteUrlIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(website_url=td.VALID_COMPANY_WEBSITE_URL_2)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.website_url == company_update_data.website_url
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.description == mock_company.description
    assert result.address_line == mock_company.address_line
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number


def test_updateCompany_updatesYoutubeVideoId_whenYoutubeVideoUrlIsProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(
        youtube_video_id=td.VALID_COMPANY_YOUTUBE_VIDEO_ID_2
    )

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.youtube_video_id == company_update_data.youtube_video_id
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id
    assert result.name == mock_company.name
    assert result.description == mock_company.description
    assert result.address_line == mock_company.address_line
    assert result.city == mock_company.city.name
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number
    assert result.website_url == mock_company.website_url


def test_updateCompany_updatesAllFields_whenAllFieldsAreProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate(
        name=td.VALID_COMPANY_NAME_2,
        address_line=td.VALID_COMPANY_ADDRESS_LINE_2,
        city_id=td.VALID_CITY_ID_2,
        description=td.VALID_COMPANY_DESCRIPTION_2,
        email=td.VALID_COMPANY_EMAIL_2,
        phone_number=td.VALID_COMPANY_PHONE_NUMBER_2,
        website_url=td.VALID_COMPANY_WEBSITE_URL_2,
        youtube_video_id=td.VALID_COMPANY_YOUTUBE_VIDEO_ID_2,
    )

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.name == company_update_data.name
    assert result.address_line == company_update_data.address_line
    assert result.city == mock_company.city.name
    assert result.description == company_update_data.description
    assert result.email == company_update_data.email
    assert result.phone_number == company_update_data.phone_number
    assert result.website_url == company_update_data.website_url
    assert result.youtube_video_id == company_update_data.youtube_video_id
    assert isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id


def test_updateCompany_updatesNothing_whenNoFieldsAreProvided(
    mocker,
    mock_db,
    mock_company,
) -> None:
    # Arrange
    company_update_data = CompanyUpdate()

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.update(
        company_id=mock_company.id,
        company_data=company_update_data,
        db=mock_db,
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert result.name == mock_company.name
    assert result.address_line == mock_company.address_line
    assert result.city == mock_company.city.name
    assert result.description == mock_company.description
    assert result.email == mock_company.email
    assert result.phone_number == mock_company.phone_number
    assert result.website_url == mock_company.website_url
    assert result.youtube_video_id == mock_company.youtube_video_id
    assert result.active_job_ads == mock_company.active_job_count or 0
    assert result.successful_matches == mock_company.successfull_matches_count or 0
    assert not isinstance(mock_company.updated_at, datetime)

    assert result.id == mock_company.id


def test_uploadLogo_uploadsLogo_whenDataIsValid(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_logo = mocker.Mock()
    mock_company = mocker.Mock(id=td.VALID_COMPANY_ID, logo=b"mock_logo_data")

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.upload_logo(
        company_id=mock_company.id, logo=mock_logo, db=mock_db
    )

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    mock_db.commit.assert_called_once()
    assert isinstance(result, MessageResponse)


def test_downloadLogo_returnsLogo_whenCompanyHasLogo(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_logo_data = b"mock_logo_data"
    mock_company = mocker.Mock(id=td.VALID_COMPANY_ID, logo=mock_logo_data)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )
    mock_bytes_io = mocker.patch("app.services.company_service.io.BytesIO")
    mock_streaming_response = mocker.patch(
        "app.services.company_service.StreamingResponse"
    )

    # Act
    result = company_service.download_logo(company_id=mock_company.id, db=mock_db)

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    mock_bytes_io.assert_called_with(mock_logo_data)
    mock_streaming_response.assert_called_with(
        mock_bytes_io.return_value, media_type="image/png"
    )
    assert result == mock_streaming_response.return_value


def test_downloadLogo_raisesHTTPException_whenCompanyHasNoLogo(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company = mocker.Mock(id=td.VALID_COMPANY_ID, logo=None)

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        company_service.download_logo(company_id=mock_company.id, db=mock_db)

    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == f"Company with id {mock_company.id} does not have a logo"


def test_deleteLogo_deletesLogo_whenCompanyHasLogo(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_company = mocker.Mock(id=td.VALID_COMPANY_ID, logo=b"mock_logo_data")

    mock_get_company_by_id = mocker.patch(
        "app.services.company_service.get_company_by_id",
        return_value=mock_company,
    )

    # Act
    result = company_service.delete_logo(company_id=mock_company.id, db=mock_db)

    # Assert
    mock_get_company_by_id.assert_called_with(company_id=mock_company.id, db=mock_db)
    mock_db.commit.assert_called_once()
    assert mock_company.logo is None
    assert isinstance(mock_company.updated_at, datetime)
    assert isinstance(result, MessageResponse)
