import json
from datetime import datetime
from typing import Optional

from fastapi_admin import constants
from fastapi_admin.widgets import Widget


class Display(Widget):
    """
    Parent class for all display widgets
    """


class DatetimeDisplay(Display):
    def __init__(self, format_: str = constants.DATETIME_FORMAT):
        super().__init__()
        self.format_ = format_

    async def render(self, value: datetime):
        if value:
            value = value.strftime(self.format_)
        return await super(DatetimeDisplay, self).render(value)


class DateDisplay(DatetimeDisplay):
    def __init__(self, format_: str = constants.DATE_FORMAT):
        super().__init__(format_)


class InputOnly(Display):
    """
    Only input without showing in display
    """


class Boolean(Display):
    template = "widgets/displays/boolean.html"


class Image(Display):
    template = "widgets/displays/image.html"

    def __init__(self, width: Optional[str] = None, height: Optional[str] = None):
        super().__init__(width=width, height=height)


class Json(Display):
    template = "widgets/displays/json.html"

    async def render(self, value: dict):
        return self.templates.get_template(self.template).render(
            value=json.dumps(value),
        )
