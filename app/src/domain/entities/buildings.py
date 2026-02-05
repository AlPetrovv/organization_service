from dataclasses import dataclass

from domain.entities.base import Entity
from domain.value_objects import Location


@dataclass(kw_only=True, slots=True)
class BuildingEntity(Entity[int]):
    address: str
    location: Location
