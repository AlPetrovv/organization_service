from abc import abstractmethod
from typing import Sequence, TYPE_CHECKING, Optional, Protocol


from sqlalchemy.ext.asyncio import AsyncSession


if TYPE_CHECKING:
    from infra.resouces.database.types import TYPE_MODEL
    from domain.entities.base import EntityType, ID
    from application.interfaces.db_mapper import DBMapperProtocol
    from application.dto.base import DtoType


class DBRepoProtocol(Protocol):
    """
    Base repository class.

    This class defines a base repository for database operations.
    All repositories should inherit from this class.
    """

    model: "TYPE_MODEL"
    mapper: "DBMapperProtocol"

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def is_exists(self, model_id: "ID") -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, model_id: "ID") -> Optional["EntityType"]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, ids: Sequence["ID"]) -> Optional[Sequence["EntityType"]]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: "ID") -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_partial(self, dto: "EntityType") -> Optional["EntityType"]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, dto: "DtoType") -> "EntityType":
        raise NotImplementedError
