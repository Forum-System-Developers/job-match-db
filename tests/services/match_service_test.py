import pytest

from app.schemas.city import City
from app.schemas.common import MessageResponse
from app.schemas.match import (
    MatchRequestAd,
    MatchRequestApplication,
    MatchRequestCreate,
    MatchResponse,
)
from app.services import match_service
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_ad.job_ad_status import JobAdStatus
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.match.match import Match
from app.sql_app.match.match_status import MatchStatus
from app.sql_app.professional.professional_status import ProfessionalStatus
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_job_ads(mocker):
    job_ads = [
        mocker.Mock(**td.JOB_AD, company=mocker.Mock(), location=City(**td.CITY)),
        mocker.Mock(**td.JOB_AD_2, company=mocker.Mock(), location=City(**td.CITY_2)),
    ]
    job_ads[0].company.name = td.VALID_COMPANY_NAME
    job_ads[1].company.name = td.VALID_COMPANY_NAME_2

    return job_ads


@pytest.fixture
def mock_job_applications(mocker):
    job_applications = [
        mocker.Mock(
            **td.JOB_APPLICATION,
            professional=mocker.Mock(
                first_name=td.VALID_PROFESSIONAL_FIRST_NAME,
                last_name=td.VALID_PROFESSIONAL_LAST_NAME,
                status=ProfessionalStatus.ACTIVE,
            ),
        ),
        mocker.Mock(
            **td.JOB_APPLICATION_2,
            professional=mocker.Mock(
                first_name=td.VALID_PROFESSIONAL_FIRST_NAME_2,
                last_name=td.VALID_PROFESSIONAL_LAST_NAME_2,
                status=ProfessionalStatus.ACTIVE,
            ),
        ),
    ]
    job_applications[0].name = td.VALID_JOB_APPLICATION_NAME
    job_applications[1].name = td.VALID_JOB_APPLICATION_NAME_2

    return job_applications


def test_create_createsMatchRequest_whenValidData(mocker, mock_db) -> None:
    # Arrange
    match_request_data = MatchRequestCreate(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        status=MatchStatus.REQUESTED_BY_JOB_APP,
    )
    mock_db.add = mocker.Mock()
    mock_db.commit = mocker.Mock()
    mock_db.refresh = mocker.Mock()

    # Act
    result = match_service.create(
        match_request_data=match_request_data,
        db=mock_db,
    )

    # Assert
    mock_db.add.assert_called()
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called()
    assert isinstance(result, MessageResponse)
    assert result.message == "Match request created successfully"


def test_getById_returnsMatch_whenValidData(mocker, mock_db) -> None:
    # Arrange
    match = mocker.Mock(**td.MATCH)

    mock_get_match_by_id = mocker.patch(
        "app.services.match_service.get_match_by_id",
        return_value=match,
    )

    # Act
    result = match_service.get_by_id(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )

    # Assert
    mock_get_match_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )
    assert result.job_ad_id == td.VALID_JOB_AD_ID
    assert result.job_application_id == td.VALID_JOB_APPLICATION_ID
    assert result.status == td.MATCH["status"]


def test_updateStatus_updatesMatchStatus_whenValidData(mocker, mock_db) -> None:
    # Arrange
    match = mocker.Mock(**td.MATCH)
    match_request_data = mocker.Mock(status=MatchStatus.ACCEPTED)

    mock_get_match_by_id = mocker.patch(
        "app.services.match_service.get_match_by_id",
        return_value=match,
    )

    # Act
    result = match_service.update_status(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        match_request_data=match_request_data,
        db=mock_db,
    )

    # Assert
    mock_get_match_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )
    assert match.status == MatchStatus.ACCEPTED
    mock_db.commit.assert_called()
    assert isinstance(result, MessageResponse)
    assert result.message == "Match request updated successfully"


def test_acceptMatchRequest_acceptsMatchRequest_whenValidData(mocker, mock_db) -> None:
    # Arrange
    job_ad = mocker.Mock(**td.JOB_AD, status=JobAdStatus.ACTIVE)
    job_ad.company = mocker.Mock(successfull_matches_count=0)
    job_application = mocker.Mock(**td.JOB_APPLICATION)
    job_application.professional = mocker.Mock(active_application_count=1)
    match = mocker.Mock(**td.MATCH, job_application=job_application, job_ad=job_ad)

    mock_get_match_by_id = mocker.patch(
        "app.services.match_service.get_match_by_id",
        return_value=match,
    )

    # Act
    result = match_service.accept_match_request(
        job_ad_id=job_ad.id,
        job_application_id=job_application.id,
        db=mock_db,
    )

    # Assert
    mock_get_match_by_id.assert_called_with(
        job_ad_id=td.VALID_JOB_AD_ID,
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
    )
    assert job_ad.status == JobAdStatus.ARCHIVED
    assert job_application.status == JobStatus.MATCHED
    assert match.status == MatchStatus.ACCEPTED
    assert match.job_application.professional.active_application_count == 0
    assert job_ad.company.successfull_matches_count == 1
    mock_db.commit.assert_called()
    assert result.message == "Match request accepted successfully"


def test_getMatchRequestsForJobApplication_returnsMatchRequests_whenValidData(
    mocker, mock_db, mock_job_ads
) -> None:
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_offset = mock_filter.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = [
        (mocker.Mock(**td.MATCH), mock_job_ads[0]),
        (mocker.Mock(**td.MATCH_2), mock_job_ads[1]),
    ]

    # Act
    result = match_service.get_match_requests_for_job_application(
        job_application_id=td.VALID_JOB_APPLICATION_ID,
        db=mock_db,
        filter_params=filter_params,
    )

    # Assert
    assert_filter_called_with(
        mock_join,
        (Match.job_application_id == td.VALID_JOB_APPLICATION_ID)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_AD),
    )
    mock_filter.offset.assert_called_with(filter_params.offset)
    mock_offset.limit.assert_called_with(filter_params.limit)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchRequestAd)
    assert isinstance(result[1], MatchRequestAd)


def test_getMatchRequestsForProfessional_returnsMatchRequests_whenValidData(
    mocker,
    mock_db,
    mock_job_ads,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_join_job_app = mock_query.join.return_value
    mock_join_job_ad = mock_join_job_app.join.return_value
    mock_filter = mock_join_job_ad.filter.return_value
    mock_filter.all.return_value = [
        (mocker.Mock(**td.MATCH), mock_job_ads[0]),
        (mocker.Mock(**td.MATCH_2), mock_job_ads[1]),
    ]

    # Act
    result = match_service.get_match_requests_for_professional(
        professional_id=td.VALID_PROFESSIONAL_ID,
        db=mock_db,
    )

    # Assert
    assert_filter_called_with(
        mock_join_job_ad,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.ACTIVE)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_APP),
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchRequestAd)
    assert isinstance(result[1], MatchRequestAd)


def test_getSentMatchRequestsForProfessional_returnsMatchRequests_whenValidData(
    mocker,
    mock_db,
    mock_job_ads,
) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_join_job_app = mock_query.join.return_value
    mock_join_job_ad = mock_join_job_app.join.return_value
    mock_filter = mock_join_job_ad.filter.return_value
    mock_filter.all.return_value = [
        (mocker.Mock(**td.MATCH), mock_job_ads[0]),
        (mocker.Mock(**td.MATCH_2), mock_job_ads[1]),
    ]

    # Act
    result = match_service.get_sent_match_requests_for_professional(
        professional_id=td.VALID_PROFESSIONAL_ID,
        db=mock_db,
    )

    # Assert
    assert_filter_called_with(
        mock_join_job_ad,
        (JobApplication.professional_id == td.VALID_PROFESSIONAL_ID)
        & (JobApplication.status == JobStatus.ACTIVE)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_APP),
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchRequestAd)
    assert isinstance(result[1], MatchRequestAd)


def test_getMatchRequestsForCompany_returnsMatchRequests_whenValidData(
    mocker, mock_db, mock_job_applications
) -> None:
    # Arrange
    filter_params = mocker.Mock(offset=0, limit=10)

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_join_job_ad = mock_join.join.return_value
    mock_filter = mock_join_job_ad.filter.return_value
    mock_offset = mock_filter.offset.return_value
    mock_limit = mock_offset.limit.return_value
    mock_limit.all.return_value = [
        (mocker.Mock(**td.MATCH), mock_job_applications[0]),
        (mocker.Mock(**td.MATCH_2), mock_job_applications[1]),
    ]

    # Act
    result = match_service.get_match_requests_for_company(
        company_id=td.VALID_COMPANY_ID,
        db=mock_db,
        filter_params=filter_params,
    )

    # Assert
    assert_filter_called_with(
        mock_join_job_ad,
        (JobAd.company_id == td.VALID_COMPANY_ID)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_APP),
    )
    mock_filter.offset.assert_called_with(filter_params.offset)
    mock_offset.limit.assert_called_with(filter_params.limit)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchRequestApplication)
    assert isinstance(result[1], MatchRequestApplication)


def test_getJobAdReceivedMatches_returnsMatches_whenValidData(mocker, mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = [
        mocker.Mock(**td.MATCH),
        mocker.Mock(**td.MATCH_2),
    ]

    # Act
    result = match_service.get_job_ad_received_matches(
        job_ad_id=td.VALID_JOB_AD_ID,
        db=mock_db,
    )

    # Assert
    assert_filter_called_with(
        mock_join,
        (JobAd.id == td.VALID_JOB_AD_ID)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_APP),
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchResponse)
    assert isinstance(result[1], MatchResponse)


def test_getJobAdSentMatches_returnsMatches_whenValidData(mocker, mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = [
        mocker.Mock(**td.MATCH),
        mocker.Mock(**td.MATCH_2),
    ]

    # Act
    result = match_service.get_job_ad_sent_matches(
        job_ad_id=td.VALID_JOB_AD_ID,
        db=mock_db,
    )

    # Assert
    assert_filter_called_with(
        mock_query,
        (Match.job_ad_id == td.VALID_JOB_AD_ID)
        & (Match.status == MatchStatus.REQUESTED_BY_JOB_AD),
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], MatchResponse)
    assert isinstance(result[1], MatchResponse)
