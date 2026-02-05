import datetime

from dataclasses import dataclass
from typing import Sequence, Optional

from application.dto.activities import ActivityDTO
from application.dto.base import DTO
from application.dto.buildings import BuildingDTO
from phonenumbers.phonenumber import PhoneNumber


@dataclass(kw_only=True, slots=True, frozen=True)
class OrganizationPhoneDTO(DTO):
    number: PhoneNumber


@dataclass(kw_only=True, slots=True, frozen=True)
class OrganizationDTO(DTO):
    name: str
    phones: Optional[Sequence[OrganizationPhoneDTO]]
    created_at: datetime.datetime = datetime.datetime.now()
    building: BuildingDTO
    activities: list[ActivityDTO]
