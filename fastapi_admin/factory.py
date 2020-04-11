import importlib
from typing import Type, List, Dict

from fastapi import FastAPI
from tortoise import Model, Tortoise

from .site import Site, Resource, Field, Menu


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
        'DateField': 'date',
        'IntEnumFieldInstance': 'select',
        'CharEnumFieldInstance': 'select',
        'DecimalField': 'number',
        'FloatField': 'number',
        'TextField': 'textarea',
        'SmallIntField': 'number',
        'JSONField': 'json',
    }
    model_menu_mapping: Dict[str, Menu] = {}

    def _get_model_menu_mapping(self):
        for menu in filter(lambda x: x.url, self.site.menus):
            self.model_menu_mapping[menu.url.split('?')[0].split('/')[-1]] = menu

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
        menu = self.model_menu_mapping[resource]
        if menu.include:
            if field not in menu.include:
                return True
        if menu.exclude:
            if field in menu.exclude:
                return True
        return False

    def _get_field_type(self, menu: Menu, name: str, field_type: str) -> str:
        """
        get field display type
        :param menu:
        :param field_type:
        :return:
        """
        field_type = menu.fields_type.get(name) or self._field_type_mapping.get(field_type) or 'text'
        return field_type

    async def _build_resource_from_model_describe(self, resource: str, model: Type[Model], model_describe: dict,
                                                  exclude_pk: bool, exclude_m2m_field=True, exclude_actions=False):
        """
        build resource
        :param resource:
        :param model:
        :param model_describe:
        :param exclude_pk:
        :param exclude_m2m_field:
        :return:
        """
        data_fields = model_describe.get('data_fields')
        pk_field = model_describe.get('pk_field')
        fk_fields = model_describe.get('fk_fields')
        m2m_fields = model_describe.get('m2m_fields')
        menu = self.model_menu_mapping[resource]
        search_fields_ret = {}
        search_fields = menu.search_fields
        sort_fields = menu.sort_fields
        fields = {}
        pk = name = pk_field.get('name')
        if not exclude_pk and not self._exclude_field(resource, name):
            fields = {
                name: Field(
                    label=pk_field.get('name').title(),
                    required=True,
                    type=self._get_field_type(menu, name, pk_field.get('field_type')),
                    sortable=name in sort_fields
                )
            }
        if not exclude_actions:
            fields['_actions'] = menu.actions

        for data_field in data_fields:
            readonly = data_field.get('constraints').get('readOnly')
            field_type = data_field.get('field_type')
            name = data_field.get('name')
            if self._exclude_field(resource, name):
                continue

            type_ = self._get_field_type(menu, name, field_type)
            options = []
            if type_ == 'select':
                for k, v in model._meta.fields_map[name].enum_type.choices().items():
                    options.append({'text': v, 'value': k})

            label = data_field.get('description') or data_field.get('name').title()
            field = Field(
                label=label,
                required=not data_field.get('nullable'),
                type=type_,
                options=options,
                sortable=name in sort_fields,
                disabled=readonly
            )
            fields[name] = field
            if name in search_fields:
                search_fields_ret[name] = field

        for fk_field in fk_fields:
            name = fk_field.get('name')
            if not self._exclude_field(resource, name):
                if name not in menu.raw_id_fields:
                    fk_model_class = model._meta.fields_map[name].model_class
                    objs = await fk_model_class.all()
                    raw_field = fk_field.get('raw_field')
                    label = fk_field.get('description') or name.title()
                    options = list(map(lambda x: {'text': str(x), 'value': x.pk}, objs))
                    field = Field(
                        label=label,
                        required=True,
                        type='select',
                        options=options,
                        sortable=name in sort_fields
                    )
                    fields[raw_field] = field
                    if name in search_fields:
                        search_fields_ret[raw_field] = field
        if not exclude_m2m_field:
            for m2m_field in m2m_fields:
                name = m2m_field.get('name')
                if not self._exclude_field(resource, name):
                    label = m2m_field.get('description') or name.title()
                    m2m_model_class = model._meta.fields_map[name].model_class
                    objs = await m2m_model_class.all()
                    options = list(map(lambda x: {'text': str(x), 'value': x.pk}, objs))
                    fields[name] = Field(
                        label=label,
                        type='tree',
                        options=options,
                        multiple=True,
                    )
        return pk, fields, search_fields_ret

    async def get_resource(self, resource: str, exclude_pk=False, exclude_m2m_field=True, exclude_actions=False):
        assert self._inited, 'must call init() first!'
        model = getattr(self.models, resource)  # type:Type[Model]
        model_describe = Tortoise.describe_model(model)
        pk, fields, search_fields = await self._build_resource_from_model_describe(resource, model, model_describe,
                                                                                   exclude_pk, exclude_m2m_field,
                                                                                   exclude_actions)
        return Resource(
            title=model_describe.get('description') or resource.title(),
            fields=fields,
            searchFields=search_fields,
            pk=pk,
            bulk_actions=self.model_menu_mapping[resource].bulk_actions,
        )


app = AdminApp(
    openapi_prefix='/admin',
)
