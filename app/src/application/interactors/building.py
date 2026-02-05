from typing import TYPE_CHECKING

from application.dto.buildings import BuildingDTO
from domain.agregates import OrganizationEntity
from domain.entities.buildings import BuildingEntity


if TYPE_CHECKING:
    from infra.resouces.database.repos import UOW


class CheckBuildingExistsInteractor:
    async def __call__(self, building_id: int, uow: "UOW") -> bool:
        is_exists = await uow.buildings.is_exists(building_id)
        return is_exists


class CreateBuildingInteractor:
    async def __call__(self, dto: BuildingDTO, uow: "UOW") -> BuildingEntity:
        building = await uow.buildings.create(dto)
        await uow.session.commit()
        return building


class GetBuildingOrganizationsInteractor:
    async def __call__(self, building_id: int, uow: "UOW") -> list[OrganizationEntity]:
        organizations = await uow.organizations.get_by_building_id(building_id)
        return organizations
