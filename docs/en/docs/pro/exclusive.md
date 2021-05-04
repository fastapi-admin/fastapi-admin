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

## Additional File Upload Providers

### ALiYunOSSProvider

### AwsS3Provider

## Error pages

### 403

You can catch all `403` error to show builtin `403` page.

```python
from fastapi_admin.exceptions import forbidden_error_exception
from starlette.status import HTTP_403_FORBIDDEN

admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
```

### 404

You can catch all `404` error to show builtin `404` page.

```python
from fastapi_admin.exceptions import not_found_error_exception
from starlette.status import HTTP_404_NOT_FOUND

app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
```

### 500

You can catch all `500` error to show builtin `500` page.

```python
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi_admin.exceptions import server_error_exception

app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
```

### Maintenance

If your site is in maintenance, you can set `true` to `admin_app.configure(...)`.

```python
admin_app.configure(maintenance=True)
```

## Admin Log

If you want to log all `create/update/delete` actions, you can set `admin_log_provider` to `admin_app.configure(...)`.

```python
admin_app.configure(admin_log_provider=AdminLogProvider(Log))
```

## Site Search

You can enable site search by set `search_provider` to `admin_app.configure(...)`.

```python
admin_app.configure(search_provider=SearchProvider())
```
