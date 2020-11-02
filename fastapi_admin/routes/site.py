from copy import deepcopy

from fastapi import APIRouter, Depends

from ..common import check_has_permission
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
    site_copy = deepcopy(site_)
    if user and app.permission and not user.is_superuser:
        await user.fetch_related("roles")
        for index, menu in enumerate(site_.menus):
            if menu.url and ("/rest" in menu.url or "/page" in menu.url):
                model = menu.url.split("/")[-1]
                if not await check_has_permission(user, model):
                    site_copy.menus.remove(menu)
            elif menu.children:
                for index_child, child in enumerate(menu.children):
                    if child.url and ("/rest" in child.url or "/page" in child.url):
                        model = child.url.split("/")[-1]
                        if not await check_has_permission(user, model):
                            site_copy.menus[index].children.remove(child)
    site_copy.menus = list(filter(lambda x: x.children != [] or x.url, site_copy.menus))
    return site_copy.dict(by_alias=True, exclude_unset=True)
