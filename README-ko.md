# FastAPI Admin 

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/fastapi-admin/fastapi-admin)](https://github.com/fastapi-admin/fastapi-admin)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/deploy/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:deploy)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:pypi)

[中文文档](./README-zh.md)
[한국어 문서](./README-ko.md)

## 개요

`fastapi-admin`은 Django admin에 영감을 받아 만든 [FastAPI](https://github.com/tiangolo/fastapi)와 [TortoiseORM](https://github.com/tortoise/tortoise-orm/) 그리고 [tabler](https://github.com/tabler/tabler) UI를 바탕으로 한 빠른 관리자 대시보드입니다.

## 설치

```shell
> pip install fastapi-admin
```

## 요구 사항

- [Redis](https://redis.io)

## 온라인 예시

[이곳](https://fastapi-admin.long2ice.io/admin/login)에서 온라인 예시를 볼 수 있습니다.

- username(유저이름): `admin`
- password(비밀번호): `123456`

또는 [이곳](https://fastapi-admin-pro.long2ice.io/admin/login)에서 프로 버전 예시를 볼 수 있습니다.

- username(유저이름): `admin`
- password(비밀번호): `123456`

## 스크린샷

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)

## 로컬 환경에서 예시 돌려보기

1. 레포지토리를 클론합니다.
2. `.env`파일을 만듭니다.

   ```dotenv
   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
   REDIS_URL=redis://localhost:6379/0
   ```

3. `docker-compose up -d --build`를 실행합니다.
4. <http://localhost:8000/admin/init>에 방문해 첫번째 관리자를 만듭니다.

## 문서

여기 <https://fastapi-admin-docs.long2ice.io> 문서를 확인하세요.

## 라이센스

이 프로젝트는 [Apache-2.0](https://github.com/fastapi-admin/fastapi-admin/blob/master/LICENSE)라이센스를 바탕으로 합니다.
