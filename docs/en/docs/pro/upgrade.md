# Upgrade from the open source version

It's so easy to upgrade `fastapi-admin` open source version to pro version, because pro version contains all of open
source and has same project structure.

1. Uninstall open source version.

    ```shell
    > pip uninstall fastapi-admin
    ```

2. Install pro version.

    ```shell
    > pip install git+https://${GH_TOKEN}@github.com/fastapi-admin/fastapi-admin-pro.git
    ```

That's all, then you can add pro version exclusive content yourself without any code change.

And you can also see the pro version [examples](https://github.com/fastapi-admin/fastapi-admin-pro/tree/dev/examples)
for reference.
