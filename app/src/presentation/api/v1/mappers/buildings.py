from geoalchemy2.shape import to_shape

from domain.entities.buildings import BuildingEntity
from presentation.api.v1.schemas.buildings import BuildingResponse


class BuildingApiMapper:
    def to_response(self, entity: BuildingEntity) -> BuildingResponse:
        point = to_shape(entity.location.value)

        response = BuildingResponse(id=entity.id, address=entity.address, location=(point.x, point.y))
        return response
