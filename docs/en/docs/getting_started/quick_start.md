# Quick Start

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
from examples.models import Admin
import aioredis
from fastapi import FastAPI

login_provider = UsernamePasswordProvider(
    admin_model=Admin,
    enable_captcha=True,
    login_logo_url="https://preview.tabler.io/static/logo.svg"
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
    admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        providers=[login_provider],
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
    icon = "fas fa-home"
    url = "/admin"
```

### Model

#### Field

The `Field` is used in `Model` resource to define how to display and input every field in model page.

The `Model` make a TortoiseORM model as a menu with CURD page.

```python

from examples.models import Admin
from fastapi_admin.app import app
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, filters, inputs

upload = FileUpload(uploads=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "admin model"
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
            input_=inputs.Image(null=True, upload=upload),
        ),
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
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]
```

### What's next?

That's all, you can run your app now. For more reference you can see [Reference](/reference).

Or you can see full [examples](https://github.com/fastapi-admin/fastapi-admin/tree/dev/examples).
