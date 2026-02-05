"""Database mapper for converting between Domain Entities and SQLAlchemy Models.

This mapper is responsible for the conversion logic between the domain layer
and the database persistence layer, following the Single Responsibility Principle.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from domain.entities.base import EntityType
    from infra.resouces.database.types import MODEL
    from application.dto.base import DtoType


class DBMapperProtocol(Protocol):
    """
    Mapper for converting between ArtifactEntity (Domain) and ArtifactModel (SQLAlchemy).

    This class provides methods for bidirectional mapping, ensuring separation of concerns
    between the domain logic and database persistence.
    """

    @abstractmethod
    def to_entity(self, model: "MODEL") -> "EntityType":
        """
        Converts an SQLAlchemy ArtifactModel to a Domain ArtifactEntity.

        Args:
            model: The SQLAlchemy ArtifactModel instance.

        Returns:
            An ArtifactEntity instance.
        """
        raise NotImplementedError

    @abstractmethod
    def to_model(self, entity: "EntityType") -> "MODEL":
        """
        Converts a Domain ArtifactEntity to an SQLAlchemy ArtifactModel.

        Args:
            entity: The Domain ArtifactEntity instance.

        Returns:
            An SQLAlchemy ArtifactModel instance.
        """
        raise NotImplementedError

    @abstractmethod
    def to_model_from_dto(self, dto: "DtoType"):
        raise NotImplementedError

    @abstractmethod
    def update_model_from_entity(self, model: "MODEL", entity: "EntityType") -> None:
        """
        Updates an existing SQLAlchemy ArtifactModel with data from a Domain ArtifactEntity.

        This method is used for updating database records based on changes in the domain entity.

        Args:
            model: The existing SQLAlchemy ArtifactModel to update.
            entity: The Domain ArtifactEntity containing the new data.
        """
        raise NotImplementedError
