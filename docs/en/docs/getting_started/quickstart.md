# Quickstart

`FastAPI-Admin` is easy to mount your `FastAPI` app, just need a few configs.

## Mount Admin App

First, you need mount the app from `FastAPI-Admin` as a sub application of `FastAPI`.

```python
from fastapi_admin.app import app as admin_app
from fastapi import FastAPI

app = FastAPI()
app.mount("/admin", admin_app)

```

## Configure Admin App

There are some configs to configure the admin app, and you need to configure it on startup of `FastAPI`.

```python
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider

login_provider = UsernamePasswordProvider(user_model=User, enable_captcha=True)


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
```

The full list of configs can be found in

## Define And Register Resource

## Start App
