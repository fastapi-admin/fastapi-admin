# Admin Log (💗 Pro only)

You can enable log all actions by using the `AdminLogProvider`.

You should just add the `AdminLogProvider` to providers.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.admin_log import AdminLogProvider
from examples.models import Log

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[AdminLogProvider(Log)]
    )
```

The `Log` model is subclass of `fastapi_admin.models.AbstractLog`.

```python
class AbstractLog(Model):
    admin = fields.ForeignKeyField("models.Admin")
    content = fields.JSONField()
    resource = fields.CharField(max_length=50)
    action = fields.CharEnumField(enums.Action, default=enums.Action.create)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-id"]
```
