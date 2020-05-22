from copy import deepcopy

from fastapi import APIRouter, Depends

from ..depends import jwt_optional
from ..factory import app
from ..shortcuts import get_object_or_404

router = APIRouter()


@router.get("/site",)
async def site(user_id=Depends(jwt_optional)):
    site_ = app.site
    user = None
    if user_id:
        user = await get_object_or_404(app.user_model, pk=user_id)
    if user and app.permission and not user.is_superuser:
        site_ = deepcopy(site_)
        await user.fetch_related("roles")
        filter_menus = filter(lambda x: (x.url and "rest" in x.url) or x.children, site_.menus)
        hide_menus = []
        for menu in filter_menus:
            has_permission = False
            for role in user.roles:
                if not has_permission:
                    model = menu.url.split("/")[-1]
                    permission = await role.permissions.filter(model=model)
                    if permission:
                        has_permission = True
            if not has_permission:
                hide_menus.append(menu.url)
        for menu in app.site.menus:
            if menu.url in hide_menus:
                site_.menus.remove(menu)

    return site_.dict(by_alias=True, exclude_unset=True)
