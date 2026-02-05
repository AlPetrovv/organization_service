from typing import TYPE_CHECKING

from application.interfaces.db_mapper import DBMapperProtocol

from domain.entities.buildings import BuildingEntity

from domain.value_objects import Location
from infra.resouces.database.models import Building

if TYPE_CHECKING:
    from application.dto.buildings import BuildingDTO


class DBBuildingMapper(DBMapperProtocol):
    def to_entity(self, building: Building) -> BuildingEntity:
        location = Location(value=building.location)

        return BuildingEntity(
            id=building.id,
            address=building.address,
            location=location,
        )

    def to_model(self, entity: BuildingEntity) -> Building:
        return Building(id=entity.id, address=entity.address, location=entity.location.value)

    def to_model_from_dto(self, dto: "BuildingDTO"):
        return Building(address=dto.address, location=dto.location.value)

    def update_model_from_entity(self, building: Building, entity: BuildingEntity) -> None:
        building.address = entity.address
        building.location = entity.location.value
