from fastapi import APIRouter

from .resources import router as resources_router

router = APIRouter()
router.include_router(resources_router)
