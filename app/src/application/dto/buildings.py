from dataclasses import dataclass
from geoalchemy2 import WKBElement
from .base import DTO


@dataclass(kw_only=True, slots=True, frozen=True)
class LocationDTO(DTO):
    value: WKBElement


@dataclass(kw_only=True, slots=True, frozen=True)
class BuildingDTO(DTO):
    address: str
    location: LocationDTO
