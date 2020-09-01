import os

import uvicorn
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_queryset_creator

from fastapi_admin.depends import get_model
from fastapi_admin.factory import app as admin_app
from fastapi_admin.schemas import BulkIn
from fastapi_admin.site import Menu, Site

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {"models": {"models": ["examples.models"], "default_connection": "default"}},
}

templates = Jinja2Templates(directory="examples/templates")


@admin_app.post("/rest/{resource}/bulk/test_bulk")
async def test_bulk(bulk_in: BulkIn, model=Depends(get_model)):
    qs = model.filter(pk__in=bulk_in.pk_list)
    pydantic = pydantic_queryset_creator(model)
    ret = await pydantic.from_queryset(qs)
    return ret.dict()


@admin_app.get("/home",)
async def home():
    return {"html": templates.get_template("home.html").render()}


def create_app():
    fast_app = FastAPI(debug=False)
    register_tortoise(fast_app, config=TORTOISE_ORM)
    fast_app.mount("/admin", admin_app)

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_app


app = create_app()


@app.on_event("startup")
async def start_up():
    await admin_app.init(  # nosec
        admin_secret="test",
        permission=True,
        admin_log=True,
        site=Site(
            name="FastAPI-Admin DEMO",
            login_footer="FASweTAPI ADMIN - FastAPI Admin Dashboard",
            login_description="FastAPI Admin Dashboard",
            locale="en-US",
            locale_switcher=True,
            theme_switcher=True,
            menus=[
                Menu(name="Home", url="/", icon="fa fa-home"),
                Menu(
                    name="Content",
                    children=[
                        Menu(
                            name="Category",
                            url="/rest/Category",
                            icon="fa fa-list",
                            search_fields=("slug",),
                        ),
                        Menu(
                            name="Config",
                            url="/rest/Config",
                            icon="fa fa-gear",
                            import_=True,
                            search_fields=("key",),
                        ),
                        Menu(
                            name="Product",
                            url="/rest/Product",
                            icon="fa fa-table",
                            search_fields=("name",),
                        ),
                    ],
                ),
                Menu(
                    name="External",
                    children=[
                        Menu(
                            name="Github",
                            url="https://github.com/long2ice/fastapi-admin",
                            icon="fa fa-github",
                            external=True,
                        ),
                    ],
                ),
                Menu(
                    name="Auth",
                    children=[
                        Menu(
                            name="User",
                            url="/rest/User",
                            icon="fa fa-user",
                            search_fields=("username",),
                        ),
                        Menu(name="Role", url="/rest/Role", icon="fa fa-group",),
                        Menu(name="Permission", url="/rest/Permission", icon="fa fa-user-plus",),
                        Menu(
                            name="AdminLog",
                            url="/rest/AdminLog",
                            icon="fa fa-align-left",
                            search_fields=("action", "admin", "model"),
                        ),
                        Menu(name="Logout", url="/logout", icon="fa fa-lock",),
                    ],
                ),
            ],
        ),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, debug=False, reload=False, lifespan="on")
