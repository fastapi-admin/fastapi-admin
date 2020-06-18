from fastapi import APIRouter, Depends
from starlette.templating import Jinja2Templates
from tortoise.contrib.pydantic import pydantic_queryset_creator

from fastapi_admin.depends import get_model
from fastapi_admin.factory import app
from fastapi_admin.schemas import BulkIn

templates = Jinja2Templates(directory="examples/templates")


@app.post("/rest/{resource}/bulk/test_bulk")
async def test_bulk(bulk_in: BulkIn, model=Depends(get_model)):
    qs = model.filter(pk__in=bulk_in.pk_list)
    pydantic = pydantic_queryset_creator(model)
    ret = await pydantic.from_queryset(qs)
    return ret.dict()


@app.get("/home",)
async def home():
    return {"html": templates.get_template("home.html").render()}


async def login():
    return {
        "user": {
            "username": "admin",
            "is_superuser": False,
            "avatar": "https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4",
        },
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.HSlcYkOEQewxyPuaqcVwCcw_wkbLB50Ws1-ZxfPoLAQ",
    }
