from datetime import datetime
from unittest.mock import ANY

import pytest
from sqlalchemy import asc, desc

from app.schemas.city import City
from app.schemas.common import FilterParams, JobAdSearchParams, MessageResponse
from app.schemas.job_ad import JobAdCreate, JobAdUpdate
from app.sql_app.job_ad.job_ad_status import JobAdStatus
from app.services.job_ad_service import (
    _filter_by_salary,
    _filter_by_skills,
    _order_by,
    _search_job_ads,
    add_skill_requirement,
    create,
    get_all,
    get_by_id,
    update,
)
from app.sql_app.job_ad.job_ad import JobAd
from tests import test_data as td
from tests.utils import assert_called_with, assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_job_ad(mocker):
    def _create_mock_job_ad(job_ad: dict):
        location = mocker.Mock()
        location.id = td.VALID_CITY_ID
        location.name = td.VALID_CITY_NAME
        category = mocker.Mock()
        category.id = td.VALID_CATEGORY_ID
        category.title = td.VALID_CATEGORY_TITLE

        return mocker.MagicMock(
            **job_ad,
            location=location,
            category=category,
            status=JobAdStatus.ACTIVE,
        )
    
    return _create_mock_job_ad


def test_getAll_returnsJobAds_whenJobAdsExist(
    mocker, 
    mock_db,
    mock_job_ad,
) -> None:
    # Arrange
    filter_params = FilterParams(offset=0, limit=10)
    search_params = JobAdSearchParams()
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]
    job_ad_responses = [mocker.Mock(), mocker.Mock()]

    mock_query = mock_db.query.return_value
    mock_offset = mock_query.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = job_ads

    mock_search_job_ads = mocker.patch(
        "app.services.job_ad_service._search_job_ads", return_value=mock_query
    )
    mock_create = mocker.patch(
        "app.schemas.job_ad.JobAdResponse.create",
        side_effect=job_ad_responses,
    )

    # Act
    result = get_all(filter_params, search_params, mock_db)

    # Assert
    mock_search_job_ads.assert_called_with(search_params=search_params, db=mock_db)
    mock_query.offset.assert_called_with(filter_params.offset)
    mock_offset.limit.assert_called_with(filter_params.limit)
    mock_create.assert_any_call(job_ads[0])
    mock_create.assert_any_call(job_ads[1])
    assert len(result) == 2
    assert result[0] == job_ad_responses[0]
    assert result[1] == job_ad_responses[1]


def test_getAll_returnsEmptyList_whenNoJobAdsExist(mocker, mock_db) -> None:
    # Arrange
    filter_params = FilterParams(offset=0, limit=10)
    search_params = JobAdSearchParams()

    mock_query = mock_db.query.return_value
    mock_offset = mock_query.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = []

    mock_search_job_ads = mocker.patch(
        "app.services.job_ad_service._search_job_ads", return_value=mock_query
    )

    # Act
    result = get_all(filter_params, search_params, mock_db)

    # Assert
    mock_search_job_ads.assert_called_with(search_params=search_params, db=mock_db)
    mock_query.offset.assert_called_with(filter_params.offset)
    mock_offset.limit.assert_called_with(filter_params.limit)
    assert result == []


def test_getById_returnsJobAd_whenJobAdExists(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_response = mocker.Mock()

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )
    mock_create = mocker.patch(
        "app.schemas.job_ad.JobAdResponse.create",
        return_value=job_ad_response,
    )

    # Act
    result = get_by_id(td.VALID_JOB_AD_ID, mock_db)

    # Assert
    mock_get_job_ad_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        db=mock_db,
    )
    mock_create.assert_called_with(job_ad)
    assert result == job_ad_response


def test_create_createsJobAd_whenValidJobAd(mocker, mock_db) -> None:
    # Arrange
    job_ad_data = JobAdCreate(
        **td.JOB_AD_CREATE,
        company_id=td.VALID_COMPANY_ID,
        location=City(id=td.VALID_CITY_ID, name=td.VALID_CITY_NAME),
        category=mocker.Mock(id=td.VALID_CATEGORY_ID, title=td.VALID_CATEGORY_TITLE),
    )
    mock_company = mocker.Mock(
        id=td.VALID_COMPANY_ID,
        job_ads=list(),
        active_job_count=0,
    )
    mock_job_ad_response = mocker.Mock()

    mock_get_company_by_id = mocker.patch(
        "app.services.job_ad_service.get_company_by_id",
        return_value=mock_company,
    )
    mock_create_response = mocker.patch(
        "app.schemas.job_ad.JobAdResponse.create",
        return_value=mock_job_ad_response,
    )

    # Act
    result = create(job_ad_data=job_ad_data, db=mock_db)

    # Assert
    mock_db.add.assert_called_with(ANY)
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_with(ANY)
    mock_get_company_by_id.assert_called_with(
        company_id=mock_company.id,
        db=mock_db,
    )
    assert mock_company.active_job_count == 1
    assert result == mock_job_ad_response


def test_update_updatesJobAd_whenValidData(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad_data = JobAdUpdate(**td.JOB_AD_UPDATE)
    job_ad = mock_job_ad(td.JOB_AD)
    mock_job_ad_response = mocker.Mock()

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )
    mock_create_response = mocker.patch(
        "app.schemas.job_ad.JobAdResponse.create",
        return_value=mock_job_ad_response,
    )

    # Act
    result = update(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    mock_get_job_ad_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        db=mock_db,
    )
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_with(job_ad)
    mock_create_response.assert_called_with(job_ad)
    assert result == mock_job_ad_response


def test_updateJobAd_updatesTitle_whenTitleIsProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(title=td.VALID_JOB_AD_TITLE_2)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.title == job_ad_data.title
    assert isinstance(result.updated_at, datetime)

    assert result.description == job_ad.description
    assert result.city.id == job_ad.location.id
    assert result.city.name == job_ad.location.name
    assert result.min_salary == job_ad.min_salary
    assert result.max_salary == job_ad.max_salary
    assert result.status == job_ad.status


def test_updateJobAd_updatesDescription_whenDescriptionIsProvided(
    mocker, 
    mock_db, 
    mock_job_ad
) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(description=td.VALID_JOB_AD_DESCRIPTION_2)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.description == job_ad_data.description
    assert isinstance(result.updated_at, datetime)

    assert result.title == job_ad.title
    assert result.city.id == job_ad.location.id
    assert result.city.name == job_ad.location.name
    assert result.min_salary == job_ad.min_salary
    assert result.max_salary == job_ad.max_salary
    assert result.status == job_ad.status


def test_updateJobAd_updatesLocation_whenLocationIsProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(location_id=td.VALID_CITY_ID)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.city.id == job_ad_data.location_id
    assert isinstance(result.updated_at, datetime)

    assert result.title == job_ad.title
    assert result.description == job_ad.description
    assert result.min_salary == job_ad.min_salary
    assert result.max_salary == job_ad.max_salary
    assert result.status == job_ad.status


def test_updateJobAd_updatesMinSalary_whenMinSalaryIsProvided(
    mocker, 
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(min_salary=500.00)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.min_salary == job_ad_data.min_salary
    assert isinstance(result.updated_at, datetime)

    assert result.title == job_ad.title
    assert result.description == job_ad.description
    assert result.city.id == job_ad.location.id
    assert result.city.name == job_ad.location.name
    assert result.max_salary == job_ad.max_salary
    assert result.status == job_ad.status


def test_updateJobAd_updatesMaxSalary_whenMaxSalaryIsProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(max_salary=3000.00)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.max_salary == job_ad_data.max_salary
    assert isinstance(result.updated_at, datetime)

    assert result.title == job_ad.title
    assert result.description == job_ad.description
    assert result.city.id == job_ad.location.id
    assert result.city.name == job_ad.location.name
    assert result.min_salary == job_ad.min_salary
    assert result.status == job_ad.status


def test_updateJobAd_updatesStatus_whenStatusIsProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(status=JobAdStatus.ARCHIVED)

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.status == job_ad_data.status
    assert isinstance(result.updated_at, datetime)

    assert result.title == job_ad.title
    assert result.description == job_ad.description
    assert result.city.id == job_ad.location.id
    assert result.city.name == job_ad.location.name
    assert result.min_salary == job_ad.min_salary
    assert result.max_salary == job_ad.max_salary


def test_updateJobAd_updatesAllFields_whenAllFieldsAreProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate(
        title=td.VALID_JOB_AD_TITLE_2,
        description=td.VALID_JOB_AD_DESCRIPTION_2,
        location_id=td.VALID_CITY_ID,
        min_salary=500.00,
        max_salary=3000.00,
        status=JobAdStatus.ARCHIVED,
    )

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.title == job_ad_data.title
    assert result.description == job_ad_data.description
    assert result.city.id == job_ad_data.location_id
    assert result.min_salary == job_ad_data.min_salary
    assert result.max_salary == job_ad_data.max_salary
    assert result.status == job_ad_data.status
    assert isinstance(result.updated_at, datetime)


def test_updateJobAd_updatesNothing_whenNoFieldsAreProvided(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    job_ad_data = JobAdUpdate()

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )

    # Act
    result = update(
        job_ad_id=job_ad.id,
        job_ad_data=job_ad_data,
        db=mock_db,
    )

    # Assert
    assert result.title == job_ad.title
    assert result.description == job_ad.description
    assert result.city.id == job_ad.location.id
    assert result.min_salary == job_ad.min_salary
    assert result.max_salary == job_ad.max_salary
    assert result.status == job_ad.status
    assert result.updated_at != datetime.now()


def test_addSkillRequirement_addsSkillRequirement_whenValidData(
    mocker, 
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    job_ad = mock_job_ad(td.JOB_AD)
    skill = mocker.Mock()
    message_response = MessageResponse(message="Skill added to job ad")

    mock_get_job_ad_by_id = mocker.patch(
        "app.services.job_ad_service.get_job_ad_by_id",
        return_value=job_ad,
    )
    mock_get_skill_by_id = mocker.patch(
        "app.services.job_ad_service.get_skill_by_id",
        return_value=skill,
    )

    # Act
    result = add_skill_requirement(
        job_ad_id=td.VALID_JOB_AD_ID,
        skill_id=td.VALID_SKILL_ID,
        db=mock_db,
    )

    # Assert
    mock_get_job_ad_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        db=mock_db,
    )
    mock_get_skill_by_id.assert_called_with(
        skill_id=td.VALID_SKILL_ID,
        db=mock_db,
    )
    mock_db.add.assert_called_with(ANY)
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_with(ANY)
    assert result == message_response


def test_searchJobAds_filtersByCompanyId(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(company_id=td.VALID_COMPANY_ID)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = job_ads

    mock_filter_by_salary = mocker.patch(
        "app.services.job_ad_service._filter_by_salary",
        return_value=mock_filter,
    )
    mock_filter_by_skills = mocker.patch(
        "app.services.job_ad_service._filter_by_skills",
        return_value=mock_filter,
    )
    mock_order_by = mocker.patch(
        "app.services.job_ad_service._order_by",
        return_value=mock_filter,
    )

    # Act
    result = _search_job_ads(search_params=search_params, db=mock_db)

    # Assert
    assert_filter_called_with(
        mock_query=mock_query,
        expected_expression=JobAd.company_id == search_params.company_id,
    )
    assert result.all() == job_ads


def test_searchJobAds_filtersByStatus(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(job_ad_status=JobAdStatus.ACTIVE)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = job_ads

    mock_filter_by_salary = mocker.patch(
        "app.services.job_ad_service._filter_by_salary",
        return_value=mock_filter,
    )
    mock_filter_by_skills = mocker.patch(
        "app.services.job_ad_service._filter_by_skills",
        return_value=mock_filter,
    )
    mock_order_by = mocker.patch(
        "app.services.job_ad_service._order_by",
        return_value=mock_filter,
    )

    # Act
    result = _search_job_ads(search_params=search_params, db=mock_db)

    # Assert
    assert_filter_called_with(
        mock_query=mock_query,
        expected_expression=JobAd.status == search_params.job_ad_status,
    )
    assert result.all() == job_ads


def test_searchJobAds_filtersByTitle(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(title=td.VALID_JOB_AD_TITLE)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = job_ads

    mock_filter_by_salary = mocker.patch(
        "app.services.job_ad_service._filter_by_salary",
        return_value=mock_filter,
    )
    mock_filter_by_skills = mocker.patch(
        "app.services.job_ad_service._filter_by_skills",
        return_value=mock_filter,
    )
    mock_order_by = mocker.patch(
        "app.services.job_ad_service._order_by",
        return_value=mock_filter,
    )

    # Act
    result = _search_job_ads(search_params=search_params, db=mock_db)

    # Assert
    assert_filter_called_with(
        mock_query=mock_query,
        expected_expression=JobAd.title.ilike(f"%{search_params.title}%"),
    )
    assert result.all() == job_ads


def test_searchJobAds_filtersByLocation(mocker, mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(location_id=td.VALID_CITY_ID)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = job_ads

    mock_filter_by_salary = mocker.patch(
        "app.services.job_ad_service._filter_by_salary",
        return_value=mock_filter,
    )
    mock_filter_by_skills = mocker.patch(
        "app.services.job_ad_service._filter_by_skills",
        return_value=mock_filter,
    )
    mock_order_by = mocker.patch(
        "app.services.job_ad_service._order_by",
        return_value=mock_filter,
    )

    # Act
    result = _search_job_ads(search_params=search_params, db=mock_db)

    # Assert
    assert_filter_called_with(
        mock_query=mock_query,
        expected_expression=JobAd.location_id == search_params.location_id,
    )
    assert result.all() == job_ads


def test_filterBySalary_filtersByMinSalary(mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(min_salary=1000.00)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_first_filter = mock_query.filter.return_value
    mock_second_filter = mock_first_filter.filter.return_value
    mock_second_filter.all.return_value = job_ads

    # Act
    result = _filter_by_salary(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_filter_called_with(
        mock_query, (JobAd.min_salary - search_params.salary_threshold) <= float("inf")
    )
    assert_filter_called_with(
        mock_first_filter,
        (JobAd.max_salary + search_params.salary_threshold) >= search_params.min_salary,
    )
    assert result.all() == job_ads


def test_filterBySalary_filtersByMaxSalary(mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(max_salary=2000.00)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_first_filter = mock_query.filter.return_value
    mock_second_filter = mock_first_filter.filter.return_value
    mock_second_filter.all.return_value = job_ads

    # Act
    result = _filter_by_salary(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_filter_called_with(
        mock_query,
        (JobAd.min_salary - search_params.salary_threshold) <= search_params.max_salary,
    )
    assert_filter_called_with(
        mock_first_filter,
        (JobAd.max_salary + search_params.salary_threshold) >= float("-inf"),
    )
    assert result.all() == job_ads


def test_filterBySalary_filtersByMinAndMaxSalary(mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(min_salary=1000.00, max_salary=2000.00)
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_first_filter = mock_query.filter.return_value
    mock_second_filter = mock_first_filter.filter.return_value
    mock_second_filter.all.return_value = job_ads

    # Act
    result = _filter_by_salary(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_filter_called_with(
        mock_query,
        (JobAd.min_salary - search_params.salary_threshold) <= search_params.max_salary,
    )
    assert_filter_called_with(
        mock_first_filter,
        (JobAd.max_salary + search_params.salary_threshold) >= search_params.min_salary,
    )
    assert result.all() == job_ads


def test_filterBySkills_returnsJobAds_whenNoSkillsProvided(mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams()
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_query.all.return_value = job_ads

    # Act
    result = _filter_by_skills(
        job_ads=mock_query, search_params=search_params, db=mock_db
    )

    # Assert
    assert result.all() == job_ads


def test_filterBySkills_filtersBySkills_whenSkillsProvided(mock_db, mock_job_ad) -> None:
    # Arrange
    search_params = JobAdSearchParams(
        skills=[td.VALID_SKILL_NAME, td.VALID_SKILL_NAME_2]
    )
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_join.all.return_value = job_ads

    # Act
    result = _filter_by_skills(
        job_ads=mock_query, search_params=search_params, db=mock_db
    )

    # Assert
    assert result.all() == job_ads


def test_filterBySkills_filtersBySkills_whenSkillThresholdIsLessThanNumberOfSkills(
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(
        skills=[td.VALID_SKILL_NAME, td.VALID_SKILL_NAME_2],
        skills_threshold=1,
    )
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_join.all.return_value = job_ads

    # Act
    result = _filter_by_skills(
        job_ads=mock_query, search_params=search_params, db=mock_db
    )

    # Assert
    assert result.all() == job_ads


def test_filterBySkills_filtersBySkills_whenSkillThresholdEqualsNumberOfSkills(
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(
        skills=[td.VALID_SKILL_NAME, td.VALID_SKILL_NAME_2],
        skills_threshold=2,
    )
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_query.all.return_value = job_ads

    # Act
    result = _filter_by_skills(
        job_ads=mock_query, search_params=search_params, db=mock_db
    )

    # Assert
    assert result.all() == job_ads


def test_orderBy_ordersByCreatedAtAsc_whenCreatedAtAscIsProvided(
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(order_by="created_at", order="asc")
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_order_by = mock_query.order_by.return_value
    mock_order_by.all.return_value = job_ads

    # Act
    result = _order_by(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_called_with(mock_query.order_by, asc(JobAd.created_at))
    assert result.all() == job_ads


def test_orderBy_ordersByCreatedAtDesc_whenCreatedAtDescIsProvided(
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(order_by="created_at", order="desc")
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_order_by = mock_query.order_by.return_value
    mock_order_by.all.return_value = job_ads

    # Act
    result = _order_by(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_called_with(mock_query.order_by, desc(JobAd.created_at))
    assert result.all() == job_ads


def test_orderBy_ordersByUpdatedAtAsc_whenUpdatedAtAscIsProvided(
    mock_db, 
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(order_by="updated_at", order="asc")
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_order_by = mock_query.order_by.return_value
    mock_order_by.all.return_value = job_ads

    # Act
    result = _order_by(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_called_with(mock_query.order_by, asc(JobAd.updated_at))
    assert result.all() == job_ads


def test_orderBy_ordersByUpdatedAtDesc_whenUpdatedAtDescIsProvided(
    mock_db,
    mock_job_ad,
) -> None:
    # Arrange
    search_params = JobAdSearchParams(order_by="updated_at", order="desc")
    job_ads = [mock_job_ad(td.JOB_AD), mock_job_ad(td.JOB_AD_2)]

    mock_query = mock_db.query.return_value
    mock_order_by = mock_query.order_by.return_value
    mock_order_by.all.return_value = job_ads

    # Act
    result = _order_by(job_ads=mock_query, search_params=search_params)

    # Assert
    assert_called_with(mock_query.order_by, desc(JobAd.updated_at))
    assert result.all() == job_ads
