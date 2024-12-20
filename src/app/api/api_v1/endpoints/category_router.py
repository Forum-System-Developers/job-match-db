from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services import category_service
from app.sql_app.database import get_db
from app.utils.processors import process_request

router = APIRouter()


@router.get("/", description="Retrieve all categories.")
def get_all_categories(db: Session = Depends(get_db)) -> JSONResponse:
    def _get_all_categories():
        return category_service.get_all(db)

    return process_request(
        get_entities_fn=_get_all_categories,
        status_code=status.HTTP_200_OK,
        not_found_err_msg="No categories found",
        db=db,
    )
