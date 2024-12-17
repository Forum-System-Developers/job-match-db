import pytest

from app.schemas.category import CategoryResponse
from app.services import category_service
from app.sql_app.category.category import Category
from tests import test_data as td


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


def test_getAll_returnsCategories_whenCategoriesExist(mocker, mock_db) -> None:
    # Arrange
    categories = [mocker.MagicMock(**td.CATEGORY), mocker.MagicMock(**td.CATEGORY_2)]

    mock_query = mock_db.query.return_value
    mock_query.all.return_value = categories

    # Act
    result = category_service.get_all(mock_db)

    # Assert
    mock_db.query.assert_called_with(Category)
    mock_query.all.assert_called_once()
    assert len(result) == 2
    assert isinstance(result, list)
    assert isinstance(result[0], CategoryResponse)
    assert isinstance(result[1], CategoryResponse)


def test_getAll_returnsEmptyList_whenNoCategoriesExist(mock_db) -> None:
    # Arrange
    mock_query = mock_db.query.return_value
    mock_query.all.return_value = []

    # Act
    result = category_service.get_all(mock_db)

    # Assert
    mock_db.query.assert_called_with(Category)
    mock_query.all.assert_called()
    assert result == []
