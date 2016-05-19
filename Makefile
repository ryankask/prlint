venv:
	virtualenv venv --python=python3

requirements:
	pip install --upgrade pip==8.1.1  # pip-tools can't use latest pip until 1.7
	pip install -r requirements/base.txt

requirements-test: requirements
	pip install -r requirements/test.txt

requirements-compile:
	pip-compile --output-file requirements/base.txt requirements/base.in

test:
	$(MAKE) -C prlint

.PHONY: venv requirements requirements-test requirements-compile test
