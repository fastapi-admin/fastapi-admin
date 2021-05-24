import os
import typing
from datetime import date
from typing import Any, List
from urllib.parse import urlencode

from jinja2 import pass_context
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fastapi_admin import VERSION
from fastapi_admin.constants import BASE_DIR

if typing.TYPE_CHECKING:
    from fastapi_admin.resources import Field, Model

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals["VERSION"] = VERSION
templates.env.globals["NOW_YEAR"] = date.today().year
templates.env.add_extension("jinja2.ext.i18n")
templates.env.add_extension("jinja2.ext.autoescape")


@pass_context
def current_page_with_params(context: dict, params: dict):
    request = context.get("request")  # type:Request
    full_path = request.scope["raw_path"].decode()
    query_params = dict(request.query_params)
    for k, v in params.items():
        query_params[k] = v
    return full_path + "?" + urlencode(query_params)


templates.env.filters["current_page_with_params"] = current_page_with_params


def set_global_env(name: str, value: Any):
    templates.env.globals[name] = value


def add_template_folder(*folders: str):
    for folder in folders:
        templates.env.loader.searchpath.insert(0, folder)


async def render_values(
    request: Request,
    model: "Model",
    fields: List["Field"],
    values: List[typing.Dict[str, Any]],
    display: bool = True,
) -> typing.Tuple[List[List[Any]], List[dict], List[dict], List[List[dict]]]:
    """
    render values with template render
    :param fields:
    :param values:
    :param display:
    :params request:
    :params model:
    :return:
    """
    ret = []
    cell_attributes: List[List[dict]] = []
    row_attributes: List[dict] = []
    column_attributes: List[dict] = []
    for field in fields:
        column_attributes.append(await model.column_attributes(request, field))
    for value in values:
        row_attributes.append(await model.row_attributes(request, value))
        item = []
        cell_item = []
        for i, k in enumerate(value):
            cell_item.append(await model.cell_attributes(request, value, fields[i]))
            if display:
                item.append(await fields[i].display.render(request, value[k]))
            else:
                item.append(await fields[i].input.render(request, value[k]))
        for compute_field in await model.get_compute_fields(request):
            item.append(await compute_field.get_value(request, value))
            cell_item.append({})
        ret.append(item)
        cell_attributes.append(cell_item)
    return ret, row_attributes, column_attributes, cell_attributes
