# Resource

There are three kinds of resources, `Link`,`Model` and `Dropdown`, all are inherited
from `fastapi_admin.resources.Resource`.

You should use `app.register` decorator to register a resource.

And all icons define come from <https://tabler-icons.io> and <https://fontawesome.com>.

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

## Field

`Field` is the object that `Model` use, which define how a field display and input.

```python
@app.register
class AdminResource(Model):
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]
```

You can pass `str` or `Field` to `fields`, if is `str`, it will try to auto mapping display and input widget, such
as `displays.Boolean` for `BooleanField`, `inputs.Date` for `DateField`.

All kind of widgets you can find in [Display](/reference/widget/display/) and [Input](/reference/widget/input/).

## Action

The `Action` define the action display in every end of row, and bulk action for every model.

By default there are two actions, Which are delete action and edit action, and one bulk action, which allow delete rows
in bulk.

To use that, you should override the `get_actions` and `get_bulk_actions`. The following example hide all default
actions with return empty list.

```python
@app.register
class AdminResource(Model):
    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []
```

## ComputeField

The class that `model.get_compute_fields` used.

```python
class ComputeField(BaseModel):
    label: str
    name: str

    async def get_value(self, request: Request, obj: dict):
        return obj.get(self.name)
```

What you need to do is just override the `get_value` method.

```python
class RestDays(ComputeField):
    async def get_value(self, request: Request, obj: dict):
        days = (obj.get(self.name) - date.today()).days
        return days if days >= 0 else 0
```

## ToolbarAction

The class that `mode.get_toolbar_actions` used.

```python
class ToolbarAction(Action):
    class_: Optional[str]
```

## Model

`Model` is the core resource, which make TortoiseORM model as a menu and display a data table with create, update, and
delete.

```python
@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    page_pre_title = "admin list"
    page_title = "Admin Model"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]

```

### Configuration

- `label`: The menu name display.
- `model`: TortoiseORM model.
- `page_pre_title`: Show page pre title in content.
- `page_title`: Show page title in content.
- `filters`: Define filters for the model, which will display filter inputs in table above, all kinds of filters you can
  find in [Filter](/reference/widget/filter/).

### row_attributes

You can add extra attributes to each row by use `row_attributes`.

```python
@app.register
class ConfigResource(Model):
    async def row_attributes(self, request: Request, obj: dict) -> dict:
        if obj.get("status") == enums.Status.on:
            return {"class": "bg-green text-white"}
        return await super().row_attributes(request, obj)
```

The example above will add the css `class = "bg-green text-white"` for the row which `status = enums.Status.on`.

### column_attributes

You can add extra attributes to each column by use `column_attributes`.

```python
@app.register
class LogResource(Model):
    async def column_attributes(self, request: Request, field: Field) -> dict:
        if field.name == "content":
            return {"class": "w-50"}
        return await super().column_attributes(request, field)
```

The example above will add the css `class = "w-50"` for the column which `content`.

### cell_attributes

Same as `row_attributes` but for the cell, you can add extra attributes to cell depends on the row object and column
field.

```python
@app.register
class AdminResource(Model):
    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)
```

### get_compute_fields

In some cases we need show some extra fields which are computed from other fields, you can use `get_compute_fields`.

```python
@app.register
class SponsorResource(Model):
    async def get_compute_fields(self, request: Request) -> List[ComputeField]:
        return [RestDays(name="invalid_date", label="Days Remaining")]
```

### get_toolbar_actions

Show toolbar actions top right of the table.

```python
@app.register
class CategoryResource(Model):
    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        actions = await super().get_toolbar_actions(request)
        actions.append(import_export_provider.import_action)
        actions.append(import_export_provider.export_action)
        return actions
```

## Dropdown

The dropdown resource just contains `Link` and `Model` resource, and which can be nested.

```python
@app.register
class Content(Dropdown):
    label = "Content"
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]
```
