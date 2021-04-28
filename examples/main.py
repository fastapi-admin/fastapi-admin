import os

import aioredis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from examples import settings
from examples.constants import BASE_DIR
from examples.models import User
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider

login_provider = UsernamePasswordProvider(user_model=User, enable_captcha=True)


def create_app():
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @app.on_event("startup")
    async def startup():
        redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
        admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            login_logo_url="https://preview.tabler.io/static/logo.svg",
            template_folders=[os.path.join(BASE_DIR, "templates")],
            login_provider=login_provider,
            maintenance=False,
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
            "apps": {"models": {"models": ["examples.models"], "default_connection": "default"}},
        },
        generate_schemas=True,
    )
    return app


app_ = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app_", debug=True, reload=True)
