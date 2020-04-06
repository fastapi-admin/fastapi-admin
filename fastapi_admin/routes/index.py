from fastapi import Depends, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_409_CONFLICT
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError

from ..depends import QueryItem, get_query, get_body, get_model
from ..factory import app
from ..responses import GetManyOut
from ..shortcuts import get_object_or_404

router = APIRouter()


@router.get(
    '/{resource}'
)
async def get_resource(
        resource: str,
        query: QueryItem = Depends(get_query),
        model=Depends(get_model)
):
    qs = model.all()
    if query.where:
        qs = qs.filter(**query.where)
    result = await qs.limit(query.size).offset((query.page - 1) * query.size)
    resource = await app.get_resource(resource)
    creator = pydantic_model_creator(model, include=resource.resource_fields.keys())
    return GetManyOut(
        total=await qs.count(),
        data=list(map(lambda x: creator.from_orm(x).dict(), result))
    )


@router.get(
    '/{resource}/form'
)
async def form(
        resource: str,
):
    resource = await app.get_resource(resource, exclude_readonly=True)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.get(
    '/{resource}/grid'
)
async def grid(
        resource: str,
):
    resource = await app.get_resource(resource)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.get(
    '/{resource}/view'
)
async def view(
        resource: str,
):
    resource = await app.get_resource(resource)
    return resource.dict(by_alias=True, exclude_unset=True)


@router.delete(
    '/{resource}/{id}'
)
async def delete_one(
        id: int,
        model=Depends(get_model)
):
    await model.filter(pk=id).delete()
    return {'success': True}


@router.put(
    '/{resource}/{id}'
)
async def update_one(
        resource: str,
        id: int,
        body=Depends(get_body),
        model=Depends(get_model)
):
    try:
        await model.filter(pk=id).update(**body)
    except IntegrityError as e:
        return ORJSONResponse(status_code=HTTP_409_CONFLICT, content=dict(
            message=f'Update Error,{e}'
        ))
    user_ = await get_object_or_404(model, pk=id)
    resource = await app.get_resource(resource, exclude_readonly=True)
    creator = pydantic_model_creator(model, include=resource.resource_fields.keys())
    return creator.from_orm(user_).dict()


@router.post(
    '/{resource}'
)
async def create_one(
        resource: str,
        body=Depends(get_body),
        model=Depends(get_model)
):
    resource = await app.get_resource(resource)
    creator = pydantic_model_creator(model, include=resource.resource_fields.keys())
    try:
        obj = await model.create(**body)
    except IntegrityError as e:
        return ORJSONResponse(status_code=HTTP_409_CONFLICT, content=dict(
            message=f'Create Error,{e}'
        ))
    return creator.from_orm(obj).dict()


@router.get(
    '/{resource}/{id}'
)
async def get_one(
        id: int,
        resource: str,
        model=Depends(get_model)
):
    obj = await get_object_or_404(model, pk=id)
    resource = await app.get_resource(resource)
    include = resource.resource_fields.keys()
    creator = pydantic_model_creator(model, include=include)
    return creator.from_orm(obj).dict()
