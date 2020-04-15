from copy import deepcopy

from fastapi import APIRouter, Depends

from ..depends import get_current_user
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
async def site(
        user=Depends(get_current_user)
):
    site_ = app.site
    if app.permission and not user.is_superuser:
        site_ = deepcopy(site_)
        await user.fetch_related('roles')
        for menu in site_.menus:
            has_permission = False
            if not has_permission:
                for role in user.roles:
                    if await role.permissions.filter(model=menu.name):
                        has_permission = True
            if not has_permission:
                site_.menus.remove(menu)
    return site_.dict(by_alias=True, exclude_unset=True)
