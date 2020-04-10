from typing import Optional, Tuple, Dict, Union, List, Set

from pydantic import BaseModel, HttpUrl


class Menu(BaseModel):
    name: str
    title: Optional[bool]
    url: Optional[str]
    icon: Optional[str]
    include: Optional[Tuple[str]]
    exclude: Optional[Tuple[str]]
    external: Optional[bool] = False
    raw_id_fields: Optional[Set[str]] = set()
    search_fields: Optional[Set[str]] = set()
    sort_fields: Optional[Set[str]] = set()
    fields_type: Dict = {}


class Site(BaseModel):
    name: str
    logo: HttpUrl
    locale: str
    locale_switcher: bool
    menus: List[Menu]

    class Config:
        fields = {
            'menus': 'menu'
        }


class Field(BaseModel):
    label: str
    cols: Optional[int]
    input_cols: Optional[int]
    group: Optional[str]
    type: str
    required: bool = True
    options: Optional[List[Dict]]
    sortable: Optional[bool]
    multiple: bool = False
    ref: Optional[str]
    description: Optional[str]
    disabled: Optional[bool] = False


class Resource(BaseModel):
    title: str
    resource_fields: Dict[str, Field]
    searchFields: Optional[Dict[str, Field]]

    class Config:
        fields = {
            'resource_fields': 'fields',
        }
