from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CTE

from domain.agregates import OrganizationEntity


if TYPE_CHECKING:
    from infra.resouces.database.repos import UOW


class CheckOrganizationExistsInteractor:
    async def __call__(self, org_id: UUID, uow: "UOW") -> bool:
        is_exists = await uow.organizations.is_exists(org_id)
        return is_exists


class GetOrganizationInteractor:
    async def __call__(self, org_id: UUID, uow: "UOW") -> OrganizationEntity:
        org = await uow.organizations.get_by_id(org_id)
        return org


class GetOrganizationByNameInteractor:
    async def __call__(self, org_name: str, uow: "UOW") -> OrganizationEntity:
        entity = await uow.organizations.get_by_name(org_name)
        return entity


class GetOrganizationsInRadiusInteractor:
    async def __call__(self, radius: int, lat: float, lon: float, uow: "UOW") -> list[OrganizationEntity]:
        orgs = await uow.organizations.get_organizations_in_radius(lat=lat, lon=lon, radius=radius)
        return orgs


class GetOrganizationsByActivityTreeInteractor:
    async def __call__(self, activity_tree: CTE, uow: "UOW") -> list[OrganizationEntity]:
        orgs = await uow.organizations.get_by_activity_tree(activity_tree)
        return orgs
