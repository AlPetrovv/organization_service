from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from domain.exceptions import ModelFoundError


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ModelFoundError)
    async def model_not_found_exception_handler(
        request: Request,
        exc: ModelFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Some error occurred"},
        )
