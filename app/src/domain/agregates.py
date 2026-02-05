import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional

from domain.entities.activities import ActivityEntity
from domain.entities.base import Entity
from domain.entities.buildings import BuildingEntity
from domain.entities.orgs import OrganizationPhoneEntity


@dataclass(kw_only=True, slots=True)
class OrganizationEntity(Entity[uuid.UUID]):
    name: str
    phones: Optional[list[OrganizationPhoneEntity]] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    building: BuildingEntity
    activities: list[ActivityEntity] = field(default_factory=list)
