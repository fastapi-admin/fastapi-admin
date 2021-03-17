from typing import Any

from tortoise.query_utils import Q
from tortoise.queryset import QuerySet

from fastapi_admin.filters import Filter, SearchFilter, register_filter
from fastapi_admin.site import Field


class CustomFilter(Filter):
    @classmethod
    def get_queryset(cls, queryset: QuerySet) -> QuerySet:
        return queryset.filter(~Q(key="test"))


@register_filter
class LikeFilter(SearchFilter):
    @classmethod
    def get_queryset(cls, queryset: QuerySet, value: Any) -> QuerySet:
        return queryset.filter(name__icontains=value)

    @classmethod
    async def get_field(cls) -> Field:
        return Field(label="NameLike", type="text")

    @classmethod
    def get_name(cls) -> str:
        return "filter"
