from application.interactors.building import CheckBuildingExistsInteractor, GetBuildingOrganizationsInteractor
from domain.agregates import OrganizationEntity
from domain.exceptions import BuildingNotFoundError


class GetBuildingOrganizationsFlow:
    def __init__(self):
        self.check_building_exists_interactor = CheckBuildingExistsInteractor()
        self.get_building_organizations_interactor = GetBuildingOrganizationsInteractor()

    async def __call__(self, building_id: int, uow) -> list[OrganizationEntity]:
        exists = await self.check_building_exists_interactor(building_id=building_id, uow=uow)
        if not exists:
            raise BuildingNotFoundError
        organizations = await self.get_building_organizations_interactor(building_id=building_id, uow=uow)
        return organizations
