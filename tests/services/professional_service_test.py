from datetime import datetime
from unittest.mock import ANY

import pytest
from fastapi import HTTPException, status

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.job_ad import JobAdPreview
from app.schemas.job_application import JobSearchStatus
from app.schemas.match import MatchRequestAd
from app.schemas.professional import ProfessionalResponse, ProfessionalUpdate
from app.schemas.skill import SkillResponse
from app.schemas.user import User
from app.services import professional_service
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.professional.professional import Professional
from app.sql_app.professional.professional_status import ProfessionalStatus
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_professional(mocker):
    professional = mocker.Mock(**td.PROFESSIONAL_MODEL)
    professional.city = mocker.Mock(id=td.VALID_CITY_ID)
    professional.city.name = td.VALID_CITY_NAME

    return professional


def test_getAll_returnsProfessionals_withOrderAsc(mocker, mock_db):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(order="asc", order_by="created_at")

    mock_professionals = [mocker.Mock(), mocker.Mock()]
    mock_professional_response = [mocker.Mock(), mocker.Mock()]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order_by = mock_filter.order_by.return_value
    mock_offset = mock_order_by.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_professionals

    mocker.patch(
        "app.schemas.professional.ProfessionalResponse.create",
        side_effect=mock_professional_response,
    )
    mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )

    # Act
    result = professional_service.get_all(
        db=mock_db,
        filter_params=filter_params,
        search_params=search_params,
    )

    # Assert
    assert result == mock_professional_response
    mock_db.query.assert_called_once_with(Professional)
    mock_filter.order_by.assert_called_once()
    mock_order_by.offset.assert_called_once_with(filter_params.offset)
    mock_offset.limit.assert_called_once_with(filter_params.limit)
    mock_limit.all.assert_called_once()


def test_getAll_returnsProfessionals_withOrderDesc(mocker, mock_db):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(order="desc", order_by="created_at")

    mock_professionals = [mocker.Mock(), mocker.Mock()]
    mock_professional_response = [mocker.Mock(), mocker.Mock()]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order_by = mock_filter.order_by.return_value
    mock_offset = mock_order_by.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_professionals

    mocker.patch(
        "app.schemas.professional.ProfessionalResponse.create",
        side_effect=mock_professional_response,
    )
    mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )

    # Act
    result = professional_service.get_all(
        db=mock_db,
        filter_params=filter_params,
        search_params=search_params,
    )

    # Assert
    assert result == mock_professional_response
    mock_db.query.assert_called_once_with(Professional)
    mock_filter.order_by.assert_called_once()
    mock_order_by.offset.assert_called_once_with(filter_params.offset)
    mock_offset.limit.assert_called_once_with(filter_params.limit)
    mock_limit.all.assert_called_once()


def test_getAll_returnsProfessionalsFilteredBySkills_whenSkillsProvided(
    mocker, mock_db
):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(order="asc", order_by="created_at")

    mock_professionals = [mocker.Mock(), mocker.Mock()]
    mock_professional_response = [mocker.Mock(), mocker.Mock()]
    mock_skills = [mocker.Mock(), mocker.Mock()]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order_by = mock_filter.order_by.return_value
    mock_offset = mock_order_by.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_professionals

    mocker.patch(
        "app.schemas.professional.ProfessionalResponse.create",
        side_effect=mock_professional_response,
    )
    mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=mock_skills,
    )

    # Act
    result = professional_service.get_all(
        db=mock_db,
        filter_params=filter_params,
        search_params=search_params,
    )

    # Assert
    assert result == mock_professional_response
    mock_db.query.assert_called_once_with(Professional)
    mock_filter.order_by.assert_called_once()
    mock_order_by.offset.assert_called_once_with(filter_params.offset)
    mock_offset.limit.assert_called_once_with(filter_params.limit)
    mock_limit.all.assert_called_once()
    assert len(result) == 2
    assert result[0] == mock_professional_response[0]
    assert result[1] == mock_professional_response[1]


def test_getById_returnsProfessionalResponse_whenProfessionalExists(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_skills = [mocker.Mock(spec=SkillResponse), mocker.Mock(spec=SkillResponse)]
    mock_sent_match_requests = [
        mocker.Mock(spec=MatchRequestAd),
        mocker.Mock(spec=MatchRequestAd),
    ]
    mock_matched_ads = [mocker.Mock(spec=JobAdPreview), mocker.Mock(spec=JobAdPreview)]

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills", return_value=mock_skills
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=mock_sent_match_requests,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches", return_value=mock_matched_ads
    )

    # Act
    response = professional_service.get_by_id(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_skills.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_sent_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_matches.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert response.id == mock_professional.id
    assert response.skills == mock_skills
    assert response.sent_match_requests == mock_sent_match_requests
    assert response.matched_ads == mock_matched_ads


def test_getById_returnsProfessionalResponseWithPrivateMatches_whenProfessionalHasPrivateMatches(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.has_private_matches = True
    mock_skills = [mocker.Mock(spec=SkillResponse), mocker.Mock(spec=SkillResponse)]
    mock_sent_match_requests = [
        mocker.Mock(spec=MatchRequestAd),
        mocker.Mock(spec=MatchRequestAd),
    ]

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills", return_value=mock_skills
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=mock_sent_match_requests,
    )
    mock_get_matches = mocker.patch("app.services.professional_service._get_matches")

    # Act
    response = professional_service.get_by_id(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_skills.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_sent_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_matches.call_count == 0
    assert response.id == mock_professional.id
    assert response.skills == mock_skills
    assert response.sent_match_requests == mock_sent_match_requests
    assert response.matched_ads is None


def test_create_createsProfessional_whenValidProfessionalData(
    mocker,
    mock_db,
) -> None:
    # Arrange
    professional_data = mocker.MagicMock(**td.PROFESSIONAL_CREATE)
    mock_professional_response = mocker.Mock()

    mock_professional_create = mocker.patch(
        "app.services.professional_service.ProfessionalResponse.create",
        return_value=mock_professional_response,
    )

    # Act
    result = professional_service.create(
        professional_data=professional_data, db=mock_db
    )

    # Assert
    mock_db.add.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(ANY)
    assert result == mock_professional_response


def test_update_updatesProfessional_whenValidDataProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(**td.PROFESSIONAL_UPDATE)

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id,
        db=mock_db,
    )
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_professional)
    assert isinstance(result, ProfessionalResponse)


def test_updatesFirstName_whenFirstNameProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(
        first_name=td.VALID_PROFESSIONAL_FIRST_NAME_2
    )

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert result.first_name == professional_data.first_name
    assert isinstance(mock_professional.updated_at, datetime)

    assert result.id == mock_professional.id
    assert result.last_name == mock_professional.last_name
    assert result.email == mock_professional.email
    assert result.city == mock_professional.city.name
    assert result.description == mock_professional.description
    assert result.photo == mock_professional.photo
    assert result.status == mock_professional.status
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updatesLastName_whenLastNameProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(last_name=td.VALID_PROFESSIONAL_LAST_NAME_2)

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert result.last_name == professional_data.last_name
    assert isinstance(mock_professional.updated_at, datetime)

    assert result.id == mock_professional.id
    assert result.first_name == mock_professional.first_name
    assert result.email == mock_professional.email
    assert result.city == mock_professional.city.name
    assert result.description == mock_professional.description
    assert result.photo == mock_professional.photo
    assert result.status == mock_professional.status
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updatesDescription_whenDescriptionProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(
        description=td.VALID_PROFESSIONAL_DESCRIPTION_2
    )

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert result.description == professional_data.description
    assert isinstance(mock_professional.updated_at, datetime)

    assert result.id == mock_professional.id
    assert result.first_name == mock_professional.first_name
    assert result.last_name == mock_professional.last_name
    assert result.email == mock_professional.email
    assert result.city == mock_professional.city.name
    assert result.photo == mock_professional.photo
    assert result.status == mock_professional.status
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updatesCityId_whenCityIdProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(city_id=td.VALID_CITY_ID_2)

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert mock_professional.city_id == professional_data.city_id
    assert isinstance(mock_professional.updated_at, datetime)

    assert result.id == mock_professional.id
    assert result.first_name == mock_professional.first_name
    assert result.last_name == mock_professional.last_name
    assert result.email == mock_professional.email
    assert result.description == mock_professional.description
    assert result.photo == mock_professional.photo
    assert result.status == mock_professional.status
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updatesStatus_whenStatusProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(status=ProfessionalStatus.BUSY)

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert mock_professional.status == professional_data.status
    assert isinstance(mock_professional.updated_at, datetime)

    assert result.id == mock_professional.id
    assert result.first_name == mock_professional.first_name
    assert result.last_name == mock_professional.last_name
    assert result.email == mock_professional.email
    assert result.city == mock_professional.city.name
    assert result.description == mock_professional.description
    assert result.photo == mock_professional.photo
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updates_updatesAllFields_whenAllFieldsAreProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate(
        first_name=td.VALID_PROFESSIONAL_FIRST_NAME_2,
        last_name=td.VALID_PROFESSIONAL_LAST_NAME_2,
        description=td.VALID_PROFESSIONAL_DESCRIPTION_2,
        city_id=td.VALID_CITY_ID_2,
        status=ProfessionalStatus.BUSY,
    )

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert isinstance(mock_professional.updated_at, datetime)
    assert result.first_name == professional_data.first_name
    assert result.last_name == professional_data.last_name
    assert result.description == professional_data.description
    assert mock_professional.city_id == professional_data.city_id
    assert result.status == ProfessionalStatus.BUSY

    assert result.id == mock_professional.id
    assert result.email == mock_professional.email
    assert result.photo == mock_professional.photo
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_updatesNothing_whenNoFieldsAreProvided(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    professional_data = ProfessionalUpdate()

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_matches = mocker.patch(
        "app.services.professional_service._get_matches",
        return_value=[],
    )
    mock_get_skills = mocker.patch(
        "app.services.professional_service.get_skills",
        return_value=[],
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.professional_service.get_sent_match_requests",
        return_value=[],
    )

    # Act
    result = professional_service.update(
        professional_id=mock_professional.id,
        professional_data=professional_data,
        db=mock_db,
    )

    # Assert
    assert not isinstance(mock_professional.updated_at, datetime)
    assert result.id == mock_professional.id
    assert result.first_name == mock_professional.first_name
    assert result.last_name == mock_professional.last_name
    assert result.email == mock_professional.email
    assert result.city == mock_professional.city.name
    assert result.description == mock_professional.description
    assert result.photo == mock_professional.photo
    assert result.status == mock_professional.status
    assert result.active_application_count == mock_professional.active_application_count
    assert result.skills == []
    assert result.matched_ads == []
    assert result.sent_match_requests == []


def test_uploadPhoto_uploadsPhoto_whenFileIsValid(mocker, mock_db):
    # Arrange
    professional_id = td.VALID_PROFESSIONAL_ID
    mock_professional = mocker.Mock()
    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_commit = mocker.patch.object(mock_db, "commit")

    mock_photo = mocker.Mock()
    mock_photo.file.read.return_value = b"valid_photo_content"

    # Act
    result = professional_service.upload_photo(
        professional_id=professional_id, photo=mock_photo, db=mock_db
    )

    # Assert
    mock_get_by_id.assert_called_once_with(professional_id=professional_id, db=mock_db)
    mock_photo.file.read.assert_called_once()
    mock_commit.assert_called_once()
    assert mock_professional.photo == b"valid_photo_content"
    assert result.message == "Photo successfully uploaded"


def test_downloadPhoto_returnsPhoto_whenPhotoExists(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.photo = b"somebinarydata"

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act
    response = professional_service.download_photo(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.media_type == "image/png"


def test_downloadPhoto_raisesHTTPException_whenPhotoNotFound(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.photo = None

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        professional_service.download_photo(
            professional_id=mock_professional.id, db=mock_db
        )

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.detail
        == f"Professional with id {mock_professional.id} does not have a photo"
    )
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )


def test_uploadCv_uploadsCv_whenFileIsValid(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_commit = mocker.patch.object(mock_db, "commit")

    mock_cv = mocker.Mock()
    mock_cv.file.read.return_value = b"valid_cv_content"
    mock_cv.content_type = "application/pdf"

    # Act
    result = professional_service.upload_cv(
        professional_id=mock_professional.id, cv=mock_cv, db=mock_db
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_cv.file.read.assert_called_once()
    mock_commit.assert_called_once()
    assert mock_professional.cv == b"valid_cv_content"
    assert result.message == "CV successfully uploaded"


def test_downloadCv_returnsCv_whenCvExists(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    cv_data = b"somebinarycvdata"
    mock_professional.cv = cv_data
    mock_streaming_response = mocker.Mock()
    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_generate_cv_response = mocker.patch(
        "app.services.professional_service._generate_cv_response",
        return_value=mock_streaming_response,
    )

    # Act
    response = professional_service.download_cv(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_generate_cv_response.assert_called_once_with(
        professional=mock_professional, cv=cv_data
    )
    assert response == mock_streaming_response


def test_downloadCv_raisesHTTPException_whenCvNotFound(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.cv = None

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        professional_service.download_cv(
            professional_id=mock_professional.id, db=mock_db
        )

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.detail
        == f"CV for professional with id {mock_professional.id} not found"
    )
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )


def test_deleteCv_deletesCv_whenCvExists(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.cv = b"some_cv_data"
    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act
    result = professional_service.delete_cv(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_db.commit.assert_called_once()
    assert mock_professional.cv is None
    assert result.message == "CV deleted successfully"


def test_deleteCv_raisesApplicationError_whenCvNotFound(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.cv = None
    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        professional_service.delete_cv(professional_id=mock_professional.id, db=mock_db)

    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.data.detail
        == f"CV for professional with id {mock_professional.id} not found"
    )


def test_setMatchesStatus_setsToPrivate_whenStatusIsTrue(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.has_private_matches = False

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_commit = mocker.patch.object(mock_db, "commit")

    private_matches = mocker.Mock(status=True)

    # Act
    result = professional_service.set_matches_status(
        professional_id=mock_professional.id,
        db=mock_db,
        private_matches=private_matches,
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_commit.assert_called_once()
    assert result.message == "Matches set as private"
    assert mock_professional.has_private_matches is True


def test_setMatchesStatus_setsToPublic_whenStatusIsFalse(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.has_private_matches = True

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_commit = mocker.patch.object(mock_db, "commit")

    private_matches = mocker.Mock(status=False)

    # Act
    result = professional_service.set_matches_status(
        professional_id=mock_professional.id,
        db=mock_db,
        private_matches=private_matches,
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_commit.assert_called_once()
    assert result.message == "Matches set as public"
    assert mock_professional.has_private_matches is False


def test_getBySub_returnsProfessional_whenProfessionalExists(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.sub = "valid_sub"
    mock_professional_response = "professional_response"

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_professional

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_by_id",
        return_value=mock_professional_response,
    )

    # Act
    result = professional_service.get_by_sub(sub=mock_professional.sub, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(mock_query, Professional.sub == mock_professional.sub)
    mock_filter.first.assert_called_once()
    mock_get_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == mock_professional_response


def test_getBySub_raisesApplicationError_whenProfessionalNotFound(
    mock_db,
) -> None:
    # Arrange
    sub = "invalid_sub"

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        professional_service.get_by_sub(sub=sub, db=mock_db)

    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(mock_query, Professional.sub == sub)
    mock_filter.first.assert_called_once()
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"User with sub {sub} does not exist"


def test_getByUsername_returnsProfessional_whenProfessionalExists(
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_professional

    # Act
    result = professional_service.get_by_username(
        username=td.VALID_PROFESSIONAL_USERNAME, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(
        mock_query, Professional.username == td.VALID_PROFESSIONAL_USERNAME
    )
    assert isinstance(result, User)
    assert result.id == mock_professional.id
    assert result.username == mock_professional.username
    assert result.password == mock_professional.password_hash


def test_getByUsername_raisesApplicationError_whenProfessionalNotFound(
    mock_db,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        professional_service.get_by_username(
            username=td.VALID_PROFESSIONAL_USERNAME, db=mock_db
        )

    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(
        mock_query, Professional.username == td.VALID_PROFESSIONAL_USERNAME
    )
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.data.detail
        == f"User with username {td.VALID_PROFESSIONAL_USERNAME} does not exist"
    )


def test_getApplications_returnsApplications_whenApplicationsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_filter_params = mocker.Mock(offset=0, limit=10)
    mock_application_response = mocker.Mock()

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_offset = mock_filter.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = [mocker.Mock(id=td.VALID_JOB_APPLICATION_ID)]

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    mocker.patch(
        "app.services.professional_service.JobApplicationResponse.create",
        return_value=mock_application_response,
    )

    # Act
    result = professional_service.get_applications(
        professional_id=td.VALID_PROFESSIONAL_ID,
        application_status=JobSearchStatus.ACTIVE,
        filter_params=mock_filter_params,
        db=mock_db,
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=td.VALID_PROFESSIONAL_ID, db=mock_db
    )
    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.ACTIVE),
    )

    assert len(result) == 1
    assert result[0] == mock_application_response


def test_getApplications_returnsEmptyList_whenNoApplicationsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_filter_params = mocker.Mock(offset=0, limit=10)

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_offset = mock_filter.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = []

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act
    result = professional_service.get_applications(
        professional_id=td.VALID_PROFESSIONAL_ID,
        application_status=JobSearchStatus.ACTIVE,
        filter_params=mock_filter_params,
        db=mock_db,
    )

    # Assert
    mock_get_by_id.assert_called_once_with(
        professional_id=td.VALID_PROFESSIONAL_ID, db=mock_db
    )
    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.ACTIVE),
    )

    assert result == []


def test_getApplications_raisesApplicationError_whenMatchesArePrivate(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.has_private_matches = True

    mock_get_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        professional_service.get_applications(
            professional_id=td.VALID_PROFESSIONAL_ID,
            application_status=JobSearchStatus.MATCHED,
            filter_params=mocker.Mock(),
            db=mock_db,
        )

    mock_get_by_id.assert_called_once_with(
        professional_id=td.VALID_PROFESSIONAL_ID, db=mock_db
    )
    assert exc.value.data.status == status.HTTP_403_FORBIDDEN
    assert exc.value.data.detail == "Professional has set their Matches to Private"


def test_getApplication_returnsApplication_whenApplicationExists(
    mocker,
    mock_db,
) -> None:
    # Arrange
    professional_id = td.VALID_PROFESSIONAL_ID
    job_application_id = td.VALID_JOB_APPLICATION_ID
    mock_job_application = mocker.Mock(id=job_application_id)
    mock_application_response = mocker.Mock()

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_job_application

    mocker.patch(
        "app.services.professional_service.JobApplicationResponse.create",
        return_value=mock_application_response,
    )

    # Act
    result = professional_service.get_application(
        professional_id=professional_id,
        job_application_id=job_application_id,
        db=mock_db,
    )

    # Assert
    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query,
        (JobApplication.professional_id == professional_id)
        & (JobApplication.id == job_application_id),
    )
    assert result == mock_application_response


def test_getApplication_raisesApplicationError_whenApplicationNotFound(mock_db) -> None:
    # Arrange
    professional_id = td.VALID_PROFESSIONAL_ID
    job_application_id = td.VALID_JOB_APPLICATION_ID

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        professional_service.get_application(
            professional_id=professional_id,
            job_application_id=job_application_id,
            db=mock_db,
        )

    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query,
        (JobApplication.professional_id == professional_id)
        & (JobApplication.id == job_application_id),
    )
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc.value.data.detail
        == f"Job Application with id {job_application_id} not found"
    )


def test_getSkills_returnsSkills_whenSkillsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_job_application = mocker.Mock(skills=[])
    mock_skill_1 = mocker.Mock(
        id=td.VALID_SKILL_ID,
        category_id=td.VALID_CATEGORY_ID,
    )
    mock_skill_1.name = td.VALID_SKILL_NAME
    mock_job_application.skills.append(mock_skill_1)

    mock_skill_2 = mocker.Mock(
        id=td.VALID_SKILL_ID_2,
        category_id=td.VALID_CATEGORY_ID_2,
    )
    mock_skill_2.name = td.VALID_SKILL_NAME_2
    mock_job_application.skills.append(mock_skill_2)
    mock_professional.job_applications = [mock_job_application]

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act
    result = professional_service.get_skills(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert len(result) == 2
    assert result[0].id == td.VALID_SKILL_ID
    assert result[0].name == td.VALID_SKILL_NAME
    assert result[0].category_id == td.VALID_CATEGORY_ID
    assert result[1].id == td.VALID_SKILL_ID_2
    assert result[1].name == td.VALID_SKILL_NAME_2
    assert result[1].category_id == td.VALID_CATEGORY_ID_2


def test_getSkills_returnsEmptyList_whenNoSkillsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_professional.job_applications = []

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )

    # Act
    result = professional_service.get_skills(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == []


def test_getMatchRequests_returnsMatchRequests_whenRequestsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_match_requests = [
        mocker.Mock(spec=MatchRequestAd),
        mocker.Mock(spec=MatchRequestAd),
    ]

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_match_requests = mocker.patch(
        "app.services.match_service.get_match_requests_for_professional",
        return_value=mock_match_requests,
    )

    # Act
    result = professional_service.get_match_requests(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == mock_match_requests


def test_getMatchRequests_returnsEmptyList_whenNoRequestsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_match_requests = mocker.patch(
        "app.services.match_service.get_match_requests_for_professional",
        return_value=[],
    )

    # Act
    result = professional_service.get_match_requests(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == []


def test_getSentMatchRequests_returnsMatchRequests_whenRequestsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_sent_match_requests = [
        mocker.Mock(spec=MatchRequestAd),
        mocker.Mock(spec=MatchRequestAd),
    ]

    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.match_service.get_sent_match_requests_for_professional",
        return_value=mock_sent_match_requests,
    )

    # Act
    result = professional_service.get_sent_match_requests(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_sent_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == mock_sent_match_requests


def test_getSentMatchRequests_returnsEmptyList_whenNoRequestsExist(
    mocker,
    mock_db,
    mock_professional,
) -> None:
    # Arrange
    mock_get_professional_by_id = mocker.patch(
        "app.services.professional_service.get_professional_by_id",
        return_value=mock_professional,
    )
    mock_get_sent_match_requests = mocker.patch(
        "app.services.match_service.get_sent_match_requests_for_professional",
        return_value=[],
    )

    # Act
    result = professional_service.get_sent_match_requests(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    mock_get_sent_match_requests.assert_called_once_with(
        professional_id=mock_professional.id, db=mock_db
    )
    assert result == []


def test_getMatches_returnsJobAds_whenMatchesExist(mocker, mock_db, mock_professional):
    # Arrange
    mock_job_ad_1 = mocker.Mock()
    mock_job_ad_2 = mocker.Mock()
    mock_job_ad_preview_1 = mocker.Mock()
    mock_job_ad_preview_2 = mocker.Mock()

    mock_query = mock_db.query.return_value
    mock_join_match = mock_query.join.return_value
    mock_join_job_app = mock_join_match.join.return_value
    mock_filter = mock_join_job_app.filter.return_value
    mock_filter.all.return_value = [mock_job_ad_1, mock_job_ad_2]

    mocker.patch(
        "app.services.professional_service.JobAdPreview.create",
        side_effect=[mock_job_ad_preview_1, mock_job_ad_preview_2],
    )

    # Act
    result = professional_service._get_matches(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_once_with(JobAd)
    mock_query.join.assert_called_once()
    mock_join_match.join.assert_called_once()
    assert_filter_called_with(
        mock_join_job_app,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.MATCHED),
    )
    assert result == [mock_job_ad_preview_1, mock_job_ad_preview_2]


def test_getMatches_returnsEmptyList_whenNoMatchesExist(
    mocker, mock_db, mock_professional
):
    # Arrange
    mock_query = mock_db.query.return_value
    mock_join_match = mock_query.join.return_value
    mock_join_job_app = mock_join_match.join.return_value
    mock_filter = mock_join_job_app.filter.return_value
    mock_filter.all.return_value = []

    # Act
    result = professional_service._get_matches(
        professional_id=mock_professional.id, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_once_with(JobAd)
    mock_query.join.assert_called_once()
    mock_join_match.join.assert_called_once()
    assert_filter_called_with(
        mock_join_job_app,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.MATCHED),
    )
    assert result == []


def test_generateCvResponse_returnsStreamingResponse_withCorrectHeaders(
    mock_professional,
) -> None:
    # Arrange
    cv_content = b"sample_cv_content"
    expected_filename = (
        f"{mock_professional.first_name}_{mock_professional.last_name}_CV.pdf"
    )

    # Act
    response = professional_service._generate_cv_response(
        professional=mock_professional, cv=cv_content
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.media_type == "application/pdf"
    assert (
        response.headers["Content-Disposition"]
        == f"attachment; filename={expected_filename}"
    )
    assert response.headers["Access-Control-Expose-Headers"] == "Content-Disposition"
