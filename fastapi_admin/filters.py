from typing import Any

from tortoise.queryset import QuerySet

from fastapi_admin.site import Field

_search_filters = {}


class Filter:
    @classmethod
    def get_queryset(cls, queryset: QuerySet) -> QuerySet:
        raise NotImplementedError


class SearchFilter:
    @classmethod
    def get_queryset(cls, queryset: QuerySet, option: Any) -> QuerySet:
        raise NotImplementedError

    @classmethod
    async def get_field(cls) -> Field:
        raise NotImplementedError

    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError


def register_filter(cls: SearchFilter):
    _search_filters[cls.get_name()] = cls
    return cls


def get_filter_by_name(name: str):
    return _search_filters.get(name)
