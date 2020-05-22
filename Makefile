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

deps:
	@pip install -r requirements-dev.txt

style: deps
	isort -rc $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
ifneq ($(shell which black),)
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
endif
	flake8 $(checkfiles)
	mypy $(checkfiles)
	pylint -d C,W,R $(checkfiles)
	bandit -r $(checkfiles)
	python setup.py check -mrs

test: deps
	$(py_warn) py.test

publish: deps
	rm -fR dist/
	python setup.py sdist
	twine upload dist/*

ci:
	@act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -b