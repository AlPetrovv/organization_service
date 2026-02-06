from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers

from infra.resouces.database.manager import DatabaseSessionManager
from infra.resouces.database.repos import UOW
from presentation.api.v1.mappers.orgs import OrganizationApiMapper
from presentation.api.v1.mappers.activities import ActivityApiMapper
from presentation.api.v1.mappers.buildings import BuildingApiMapper
from application.interactors import orgs as orgs_interactors
from application.interactors import building as building_interactors
from application.interactors import activities as activities_interactors
from flows.buildings import GetBuildingOrganizationsFlow
from flows.activities import GetActivityOrganizationsFlow


class ApiMapperContainer(DeclarativeContainer):
    org_mapper = providers.Factory(OrganizationApiMapper)
    activity_mapper = providers.Factory(ActivityApiMapper)
    building_mapper = providers.Factory(BuildingApiMapper)


class MainMappersContainer(DeclarativeContainer):
    api_mappers: ApiMapperContainer = providers.Container(ApiMapperContainer)


class OrganizationInteractorsContainer(DeclarativeContainer):
    exists = providers.Factory(orgs_interactors.CheckOrganizationExistsInteractor)
    get_by_name = providers.Factory(orgs_interactors.GetOrganizationByNameInteractor)
    get_in_radius = providers.Factory(orgs_interactors.GetOrganizationsInRadiusInteractor)
    get_in_square = providers.Factory(orgs_interactors.GetOrganizationsInSquareInteractor)
    get_by_id = providers.Factory(orgs_interactors.GetOrganizationInteractor)


class BuildingInteractorsContainer(DeclarativeContainer):
    exists = providers.Factory(building_interactors.CheckBuildingExistsInteractor)
    get_organizations = providers.Factory(building_interactors.GetBuildingOrganizationsInteractor)


class ActivityInteractorsContainer(DeclarativeContainer):
    exists = providers.Factory(activities_interactors.CheckActivityExistsInteractor)
    get_by_id = providers.Factory(activities_interactors.GetActivityTreeInteractor)


class InteractorsContainer(DeclarativeContainer):
    orgs: OrganizationInteractorsContainer = providers.Container(OrganizationInteractorsContainer)
    activities: ActivityInteractorsContainer = providers.Container(ActivityInteractorsContainer)
    buildings: BuildingInteractorsContainer = providers.Container(BuildingInteractorsContainer)


class FlowsContainer(DeclarativeContainer):
    get_orgs_by_activity = providers.Factory(GetActivityOrganizationsFlow)
    get_building_orgs = providers.Factory(GetBuildingOrganizationsFlow)


class DatabaseContainer(DeclarativeContainer):
    config = providers.Configuration()

    db_manager = providers.Singleton(
        DatabaseSessionManager, db_url=config.db.url, engine_kwargs=config.db.engine_kwargs
    )
    uow = providers.Factory(UOW, session_maker=db_manager.provided.session)


class Container(DeclarativeContainer):
    config = providers.Configuration()

    db: DatabaseContainer = providers.Container(DatabaseContainer, config=config)
    interactors: InteractorsContainer = providers.Container(InteractorsContainer)
    flow: FlowsContainer = providers.Container(FlowsContainer)
    mappers: MainMappersContainer = providers.Container(MainMappersContainer)
