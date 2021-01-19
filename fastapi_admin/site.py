from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, HttpUrl


class Menu(BaseModel):
    name: str
    # must be format with /rest/<Model> if it's a model resource.
    url: Optional[str]
    icon: Optional[str]
    # children menu
    children: Optional[List["Menu"]] = []
    # include fields
    include: Optional[Tuple[str, ...]] = tuple()
    # exclude fields
    exclude: Optional[Tuple[str, ...]] = tuple()
    # external link
    external: Optional[bool] = False
    # raw id fields
    raw_id_fields: Optional[Tuple[str, ...]] = tuple()
    # searchable fields
    search_fields = tuple()
    # sortable fields
    sort_fields: Optional[Tuple[str, ...]] = tuple()
    # define field type,like select,radiolist,text,date
    fields_type: Dict = {}
    # define field attr,like cols which in bootstrap table
    attrs: Dict[str, Dict] = {"created_at": {"label": "CreatedAt"}}
    # active table export
    export: bool = True
    import_: bool = False
    actions: Optional[Dict]
    bulk_actions: List[Dict] = [{"value": "delete", "text": "delete_all"}]
    custom_filters: List = []


Menu.update_forward_refs()


class Site(BaseModel):
    name: str
    logo: Optional[HttpUrl]
    login_logo: Optional[HttpUrl]
    login_footer: Optional[str]
    login_description: Optional[str]
    locale: str
    locale_switcher: bool = False
    theme_switcher: bool = False
    theme: Optional[str]
    url: Optional[HttpUrl]
    # custom css
    css: Optional[List[HttpUrl]]
    # menu define
    menus: Optional[List[Menu]]
    # custom footer with html
    footer: Optional[str]
    # custom header - require html beginning with a <div> due to being rendered in a <custom-component>
    header: Optional[str]
    page_header: Optional[str]


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
    step: str = "any"


class Resource(BaseModel):
    title: str
    pk: str
    resource_fields: Dict[str, Union[Field, Dict]]
    searchFields: Optional[Dict[str, Field]]
    bulk_actions: Optional[List[Dict]]
    export: bool
    import_: bool

    class Config:
        fields = {
            "resource_fields": "fields",
        }
