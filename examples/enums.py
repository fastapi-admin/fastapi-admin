from enum import IntEnum

from fastapi_admin.enums import EnumMixin


class ProductType(EnumMixin, IntEnum):
    article = 1
    page = 2

    @classmethod
    def choices(cls):
        return {cls.article: "Article", cls.page: "Page"}


class Status(EnumMixin, IntEnum):
    on = 1
    off = 0

    @classmethod
    def choices(cls):
        return {cls.on: "On", cls.off: "Off"}
