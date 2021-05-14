from starlette.responses import RedirectResponse
from starlette.status import HTTP_404_NOT_FOUND

from examples.models import Config
from fastapi import Depends, HTTPException
from starlette.requests import Request

from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates


@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "home.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Home",
            "page_pre_title": "home",
            "page_title": "Home page",
        },
    )


@app.get("/config/switch_status/{config_id}")
async def switch_config_status(request: Request, config_id: int):
    config = await Config.get_or_none(pk=config_id)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"))
