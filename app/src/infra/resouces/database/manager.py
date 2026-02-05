from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine


class DatabaseSessionManager:
    """Manager for database sessions.

    This class creates and manages connections to the database.
    It is used to create and manage database sessions.

    Attributes:
        _engine (AsyncEngine | None): The SQLAlchemy engine used to connect to the database.
        _sessionmaker (async_sessionmaker[AsyncSession] | None): The SQLAlchemy sessionmaker used to create sessions.

    Methods:
        init(self) -> None:
            Initializes the database engine and sessionmaker if they are not already initialized.

        get_session(self) -> AsyncIterator[AsyncSession]:
            Returns a context manager that wraps a database session.

    """

    def __init__(self, db_url: PostgresDsn, engine_kwargs: dict[str, Any]):
        self._engine: AsyncEngine = create_async_engine(str(db_url), **engine_kwargs)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self._sessionmaker() as session:
            yield session

    async def dispose(self):
        await self._engine.dispose()

    @property
    def active(self) -> bool:
        return self._engine is not None
