# Global Search (💗 Pro only)

You can enable site search by add `SearchProvider` to `admin_app.configure(...)`.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.search import SearchProvider

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[SearchProvider()]
    )
```

The builtin search provider can search for the all available resources by resource name.
