## Builtin Auth And Permissions Control

You should inherit `fastapi_admin.models.AbstractUser`,`fastapi_admin.models.AbstractPermission`,`fastapi_admin.models.AbstractRole` and add extra fields.

```python
from fastapi_admin.models import AbstractUser, AbstractPermission, AbstractRole

class AdminUser(AbstractUser):
    is_active = fields.BooleanField(default=False, description='Is Active')
    is_superuser = fields.BooleanField(default=False, description='Is Superuser')
    status = fields.IntEnumField(Status, description='User Status')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Permission(AbstractPermission):
    """
    must inheritance AbstractPermission
    """


class Role(AbstractRole):
    """
    must inheritance AbstractRole
    """


class AdminLog(AbstractAdminLog):
    """
    must inheritance AbstractAdminLog
    """
```

And set `permission=True` to active it:

```python
await admin_app.init(
    ...
    permission=True,
    site=Site(
        ...
    ),
)
```

And createsuperuser:

```shell
> fastapi-admin -h
usage: fastapi-admin [-h] -c CONFIG [--version] {createsuperuser} ...

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Tortoise-orm config dict import path,like settings.TORTOISE_ORM.
  --version, -V         show the version

subcommands:
  {createsuperuser}
```

Before you use this command - remember that you have to define your own user model that inherits from fastapi-admin `AbstractUser`.
eg.
```python
from fastapi_admin.models import AbstractUser
from tortoise import fields

class User(AbstractUser):
    id = fields.BigIntField(pk=True)

```

Here's an example of how createsuperuser command can look like: 

```shell
fastapi-admin -c "db.DB_CONFIG" createsuperuser -u User
```
The code above assumes that in your module's dir you have an `db.py` file in which there's, or that you provide a correct path on your own.
`-c` flag proceeds the path to your database config dict. It can look something like this.

```python
# db.py file
import os

DB_CONFIG: dict = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.environ.get("DB_HOST", "localhost"),
                "port": os.environ.get("DB_PORT", 5432),
                "user": os.environ.get("DB_USER", "user"),
                "password": os.environ.get("DB_PASSWORD", "secret_pass"),
                "database": os.environ.get("DB_DATABASE_NAME", "db"),
            },
        }
        # alternatively, probably only for testing purposes
        # "default": "sqlite://db.sqlite3",
    },
    "apps": {"models": {"models": ["app.db_models"]}},
}
```
[Read more about configs and initialization in tortoise orm](https://tortoise-orm.readthedocs.io/en/latest/setup.html?highlight=config#tortoise.Tortoise.init)

After `-u` you can tell fastapi-admin which model inherits from AdminUser.

## Custom Login

You can write your own login view logic:

```python
await admin_app.init(
    ...,
    login_view="examples.routes.login"
)
```

And must return json like:

```json
{
  "user": {
    "username": "admin",
    "is_superuser": false,
    "avatar": "https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.HSlcYkOEQewxyPuaqcVwCcw_wkbLB50Ws1-ZxfPoLAQ"
}
```

## Enum Support

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

## Help Text

FastAPI-Admin will auto read `description` defined in tortoise-orm model
`Field` and display in front with form help text.

## ForeignKeyField Support

If `ForeignKeyField` is not passed in `menu.raw_id_fields`,FastAPI-Admin
will get all related objects and display `select` in front with
`Model.__str__`.

## ManyToManyField Support

FastAPI-Admin will render `ManyToManyField` with multiple `select` in
`form` edit with `Model.__str__`.

## JSONField Render

FastAPI-Admin will render `JSONField` with `jsoneditor` as beauty
interface.

## Search Fields

Defined `menu.search_fields` in `menu` will render a search form by
fields.

## Xlsx Export

FastAPI-Admin can export searched data to excel file when define
`export=True` in `menu`.

## Bulk Actions

Current FastAPI-Admin supports builtin bulk action `delete_all`,if you
want to write your own bulk actions:

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

## Default Menus

Default, FastAPI-Admin provide default menus by your models, without
doing tedious works. Therefore you do not need to fill the optional argument `menus` in Site definition.


## Custom Menus
You can define a custom menu that'll be used by fastapi-admin. Here's an example of how that might look.

```python

menus = [
    Menu(name="Home", url="/", icon="fa fa-home"),
    Menu(
        name="Content",
        children=[
            Menu(name="Category", url="/rest/Category", icon="fa fa-list", search_fields=("slug",)),
            Menu(name="Config", url="/rest/Config", icon="fa fa-gear", import_=True, search_fields=("key",)),
            Menu(name="Product", url="/rest/Product", icon="fa fa-table", search_fields=("name",)),
        ],
    ),
    Menu(
        name="External",
        children=[
            Menu(name="Github", url="https://github.com/long2ice/fastapi-admin", icon="fa fa-github", external=True),
        ],
    ),
    Menu(
        name="Auth",
        children=[
            Menu(name="User", url="/rest/User", icon="fa fa-user", search_fields=("username",),),
            Menu(name="Role", url="/rest/Role", icon="fa fa-group", ),
            Menu(name="Permission", url="/rest/Permission", icon="fa fa-user-plus", ),
            Menu(name="Logout", url="/logout", icon="fa fa-lock", ),
            Menu(
                name="AdminLog",
                url="/rest/AdminLog",
                icon="fa fa-align-left",
                search_fields=("action", "admin", "model"),
            ),
        ],
    ),
]

```
Each menu can either be a single element menu that'll only link to a given resource, or it can be a gathering of multiple links, that you add by using the `children` optional argument.

`children` should be a list of `Menu` objects.

Now that you have your menus you can use them during the app initialization.

```python

menus = ...  # look at the code above. You can define it here or in separate file to make things neat

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
            menus=menus
        ),
    )
```

## Table Variant

You can define `RowVariant` and `CellVariants` in `computed` of `tortoise-orm`, which will effect table rows and cells variant.

```python
class User(AbstractUser):
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"

    def rowVariant(self) -> str:
        if not self.is_active:
            return "warning"
        return ""

    def cellVariants(self) -> dict:
        if self.is_active:
            return {
                "intro": "info",
            }
        return {}

    class PydanticMeta:
        computed = ("rowVariant", "cellVariants")
```

## Admin log

You can log each admin action like `delete`,`create` and `update`,just set `admin_log=True` in `admin_app.init()` and just create a model in your app that inherits from `fastapi_admin.models.AbstractAdminLog`.

## Import from excel

You can enable `import` by set `import_=True` in `Menu` definition, and data format must same as `Model` fields.

## Custom filters

There are two kinds of filters named `Filter` and `SearchFilter`.

`Filter` use to filter view list default, and `SearchFilter` add a custom search input in front.

To use `Filter` you should only inherit `fastapi_admin.filters.Filter` then implement `get_queryset`, for example:

```py
from fastapi_admin.filters import Filter

class CustomFilter(Filter):
    @classmethod
    def get_queryset(cls, queryset: QuerySet) -> QuerySet:
        return queryset.filter(~Q(key="test"))
```

Then add it to `Menu.custom_filters`.

```py
Menu(
    name="Config",
    url="/rest/Config",
    icon="fa fa-gear",
    import_=True,
    search_fields=("key",),
    custom_filters=[CustomFilter],
)
```

And to use `SearchFilter`, like `Filter` but inherit `fastapi_admin.filters.SearchFilter`, note that you show register it by `register_filter`, for example:

```py
from fastapi_admin.filters import SearchFilter, register_filter
from fastapi_admin.site import Field

@register_filter
class LikeFilter(SearchFilter):
    @classmethod
    def get_queryset(cls, queryset: QuerySet, value: Any) -> QuerySet:
        return queryset.filter(name__icontains=value)

    @classmethod
    async def get_field(cls) -> Field:
        return Field(label="NameLike", type="text")

    @classmethod
    def get_name(cls) -> str:
        return "filter"
```

`get_name` must return an unque `name` for all `SearchFilter` and `get_field` should return a `Field` instance.
