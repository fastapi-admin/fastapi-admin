from fastapi import APIRouter, Depends

from fastapi_admin.depends import get_current_admin

from .resources import router as resources_router

router = APIRouter()
router.include_router(resources_router, dependencies=[Depends(get_current_admin)])
