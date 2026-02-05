from typing import Optional, Sequence, TYPE_CHECKING

from sqlalchemy import select, exists
from sqlalchemy.exc import SQLAlchemyError

from infra.resouces.database.mappers.buildings import DBBuildingMapper
from infra.resouces.database.models import Building


if TYPE_CHECKING:
    from domain.entities.buildings import BuildingEntity
    from application.dto.buildings import BuildingDTO

from application.interfaces.db_repository import DBRepoProtocol


class DBBuildingRepo(DBRepoProtocol):
    model = Building
    mapper = DBBuildingMapper()

    async def is_exists(self, building_id: int) -> bool:
        stmt = select(exists().where(self.model.id == building_id))
        result = await self.session.scalar(stmt)
        return result is True

    async def get_by_id(self, building_id: int) -> Optional["BuildingEntity"]:
        stmt = select(self.model).where(self.model.id == building_id)
        building = await self.session.scalar(stmt)
        if building is None:
            return None
        return self.mapper.to_entity(building=building)

    async def get_by_ids(self, ids: Sequence[int]) -> Optional[Sequence["BuildingEntity"]]:
        smtp = select(self.model).where(self.model.id.in_(ids))
        result = await self.session.scalars(smtp)
        buildings = result.all()
        return [self.mapper.to_entity(building) for building in buildings]

    async def create(self, dto: "BuildingDTO") -> "BuildingEntity":
        building = self.mapper.to_model_from_dto(dto)
        self.session.add(building)
        await self.session.flush()
        await self.session.refresh(building)
        return self.mapper.to_entity(building)

    async def create_from_entity(self, entity: "BuildingEntity") -> "BuildingEntity":
        building = self.mapper.to_model(entity)
        self.session.add(building)
        await self.session.flush()
        await self.session.refresh(building)
        return entity

    async def delete(self, building_id: int) -> None:
        instance = await self.get_by_id(building_id)
        if instance is not None:
            await self.session.delete(instance)
            await self.session.flush()

    async def update_partial(self, building: "BuildingEntity") -> Optional["BuildingEntity"]:
        try:
            building_entity = await self.get_by_id(building.id)
            if building_entity is None:
                return building_entity
            building = self.mapper.to_model(entity=building_entity)
            self.mapper.update_model_from_entity(building=building, entity=building_entity)
            await self.session.flush()
            return building_entity
        except SQLAlchemyError as ex:
            raise ex

    async def get_all(self) -> Sequence["BuildingEntity"]:
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        buildings = result.all()
        return [self.mapper.to_entity(building) for building in buildings]
