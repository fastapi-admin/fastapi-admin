from typing import Generic

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from tortoise.models import MODEL


async def get_object_or_404(model: Generic[MODEL], **kwargs):
    """
    get_object_or_404
    :param model:
    :param kwargs:
    :return:
    """
    obj = await model.filter(**kwargs).first()  # type:model
    if not obj:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not Found")
    return obj
