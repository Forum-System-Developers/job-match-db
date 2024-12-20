import json

import pytest
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.exceptions.custom_exceptions import ApplicationError
from app.utils.processors import (
    _format_response,
    process_db_transaction,
    process_request,
)


@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


def test_processRequest_returnsSuccessfulResponse_whenDataIsValid(
    mocker,
    mock_db,
) -> None:
    # Arrange
    get_entities_fn = mocker.Mock()
    status_code = status.HTTP_200_OK
    not_found_err_msg = "Entity not found"
    mock_result = mocker.Mock()

    mock_process_db_transaction = mocker.patch(
        "app.utils.processors.process_db_transaction",
        return_value=mock_result,
    )
    mock_format_response = mocker.patch(
        "app.utils.processors._format_response",
        return_value={"key": "value"},
    )

    # Act
    response = process_request(
        get_entities_fn=get_entities_fn,
        status_code=status_code,
        not_found_err_msg=not_found_err_msg,
        db=mock_db,
    )

    # Assert
    mock_process_db_transaction.assert_called_once_with(
        transaction_func=get_entities_fn,
        db=mock_db,
    )
    mock_format_response.assert_called_once_with(mock_result)
    assert response.status_code == status_code
    assert json.loads(response.body) == {"key": "value"}


def test_processRequest_handlesApplicationError(mocker, mock_db) -> None:
    # Arrange
    get_entities_fn = mocker.Mock()
    status_code = status.HTTP_200_OK
    not_found_err_msg = "Entity not found"

    mock_process_db_transaction = mocker.patch(
        "app.utils.processors.process_db_transaction",
        side_effect=ApplicationError(
            detail="Application error occurred",
            status_code=status.HTTP_404_NOT_FOUND,
        ),
    )

    # Act
    response = process_request(
        get_entities_fn=get_entities_fn,
        status_code=status_code,
        not_found_err_msg=not_found_err_msg,
        db=mock_db,
    )

    # Assert
    mock_process_db_transaction.assert_called_once_with(
        transaction_func=get_entities_fn,
        db=mock_db,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.body) == {
        "detail": {"error": "Application error occurred"}
    }


def test_processRequest_handlesTypeError(mocker, mock_db) -> None:
    # Arrange
    get_entities_fn = mocker.Mock()
    status_code = status.HTTP_200_OK
    not_found_err_msg = "Entity not found"

    mock_process_db_transaction = mocker.patch(
        "app.utils.processors.process_db_transaction",
        side_effect=TypeError("Type error occurred"),
    )

    # Act
    response = process_request(
        get_entities_fn=get_entities_fn,
        status_code=status_code,
        not_found_err_msg=not_found_err_msg,
        db=mock_db,
    )

    # Assert
    mock_process_db_transaction.assert_called_once_with(
        transaction_func=get_entities_fn,
        db=mock_db,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.body) == {"detail": {"error": "Type error occurred"}}


def test_processRequest_handlesSyntaxError(mocker, mock_db) -> None:
    # Arrange
    get_entities_fn = mocker.Mock()
    status_code = status.HTTP_200_OK
    not_found_err_msg = "Entity not found"

    mock_process_db_transaction = mocker.patch(
        "app.utils.processors.process_db_transaction",
        side_effect=SyntaxError("Syntax error occurred"),
    )

    # Act
    response = process_request(
        get_entities_fn=get_entities_fn,
        status_code=status_code,
        not_found_err_msg=not_found_err_msg,
        db=mock_db,
    )

    # Assert
    mock_process_db_transaction.assert_called_once_with(
        transaction_func=get_entities_fn,
        db=mock_db,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.body) == {"detail": {"error": "Syntax error occurred"}}


def test_processDbTransaction_executesSuccessfully(mocker, mock_db) -> None:
    # Arrange
    transaction_func = mocker.Mock(return_value="success")

    # Act
    result = process_db_transaction(
        transaction_func=transaction_func,
        db=mock_db,
    )

    # Assert
    transaction_func.assert_called_once()
    assert result == "success"


def test_processDbTransaction_handlesIntegrityError(mocker, mock_db) -> None:
    # Arrange
    transaction_func = mocker.Mock(
        side_effect=IntegrityError(
            "Integrity error",
            params={},
            orig=Exception(),
        ),
    )

    # Act & Assert
    with pytest.raises(ApplicationError) as exc_info:
        process_db_transaction(transaction_func, mock_db)

    mock_db.rollback.assert_called_once()
    assert exc_info.value.data.detail == "Database conflict occurred"
    assert exc_info.value.data.status == status.HTTP_409_CONFLICT


def test_process_db_transaction_handlesSQLAlchemyError(mocker, mock_db) -> None:
    # Arrange
    transaction_func = mocker.Mock(side_effect=SQLAlchemyError("SQLAlchemy error"))

    # Act & Assert
    with pytest.raises(ApplicationError) as exc_info:
        process_db_transaction(transaction_func, mock_db)

    mock_db.rollback.assert_called_once()
    assert exc_info.value.data.detail == "Internal server error"
    assert exc_info.value.data.status == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_formatResponse_withSingleModel() -> None:
    # Arrange
    class MockModel(BaseModel):
        key: str

    data = MockModel(key="value")

    # Act
    result = _format_response(data)

    # Assert
    assert result == {"key": "value"}


def test_formatResponse_withListOfModels() -> None:
    # Arrange
    class MockModel(BaseModel):
        key: str

    data: list[BaseModel] = [
        MockModel(key="value1"),
        MockModel(key="value2"),
    ]

    # Act
    result = _format_response(data)

    # Assert
    assert result == [{"key": "value1"}, {"key": "value2"}]
