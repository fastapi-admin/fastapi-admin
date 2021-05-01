checkfiles = fastapi_admin/ tests/ examples/ conftest.py
black_opts = -l 100 -t py38
py_warn = PYTHONDEVMODE=1
locales = fastapi_admin/locales

up:
	@poetry update

deps:
	@poetry install --no-root

style: deps
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	flake8 $(checkfiles)
	mypy $(checkfiles)
	pylint $(checkfiles)

test: deps
	$(py_warn) py.test

build: deps
	@poetry build

ci: check test

# i18n
extract:
	@pybabel extract -F babel.cfg -o $(locales)/messages.pot ./

update:
	@pybabel update -d $(locales) -i $(locales)/messages.pot

compile:
	@pybabel compile -d $(locales)

babel: extract update
