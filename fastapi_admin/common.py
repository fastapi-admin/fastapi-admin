import importlib
from copy import deepcopy

from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise import Tortoise

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def handle_m2m_fields_create_or_update(
    body, m2m_fields, model, user_model, create=True, pk=None
):
    """
    handle m2m update or create
    :param user_model:
    :param body:
    :param m2m_fields:
    :param model:
    :param create:
    :param pk:
    :return:
    """
    copy_body = deepcopy(body)
    m2m_body = {}
    for k, v in body.items():
        if k in m2m_fields:
            m2m_body[k] = copy_body.pop(k)
    if model == user_model:
        password = copy_body.get("password")
        if not create:
            user = await user_model.get(pk=pk)
            if user.password != password:
                copy_body["password"] = pwd_context.hash(password)
        else:
            copy_body["password"] = pwd_context.hash(password)
    if create:
        obj = await model.create(**copy_body)
    else:
        await model.filter(pk=pk).update(**copy_body)
        obj = await model.get(pk=pk)
    for k, v in m2m_body.items():
        m2m_related = getattr(obj, k)
        if not create:
            await m2m_related.clear()
        m2m_model = m2m_related.remote_model
        m2m_objs = await m2m_model.filter(pk__in=v)
        await m2m_related.add(*m2m_objs)
    return obj


def import_obj(path: str):
    """
    import obj from module path
    :param path:
    :return:
    """
    splits = path.split(".")
    module = ".".join(splits[:-1])
    class_name = splits[-1]
    return getattr(importlib.import_module(module), class_name)


def get_all_models():
    """
    get all tortoise models
    :return:
    """
    for tortoise_app, models in Tortoise.apps.items():
        for model_item in models.items():
            yield model_item


async def check_has_permission(user, model: str):
    """
    check user has permission for model
    :param user:
    :param model:
    :return:
    """
    has_permission = False
    for role in user.roles:
        permission = await role.permissions.filter(model=model).exists()
        if permission:
            has_permission = True
            break
    return has_permission
