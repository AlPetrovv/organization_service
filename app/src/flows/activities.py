from typing import TYPE_CHECKING

from application.interactors.activities import GetActivityTreeInteractor, CheckActivityExistsInteractor
from application.interactors.orgs import GetOrganizationsByActivityTreeInteractor
from domain.agregates import OrganizationEntity
from domain.exceptions import ActivityNotFoundError

if TYPE_CHECKING:
    from infra.resouces.database.repos import UOW


class GetActivityOrganizationsFlow:
    def __init__(self):
        self.check_activity_exists_interactor = CheckActivityExistsInteractor()
        self.get_activity_tree_interactor = GetActivityTreeInteractor()
        self.get_organizations_by_activity_tree_interactor = GetOrganizationsByActivityTreeInteractor()

    async def __call__(self, activity_id: int, uow: "UOW") -> list[OrganizationEntity]:
        is_exists = await self.check_activity_exists_interactor(activity_id=activity_id, uow=uow)
        if not is_exists:
            raise ActivityNotFoundError
        activity_tree = await self.get_activity_tree_interactor(activity_id=activity_id, uow=uow)
        organizations = await self.get_organizations_by_activity_tree_interactor(activity_tree=activity_tree, uow=uow)
        return organizations
