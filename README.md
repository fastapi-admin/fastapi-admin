# FastAPI Admin

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/long2ice/fastapi-admin)](https://github.com/long2ice/fastapi-admin)
[![image](https://github.com/long2ice/fastapi-admin/workflows/gh-pages/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:gh-pages)
[![image](https://github.com/long2ice/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:pypi)

[中文文档](https://blog.long2ice.cn/2020/05/fastapi-admin%E5%BF%AB%E9%80%9F%E6%90%AD%E5%BB%BA%E5%9F%BA%E4%BA%8Efastapi%E4%B8%8Etortoise-orm%E7%9A%84%E7%AE%A1%E7%90%86%E5%90%8E%E5%8F%B0/)

## Introduction

FastAPI-Admin is a admin dashboard based on
[fastapi](https://github.com/tiangolo/fastapi) and
[tortoise-orm](https://github.com/tortoise/tortoise-orm).

FastAPI-Admin provide crud feature out-of-the-box with just a few
config.

## Live Demo

Check a live Demo here
[https://fastapi-admin.long2ice.cn](https://fastapi-admin.long2ice.cn/).

- username: `admin`
- password: `123456`

Data in database will restore every day.

## Screenshots

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/login.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/list.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/view.png)

![image](https://github.com/long2ice/fastapi-admin/raw/master/images/create.png)

## Requirements

- [FastAPI](https://github.com/tiangolo/fastapi) framework as your
  backend framework.
- [Tortoise-ORM](https://github.com/tortoise/tortoise-orm) as your orm
  framework, by the way, which is best asyncio orm so far and I\'m one
  of the contributors😋.

## Quick Start

### Run Example Local

Look at
[examples](https://github.com/long2ice/fastapi-admin/tree/master/examples).

1. `git clone https://github.com/long2ice/fastapi-admin.git`.
2. create database `fastapi-admin` and import from
   `examples/example.sql`.
3. `python setup.py install`.
4. `env DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin PYTHONPATH=./ python3 examples/main.py`,then
   you can see:

```log
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [89005]
INFO:     Started server process [89009]
INFO:     Waiting for application startup.
INFO:     Tortoise-ORM startup
    connections: {'default': 'mysql://root:123456@127.0.0.1:3306/fastapi-admin'}
    apps: {'models': {'models': ['examples.models'], 'default_connection': 'default'}}
INFO:     Tortoise-ORM started, {'default': <tortoise.backends.mysql.client.MySQLClient object at 0x110ed6760>}, {'models': {'Category': <class 'examples.models.Category'>, 'Product': <class 'examples.models.Product'>, 'User': <class 'examples.models.User'>}}
INFO:     Tortoise-ORM generating schema
INFO:     Application startup complete.
```

### Backend Integration

```shell
> pip3 install fastapi-admin
```

```python
from fastapi_admin.factory import app as admin_app

fast_app = FastAPI()

register_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)

fast_app.mount('/admin', admin_app)

@fast_app.on_event('startup')
async def startup():
    admin_app.init(
        user_model='User',
        tortoise_app='models',
        admin_secret='test',
        permission=True,
        site=Site(...)
    )
```

### Front

See
[fastapi-admin-front](https://github.com/long2ice/fastapi-admin-front)
for reference.

## Features

### Builtin Auth And Permissions Control

Inherit `fastapi_admin.models.User` and add you own fields,must contains
`is_active` and `is_superuser`.

```python
from fastapi_admin.models import User as AdminUser

class AdminUser(AdminUser,Model):
    is_active = fields.BooleanField(default=False, description='Is Active')
    is_superuser = fields.BooleanField(default=False, description='Is Superuser')
    status = fields.IntEnumField(Status, description='User Status')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
```

Then add `fastapi_admin.models` to `Tortoise-ORM` config, example:

```python
TORTOISE_ORM = {
    'connections': {
        'default': os.getenv('DATABASE_URL')
    },
    'apps': {
        'models': {
            'models': ['examples.models', 'fastapi_admin.models'],
            'default_connection': 'default',
        }
    }
}
```

And set `permission=True` to active it:

```python
admin_app.init(
    user_model='AdminUser',
    admin_secret='123456',
    models='examples.models',
    permission=True,
    site=Site(
        ...
    )
)
```

And register permissions and createsuperuser:

```shell
> fastapi-admin -h
usage: fastapi-admin [-h] -c CONFIG {register_permissions,createsuperuser} ...

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Tortoise-orm config dict import path,like settings.TORTOISE_ORM.

subcommands:
  {register_permissions,createsuperuser}
```

### Custom Login

You can write your own login view logic:

```python
admin_app.init(
    ...
    login_view="examples.routes.login"
)
```

And must return json like:

```json
{
  "user": {
    "username": "admin",
    "is_superuser": False,
    "avatar": "https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.HSlcYkOEQewxyPuaqcVwCcw_wkbLB50Ws1-ZxfPoLAQ"
}
```

### Enum Support

When you define a enum field of tortoise-orm,like `IntEnumField`,you can
inherit `fastapi_admin.enums.EnumMixin` and impl `choices()` method,
FastAPI-Admin will auto read and display and render a `select` widget in
front.

```python
class Status(EnumMixin, IntEnum):
    on = 1
    off = 2

    @classmethod
    def choices(cls):
        return {
            cls.on: 'ON',
            cls.off: 'OFF'
        }
```

### Help Text

FastAPI-Admin will auto read `description` defined in tortoise-orm model
`Field` and display in front with form help text.

### ForeignKeyField Support

If `ForeignKeyField` not passed in `menu.raw_id_fields`,FastAPI-Admin
will get all related objects and display `select` in front with
`Model.__str__`.

### ManyToManyField Support

FastAPI-Admin will render `ManyToManyField` with multiple `select` in
`form` edit with `Model.__str__`.

### JSONField Render

FastAPI-Admin will render `JSONField` with `jsoneditor` as beauty
interface.

### Search Fields

Defined `menu.search_fields` in `menu` will render a search form by
fields.

### Xlsx Export

FastAPI-Admin can export searched data to excel file when define
`export=True` in `menu`.

### Bulk Actions

Current FastAPI-Admin support builtin bulk action `delete_all`,if you
want write your own bulk actions:

1. pass `bulk_actions` in `Menu`,example:

```python
Menu(
    ...
    bulk_actions=[{
        'value': 'delete', # this is fastapi router path param.
        'text': 'delete_all', # this will show in front.
    }]
)
```

2. write fastapi route,example:

```python
from fastapi_admin.schemas import BulkIn
from fastapi_admin.factory import app as admin_app

@admin_app.post(
    '/rest/{resource}/bulk/delete' # `delete` is defined in Menu before.
)
async def bulk_delete(
        bulk_in: BulkIn,
        model=Depends(get_model)
):
    await model.filter(pk__in=bulk_in.pk_list).delete()
    return {'success': True}
```

### Default Menus

Default, FastAPI-Admin provide default menus by your models, without
doing tedious works.

## Deployment

Deploy fastapi app by gunicorn+uvicorn or reference
<https://fastapi.tiangolo.com/deployment/>.

## Restful API Docs

See [restful api](https://api-fastapi-admin.long2ice.cn:8443/admin/docs)
docs.

## Documents

See [documents](https://fastapi-admin-docs.long2ice.cn) for reference.

## Support this project

- Just give a star!
- Donation.

### AliPay

<img width="200" src="https://github.com/long2ice/fastapi-admin/raw/dev/images/alipay.jpeg"/>

### WeChat Pay

<img width="200" src="https://github.com/long2ice/fastapi-admin/raw/dev/images/wechatpay.jpeg"/>

### PayPal

Donate money by [paypal](https://www.paypal.me/long2ice) to my
account long2ice.

## ThanksTo

- [fastapi](https://github.com/tiangolo/fastapi) ,high performance
  async api framework.
- [tortoise-orm](https://github.com/tortoise/tortoise-orm) ,familiar
  asyncio ORM for python.

## License

This project is licensed under the
[Apache-2.0](https://github.com/long2ice/fastapi-admin/blob/master/LICENSE)
License.
