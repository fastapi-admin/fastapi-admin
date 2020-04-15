from fastapi import Depends, APIRouter
from fastapi.responses import UJSONResponse
from starlette.status import HTTP_409_CONFLICT
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError
from tortoise.fields import ManyToManyRelation

from ..common import handle_m2m_fields_create_or_update
from ..depends import QueryItem, get_query, parse_body, get_model, read_checker, delete_checker, update_checker, \
    create_checker
from ..factory import app
from ..responses import GetManyOut
from ..schemas import BulkIn
from ..shortcuts import get_object_or_404

router = APIRouter()


@router.get(
    '/{resource}',
    dependencies=[Depends(read_checker)]
)
async def get_resource(
        resource: str,
        query: QueryItem = Depends(get_query),
        model=Depends(get_model)
):
    menu = app.model_menu_mapping[resource]
    qs = model.all()
    if query.where:
        qs = qs.filter(**query.where)
    sort = query.sort
    for k, v in sort.items():
        if k in menu.sort_fields:
            if v == -1:
                qs = qs.order_by(f'-{k}')
            elif v == 1:
                qs = qs.order_by(k)
    resource = await app.get_resource(resource)
    result = await qs.limit(query.size).offset((query.page - 1) * query.size)
    creator = pydantic_model_creator(model, include=resource.resource_fields.keys(), exclude=model._meta.m2m_fields)
    return GetManyOut(
        total=await qs.count(),
        data=list(map(lambda x: creator.from_orm(x).dict(), result))
    )


@router.get(
    '/{resource}/form',
    dependencies=[Depends(read_checker)]
)
async def form(
        resource: str,
):
    resource = await app.get_resource(resource, exclude_pk=True, exclude_m2m_field=False, exclude_actions=True)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.get(
    '/{resource}/grid',
    dependencies=[Depends(read_checker)]
)
async def grid(
        resource: str,
):
    resource = await app.get_resource(resource)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.get(
    '/{resource}/view',
    dependencies=[Depends(read_checker)]
)
async def view(
        resource: str,
):
    resource = await app.get_resource(resource)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.post(
    '/{resource}/bulk/delete',
    dependencies=[Depends(delete_checker)]
)
async def bulk_delete(
        bulk_in: BulkIn,
        model=Depends(get_model)
):
    await model.filter(pk__in=bulk_in.pk_list).delete()
    return {'success': True}


@router.delete(
    '/{resource}/{id}',
    dependencies=[Depends(delete_checker)]
)
async def delete_one(
        id: int,
        model=Depends(get_model)
):
    await model.filter(pk=id).delete()
    return {'success': True}


@router.put(
    '/{resource}/{id}',
    dependencies=[Depends(update_checker)]
)
async def update_one(
        id: int,
        parsed=Depends(parse_body),
        model=Depends(get_model)
):
    body, resource_fields = parsed
    m2m_fields = model._meta.m2m_fields
    try:
        obj = await handle_m2m_fields_create_or_update(body, m2m_fields, model, False, id)
    except IntegrityError as e:
        return UJSONResponse(status_code=HTTP_409_CONFLICT, content=dict(
            message=f'Update Error,{e}'
        ))
    creator = pydantic_model_creator(model, include=resource_fields, exclude=m2m_fields)
    return creator.from_orm(obj).dict()


@router.post(
    '/{resource}',
    dependencies=[Depends(create_checker)]
)
async def create_one(
        parsed=Depends(parse_body),
        model=Depends(get_model)
):
    body, resource_fields = parsed
    m2m_fields = model._meta.m2m_fields
    creator = pydantic_model_creator(model, include=resource_fields, exclude=m2m_fields)
    try:
        obj = await handle_m2m_fields_create_or_update(body, m2m_fields, model)
    except IntegrityError as e:
        return UJSONResponse(status_code=HTTP_409_CONFLICT, content=dict(
            message=f'Create Error,{e}'
        ))
    return creator.from_orm(obj).dict()


@router.get(
    '/{resource}/{id}',
    dependencies=[Depends(read_checker)]
)
async def get_one(
        id: int,
        resource: str,
        model=Depends(get_model)
):
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
    ret['__str__'] = str(obj)
    return ret
