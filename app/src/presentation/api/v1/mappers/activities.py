from domain.entities.activities import ActivityEntity
from presentation.api.v1.schemas.activities import ActivityResponse


class ActivityApiMapper:
    def to_response(self, entity: ActivityEntity) -> ActivityResponse:
        response = ActivityResponse(id=entity.id, name=entity.name)
        return response
