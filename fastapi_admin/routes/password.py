from fastapi import APIRouter, Depends, Form
from starlette.requests import Request

from fastapi_admin.depends import get_current_admin, get_resources
from fastapi_admin.i18n import _
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.template import templates

router = APIRouter()


@router.get("")
async def update_password_view(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "password.html",
        context={
            "request": request,
            "resources": resources,
        },
    )


@router.post("")
async def update_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    re_new_password: str = Form(...),
    admin: AbstractAdmin = Depends(get_current_admin),
    resources=Depends(get_resources),
):
    login_provider = request.app.login_provider
    error = None
    if not login_provider.check_password(admin, old_password):
        error = _("old_password_error")
    elif new_password != re_new_password:
        error = _("new_password_different")
    if error:
        return templates.TemplateResponse(
            "password.html",
            context={"request": request, "resources": resources, "error": error},
        )
    await login_provider.update_password(admin, new_password)
    return await login_provider.logout(request)
