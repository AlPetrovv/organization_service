from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from lifespan import lifespan
from presentation.api.authentication import auth_api_key_dep
from presentation.api.error_handlers import setup_exception_handlers
from routers import api_router


def create_app():

    app = FastAPI(
        title="Organization service",
        description="Welcome to the Organization service API",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        dependencies=[auth_api_key_dep],
    )
    app.include_router(api_router)
    setup_exception_handlers(app)

    return app


main_app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:main_app", host="0.0.0.0", reload=True)
