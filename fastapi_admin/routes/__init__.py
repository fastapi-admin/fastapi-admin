from fastapi import APIRouter

from .password import router as password_router
from .resources import router as resources_router

router = APIRouter()
router.include_router(resources_router)
router.include_router(password_router, prefix="/password")
