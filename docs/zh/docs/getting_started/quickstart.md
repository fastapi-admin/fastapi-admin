# 入门指南

`FastAPI-Admin` is easy to mount your `FastAPI` app, just need a few configs.

## Mount Admin App

First, you need mount the admin app from `FastAPI-Admin` as a sub application of `FastAPI`.

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
import aioredis
from fastapi import FastAPI

login_provider = UsernamePasswordProvider(user_model=User, enable_captcha=True)

app = FastAPI()


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

The full list of configs and detail can be found in [Configuration](/reference/configuration).

## Define And Register Resource

There are three kinds of resources, which are `Link`,`Model`, and `Dropdown`.

### Link

The `Link` will display a menu in sidebar with custom page or third page.

```python
from fastapi_admin.app import app
from fastapi_admin.resources import Link


@app.register
class Home(Link):
    label = "Home"
    icon = "ti ti-home"
    url = "/admin"
```

### Field

The `Field` is used in `Model` resource to define how to display and input every field in model page.

### Model

The `Model` make a TortoiseORM model as a menu with CURD page.

```python

from examples.models import User
from fastapi_admin.app import app
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, filters, inputs


@app.register
class UserResource(Model):
    label = "User"
    model = User
    icon = "ti ti-user"
    page_pre_title = "user list"
    page_title = "user model"
    filters = [
        filters.Search(
            name="username", label="Name", search_mode="contains", placeholder="Search for username"
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload_provider=upload_provider),
        ),
        "is_superuser",
        "is_active",
        "created_at",
    ]
```

### Dropdown

The `Dropdown` can contains both `Link` and `Model`, which can be nested.

```python


from examples import enums
from examples.models import Category, Product
from fastapi_admin.app import app
from fastapi_admin.resources import Dropdown, Field, Model
from fastapi_admin.widgets import displays, filters


@app.register
class Content(Dropdown):
    class CategoryResource(Model):
        label = "Category"
        model = Category
        fields = ["id", "name", "slug", "created_at"]

    class ProductResource(Model):
        label = "Product"
        model = Product
        filters = [
            filters.Enum(enum=enums.ProductType, name="type", label="ProductType"),
            filters.Datetime(name="created_at", label="CreatedAt"),
        ]
        fields = [
            "id",
            "name",
            "view_num",
            "sort",
            "is_reviewed",
            "type",
            Field(name="image", label="Image", display=displays.Image(width="40")),
            "body",
            "created_at",
        ]

    label = "Content"
    icon = "ti ti-package"
    resources = [ProductResource, CategoryResource]
```

### What's next?

That's all, you can run your app now. For more reference you can see [Reference](/reference).
