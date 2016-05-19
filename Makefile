venv:
	virtualenv venv --python=python3

requirements:
	pip install -U pip
	pip install -r requirements.txt

requirements-test: requirements
	pip install -r test-requirements.txt

flake8:
	flake8 prlint

.PHONY: venv requirements requirements-test flake8
