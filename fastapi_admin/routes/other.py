from fastapi import APIRouter

from ..factory import app

router = APIRouter()


@router.get(
    '/home',
)
async def home():
    return {
        'title': "Welcome to REST ADMIN"
    }


@router.get(
    '/site',
)
async def site():
    return app.site.dict(by_alias=True, exclude_unset=True)
