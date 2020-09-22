## Import app

First of all suppose you have a fastapi+tortoise-orm project and running normally, then first you should is import admin app from `fastapi-admin` and mount in root fastapi app.

```python hl_lines="6"
from fastapi_admin.factory import app as admin_app

def create_app():
    fast_app = FastAPI(debug=False)
    register_tortoise(fast_app, config=TORTOISE_ORM)
    fast_app.mount("/admin", admin_app)
    return fast_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, debug=False, reload=False, lifespan="on")

```

Now you can visit `http://127.0.0.1:8000/admin/docs` see all restful api comes from fastapi-admin.

## Init App

After mount admin app, you should init app now. Pay attention to that you should init admin app in fastapi `startup` event instead of run it directly.

```python
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
            menus=[
                Menu(name="Home", url="/", icon="fa fa-home"),
                Menu(
                    name="Content",
                    children=[
                        Menu(
                            name="Category",
                            url="/rest/Category",
                            icon="fa fa-list",
                            search_fields=("slug",),
                        ),
                        Menu(
                            name="Config",
                            url="/rest/Config",
                            icon="fa fa-gear",
                            import_=True,
                            search_fields=("key",),
                        ),
                        Menu(
                            name="Product",
                            url="/rest/Product",
                            icon="fa fa-table",
                            search_fields=("name",),
                        ),
                    ],
                ),
                Menu(
                    name="External",
                    children=[
                        Menu(
                            name="Github",
                            url="https://github.com/long2ice/fastapi-admin",
                            icon="fa fa-github",
                            external=True,
                        ),
                    ],
                ),
                Menu(
                    name="Auth",
                    children=[
                        Menu(
                            name="User",
                            url="/rest/User",
                            icon="fa fa-user",
                            search_fields=("username",),
                        ),
                        Menu(name="Role", url="/rest/Role", icon="fa fa-group",),
                        Menu(name="Permission", url="/rest/Permission", icon="fa fa-user-plus",),
                        Menu(
                            name="AdminLog",
                            url="/rest/AdminLog",
                            icon="fa fa-align-left",
                            search_fields=("action", "admin", "model"),
                        ),
                        Menu(name="Logout", url="/logout", icon="fa fa-lock",),
                    ],
                ),
            ],
        ),
    )
```
