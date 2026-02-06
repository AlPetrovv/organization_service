from typing import TYPE_CHECKING
from uuid import UUID

from geoalchemy2.functions import ST_MakeEnvelope
from sqlalchemy import CTE

from domain.agregates import OrganizationEntity

import math


if TYPE_CHECKING:
    from infra.resouces.database.repos import UOW


class CheckOrganizationExistsInteractor:
    async def __call__(self, org_id: UUID, uow: "UOW") -> bool:
        is_exists = await uow.organizations.is_exists(org_id)
        return is_exists


class GetOrganizationInteractor:
    async def __call__(self, org_id: UUID, uow: "UOW") -> OrganizationEntity:
        org = await uow.organizations.get_by_id_with_relations(org_id)
        return org


class GetOrganizationByNameInteractor:
    async def __call__(self, org_name: str, uow: "UOW") -> OrganizationEntity:
        entity = await uow.organizations.get_by_name_with_relations(org_name)
        return entity


class GetOrganizationsInRadiusInteractor:
    async def __call__(self, radius: int, lat: float, lon: float, uow: "UOW") -> list[OrganizationEntity]:
        orgs = await uow.organizations.get_organizations_in_radius(lat=lat, lon=lon, radius=radius)
        return orgs


class GetOrganizationsInSquareInteractor:
    async def __call__(self, side: int, lat: float, lon: float, uow: "UOW") -> list[OrganizationEntity]:
        half_side_m = side / 2.0
        meters_per_degree_lat = 111_195.0
        meters_per_degree_lon = 111_195.0 * max(math.cos(math.radians(lat)), 1e-6)
        half_deg_lat = half_side_m / meters_per_degree_lat
        half_deg_lon = half_side_m / meters_per_degree_lon
        envelope = ST_MakeEnvelope(
            lon - half_deg_lon,
            lat - half_deg_lat,
            lon + half_deg_lon,
            lat + half_deg_lat,
            4326,
        )

        orgs = await uow.organizations.get_organizations_in_square(envelope=envelope)
        return orgs


class GetOrganizationsByActivityTreeInteractor:
    async def __call__(self, activity_tree: CTE, uow: "UOW") -> list[OrganizationEntity]:
        orgs = await uow.organizations.get_by_activity_tree(activity_tree)
        return orgs
