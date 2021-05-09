# Notification (💗 Pro only)

`FastAPI-Admin` provide a notification center implement by websocket.

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/notification.png)

## Usage

You should add it to providers to enable it.

```python
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.notification import NotificationProvider

app = FastAPI()

provider = NotificationProvider()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[provider]
    )
```

There are two ways to send notifications.

One is call `await provider.broadcast()` directly.

```python
data = {
    "title": "test",
    "content": "//avatars.githubusercontent.com/u/13377178?v=4",
    "image": "https://avatars.githubusercontent.com/u/13377178?v=4",
    "link": "https://fastapi-admin-docs.long2ice.cn"
}
await provider.broadcast(data)
```

If you want to send notifications out of application, another way is use http api.

```python
import requests

requests.post('http://localhost:8000/admin/notification', json=data)
```
