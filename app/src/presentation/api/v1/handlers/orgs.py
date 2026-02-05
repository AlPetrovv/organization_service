from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query, Depends

from starlette import status

from application.interactors.orgs import (
    GetOrganizationInteractor,
    GetOrganizationByNameInteractor,
    GetOrganizationsInRadiusInteractor,
)
from infra.resouces.database.repos import UOW

from ioc import Container

from presentation.api.v1.mappers.orgs import OrganizationApiMapper
from presentation.api.v1.schemas.orgs import OrganizationResponse, OrganizationResponseDetail, RadiusSearch

router = APIRouter(
    prefix="/organization",
    tags=["Organizations"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/{org_id:uuid}")
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


@router.get("/name/{org_name}")
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


@router.get("/search/radius")
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
