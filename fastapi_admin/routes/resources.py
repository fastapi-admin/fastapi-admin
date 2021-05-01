from typing import Optional

from fastapi import APIRouter, Depends, Path
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from tortoise import Model

from fastapi_admin.depends import get_model, get_model_resource, get_resources
from fastapi_admin.resources import Model as ModelResource
from fastapi_admin.responses import redirect
from fastapi_admin.template import render_values, templates

router = APIRouter()


@router.get("/{resource}/list")
async def list_view(
    request: Request,
    model: Model = Depends(get_model),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    resource: str = Path(...),
    page_size: int = 10,
    page_num: int = 1,
):
    fields_name = model_resource.get_fields_name()
    fields_label = model_resource.get_fields_label()
    fields = model_resource.get_fields()
    params = await model_resource.resolve_query_params(dict(request.query_params))
    filters = await model_resource.get_filters(params)
    qs = model.filter(**params)
    total = await qs.count()
    if page_size:
        qs = qs.limit(page_size)
    else:
        page_size = model_resource.page_size
    qs = qs.offset((page_num - 1) * page_size)
    values = await qs.values_list(*fields_name)
    values = await render_values(fields, values)
    return templates.TemplateResponse(
        "list.html",
        context={
            "request": request,
            "resources": resources,
            "fields_label": fields_label,
            "fields": fields,
            "values": values,
            "filters": filters,
            "resource": resource,
            "model_resource": model_resource,
            "resource_label": model_resource.label,
            "page_size": page_size,
            "page_num": page_num,
            "total": total,
            "from": page_size * (page_num - 1) + 1,
            "to": page_size * page_num,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        },
    )


@router.post("/{resource}/update/{pk}")
async def update(
    request: Request,
    resource: str = Path(...),
    pk: int = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model=Depends(get_model),
):
    form = await request.form()
    data = await model_resource.resolve_data(dict(form))
    obj = await model.get(pk=pk)
    await obj.update_from_dict(data).save()
    inputs = await model_resource.get_inputs(obj)
    if "save" in form.keys():
        return templates.TemplateResponse(
            "update.html",
            context={
                "request": request,
                "resources": resources,
                "resource_label": model_resource.label,
                "resource": resource,
                "model_resource": model_resource,
                "inputs": inputs,
                "pk": pk,
                "page_title": model_resource.page_title,
                "page_pre_title": model_resource.page_pre_title,
            },
        )
    return redirect(request, "list_view", resource=resource)


@router.get("/{resource}/update/{pk}")
async def update_view(
    request: Request,
    resource: str = Path(...),
    pk: int = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model=Depends(get_model),
):
    obj = await model.get(pk=pk)
    inputs = await model_resource.get_inputs(obj)
    return templates.TemplateResponse(
        "update.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": model_resource.label,
            "resource": resource,
            "inputs": inputs,
            "pk": pk,
            "model_resource": model_resource,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        },
    )


@router.get("/{resource}/create")
async def create_view(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
):
    inputs = await model_resource.get_inputs()
    return templates.TemplateResponse(
        "create.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": model_resource.label,
            "resource": resource,
            "inputs": inputs,
            "model_resource": model_resource,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        },
    )


@router.post("/{resource}/create")
async def create(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    model=Depends(get_model),
):
    inputs = await model_resource.get_inputs()
    form = await request.form()
    data = await model_resource.resolve_data(dict(form))
    await model.create(**data)
    if "save" in form.keys():
        return redirect(request, "list_view", resource=resource)
    return templates.TemplateResponse(
        "create.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": model_resource.label,
            "resource": resource,
            "inputs": inputs,
            "model_resource": model_resource,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        },
    )


@router.delete("/{resource}/delete/{pk}")
async def delete(request: Request, pk: int, model: Model = Depends(get_model)):
    await model.filter(pk=pk).delete()
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)


@router.delete("/{resource}/bulk_actions/delete")
async def bulk_delete(request: Request, ids: str, model: Model = Depends(get_model)):
    await model.filter(pk__in=ids.split(",")).delete()
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)
