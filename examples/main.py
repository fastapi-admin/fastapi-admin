import os

import aioredis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from examples import settings
from examples.constants import BASE_DIR
from examples.models import Admin
from examples.providers import LoginProvider
from fastapi_admin.app import app as admin_app


def create_app():
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @app.get("/")
    async def index():
        return RedirectResponse(url="/admin")

    @app.on_event("startup")
    async def startup():
        redis = await aioredis.create_redis_pool(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            encoding="utf8",
        )
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            login_logo_url="https://preview.tabler.io/static/logo.svg",
            template_folders=[os.path.join(BASE_DIR, "templates")],
            providers=[LoginProvider(admin_model=Admin)],
            redis=redis,
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
            "apps": {
                "models": {
                    "models": ["examples.models"],
                    "default_connection": "default",
                }
            },
        },
        generate_schemas=True,
    )
    return app


app_ = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app_", debug=True, reload=True)
