# FastAPI ADMIN

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/fastapi-admin/fastapi-admin)](https://github.com/fastapi-admin/fastapi-admin)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/gh-pages/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:gh-pages)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:pypi)

## 简介

`fastapi-admin` 是一个基于 [FastAPI](https://github.com/tiangolo/fastapi)
和 [TortoiseORM](https://github.com/tortoise/tortoise-orm/) 以及 [tabler](https://github.com/tabler/tabler) UI框架的后台管理面板，
灵感来自Django admin。

## 线上 DEMO

你可以在 [此处](https://fastapi-admin.long2ice.io/admin/login) 查看线上 demo。

- 用户名： `admin`
- 密码： `123456`

或者在 [此处](https://fastapi-admin-pro.long2ice.io/admin/login) 查看 Pro 版本 demo。

- 用户名： `admin`
- 密码： `123456`

## 截图

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)

## 本地运行示例

1. 克隆仓库。
2. 创建 `.env` 文件。

   ```dotenv
   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
   REDIS_URL=redis://localhost:6379/0
   ```

3. 运行 `docker-compose up -d --build`。
4. 访问 <http://localhost:8000/admin/init> 创建第一个管理员。

## 文档

文档地址 <https://fastapi-admin.github.io>。

## 许可

本项目遵循 [Apache-2.0](https://github.com/fastapi-admin/fastapi-admin/blob/master/LICENSE) 开源许可。
