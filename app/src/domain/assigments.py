from dataclasses import dataclass

from sqlalchemy import UUID


@dataclass(kw_only=True, slots=True)
class OrganizationActivityAssignment:
    organization_id: UUID
    activity_id: int

    def __eq__(self, other):
        return (self.organization_id, self.activity_id) == (other.organization_id, other.activity_id)
