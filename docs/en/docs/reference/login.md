# Login

## Uername and password

There is a builtin `UsernamePasswordProvider`, if you want to enable it, you need add in to providers.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ]
    )
```

Then admin can login with `username` and `password`.

## OAuth2  (💗 Pro only)

If want admin login with [oauth2](https://datatracker.ietf.org/doc/html/rfc6749) method, such as `GitHub` or `Google`,
you can use `OAuth2Provider`.

Current there are two builtin providers, `GitHubOAuth2Provider` and `GoogleOAuth2Provider`.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from examples.providers import GitHubProvider, GoogleProvider, LoginProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            GitHubProvider(Admin, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET),
            GoogleProvider(
                Admin,
                settings.GOOGLE_CLIENT_ID,
                settings.GOOGLE_CLIENT_SECRET,
                redirect_uri="https://fastapi-admin-pro.long2ice.cn/admin/oauth2/google_oauth2_provider",
            ),
        ]
    )
```

If you want custom oauth2 provider, just inherit `fastapi_admin.providers.login.OAuth2Provider` and implement its
methods. And the `redirect_uri` format is `{server_url}/{admin_path}/oauth2/{provider_name}`.
