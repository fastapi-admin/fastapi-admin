# Permission Control (💗 Pro only)

There are for kinds of permissions builtin. The `Link` has only `read`, and `Model` resource has all kinds of
permissions.

```python
class Permission(str, Enum):
    create = "create"
    delete = "delete"
    update = "update"
    read = "read"
```

If an admin user has no `read` for a resource, it won't show the menu in dashboard. The `update`/`delete`/`create`
permissions is also related with the `actions` display.

## Usage

First, inherit and add the necessary models to your `models.py`.

```python
from fastapi_admin.models import (
    AbstractPermission,
    AbstractResource,
    AbstractRole,
)


class Resource(AbstractResource):
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass
```

Then also add `PermissionProvider` to providers.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.permission import PermissionProvider

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            PermissionProvider(
                Admin,
                Resource,
                Permission,
            ),
        ]
    )
```

That's the all code, after that, all resources and permissions will autofill in database, what you need do is just add
role and relate admins in dashboard and configure permissions yourself.
