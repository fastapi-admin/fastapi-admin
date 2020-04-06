from typing import Optional, Tuple, Dict, Union, List

from pydantic import BaseModel, HttpUrl


class Menu(BaseModel):
    name: str
    title: Optional[bool]
    url: Optional[str]
    icon: Optional[str]
    include: Optional[Tuple[str]]
    exclude: Optional[Tuple[str]]
    external: Optional[bool] = False


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
    type: Optional[Union[str, Dict]]
    required: bool = True
    options: Optional[List[Dict]]


class Resource(BaseModel):
    title: str
    resource_fields: Dict[str, Field]

    class Config:
        fields = {
            'resource_fields': 'fields'
        }
