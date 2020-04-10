import io

import xlsxwriter
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse, FileResponse
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi_admin.depends import QueryItem, get_model, get_query
from fastapi_admin.factory import app

router = APIRouter()


@router.get(
    '/{resource}/export'
)
async def export(
        resource: str,
        query: QueryItem = Depends(get_query),
        model=Depends(get_model)
):
    qs = model.all()
    if query.where:
        qs = qs.filter(**query.where)
    resource = await app.get_resource(resource)
    result = await qs
    creator = pydantic_model_creator(model, include=resource.resource_fields.keys(), exclude=model._meta.m2m_fields)
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
