from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from presentation.api.v1.schemas.activities import ActivityResponse
from presentation.api.v1.schemas.buildings import BuildingResponse


class GeoSearch(BaseModel):
    lat: float = Field(..., ge=-180, le=180, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    distance: int = Field(
        ...,
        gt=0,
        le=100_000_000,
        description="Search area in **meters**",
    )


class OrganizationPhone(BaseModel):
    id: int
    number: PhoneNumber


class OrganizationResponse(BaseModel):
    id: UUID
    name: str


class OrganizationResponseDetail(OrganizationResponse):
    building: BuildingResponse
    activities: list[ActivityResponse]
    phone_numbers: list[OrganizationPhone]


class RadiusSearch(GeoSearch):
    pass


class SquareSearch(GeoSearch):
    pass
