import pytest
from fastapi import status

from app.exceptions.custom_exceptions import ApplicationError
from app.schemas.skill import SkillCreate, SkillResponse
from app.services import skill_service
from app.sql_app.skill.skill import Skill
from tests import test_data as td
from tests.utils import assert_filter_called_with


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_skill(mocker):
    def _create_mock_skill(id, name, category_id):
        skill = mocker.Mock()
        skill.id = id
        skill.name = name
        skill.category_id = category_id
        return skill

    return _create_mock_skill


def test_getAllForCategory_returnsListOfSkillResponse_whenSkillsExist(
    mock_db, mock_skill
):
    # Arrange
    category_id = td.VALID_CATEGORY_ID
    skills = [
        mock_skill(
            id=td.VALID_SKILL_ID,
            name=td.VALID_SKILL_NAME,
            category_id=category_id,
        ),
        mock_skill(
            id=td.VALID_SKILL_ID_2,
            name=td.VALID_SKILL_NAME_2,
            category_id=category_id,
        ),
    ]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = skills

    # Act
    response = skill_service.get_all_for_category(category_id=category_id, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.category_id == category_id)
    mock_filter.all.assert_called_once()
    assert len(response) == 2
    assert response[0].id == td.VALID_SKILL_ID
    assert response[0].name == td.VALID_SKILL_NAME
    assert response[0].category_id == category_id
    assert response[1].id == td.VALID_SKILL_ID_2
    assert response[1].name == td.VALID_SKILL_NAME_2
    assert response[1].category_id == category_id


def test_getAllForCategory_returnsEmptyList_whenNoSkillsExist(mock_db):
    # Arrange
    category_id = td.VALID_CATEGORY_ID

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = []

    # Act
    response = skill_service.get_all_for_category(category_id=category_id, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.category_id == category_id)
    mock_filter.all.assert_called_once()
    assert response == []


def test_getById_returnsSkillResponse_whenSkillExists(mock_db, mock_skill):
    # Arrange
    skill_id = td.VALID_SKILL_ID
    skill = mock_skill(
        id=skill_id,
        name=td.VALID_SKILL_NAME,
        category_id=td.VALID_CATEGORY_ID,
    )

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = skill

    # Act
    response = skill_service.get_by_id(skill_id=skill_id, db=mock_db)

    # Assert
    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.id == skill_id)
    mock_filter.first.assert_called_once()
    assert response.id == skill_id
    assert response.name == td.VALID_SKILL_NAME
    assert response.category_id == td.VALID_CATEGORY_ID


def test_getById_raisesError_whenSkillDoesNotExist(mock_db):
    # Arrange
    skill_id = td.VALID_SKILL_ID

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        skill_service.get_by_id(skill_id=skill_id, db=mock_db)

    mock_db.query.assert_called_once_with(Skill)
    assert_filter_called_with(mock_query, Skill.id == skill_id)
    mock_filter.first.assert_called_once()
    assert exc.value.data.status == status.HTTP_404_NOT_FOUND
    assert exc.value.data.detail == f"Skill with id {skill_id} not found"


def test_create_createsSkill_whenValidData(mocker, mock_db):
    # Arrange
    skill_data = SkillCreate(name=td.VALID_SKILL_NAME, category_id=td.VALID_CATEGORY_ID)
    mock_response = mocker.Mock()
    mock_skill_response_create = mocker.patch(
        "app.services.skill_service.SkillResponse.create",
        return_value=mock_response,
    )

    # Act
    response = skill_service.create(skill_data=skill_data, db=mock_db)

    # Assert
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    mock_skill_response_create.assert_called_once()
    assert response == mock_response


def test_createPendingSkill_createsSkill_whenValidData(mocker, mock_db):
    # Arrange
    skill_data = SkillCreate(name=td.VALID_SKILL_NAME, category_id=td.VALID_CATEGORY_ID)
    skill_response = (
        SkillResponse(
            id=td.VALID_SKILL_ID,
            name=td.VALID_SKILL_NAME,
            category_id=td.VALID_CATEGORY_ID,
        ),
    )

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    mock_skill_response = mocker.patch(
        "app.services.skill_service.SkillResponse",
        return_value=skill_response,
    )

    # Act
    response = skill_service.create_pending_skill(
        company_id=td.VALID_COMPANY_ID, skill_data=skill_data, db=mock_db
    )

    # Assert
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    mock_skill_response.assert_called_once()
    assert response == skill_response


def test_createPendingSkill_raisesError_whenSkillAlreadyExists(mocker, mock_db):
    # Arrange
    skill_data = SkillCreate(name=td.VALID_SKILL_NAME, category_id=td.VALID_CATEGORY_ID)
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(ApplicationError) as exc:
        skill_service.create_pending_skill(
            company_id=td.VALID_COMPANY_ID, skill_data=skill_data, db=mock_db
        )

    assert exc.value.data.status == status.HTTP_409_CONFLICT
    assert exc.value.data.detail == f"Skill with name {skill_data.name} already exists"
