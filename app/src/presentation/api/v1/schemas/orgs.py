from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber

from presentation.api.v1.schemas.activities import ActivityResponse
from presentation.api.v1.schemas.buildings import BuildingResponse


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


class RadiusSearch(BaseModel):
    lat: float
    lon: float
    radius: int
