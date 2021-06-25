# Exclusive content

## Login Captcha

You can set captcha in admin login page, just set `enable_captcha=True`.

```python3
login_provider = UsernamePasswordProvider(user_model=User, enable_captcha=True)
```

## Google Recaptcha V2

In addition to captcha, you can also use `Google Recaptcha V2` to protect your site.

The `GoogleRecaptcha` schema:

```python
class GoogleRecaptcha(BaseModel):
    cdn_url: str = "https://www.google.com/recaptcha/api.js"
    verify_url: str = "https://www.google.com/recaptcha/api/siteverify"
    site_key: str
    secret: str
```

Just set `google_recaptcha` in login provider.

```python
from fastapi_admin.providers.login import GoogleRecaptcha

await admin_app.configure(
    providers=[
        LoginProvider(
            google_recaptcha=GoogleRecaptcha(
                site_key=settings.GOOGLE_RECAPTCHA_SITE_KEY,
                secret=settings.GOOGLE_RECAPTCHA_SECRET,
            ),
        ),
    ]
)
```

## Failed Login IP Limitation

If you want limit login failed ip with error password, you can use `LoginPasswordMaxTryMiddleware`.

```python
admin_app.add_middleware(BaseHTTPMiddleware, dispatch=LoginPasswordMaxTryMiddleware(max_times=3, after_seconds=360))
```

## Permission Control

`PermissionProvider` allow you to configure the access control for resources of admin users with permissions `read`
/`create`/`update`/`delete`.

## Additional File Upload

### ALiYunOSS

File upload for ALiYunOSS.

### AwsS3

File upload for AWS S3.

## Maintenance

If your site is in maintenance, you can set `true` to `admin_app.configure(...)`.

```python
await admin_app.configure(maintenance=True)
```

## Admin Log

If you want to log all `create/update/delete` actions, you can add `AdminLogProvider` to `admin_app.configure(...)`.

```python
await admin_app.configure(providers=[AdminLogProvider(Log)])
```

## Site Search

You can enable site search by add `SearchProvider` to `admin_app.configure(...)`.

```python
await admin_app.configure(providers=[SearchProvider()])
```

## Notification

You can use notification by adding `NotificationProvider` to `admin_app.configure(...) implement by websocket.

```python
await admin_app.configure(providers=[NotificationProvider()])
```

## OAuth2

Current there are two builtin oauth2 implementations `GitHubOAuth2Provider` and `GoogleOAuth2Provider`.

```python
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
