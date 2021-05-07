# Error Pages

`fastapi-admin` can catch all `403`,`404`,`500` errors and redirect to builtin error pages.

To enable that, you should use `add_exception_handler`.

```python
from fastapi_admin.exceptions import forbidden_error_exception, not_found_error_exception, server_error_exception
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
```
