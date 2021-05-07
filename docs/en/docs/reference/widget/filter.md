# Filter

The filter define how to filter the model resource.

## Search

Search by a field.

```python
@app.register
class AdminResource(Model):
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
    ]
```

- `search_mode` choices: `equal`,`contains`,`icontains`,`startswith`,`istartswith`,`endswith`,`iendswith`,`iexact`,`search`

## Datetime

Datetime field filter.

```python
@app.register
class AdminResource(Model):
    filters = [
        filters.Datetime(name="created_at", label="CreatedAt"),
    ]
```

## Date

Date field filter.

```python
@app.register
class AdminResource(Model):
    filters = [
        filters.Date(name="created_at", label="CreatedAt"),
    ]
```

## Select

Select filter.

## Enum

Like select filter but choice from a enum class.

```python
class ProductResource(Model):
    filters = [
        filters.Enum(enum=enums.ProductType, name="type", label="ProductType"),
    ]
```

## ForeignKey

Like select filter but choice from a `ForeignKey` model.
