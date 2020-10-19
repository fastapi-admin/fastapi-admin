## Builtin Auth And Permissions Control

You should inherit `fastapi_admin.models.AbstractUser`,`fastapi_admin.models.AbstractPermission`,`fastapi_admin.models.AbstractRole` and add extra fields.

```python
from fastapi_admin.models import AbstractUser,AbstractPermission,AbstractRole

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
    users = fields.ManyToManyField("models.AdminUser")


class AdminLog(AbstractAdminLog):
    """
    must inheritance AbstractAdminLog
    """
    users = fields.ManyToManyField("models.AdminUser")

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

## Custom Login

You can write your own login view logic:

```python
await admin_app.init(
    ...
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

If `ForeignKeyField` not passed in `menu.raw_id_fields`,FastAPI-Admin
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

## Default Menus

Default, FastAPI-Admin provide default menus by your models, without
doing tedious works.

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

You can log each admin action like `delete`,`create` and `update`,just set `admin_log=True` in `admin_app.init()` and inherit `fastapi_admin.models.AbstractAdminLog`.

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
