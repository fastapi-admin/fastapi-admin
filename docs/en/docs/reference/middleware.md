# Middleware

## LoginPasswordMaxTryMiddleware (💗 Pro only)

If you want limit login failed ip with error password, you can use `LoginPasswordMaxTryMiddleware`.

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_admin import middlewares
from fastapi_admin.app import app as admin_app

admin_app.add_middleware(BaseHTTPMiddleware,
                         dispatch=middlewares.LoginPasswordMaxTryMiddleware(max_times=3, after_seconds=3600))
```

After that, user can try max `3` times password, if all failed, the ip will be limited `3600` seconds.
