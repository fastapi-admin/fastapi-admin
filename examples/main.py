import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from examples import providers, settings
from examples.constants import BASE_DIR
from fastapi_admin.app import app as admin_app


def create_app():
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )
    admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        login_provider=providers.Login,
    )
    app.mount("/admin", admin_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    register_tortoise(
        app,
        config={
            "connections": {"default": settings.DATABASE_URL},
            "apps": {"models": {"models": ["examples.models"], "default_connection": "default"}},
        },
        generate_schemas=True,
    )
    return app


app_ = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app_", debug=True, reload=True)
