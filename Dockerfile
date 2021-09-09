FROM jfloff/alpine-python
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
WORKDIR /tmp
ADD pyproject.toml .
ADD poetry.lock .
RUN poetry install --no-root
WORKDIR /fastapi-admin
