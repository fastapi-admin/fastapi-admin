from enum import IntEnum

from fastapi_admin.enum import EnumMixin


class ProductType(EnumMixin, IntEnum):
    article = 1
    page = 2

    @classmethod
    def choices(cls):
        return {
            cls.article: 'Article',
            cls.page: 'Page'
        }
