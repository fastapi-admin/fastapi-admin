# Custom Page

It is easy to create custom pages.

## Template folders

You should configure your template folders when configure `fastapi-admin`.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(template_folders=["templates"])

```

## Write router

Then write a router to render the template.

If you want you page can access only after login, you need use `get_current_admin` dependency.

```python
from fastapi_admin.app import app as admin_app
from fastapi_admin.template import templates
from starlette.requests import Request
from fastapi import Depends
from fastapi_admin.depends import get_current_admin


@admin_app.get("/", dependencies=[Depends(get_current_admin)])
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", context={"request": request})
```

Don't forget to create the template `dashboard.html` and write content.

## Register resource

Finally, register it as a `Link` resource.

```python
from fastapi_admin.app import app as admin_app
from fastapi_admin.resources import Link


@admin_app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"
```

That's all, if you are a superuser, you can see a menu in navbar now, otherwise you need give the admin permission of
the resource.
