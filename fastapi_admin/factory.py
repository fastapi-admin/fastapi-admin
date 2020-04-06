import importlib
from typing import Type

from fastapi import FastAPI
from tortoise import Model, Tortoise

from .site import Site, Resource, Field


class AdminApp(FastAPI):
    models: str
    admin_secret: str
    user_model: str
    site: Site
    _inited: bool = False
    _field_type_mapping = {
        'IntField': 'number',
        'BooleanField': 'checkbox',
        'DatetimeField': 'datetime',
        'IntEnumFieldInstance': 'select',
        'CharEnumFieldInstance': 'select',
        'DecimalField': 'number',
        'FloatField': 'number',
        'TextField': 'textarea',
        'SmallIntField': 'number',
        'ForeignKeyFieldInstance': 'select',
    }
    _model_menu_mapping = {}

    def _get_model_menu_mapping(self):
        for menu in filter(lambda x: x.url, self.site.menus):
            self._model_menu_mapping[menu.url.split('?')[0].split('/')[-1]] = menu

    def init(self, site: Site, user_model: str, admin_secret: str, models: str, ):
        """
        init admin site
        :param site:
        :param user_model: admin user model path,like admin.models.user
        :param admin_secret: admin jwt secret.
        :param models: tortoise models
        :return:
        """
        self.site = site
        self.admin_secret = admin_secret
        self.models = importlib.import_module(models)
        self.user_model = getattr(self.models, user_model)
        self._inited = True
        self._get_model_menu_mapping()

    def _exclude_field(self, resource: str, field: str):
        """
        exclude field by menu include and exclude
        :param resource:
        :param field:
        :return:
        """
        menu = self._model_menu_mapping[resource]
        if menu.include:
            if field not in menu.include:
                return True
        if menu.exclude:
            if field in menu.exclude:
                return True
        return False

    async def _build_resource_from_model_describe(self, resource: str, model: Type[Model], model_describe: dict,
                                                  exclude_readonly: bool):
        data_fields = model_describe.get('data_fields')
        pk_field = model_describe.get('pk_field')
        fk_fields = model_describe.get('fk_fields')
        if exclude_readonly:
            ret = {}
        else:
            ret = {
                pk_field.get('name'): Field(
                    label=pk_field.get('name').title(),
                    required=True,
                    type=self._field_type_mapping.get(pk_field.get('field_type')) or 'text',
                )
            }
        for field in data_fields:
            read_only = field.get('constraints').get('readOnly')
            field_type = field.get('field_type')
            name = field.get('name')

            if (read_only and exclude_readonly) or self._exclude_field(resource, name):
                continue

            type_ = self._field_type_mapping.get(field_type) or 'text'
            options = []
            if type_ == 'select':
                for k, v in model._meta.fields_map[name].enum_type.choices().items():
                    options.append({'text': v, 'value': k})

            ret[name] = Field(
                label=field.get('description') or field.get('name').title(),
                required=not field.get('nullable'),
                type=type_,
                options=options
            )

        menu = self._model_menu_mapping[resource]
        for fk_field in fk_fields:
            name = fk_field.get('name')
            if name not in menu.raw_id_fields:
                fk_model_class = model._meta.fields_map[name].model_class
                objs = await fk_model_class.all()
                ret[fk_field.get('raw_field')] = Field(
                    label=fk_field.get('description') or name.title(),
                    required=True,
                    type='select',
                    options=list(map(lambda x: {'text': str(x), 'value': x.pk}, objs))
                )

        return ret

    async def get_resource(self, resource: str, exclude_readonly=False, ):
        assert self._inited, 'must call init() first!'
        model = getattr(self.models, resource)  # type:Type[Model]
        model_describe = Tortoise.describe_model(model)
        return Resource(
            title=model_describe.get('description') or resource.title(),
            fields=await self._build_resource_from_model_describe(resource, model, model_describe, exclude_readonly)
        )


app = AdminApp(
    openapi_prefix='/admin',
)
