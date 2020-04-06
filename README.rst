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

Features
========

* Out-of-the-box admin dashboard.
* Automatic field type mapping.
* Build-in user authorization.
* Easy to extension.

Screenshots
===========

.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/login.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/list.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/view.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/create.png


Quick Start
===========

Backend
-------

example
~~~~~~~
Only you should do is runing a fastapi app and mount admin app from fastapi-admin,then call ``init()``.

.. code-block:: python

    import uvicorn
    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware
    from tortoise.contrib.fastapi import register_tortoise

    from fastapi_admin.factory import app as admin_app
    from fastapi_admin.site import Site, Menu

    TORTOISE_ORM = {
        'connections': {
            'default': 'mysql://root:123456@127.0.0.1:3306/test'
        },
        'apps': {
            'models': {
                'models': ['examples.models'],
                'default_connection': 'default',
            }
        }
    }


    def create_app():
        fast_app = FastAPI()

        register_tortoise(fast_app, config=TORTOISE_ORM)

        fast_app.mount('/admin', admin_app)

        admin_app.init(
            user_model='TestUser',
            admin_secret='test',
            models='examples.models',
            site=Site(
                name='FastAPI-Admin',
                logo='https://github.com/long2ice/fastapi-admin/raw/master/front/static/img/logo.png',
                locale='en-US',
                locale_switcher=True,
                menu=[
                    Menu(
                        name='Home',
                        url='/home',
                        icon='fa fa-home',
                    ),
                    Menu(
                        name='Information',
                        title=True,
                        icon='fa fa-user',
                    ),
                    Menu(
                        name='User',
                        url='/rest/TestUser', #important,TestUser is same of the Model class TestUser and must be /rest/<Model>.
                        icon='fa fa-user',
                    ),
                    Menu(
                        name='Logout',
                        url='/logout',
                        icon='icon-lock',
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
        uvicorn.run('main:app', port=8000, debug=True, reload=True)

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

Front
-----

Just run ``cd front && npm run serve``,more reference in `rest-admin <https://github.com/wxs77577/rest-admin>`_.

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