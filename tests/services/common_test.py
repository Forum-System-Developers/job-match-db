import pytest
from fastapi import status

from app.exceptions.custom_exceptions import ApplicationError
from app.services.common import (
    get_company_by_id,
    get_job_ad_by_id,
    get_job_application_by_id,
    get_match_by_id,
    get_professional_by_id,
    get_skill_by_id,
    get_skill_by_name,
)
from app.sql_app.company.company import Company
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.match.match import Match
from app.sql_app.professional.professional import Professional
from app.sql_app.skill.skill import Skill
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


def test_getCompanyById_returnsCompany_whenCompanyFound(mocker, mock_db) -> None:
    # Arrange
    company = mocker.Mock(id=td.VALID_COMPANY_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = company

    # Act
    result = get_company_by_id(company_id=td.VALID_COMPANY_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Company)
    assert_filter_called_with(mock_query, Company.id == td.VALID_COMPANY_ID)
    assert result == company


def test_getCompanyById_raisesApplicationError_whenCompanyNotFound(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_company_by_id(company_id=td.VALID_COMPANY_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Company)
    assert_filter_called_with(mock_query, Company.id == td.VALID_COMPANY_ID)
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc_info.value.data.detail == f"No company found with id {td.VALID_COMPANY_ID}"
    )


def test_getJobAdById_returnsJobAd_whenJobAdFound(mocker, mock_db) -> None:
    # Arrange
    job_ad = mocker.Mock(id=td.VALID_JOB_AD_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = job_ad

    # Act
    result = get_job_ad_by_id(job_ad_id=td.VALID_JOB_AD_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(JobAd)
    assert_filter_called_with(mock_query, JobAd.id == td.VALID_JOB_AD_ID)
    assert result == job_ad


def test_getJobAdById_raisesApplicationError_whenJobAdNotFound(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_job_ad_by_id(job_ad_id=td.VALID_JOB_AD_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(JobAd)
    assert_filter_called_with(mock_query, JobAd.id == td.VALID_JOB_AD_ID)
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc_info.value.data.detail == f"Job ad with id {td.VALID_JOB_AD_ID} not found"
    )


def test_getJobApplicationById_returnsJobApplication_whenJobApplicationFound(
    mocker, mock_db
) -> None:
    # Arrange
    job_application = mocker.Mock(id=td.VALID_JOB_APPLICATION_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = job_application

    # Act
    result = get_job_application_by_id(
        job_application_id=td.VALID_JOB_APPLICATION_ID, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query, JobApplication.id == td.VALID_JOB_APPLICATION_ID
    )
    assert result == job_application


def test_getJobApplicationById_raisesApplicationError_whenJobApplicationNotFound(
    mock_db,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_job_application_by_id(
            job_application_id=td.VALID_JOB_APPLICATION_ID, db=mock_db
        )

    # Assert
    mock_db.query.assert_called_once_with(JobApplication)
    assert_filter_called_with(
        mock_query, JobApplication.id == td.VALID_JOB_APPLICATION_ID
    )
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc_info.value.data.detail
        == f"Job Aplication with id {td.VALID_JOB_APPLICATION_ID} not found."
    )


def test_getProfessionalById_returnsProfessional_whenProfessionalFound(
    mocker, mock_db
) -> None:
    # Arrange
    professional = mocker.Mock(id=td.VALID_PROFESSIONAL_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = professional

    # Act
    result = get_professional_by_id(
        professional_id=td.VALID_PROFESSIONAL_ID, db=mock_db
    )

    # Assert
    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(mock_query, Professional.id == td.VALID_PROFESSIONAL_ID)
    assert result == professional


def test_getProfessionalById_raisesApplicationError_whenProfessionalNotFound(
    mock_db,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_professional_by_id(professional_id=td.VALID_PROFESSIONAL_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Professional)
    assert_filter_called_with(mock_query, Professional.id == td.VALID_PROFESSIONAL_ID)
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc_info.value.data.detail
        == f"Professional with id {td.VALID_PROFESSIONAL_ID} not found"
    )


def test_getSkillById_returnsSkill_whenSkillFound(mocker, mock_db) -> None:
    # Arrange
    skill = mocker.Mock(id=td.VALID_SKILL_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = skill

    # Act
    result = get_skill_by_id(skill_id=td.VALID_SKILL_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.id == td.VALID_SKILL_ID)
    assert result == skill


def test_getSkillById_raisesApplicationError_whenSkillNotFound(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_skill_by_id(skill_id=td.VALID_SKILL_ID, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.id == td.VALID_SKILL_ID)
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc_info.value.data.detail == f"Skill with id {td.VALID_SKILL_ID} not found"


def test_getSkillByName_returnsSkill_whenSkillFound(mocker, mock_db) -> None:
    # Arrange
    skill = mocker.Mock(name=td.VALID_SKILL_NAME)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = skill

    # Act
    result = get_skill_by_name(skill_name=td.VALID_SKILL_NAME, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.name == td.VALID_SKILL_NAME)
    assert result == skill


def test_getSkillByName_raisesApplicationError_whenSkillNotFound(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_skill_by_name(skill_name=td.VALID_SKILL_NAME, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.name == td.VALID_SKILL_NAME)
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert (
        exc_info.value.data.detail
        == f"Skill with name {td.VALID_SKILL_NAME} not found."
    )


def test_getMatchById_returnsMatch_whenMatchFound(mocker, mock_db) -> None:
    # Arrange
    match = mocker.Mock(
        job_ad_id=td.VALID_JOB_AD_ID, job_application_id=td.VALID_JOB_APPLICATION_ID
    )
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = match

    # Act
    result = get_match_by_id(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )

    # Assert
    mock_db.query.assert_called_once_with(Match)
    assert_filter_called_with(
        mock_query,
        (Match.job_ad_id == td.VALID_JOB_AD_ID)
        & (Match.job_application_id == td.VALID_JOB_APPLICATION_ID),
    )
    assert result == match


def test_getMatchById_raisesApplicationError_whenMatchNotFound(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    with pytest.raises(ApplicationError) as exc_info:
        get_match_by_id(
            job_ad_id=td.VALID_JOB_AD_ID,
            job_application_id=td.VALID_JOB_APPLICATION_ID,
            db=mock_db,
        )

    # Assert
    mock_db.query.assert_called_once_with(Match)
    assert_filter_called_with(
        mock_query,
        (Match.job_ad_id == td.VALID_JOB_AD_ID)
        & (Match.job_application_id == td.VALID_JOB_APPLICATION_ID),
    )
    assert exc_info.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc_info.value.data.detail == "Match request not found"
