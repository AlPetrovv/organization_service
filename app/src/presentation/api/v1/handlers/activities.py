from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from flows.activities import GetActivityOrganizationsFlow
from infra.resouces.database.repos import UOW
from ioc import Container
from presentation.api.v1.mappers.orgs import OrganizationApiMapper
from presentation.api.v1.schemas.orgs import OrganizationResponse

router = APIRouter(
    prefix="/activity",
    tags=["Activities"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get(
    "/{activity_id}/organizations/",
    summary="Get organizations associated with an activity",
    description=(
        "Returns the list of organizations linked to the specified activity.\n\n"
        "Useful for displaying partners, organizers, sponsors, or co-hosts of a particular activity."
    ),
)
@inject
async def get_activity_organizations(
    activity_id: int,
    interactor: GetActivityOrganizationsFlow = Depends(Provide[Container.flow.get_orgs_by_activity]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[OrganizationResponse]:
    async with uow:
        organization_entities = await interactor(activity_id=activity_id, uow=uow)
        response = [mapper.to_response(organization_entity) for organization_entity in organization_entities]
        return response
