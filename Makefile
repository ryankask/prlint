venv:
	virtualenv venv --python=python3

requirements:
	pip install --upgrade pip==8.1.1  # pip-tools can't use latest pip until 1.7
	pip install -r requirements/base.txt

requirements-test: requirements
	pip install -r requirements/test.txt

flake8:
	flake8 prlint

requirements-compile:
	pip-compile --output-file requirements/base.txt requirements/base.in

.PHONY: venv requirements requirements-test requirements-compile flake8
