# Display

## Display

Default display, which will just display the value with any change.

## DatetimeDisplay

Will display the value by the giving format, default is `%Y-%m-%d %H:%M:%S`.

```python
class DatetimeDisplay(Display):
    def __init__(self, format_: str = constants.DATETIME_FORMAT):
```

## DateDisplay

Will display the value by the giving format, default is `%Y-%m-%d`.

```python
class DatetimeDisplay(Display):
    def __init__(self, format_: str = constants.DATETIME_FORMAT):
```

## InputOnly

Which is a special display widget, for that will not display in table content, but display in edit page only.

## Boolean

Will display the value in bool mode.

## Image

Will display the value as a image.

## Json

Will display the value with json highlight.
