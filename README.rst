=============
FastAPI Admin
=============

.. image:: https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat
   :target: https://pypi.python.org/pypi/fastapi-admin
.. image:: https://img.shields.io/github/license/long2ice/fastapi-admin
   :target: https://github.com/long2ice/fastapi-admin

Introduction
============

FastAPI-admin is a admin dashboard based on `fastapi <https://github.com/tiangolo/fastapi>`_ and `tortoise-orm <https://github.com/tortoise/tortoise-orm>`_ and `rest-admin <https://github.com/wxs77577/rest-admin>`_.

FastAPI-admin provide crud feature out-of-the-box with just a few config.


Screenshots
===========

.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/login.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/list.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/view.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/create.png


Quick Start
===========

Example
~~~~~~~
Look at `examples <https://github.com/long2ice/fastapi-admin/tree/master/examples>`_.

1. ``git clone https://github.com/long2ice/fastapi-admin.git``.
2. create database ``fastapi-admin`` and import from ``examples/example.sql``.
3. ``pip install -r requirements.txt``.
4. ``cd examples && python3 main.py``,then you can see:

.. code-block:: python

    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [89005]
    INFO:     Started server process [89009]
    INFO:     Waiting for application startup.
    INFO:     Tortoise-ORM startup
        connections: {'default': 'mysql://root:123456@127.0.0.1:3306/fastapi-admin'}
        apps: {'models': {'models': ['examples.models'], 'default_connection': 'default'}}
    INFO:     Tortoise-ORM started, {'default': <tortoise.backends.mysql.client.MySQLClient object at 0x110ed6760>}, {'models': {'Category': <class 'examples.models.Category'>, 'Product': <class 'examples.models.Product'>, 'User': <class 'examples.models.User'>}}
    INFO:     Tortoise-ORM generating schema
    INFO:     Application startup complete.

That's all,enjoy it!

Backend
~~~~~~~
Only you should do is runing a fastapi app and mount admin app from fastapi-admin,then call ``init()``.

.. code-block:: python

    import uvicorn
    from fastapi import FastAPI, Depends
    from starlette.middleware.cors import CORSMiddleware
    from tortoise.contrib.fastapi import register_tortoise
    from tortoise.contrib.pydantic import pydantic_queryset_creator
    from fastapi_admin.depends import get_model
    from fastapi_admin.factory import app as admin_app
    from fastapi_admin.schemas import BulkIn
    from fastapi_admin.site import Site, Menu

    TORTOISE_ORM = {
        'connections': {
            'default': 'mysql://root:123456@127.0.0.1:3306/fastapi-admin'
        },
        'apps': {
            'models': {
                'models': ['examples.models'],
                'default_connection': 'default',
            }
        }
    }


    @admin_app.post(
        '/{resource}/bulk/test_bulk'
    )
    async def test_bulk(
            bulk_in: BulkIn,
            model=Depends(get_model)
    ):
        qs = model.filter(pk__in=bulk_in.pk_list)
        pydantic = pydantic_queryset_creator(model)
        ret = await pydantic.from_queryset(qs)
        return ret.dict()


    def create_app():
        fast_app = FastAPI(debug=True)

        register_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)
        fast_app.mount('/admin', admin_app)

        admin_app.init(
            user_model='User',
            admin_secret='test',
            models='examples.models',
            site=Site(
                name='FastAPI-admin Demo',
                logo='https://github.com/long2ice/fastapi-admin/raw/master/front/static/img/logo.png',
                locale='en-US',
                locale_switcher=True,
                menu=[
                    Menu(
                        name='Home',
                        url='/',
                        icon='fa fa-home'
                    ),
                    Menu(
                        name='Content',
                        title=True
                    ),
                    Menu(
                        name='Product',
                        url='/rest/Product',
                        icon='icon-list',
                        search_fields=('type',),
                        fields_type={
                            'type': 'radiolist'
                        },
                        bulk_actions=[
                            {
                                'value': 'delete',
                                'text': 'delete_all',
                            }
                            , {
                                'value': 'test_bulk',
                                'text': 'TestBulk'
                            }
                        ]
                    ),
                    Menu(
                        name='Category',
                        url='/rest/Category',
                        icon='icon-list'
                    ),
                    Menu(
                        name='External',
                        title=True
                    ),
                    Menu(
                        name='Github',
                        url='https://github.com/long2ice/fastapi-admin',
                        icon='fa fa-github',
                        external=True
                    ),
                    Menu(
                        name='Auth',
                        title=True
                    ),
                    Menu(
                        name='User',
                        url='/rest/User',
                        icon='fa fa-user',
                        fields_type={
                            'avatar': 'image'
                        },
                        exclude=('password',),
                        search_fields=('username',)
                    ),
                    Menu(
                        name='Logout',
                        url='/logout',
                        icon='fa fa-lock'
                    )
                ]
            )
        )

        fast_app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        return fast_app


    app = create_app()

    if __name__ == '__main__':
        uvicorn.run('main:app', port=8000, debug=True, reload=True, lifespan='on')

Front
~~~~~
``cp .env.development.local.example .env`` and modify,then just run ``cd front && npm run serve``,more reference in `rest-admin <https://github.com/wxs77577/rest-admin>`_.

Features
========

Enum Support
~~~~~~~~~~~~
When you define a enum field of tortoise-orm,like ``IntEnumField``,you can inherit ``fastapi_admin.enum.EnumMixin`` and impl ``choices()`` method,
FastAPI-admin will auto read and display and render a ``select`` widget in front.

.. code-block:: python

    class Status(EnumMixin, IntEnum):
        on = 1
        off = 2

        @classmethod
        def choices(cls):
            return {
                cls.on: 'ON',
                cls.off: 'OFF'
            }

Admin User Model
~~~~~~~~~~~~~~~~
Inherit ``fastapi_admin.models.User`` and add you own fields,then pass in ``init()``.

.. code-block:: python

    class AdminUser(User):
        is_active = fields.BooleanField(default=False, description='Is Active')
        status = fields.IntEnumField(Status, description='User Status')
        created_at = fields.DatetimeField(auto_now_add=True)
        updated_at = fields.DatetimeField(auto_now=True)


Verbose Name
~~~~~~~~~~~~
FastAPI-admin will auto read ``description`` defined in tortoise-orm model ``Field`` and display in front.

ForeignKeyField Support
~~~~~~~~~~~~~~~~~~~~~~~
If ``ForeignKeyField`` not passed in ``menu.raw_id_fields``,FastAPI-admin will get all related objects and display ``select`` in front with ``Model.__str__``.

ManyToManyField Support
~~~~~~~~~~~~~~~~~~~~~~~
FastAPI-admin will render ``ManyToManyField`` with multiple ``select`` in ``form`` edit with ``Model.__str__``.

JSONField Render
~~~~~~~~~~~~~~~~
FastAPI-admin will render ``JSONField`` with ``jsoneditor`` as beauty interface.

Search Fields
~~~~~~~~~~~~~
Defined ``menu.search_fields`` in ``menu`` will render a search form by fields.

Xlsx Export
~~~~~~~~~~~
FastAPI-admin can export searched data to excel file when define ``{export : True}`` in ``menu.actions``.

Bulk Actions
~~~~~~~~~~~~
Current FastAPI-admin support builtin bulk action ``delete_all``,if you want write your own bulk actions:

1. pass ``bulk_actions`` in ``Menu``,example:

.. code-block:: python

    Menu(
        ...
        bulk_actions=[{
            'value': 'delete', # this is fastapi router path param.
            'text': 'delete_all', # this will show in front.
        }]
    )

2. write fastapi route,example:

.. code-block:: python

    from fastapi_admin.schemas import BulkIn
    from fastapi_admin.factory import app as admin_app

    @admin_app.post(
        '/{resource}/bulk/delete' # delete is defined before.
    )
    async def bulk_delete(
            bulk_in: BulkIn,
            model=Depends(get_model)
    ):
        await model.filter(pk__in=bulk_in.pk_list).delete()
        return {'success': True}

Deployment
==========
1. Deploy fastapi app by gunicorn+uvicorn or reference https://fastapi.tiangolo.com/deployment/.
2. Run ``npm run build`` in ``front`` dir,then copy static files in ``dists`` to you server,deployment by ``nginx``.

.. note::
   Maybe you should config ``VUE_APP_API_URL``, ``BASE_URL`` environment .etc in ``.env`` of ``front`` dir,just reference docs of `rest-admin <https://github.com/wxs77577/rest-admin>`_.

ThanksTo
========

* `fastapi <https://github.com/tiangolo/fastapi>`_ ,high performance async api framework.
* `tortoise-orm <https://github.com/tortoise/tortoise-orm>`_ ,familiar asyncio ORM for python.
* `rest-admin <https://github.com/wxs77577/rest-admin>`_,restful Admin Dashboard Based on Vue and Boostrap 4.