from typing import Optional, Sequence, TYPE_CHECKING

from sqlalchemy import select, exists, CTE
from sqlalchemy.exc import SQLAlchemyError

from infra.resouces.database.mappers.activities import DBActivityMapper
from infra.resouces.database.models import Activity


if TYPE_CHECKING:
    from domain.entities.activities import ActivityEntity
    from application.dto.activities import ActivityDTO

from application.interfaces.db_repository import DBRepoProtocol


class DBActivityRepo(DBRepoProtocol):
    model = Activity
    mapper = DBActivityMapper()

    async def is_exists(self, activity_id: int) -> bool:
        stmt = select(exists().where(self.model.id == activity_id))
        result = await self.session.scalar(stmt)
        return result is True

    async def get_by_id(self, activity_id: int) -> Optional["ActivityEntity"]:
        stmt = select(self.model).where(self.model.id == activity_id)
        activity = await self.session.scalar(stmt)
        if activity is None:
            return None
        return self.mapper.to_entity(activity=activity)

    async def get_by_ids(self, ids: Sequence[int]) -> Optional[Sequence["ActivityEntity"]]:
        smtp = select(self.model).where(self.model.id.in_(ids))
        result = await self.session.scalars(smtp)
        activities = result.all()
        return [self.mapper.to_entity(activity) for activity in activities]

    async def create(self, dto: "ActivityDTO") -> "ActivityEntity":
        activity = self.mapper.to_model_from_dto(dto)
        self.session.add(activity)
        await self.session.flush()
        await self.session.refresh(activity)
        return self.mapper.to_entity(activity)

    async def create_from_entity(self, entity: "ActivityEntity") -> "ActivityEntity":
        activity = self.mapper.to_model(entity)
        self.session.add(activity)
        await self.session.flush()
        await self.session.refresh(activity)
        return entity

    async def delete(self, activity_id: int) -> None:
        instance = await self.get_by_id(activity_id)
        if instance is not None:
            await self.session.delete(instance)
            await self.session.flush()

    async def update_partial(self, activity: "ActivityEntity") -> Optional["ActivityEntity"]:
        try:
            activity_entity = await self.get_by_id(activity.id)
            if activity_entity is None:
                return activity_entity
            activity = self.mapper.to_model(entity=activity_entity)
            self.mapper.update_model_from_entity(activity=activity, entity=activity_entity)
            await self.session.flush()
            return activity_entity
        except SQLAlchemyError as ex:
            raise ex

    async def get_all(self) -> Sequence["ActivityEntity"]:
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        activities = result.all()
        return [self.mapper.to_entity(activity) for activity in activities]

    async def get_activity_tree(self, activity_id: int) -> CTE:
        tree = (
            select(self.model.id.label("id"))
            .where(Activity.id == activity_id)
            .cte(name="activity_tree", recursive=True)
        )

        tree = tree.union_all(select(Activity.id).join(tree, Activity.parent_id == tree.c.id))
        return tree
