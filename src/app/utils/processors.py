import logging
from typing import Callable

from fastapi import status
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import ApplicationError

logger = logging.getLogger(__name__)


def process_request(
    get_entities_fn: Callable,
    status_code: int,
    not_found_err_msg: str,
) -> JSONResponse:
    """
    Processes a request by calling the provided function and handling exceptions.

    Args:
        get_entities_fn (Callable): A function that retrieves entities.
        status_code (int): The status code to return on successful processing.
        not_found_err_msg (str): The error message to log if a TypeError occurs.

    Returns:
        JSONResponse: A JSON response with the appropriate status code and content.

    Raises:
        ApplicationError: If an application-specific error occurs.
        TypeError: If a type error occurs.
        SyntaxError: If a syntax error occurs.
    """
    try:
        response = get_entities_fn()
        return JSONResponse(status_code=status_code, content=response)
    except ApplicationError as ex:
        logger.exception(str(ex))
        return JSONResponse(
            status_code=ex.data.status,
            content={"detail": {"error": ex.data.detail}},
        )
    except TypeError as ex:
        logger.exception(not_found_err_msg)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": {"error": str(ex)}},
        )
    except SyntaxError as ex:
        logger.exception("Pers thrown an exception")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": {"error": str(ex)}},
        )
