from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID


from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin, ST_SetSRID, ST_MakePoint, ST_MakeEnvelope, ST_Intersects
from sqlalchemy import select, exists, cast, CTE, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, aliased, selectinload

from domain.exceptions import OrganizationNotFoundError
from infra.resouces.database.mappers.orgs import DBOrganizationMapper
from infra.resouces.database.models import Organization, Building, Activity

if TYPE_CHECKING:
    from domain.agregates import OrganizationEntity
    from application.dto.orgs import OrganizationDTO

from application.interfaces.db_repository import DBRepoProtocol


class DBOrganizationRepo(DBRepoProtocol):
    model = Organization
    mapper = DBOrganizationMapper()

    async def is_exists(self, org_id: UUID) -> bool:
        stmt = select(exists().where(self.model.id == org_id))
        result = await self.session.scalar(stmt)
        return result is True

    async def get_by_id(self, org_id: UUID) -> "OrganizationEntity":
        stmt = select(self.model).where(self.model.id == org_id)
        org = await self.session.scalar(stmt)
        if org is None:
            raise OrganizationNotFoundError
        return self.mapper.to_entity(org=org)

    async def get_by_id_with_relations(self, org_id: UUID):
        stmt = (
            select(self.model)
            .where(self.model.id == org_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        org = await self.session.scalar(stmt)
        if org is None:
            raise OrganizationNotFoundError
        return self.mapper.to_entity(org=org)

    async def get_by_ids(self, ids: Sequence[int]) -> Optional[Sequence["OrganizationEntity"]]:
        smtp = select(self.model).where(self.model.id.in_(ids))
        result = await self.session.scalars(smtp)
        orgs = result.all()
        return [self.mapper.to_entity(org) for org in orgs]

    async def create(self, dto: "OrganizationDTO") -> "OrganizationEntity":
        org = self.mapper.to_model_from_dto(dto)
        self.session.add(org)
        await self.session.flush()
        await self.session.refresh(org)
        return self.mapper.to_entity(org)

    async def create_from_entity(self, entity: "OrganizationEntity") -> OrganizationEntity:
        org = self.mapper.to_model(entity)
        self.session.add(org)
        await self.session.flush()
        await self.session.refresh(org)
        return entity

    async def delete(self, org_id: UUID) -> None:
        instance = await self.get_by_id(org_id)
        if instance is not None:
            await self.session.delete(instance)
            await self.session.flush()

    async def update_partial(self, org: "OrganizationEntity") -> Optional["OrganizationEntity"]:
        try:
            org_entity = await self.get_by_id(org.id)
            if org_entity is None:
                return org_entity
            org = self.mapper.to_model(entity=org_entity)
            self.mapper.update_model_from_entity(org=org, entity=org_entity)
            await self.session.flush()
            return org_entity
        except SQLAlchemyError as ex:
            raise ex

    async def get_all(self) -> Sequence["OrganizationEntity"]:
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        orgs = result.all()
        return [self.mapper.to_entity(org) for org in orgs]

    async def get_by_building_id(self, building_id: int) -> list["OrganizationEntity"]:
        stmt = select(self.model).where(self.model.building_id == building_id)
        result = await self.session.scalars(stmt)
        orgs = result.unique().all()
        return [self.mapper.to_entity(org) for org in orgs]

    async def get_by_name_with_relations(self, org_name: str) -> "OrganizationEntity":
        stmt = (
            select(self.model)
            .where(self.model.name == org_name)
            .options(
                joinedload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
        )
        org = await self.session.scalar(stmt)
        if org is None:
            raise OrganizationNotFoundError
        return self.mapper.to_entity(org=org)

    async def get_organizations_in_radius(self, lon: float, lat: float, radius: int) -> list["OrganizationEntity"]:
        stmt = (
            select(self.model)
            .join(self.model.building)
            .where(
                ST_DWithin(
                    cast(Building.location, Geography),
                    cast(
                        ST_SetSRID(ST_MakePoint(lon, lat), 4326),
                        Geography,
                    ),
                    radius,
                )
            )
            .options(joinedload(self.model.building))
        )
        result = await self.session.scalars(stmt)
        orgs = result.unique().all()
        return [self.mapper.to_entity(org) for org in orgs]

    async def get_organizations_in_square(self, envelope: ST_MakeEnvelope) -> list["OrganizationEntity"]:
        stmt = (
            select(self.model)
            .join(self.model.building)
            .where(func.ST_Intersects(Building.location, envelope))
            .options(joinedload(self.model.building))
        )

        result = await self.session.scalars(stmt)
        orgs = result.unique().all()
        return [self.mapper.to_entity(org) for org in orgs]

    async def get_by_activity_tree(self, activity_tree: CTE) -> list["OrganizationEntity"]:
        activity_alias = aliased(Activity, activity_tree)
        stmt = select(self.model).join(self.model.activities.of_type(activity_alias)).distinct()
        result = await self.session.scalars(stmt)
        orgs = result.unique().all()
        return [self.mapper.to_entity(org) for org in orgs]
