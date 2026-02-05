from typing import TYPE_CHECKING

from application.interfaces.db_mapper import DBMapperProtocol

from domain.entities.activities import ActivityEntity

from infra.resouces.database.models import Activity

if TYPE_CHECKING:
    from application.dto.activities import ActivityDTO


class DBActivityMapper(DBMapperProtocol):
    def to_entity(self, activity: Activity) -> ActivityEntity:
        return ActivityEntity(
            id=activity.id,
            name=activity.name,
            parent_id=activity.parent_id,
            depth=activity.depth,
        )

    def to_model(self, entity: ActivityEntity) -> Activity:
        return Activity(id=entity.id, name=entity.name, parent_id=entity.parent_id, depth=entity.depth)

    def to_model_from_dto(self, dto: "ActivityDTO") -> Activity:
        return Activity(name=dto.name, parent_id=dto.parent_id, depth=dto.depth)

    def update_model_from_entity(self, activity: Activity, entity: ActivityEntity) -> None:
        activity.name = entity.name
        activity.parent_id = entity.parent_id
        activity.depth = entity.depth
