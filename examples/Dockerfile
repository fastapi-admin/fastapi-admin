FROM python:3
RUN mkdir -p /src
WORKDIR /src
COPY ../pyproject.toml ../poetry.lock /src/
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
RUN poetry install --no-root
COPY . /src

