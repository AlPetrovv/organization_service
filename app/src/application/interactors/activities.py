from typing import TYPE_CHECKING

from sqlalchemy import CTE

if TYPE_CHECKING:
    from infra.resouces.database.repos import UOW


class CheckActivityExistsInteractor:
    async def __call__(self, activity_id: int, uow: "UOW") -> bool:
        is_exists = await uow.activities.is_exists(activity_id)
        return is_exists


class GetActivityTreeInteractor:
    async def __call__(self, activity_id: int, uow: "UOW") -> CTE:
        activity_tree = await uow.activities.get_activity_tree(activity_id)
        return activity_tree
