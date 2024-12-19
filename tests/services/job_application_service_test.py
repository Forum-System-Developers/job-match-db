from datetime import datetime
from unittest.mock import ANY

import pytest

from app.schemas.job_application import JobApplicationResponse, JobApplicationUpdate
from app.schemas.skill import SkillResponse
from app.services import job_application_service
from app.sql_app.job_application.job_application_status import JobStatus
from tests import test_data as td


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_job_application(mocker):
    job_application = mocker.Mock(
        id=td.VALID_JOB_APPLICATION_ID,
        category_id=td.VALID_CATEGORY_ID,
        category_title=td.VALID_CATEGORY_TITLE,
        description=td.VALID_JOB_APPLICATION_DESCRIPTION,
        city_id=td.VALID_CITY_ID,
        min_salary=1000.00,
        max_salary=2000.00,
        status=JobStatus.ACTIVE,
        created_at=datetime.now(),
        is_main=False,
    )
    job_application.name = td.VALID_JOB_APPLICATION_NAME
    city = mocker.Mock(id=td.VALID_CITY_ID)
    city.name = td.VALID_CITY_NAME
    job_application.professional = mocker.Mock(
        id=td.VALID_PROFESSIONAL_ID,
        first_name=td.VALID_PROFESSIONAL_FIRST_NAME,
        last_name=td.VALID_PROFESSIONAL_LAST_NAME,
        email=td.VALID_PROFESSIONAL_EMAIL,
        photo=b"photo",
        city=city,
    )
    job_application.category = mocker.Mock(
        id=td.VALID_CATEGORY_ID, title=td.VALID_CATEGORY_TITLE
    )
    job_application.skills = [
        mocker.Mock(
            id=td.VALID_SKILL_ID,
            category_id=td.VALID_CATEGORY_ID,
        ),
        mocker.Mock(
            id=td.VALID_SKILL_ID_2,
            category_id=td.VALID_CATEGORY_ID_2,
        ),
    ]
    job_application.skills[0].name = td.VALID_SKILL_NAME
    job_application.skills[1].name = td.VALID_SKILL_NAME_2

    return job_application


@pytest.fixture
def skills_response(mock_job_application):
    return [SkillResponse.create(skill) for skill in mock_job_application.skills]


def test_getAllJobApplications_withSkills(mocker, mock_db):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(
        order="asc", order_by="created_at", skills=["Python", "Linux", "React"]
    )

    mock_job_app = [(mocker.Mock(), mocker.Mock())]
    mock_job_app_response = [(mocker.Mock(), mocker.Mock())]

    mock_query = mock_db.query.return_value
    mock_join_1 = mock_query.join.return_value
    mock_filter_1 = mock_join_1.filter.return_value
    mock_join_2 = mock_filter_1.join.return_value
    mock_join_3 = mock_join_2.join.return_value
    mock_filter_2 = mock_join_3.filter.return_value
    mock_offset = mock_filter_2.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_job_app

    mocker.patch(
        "app.schemas.job_application.JobApplicationResponse.create",
        side_effect=mock_job_app_response,
    )

    # Act
    result = job_application_service.get_all(
        filter_params=filter_params,
        search_params=search_params,
        db=mock_db,
    )

    # Assert
    assert result == mock_job_app_response


def test_getAllJobApplications_withNoSkills(mocker, mock_db):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(order="asc", order_by="created_at", skills=[])

    mock_job_app = [(mocker.Mock(), mocker.Mock())]
    mock_job_app_response = [(mocker.Mock(), mocker.Mock())]

    mock_query = mock_db.query.return_value
    mock_join_1 = mock_query.join.return_value
    mock_filter_1 = mock_join_1.filter.return_value
    mock_offset = mock_filter_1.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_job_app

    mocker.patch(
        "app.schemas.job_application.JobApplicationResponse.create",
        side_effect=mock_job_app_response,
    )

    # Act
    result = job_application_service.get_all(
        filter_params=filter_params,
        search_params=search_params,
        db=mock_db,
    )

    # Assert
    assert result == mock_job_app_response


def test_getAllJobApplications_withOrderDesc(mocker, mock_db):
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)
    search_params = mocker.Mock(order="desc", order_by="created_at", skills=[])

    mock_job_app = [(mocker.Mock(), mocker.Mock())]
    mock_job_app_response = [(mocker.Mock(), mocker.Mock())]

    mock_query = mock_db.query.return_value
    mock_join_1 = mock_query.join.return_value
    mock_filter_1 = mock_join_1.filter.return_value
    mock_offset = mock_filter_1.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = mock_job_app

    mocker.patch(
        "app.schemas.job_application.JobApplicationResponse.create",
        side_effect=mock_job_app_response,
    )

    # Act
    result = job_application_service.get_all(
        filter_params=filter_params,
        search_params=search_params,
        db=mock_db,
    )

    # Assert
    assert result == mock_job_app_response


def test_getById_ReturnsJobApplicationResponse(
    mocker,
    mock_db,
    mock_job_application,
):
    # Arrange
    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.get_by_id(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_once_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )

    assert isinstance(result, JobApplicationResponse)


def test_create_createsJobApplication_whenValidData(
    mocker,
    mock_db,
) -> None:
    # Arrange
    mock_professional = mocker.Mock(
        id=td.VALID_PROFESSIONAL_ID,
        active_application_count=0,
    )
    job_application_create = mocker.Mock(
        professional_id=td.VALID_PROFESSIONAL_ID,
        skills=[mocker.Mock(name=td.VALID_SKILL_NAME)],
        status=JobStatus.ACTIVE,
    )
    mock_job_application_response = mocker.Mock()

    mock_get_professional_by_id = mocker.patch(
        "app.services.job_application_service.get_professional_by_id",
        return_value=mock_professional,
    )

    job_application_create.model_dump.return_value = {}

    mock_add_skills = mocker.patch("app.services.job_application_service._add_skills")

    mock_job_application_create = mocker.patch(
        "app.services.job_application_service.JobApplicationResponse.create",
        return_value=mock_job_application_response,
    )

    # Act
    result = job_application_service.create(
        job_application_create=job_application_create,
        db=mock_db,
    )

    # Assert
    mock_get_professional_by_id.assert_called_once_with(
        professional_id=job_application_create.professional_id,
        db=mock_db,
    )
    mock_db.add.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(ANY)
    assert mock_professional.active_application_count == 1
    assert result == mock_job_application_response


def test_update_updatesJobApplication_whenValidData(
    mocker, mock_db, mock_job_application
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(
        **td.JOB_APPLICATION_UPDATE,
    )

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_with(mock_job_application)
    assert isinstance(result, JobApplicationResponse)


def test_update_updatesName_whenNameIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(name=td.VALID_JOB_APPLICATION_NAME)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert result.name == job_application_data.name
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesDescription_whenDescriptionIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(
        description=td.VALID_JOB_APPLICATION_DESCRIPTION
    )

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert result.description == job_application_data.description
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesMinSalary_whenMinSalaryIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(min_salary=500.00)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert result.min_salary == job_application_data.min_salary
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesMaxSalary_whenMaxSalaryIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(max_salary=3000.00)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert result.max_salary == job_application_data.max_salary
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesStatus_whenStatusIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    status = JobStatus.PRIVATE
    job_application_data = JobApplicationUpdate(status=status)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert result.status == status.value
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesCityId_whenCityIdIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(city_id=td.VALID_CITY_ID_2)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert mock_job_application.city_id == job_application_data.city_id
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.skills == skills_response


def test_update_updatesIsMain_whenIsMainIsProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate(is_main=True)

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert mock_job_application.is_main == job_application_data.is_main
    assert isinstance(mock_job_application.updated_at, datetime)

    assert result.name == mock_job_application.name
    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_update_updatesAllFields_whenAllFieldsAreProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    status = JobStatus.PRIVATE
    job_application_data = JobApplicationUpdate(
        name=td.VALID_JOB_APPLICATION_NAME_2,
        description=td.VALID_JOB_APPLICATION_DESCRIPTION_2,
        min_salary=50.00,
        max_salary=3500.00,
        status=status,
        city_id=td.VALID_CITY_ID_2,
        is_main=True,
    )

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert isinstance(mock_job_application.updated_at, datetime)
    assert result.name == job_application_data.name
    assert result.description == job_application_data.description
    assert result.min_salary == job_application_data.min_salary
    assert result.max_salary == job_application_data.max_salary
    assert result.status == status.value
    assert mock_job_application.is_main == job_application_data.is_main
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response

    assert result.application_id == mock_job_application.id
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary


def test_update_updatesNothing_whenNoFieldsAreProvided(
    mocker,
    mock_db,
    mock_job_application,
    skills_response,
) -> None:
    # Arrange
    job_application_data = JobApplicationUpdate()

    mock_get_job_application_by_id = mocker.patch(
        "app.services.job_application_service.get_job_application_by_id",
        return_value=mock_job_application,
    )

    # Act
    result = job_application_service.update(
        job_application_id=mock_job_application.id,
        job_application_data=job_application_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_application_by_id.assert_called_with(
        job_application_id=mock_job_application.id,
        db=mock_db,
    )
    assert not isinstance(mock_job_application, datetime)
    assert mock_job_application.is_main == mock_job_application.is_main
    assert result.application_id == mock_job_application.id
    assert result.name == mock_job_application.name
    assert result.professional_id == mock_job_application.professional.id
    assert result.created_at == mock_job_application.created_at
    assert result.category_id == mock_job_application.category_id
    assert result.category_title == mock_job_application.category.title
    assert result.photo == mock_job_application.professional.photo
    assert result.first_name == mock_job_application.professional.first_name
    assert result.last_name == mock_job_application.professional.last_name
    assert result.email == mock_job_application.professional.email
    assert result.status == mock_job_application.status.value
    assert result.min_salary == mock_job_application.min_salary
    assert result.max_salary == mock_job_application.max_salary
    assert result.description == mock_job_application.description
    assert result.city == mock_job_application.professional.city.name
    assert result.skills == skills_response


def test_addSkills_addsNewSkills_whenSkillsListIsNotEmpty(mocker, mock_db):
    # Arrange
    job_application = mocker.Mock(id=td.VALID_JOB_APPLICATION_ID, skills=[])
    skills = [mocker.Mock(), mocker.Mock()]
    skills[0].name = td.VALID_SKILL_NAME
    skills[1].name = td.VALID_SKILL_NAME_2

    mock_get_skill_by_name = mocker.patch(
        "app.services.job_application_service.get_skill_by_name", side_effect=skills
    )

    # Act
    job_application_service._add_skills(
        job_application=job_application,
        skills=skills,
        db=mock_db,
    )

    # Assert
    mock_get_skill_by_name.assert_any_call(skill_name=td.VALID_SKILL_NAME, db=mock_db)
    mock_get_skill_by_name.assert_any_call(skill_name=td.VALID_SKILL_NAME_2, db=mock_db)
    assert len(job_application.skills) == 2
    assert job_application.skills[0].name == td.VALID_SKILL_NAME
    assert job_application.skills[1].name == td.VALID_SKILL_NAME_2


def test_addSkills_doesNotAddAnySkills_whenSkillsListIsEmpty(mocker, mock_db):
    # Arrange
    job_application = mocker.Mock(id=td.VALID_JOB_APPLICATION_ID, skills=[])
    skills = []

    # Act
    job_application_service._add_skills(
        job_application=job_application,
        skills=skills,
        db=mock_db,
    )

    # Assert
    assert len(job_application.skills) == 0
