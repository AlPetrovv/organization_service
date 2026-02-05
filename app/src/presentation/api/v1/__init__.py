from fastapi import APIRouter

from .handlers.activities import router as activities_router
from .handlers.orgs import router as orgs_router
from .handlers.buildings import router as buildings_router


api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(activities_router)
api_v1_router.include_router(orgs_router)
api_v1_router.include_router(buildings_router)
