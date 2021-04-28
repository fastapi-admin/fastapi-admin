# 安装

## 从 pypi

You can install from pypi.

```shell
> pip install fastapi-admin
```

## 从源码

Or you can install from source with latest code.

```shell
> pip install git+https://github.com/fastapi-admin/fastapi-admin.git
```

### 使用 requirements.txt

Add the following line.

```
-e https://github.com/fastapi-admin/fastapi-admin.git@develop#egg=fastapi-admin
```

### 使用 poetry

Add the following line in section `[tool.poetry.dependencies]`.

```toml
fastapi-admin = { git = 'https://github.com/fastapi-admin/fastapi-admin.git', branch = 'develop' }
```
