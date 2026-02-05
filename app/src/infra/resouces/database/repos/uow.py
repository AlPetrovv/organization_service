from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .activities import DBActivityRepo
from .buildings import DBBuildingRepo
from .orgs import DBOrganizationRepo


@dataclass
class UOW:
    session: AsyncSession

    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    async def __aenter__(self):
        async with self.session_maker() as session:
            self.session = session
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    @property
    def activities(self) -> DBActivityRepo:
        return DBActivityRepo(self.session)

    @property
    def buildings(self) -> DBBuildingRepo:
        return DBBuildingRepo(self.session)

    @property
    def organizations(self) -> DBOrganizationRepo:
        return DBOrganizationRepo(self.session)
