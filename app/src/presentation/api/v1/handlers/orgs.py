from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query, Depends

from starlette import status

from application.interactors.orgs import (
    GetOrganizationInteractor,
    GetOrganizationByNameInteractor,
    GetOrganizationsInRadiusInteractor,
    GetOrganizationsInSquareInteractor,
)
from infra.resouces.database.repos import UOW

from ioc import Container

from presentation.api.v1.mappers.orgs import OrganizationApiMapper
from presentation.api.v1.schemas.orgs import (
    OrganizationResponse,
    OrganizationResponseDetail,
    RadiusSearch,
    SquareSearch,
)

router = APIRouter(
    prefix="/organization",
    tags=["Organizations"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get(
    "/{org_id:uuid}",
    summary="Get organization by ID",
    description=(
        "Retrieves detailed information about a single organization using its unique UUID.\n\n"
        "Returns extended details including full profile, contacts, addresses, and other metadata."
    ),
    response_description="Detailed organization information",
)
@inject
async def get_org(
    org_id: UUID,
    interactor: GetOrganizationInteractor = Depends(Provide[Container.interactors.orgs.get_by_id]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> OrganizationResponseDetail:
    async with uow:
        organization_entity = await interactor(org_id=org_id, uow=uow)
        response = mapper.to_detail_response(organization_entity)
        return response


@router.get(
    "/name/{org_name}",
    summary="Get organization by name",
    description="Finds and returns detailed information about an organization using its name.\n\n",
    response_description="Detailed organization information",
)
@inject
async def get_org_by_name(
    org_name: str,
    interactor: GetOrganizationByNameInteractor = Depends(Provide[Container.interactors.orgs.get_by_name]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> OrganizationResponseDetail:
    async with uow:
        organization_entity = await interactor(org_name=org_name, uow=uow)
        response = mapper.to_detail_response(organization_entity)
        return response


@router.get(
    "/search/radius",
    summary="Find organizations within a geographic radius",
    description="Returns a list of organizations located within the specified radius (in meters)",
    response_description="List of organizations within the search radius",
)
@inject
async def get_orgs_in_radius(
    search_data: RadiusSearch = Query(...),
    interactor: GetOrganizationsInRadiusInteractor = Depends(Provide[Container.interactors.orgs.get_in_radius]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[OrganizationResponse]:
    async with uow:
        organization_entities = await interactor(
            radius=search_data.radius,
            lat=search_data.lat,
            lon=search_data.lon,
            uow=uow,
        )
        response = [mapper.to_response(organization_entity) for organization_entity in organization_entities]
        return response


@router.get(
    "/search/square",
    summary="Find organizations within a bounding box",
    description="Returns a list of organizations located within the specified bounding box ",
    response_description="List of organizations within the bounding box",
)
@inject
async def get_orgs_in_square(
    search_data: SquareSearch = Query(...),
    interactor: GetOrganizationsInSquareInteractor = Depends(Provide[Container.interactors.orgs.get_in_square]),
    mapper: OrganizationApiMapper = Depends(Provide[Container.mappers.api_mappers.org_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[OrganizationResponse]:
    async with uow:
        orgs = await interactor(side=search_data.distance, lat=search_data.lat, lon=search_data.lon, uow=uow)
        response = [mapper.to_response(org) for org in orgs]
        return response
