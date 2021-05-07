# Resource

There are three kinds of resources, `Link`,`Model` and `Dropdown`, all are inherited
from `fastapi_admin.resources.Resource`.

You should use `app.register` decorator to register a resource.
## Link

`Link` just display a menu with a link.

```python
from fastapi_admin.app import app
from fastapi_admin.resources import Link


@app.register
class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"
```

## Model

## Dropdown
