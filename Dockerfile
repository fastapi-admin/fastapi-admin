FROM jfloff/alpine-python
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN mkdir -p /fastapi-admin
WORKDIR /fastapi-admin
COPY pyproject.toml poetry.lock /fastapi-admin/
RUN pip install --upgrade pip
RUN pip3 install poetry
ENV POETRY_VIRTUALENVS_CREATE false
RUN poetry install --no-root
COPY . /fastapi-admin
RUN poetry install
RUN make compile
