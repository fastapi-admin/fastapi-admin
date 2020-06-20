import importlib
from copy import deepcopy

from passlib.context import CryptContext

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
    if model == user_model:
        copy_body["password"] = pwd_context.hash(copy_body.pop("password"))
    m2m_body = {}
    for k, v in body.items():
        if k in m2m_fields:
            m2m_body[k] = copy_body.pop(k)
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
