# Exclusive content

## Login Captcha

You can set captcha in admin login page, just set `enable_captcha=True`.

```python3
login_provider = UsernamePasswordProvider(user_model=User, enable_captcha=True)
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
