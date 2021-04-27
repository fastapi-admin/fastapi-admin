# Installation

## From pypi

You can install from pypi.

```shell
> pip install fastapi-admin
```

## From source

Or you can install from source with latest code.

```shell
> pip install git+https://github.com/fastapi-admin/fastapi-admin.git
```

### With requirements.txt

Add the following line.

```shell
-e https://github.com/fastapi-admin/fastapi-admin.git@develop#egg=fastapi-admin
```

### With poetry

Add the following line in section `[tool.poetry.dependencies]`.

```toml
fastapi-admin = { git = 'https://github.com/fastapi-admin/fastapi-admin.git', branch = 'develop' }
```
