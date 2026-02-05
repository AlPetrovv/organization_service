import contextlib

from fastapi import FastAPI


__all__ = ("lifespan",)

from config import settings


@contextlib.asynccontextmanager
async def lifespan(app: "FastAPI"):
    from ioc import Container
    from test_data import create_test_data

    container = Container()
    container.config.from_pydantic(settings)
    container.wire(
        packages=[
            "presentation.api.v1.handlers.orgs",
            "presentation.api.v1.handlers.activities",
            "presentation.api.v1.handlers.buildings",
        ]
    )
    ouw = container.db.uow()
    await create_test_data(ouw)

    app.container = container

    yield
