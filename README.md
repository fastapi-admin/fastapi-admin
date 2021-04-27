# FastAPI ADMIN

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/long2ice/fastapi-admin)](https://github.com/long2ice/fastapi-admin)
[![image](https://github.com/long2ice/fastapi-admin/workflows/gh-pages/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:gh-pages)
[![image](https://github.com/long2ice/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:pypi)

## Introduction

FastAPI-Admin is a admin dashboard based on
[fastapi](https://github.com/tiangolo/fastapi) and
[tortoise-orm](https://github.com/tortoise/tortoise-orm).

FastAPI-Admin provide crud feature out-of-the-box with just a few config.

## Live Demo

Check a live Demo here
[https://fastapi-admin-v1.long2ice.cn](https://fastapi-admin-v1.long2ice.cn/).

- username: `admin`
- password: `123456`

Data in database will restore every day.

## Screenshots

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/login.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/list.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/view.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/create.png)

## Requirements

- [FastAPI](https://github.com/tiangolo/fastapi) framework as your backend framework.
- [Tortoise-ORM](https://github.com/tortoise/tortoise-orm) as your orm framework, by the way, which is best asyncio orm
  so far and I\'m one of the contributors😋.

## Quick Start

### Run Backend

Look full example at
[examples](https://github.com/long2ice/fastapi-admin/tree/dev/examples).

1. `git clone https://github.com/long2ice/fastapi-admin.git`.
2. `docker-compose up -d --build`.
3. `docker-compose exec -T mysql mysql -uroot -p123456 < examples/example.sql fastapi-admin`.
4. That's just all, api server is listen at [http://127.0.0.1:8000](http://127.0.0.1:8000) now.

### Run Front

See
[restful-admin](https://github.com/long2ice/restful-admin)
for reference.

## Backend Integration

```shell
> pip3 install fastapi-admin
```

```Python
from fastapi_admin.factory import app as admin_app

fast_app = FastAPI()

register_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)

fast_app.mount('/admin', admin_app)


@fast_app.on_event('startup')
async def startup():
    await admin_app.init(
        admin_secret="test",
        permission=True,
        site=Site(
            name="FastAPI-Admin DEMO",
            login_footer="FASTAPI ADMIN - FastAPI Admin Dashboard",
            login_description="FastAPI Admin Dashboard",
            locale="en-US",
            locale_switcher=True,
            theme_switcher=True,
        ),
    )
```

## Documentation

See documentation [here](https://fastapi-admin.github.io/fastapi-admin/0.3.3).

## Deployment

Deploy fastapi app by gunicorn+uvicorn or reference
<https://fastapi.tiangolo.com/deployment/>.

## Restful API Docs

See [restful api](https://fastapi-admin-api-v1.long2ice.cn/admin/docs)
docs.

## License

This project is licensed under the
[Apache-2.0](https://github.com/long2ice/fastapi-admin/blob/v1/LICENSE)
License.
