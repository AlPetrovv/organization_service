from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from domain.exceptions import ModelFoundError


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ModelFoundError)
    async def artifact_not_found_exception_handler(
        request: Request,
        exc: ModelFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )
