from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from flows.buildings import GetBuildingOrganizationsFlow
from infra.resouces.database.repos import UOW

from ioc import Container
from presentation.api.v1.mappers.orgs import OrganizationApiMapper
from presentation.api.v1.schemas.orgs import OrganizationResponse

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/{building_id}/organizations/")
@inject
async def get_org_detail(
    building_id: int,
    interactor: GetBuildingOrganizationsFlow = Depends(Provide[Container.flow.get_building_orgs]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[OrganizationResponse]:
    async with uow:
        organization_entities = await interactor(building_id=building_id, uow=uow)
        response = [mapper.to_response(organization_entity) for organization_entity in organization_entities]
        return response
