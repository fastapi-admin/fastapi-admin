# Configuration

You should configure predefined `app` from `fastapi-admin` on startup event of `fastapi`, because which should be in
asyncio loop context.

```python
import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(address='redis://localhost')
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=["templates"],
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg", admin_model=Admin
            )
        ],
        redis=redis,
    )
```

## Parameters

- `logo_url`: Will show the logo image in admin dashboard.
- `admin_path`: Default is `/admin`, but you can change to other path.
- `maintenance`: If set to `true`, all pages will be redirected to the `/maintenance` page. (💗 Pro only)
- `redis`: Instance of `aioredis`.
- `default_locale`: Current support `zh_CN` and `en_US`, default is `en_US`.
- `template_folders`: Template folders registered to jinja2 and also can be used to override builtin templates.
- `providers`: List of providers to register, all are subclasses of `fastapi_admin.providers.Provider`.
- `language_switch`: Whether show a language switch in page, default is `True`.
- `default_layout`: Set default layout, current there are both layouts `layout.html` and `layout-navbar.html`, default is `layout.html`. (💗 Pro only)
