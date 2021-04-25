import abc
from enum import Enum as EnumCLS
from typing import Any, Optional, Type

from tortoise import Model

from fastapi_admin import constants
from fastapi_admin.widgets.inputs import Input


class Filter(Input):
    def __init__(self, name: str, label: str, placeholder: str = ""):
        """
        Parent class for all filters
        :param name: model field name
        :param label:
        """
        super().__init__(name=name, label=label, placeholder=placeholder)


class Search(Filter):
    template = "widgets/filters/search.html"

    def __init__(
        self,
        name: str,
        label: str,
        search_mode: str = "equal",
        placeholder: str = "",
    ):
        """
        Search for keyword
        :param name:
        :param label:
        :param search_mode: equal,contains,icontains,startswith,istartswith,endswith,iendswith,iexact,search
        """
        if search_mode == "equal":
            super().__init__(name, label, placeholder)
        else:
            super().__init__(name + "__" + search_mode, label, placeholder)
        self.context.update(search_mode=search_mode)


class Datetime(Filter):
    template = "widgets/filters/datetime.html"

    def __init__(
        self,
        name: str,
        label: str,
        format_: str = constants.DATE_FORMAT_MOMENT,
    ):
        """
        Datetime filter
        :param name:
        :param label:
        :param format_: the format of moment.js
        """
        super().__init__(
            name + "__range",
            label,
        )
        self.context.update(format=format_)

    async def parse_value(self, value: Optional[str]):
        return value.split(" - ")

    async def render(self, value: Any):
        if value is not None:
            value = " - ".join(value)
        return await super().render(value)


class Date(Datetime):
    def __init__(
        self,
        name: str,
        label: str,
        format_: str = constants.DATE_FORMAT_MOMENT,
    ):
        super().__init__(
            name,
            label,
            format_,
        )


class Select(Filter):
    template = "widgets/filters/select.html"

    def __init__(self, name: str, label: str, null: bool = False):
        super().__init__(name, label)
        self.null = null

    @abc.abstractmethod
    async def get_options(self):
        """
        return list of tuple with display and value

        [("on",1),("off",2)]

        :return: list of tuple with display and value
        """

    async def render(self, value: Any):
        options = await self.get_options()
        self.context.update(options=options)
        return await super(Select, self).render(value)


class Enum(Select):
    def __init__(
        self,
        enum: Type[EnumCLS],
        name: str,
        label: str,
        enum_type: Type = int,
        null: bool = False,
    ):
        super().__init__(name, label, null)
        self.enum = enum
        self.enum_type = enum_type

    async def parse_value(self, value: Any):
        return self.enum(self.enum_type(value))

    async def get_options(self):
        options = [(v.name, v.value) for v in self.enum]
        if self.null:
            options = [("", "")] + options
        return options


class ForeignKey(Select):
    def __init__(
        self,
        model: Type[Model],
        name: str,
        label: str,
    ):
        super().__init__(name=name, label=label)
        self.model = model

    async def get_options(self):
        ret = await self.get_queryset()
        options = [
            (
                str(x),
                x.pk,
            )
            for x in ret
        ]
        if self.context.get("null"):
            options = [("", "")] + options
        return options

    async def get_queryset(self):
        return await self.model.all()

    async def render(self, value: Any):
        if value is not None:
            value = int(value)
        return await super().render(value)
