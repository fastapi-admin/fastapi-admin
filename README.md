# FastAPI Admin

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/fastapi-admin/fastapi-admin)](https://github.com/fastapi-admin/fastapi-admin)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/gh-pages/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:gh-pages)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:pypi)

## Introduction

`fastapi-admin` is a fast admin dashboard based on [FastAPI](https://github.com/tiangolo/fastapi)
and [TortoiseORM](https://github.com/tortoise/tortoise-orm/) with [tabler](https://github.com/tabler/tabler) ui,
inspired by Django admin.

Looking for old version? See branch [v1](https://github.com/fastapi-admin/fastapi-admin/tree/v1).

## Installation

```shell
> pip install fastapi-admin
```

## Requirements

- [Redis](https://redis.io)

## Online Demo

You can check a online demo [here](https://fastapi-admin.long2ice.cn/admin/login).

- username: `admin`
- password: `123456`

Or pro version online demo [here](https://fastapi-admin-pro.long2ice.cn/admin/login).

- username: `admin`
- password: `123456`

## Screenshots

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)

## Run examples in local

1. Clone repo.
2. Create `.env` file.

   ```dotenv
   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=
   REDIS_DB=0
   ```

3. Run `docker-compose up -d --build`.
4. Visit <http://localhost:8000/admin/init> to create first admin.

## Documentation

See documentation at <https://fastapi-admin-docs.long2ice.cn>.

## License

This project is licensed under the
[Apache-2.0](https://github.com/fastapi-admin/fastapi-admin/blob/master/LICENSE)
License.
