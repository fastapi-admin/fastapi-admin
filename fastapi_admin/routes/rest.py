import io
from typing import Type

import xlsxwriter
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.status import HTTP_409_CONFLICT
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError
from tortoise.fields import ManyToManyRelation

from .. import enums
from ..common import handle_m2m_fields_create_or_update
from ..depends import (
    QueryItem,
    admin_log_create,
    admin_log_delete,
    admin_log_update,
    create_checker,
    delete_checker,
    get_current_user,
    get_model,
    get_query,
    has_resource_permission,
    parse_body,
    read_checker,
    update_checker,
)
from ..factory import app
from ..filters import get_filter_by_name
from ..responses import GetManyOut
from ..schemas import BulkIn
from ..shortcuts import get_object_or_404

router = APIRouter()


@router.get("/{resource}/export")
async def export(resource: str, query: QueryItem = Depends(get_query), model=Depends(get_model)):
    qs = model.all()
    if query.where:
        qs = qs.filter(**query.where)
    resource = await app.get_resource(resource)
    result = await qs
    creator = pydantic_model_creator(
        model, include=resource.resource_fields.keys(), exclude=model._meta.m2m_fields
    )
    data = map(lambda x: creator.from_orm(x).dict(), result)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    for row, item in enumerate(data):
        col = 0
        for k, v in item.items():
            if row == 0:
                worksheet.write(row, col, k)
            worksheet.write(row + 1, col, v)
            col += 1

    workbook.close()
    output.seek(0)

    return StreamingResponse(output)


@router.post("/{resource}/import")
async def import_data(request: Request, model: Type[Model] = Depends(get_model)):
    items = await request.json()
    objs = []
    for item in items:
        obj = model(**item)
        objs.append(obj)
    try:
        await model.bulk_create(objs)
        return {"success": True, "data": len(objs)}
    except IntegrityError as e:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content=dict(msg=f"Import Error,{e}"))


@router.get("/{resource}", dependencies=[Depends(read_checker)])
async def get_resource(
    resource: str, query: QueryItem = Depends(get_query), model=Depends(get_model)
):
    menu = app.model_menu_mapping[resource]
    qs = model.all()
    for filter_ in menu.custom_filters:
        qs = filter_.get_queryset(qs)
    if query.where:
        for name, value in query.where.items():
            filter_cls = get_filter_by_name(name)
            if filter_cls:
                qs = filter_cls.get_queryset(qs, value)
            else:
                qs = qs.filter(**{name: value})
    sort = query.sort
    for k, v in sort.items():
        if k in menu.sort_fields:
            if v == -1:
                qs = qs.order_by(f"-{k}")
            elif v == 1:
                qs = qs.order_by(k)
    resource = await app.get_resource(resource)
    result = await qs.limit(query.size).offset((query.page - 1) * query.size)
    creator = pydantic_model_creator(
        model, include=resource.resource_fields.keys(), exclude=model._meta.m2m_fields
    )
    data = []
    for item in result:
        item_dict = creator.from_orm(item).dict()
        item_dict["_rowVariant"] = item_dict.pop("rowVariant", None)
        item_dict["_cellVariants"] = item_dict.pop("cellVariants", None)
        data.append(item_dict)
    return GetManyOut(total=await qs.count(), data=data)


@router.get("/{resource}/form", dependencies=[Depends(read_checker)])
async def form(resource: str,):
    resource = await app.get_resource(
        resource, exclude_pk=True, exclude_m2m_field=False, exclude_actions=True
    )
    return resource.dict(by_alias=True, exclude_unset=True)


@router.get("/{resource}/grid", dependencies=[Depends(read_checker)])
async def grid(resource: str, user=Depends(get_current_user)):
    fetched_resource = await app.get_resource(resource)
    resource_response = fetched_resource.dict(by_alias=True, exclude_unset=True)
    resource_response["fields"]["_actions"] = {
        "delete": await has_resource_permission(enums.PermissionAction.delete, resource, user),
        "edit": await has_resource_permission(enums.PermissionAction.update, resource, user),
        "toolbar": {
            "create": await has_resource_permission(enums.PermissionAction.create, resource, user)
        },
    }
    return resource_response


@router.get("/{resource}/view", dependencies=[Depends(read_checker)])
async def view(resource: str,):
    resource = await app.get_resource(resource)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.post(
    "/{resource}/bulk/delete", dependencies=[Depends(delete_checker), Depends(admin_log_delete)]
)
async def bulk_delete(bulk_in: BulkIn, model=Depends(get_model)):
    await model.filter(pk__in=bulk_in.pk_list).delete()
    return {"success": True}


@router.delete(
    "/{resource}/{id}", dependencies=[Depends(delete_checker), Depends(admin_log_delete)]
)
async def delete_one(id: int, model=Depends(get_model)):
    await model.filter(pk=id).delete()
    return {"success": True}


@router.put("/{resource}/{id}", dependencies=[Depends(update_checker), Depends(admin_log_update)])
async def update_one(id: int, parsed=Depends(parse_body), model=Depends(get_model)):
    body, resource_fields = parsed
    m2m_fields = model._meta.m2m_fields
    try:
        obj = await handle_m2m_fields_create_or_update(
            body, m2m_fields, model, app.user_model, False, id
        )
    except IntegrityError as e:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content=dict(msg=f"Update Error,{e}"))
    creator = pydantic_model_creator(model, include=resource_fields, exclude=m2m_fields)
    return creator.from_orm(obj).dict()


@router.post("/{resource}", dependencies=[Depends(create_checker), Depends(admin_log_create)])
async def create_one(parsed=Depends(parse_body), model=Depends(get_model)):
    body, resource_fields = parsed
    m2m_fields = model._meta.m2m_fields
    creator = pydantic_model_creator(model, include=resource_fields, exclude=m2m_fields)
    try:
        obj = await handle_m2m_fields_create_or_update(body, m2m_fields, model, app.user_model)
    except IntegrityError as e:
        return JSONResponse(status_code=HTTP_409_CONFLICT, content=dict(msg=f"Create Error,{e}"))
    return creator.from_orm(obj).dict()


@router.get("/{resource}/{id}", dependencies=[Depends(read_checker)])
async def get_one(id: int, resource: str, model=Depends(get_model)):
    obj = await get_object_or_404(model, pk=id)  # type:Model
    m2m_fields = model._meta.m2m_fields
    resource = await app.get_resource(resource, exclude_m2m_field=False)
    include = resource.resource_fields.keys()
    creator = pydantic_model_creator(model, include=include, exclude=m2m_fields)
    ret = creator.from_orm(obj).dict()
    for m2m_field in m2m_fields:
        if m2m_field in include:
            relate_model = getattr(obj, m2m_field)  # type:ManyToManyRelation
            ids = await relate_model.all().values_list(relate_model.remote_model._meta.pk_attr)
            ret[m2m_field] = list(map(lambda x: x[0], ids))
    ret["__str__"] = str(obj)
    return ret
