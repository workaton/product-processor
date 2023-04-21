SHELL=/bin/sh
PYTHON_BIN=/usr/bin/env python3
VENV=.venv

.PHONY: all build dev lint test clean

all: build

${VENV}:
	${PYTHON_BIN} -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip setuptools wheel

build: ${VENV}
	${VENV}/bin/pip install .

dev: ${VENV}
	source ${VENV}/bin/activate; poetry install -v

lint: dev
	${VENV}/bin/flake8 app tests
	${VENV}/bin/mypy --ignore-missing-imports app tests

test: dev
	${VENV}/bin/pytest -W ignore::pytest.PytestDeprecationWarning --cov ngitws --cov-report term --cov-report html:coverage --junitxml junit.xml tests

clean:
	rm -rf ${VENV}
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.py[co]' -exec rm -f {} +
	rm -rf .cache .coverage .eggs .mypy_cache .pytest_cache coverage dist junit.xml
