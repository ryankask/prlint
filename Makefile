venv:
	virtualenv venv --python=python3

requirements:
	pip install --upgrade pip==8.1.1  # pip-tools can't use latest pip until 1.7
	pip install -r requirements.txt

requirements-test: requirements
	pip install -r test-requirements.txt

flake8:
	flake8 prlint

.PHONY: venv requirements requirements-test flake8
