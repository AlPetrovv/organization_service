from abc import ABC, abstractmethod
from typing import Generic

from domain.entities.base import EntityType
from application.dto.base import DtoType


class DataMapper(Generic[DtoType], ABC):
    dto_class: DtoType

    @abstractmethod
    def to_dto(self, entity: EntityType) -> DtoType:
        """Converts a Domain Entity to an Application DTO."""
        raise NotImplementedError

    @abstractmethod
    def dto_to_dict(self, dto: DtoType) -> dict:
        raise NotImplementedError
