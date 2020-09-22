checkfiles = fastapi_admin/ examples/ tests/
black_opts = -l 100 -t py38
py_warn = PYTHONDEVMODE=1

help:
	@echo "FastAPI-Admin development makefile"
	@echo
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    deps		Ensure dev/test dependencies are installed"
	@echo  "    check		Checks that build is sane"
	@echo  "    lint		Reports all linter violations"
	@echo  "    test		Runs all tests"
	@echo  "    style		Auto-formats the code"

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
	bandit -r $(checkfiles)

test: deps
	$(py_warn) py.test

build: deps
	@poetry build

docs: deps
	@mkdocs build

deploy-docs: docs
	@mkdocs gh-deploy
