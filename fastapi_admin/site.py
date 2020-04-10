from typing import Optional, Tuple, Dict, Union, List, Set

from pydantic import BaseModel, HttpUrl


class Menu(BaseModel):
    name: str
    title: Optional[bool]
    url: Optional[str]
    icon: Optional[str]
    # include fields
    include: Optional[Tuple[str]]
    # exclude fields
    exclude: Optional[Tuple[str]]
    # external link
    external: Optional[bool] = False
    # raw id fields
    raw_id_fields: Optional[Set[str]] = set()
    # searchable fields
    search_fields: Optional[Set[str]] = set()
    # sortable fields
    sort_fields: Optional[Set[str]] = set()
    # define field type,like select,radiolist,text,date
    fields_type: Dict = {}
    actions: Dict = {
        'toolbar': {
            'delete_all': True
        },
        'export': True
    }


class Site(BaseModel):
    name: str
    logo: HttpUrl
    locale: str
    locale_switcher: bool = False
    theme_switcher: bool = False
    theme: Optional[str]
    url: Optional[HttpUrl]
    grid_style: int = 1
    # custom css
    css: Optional[List[HttpUrl]]
    # menu define
    menus: List[Menu]
    # custom footer with html
    footer: Optional[str]

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
    resource_fields: Dict[str, Union[Field, Dict]]
    searchFields: Optional[Dict[str, Field]]

    class Config:
        fields = {
            'resource_fields': 'fields',
        }
