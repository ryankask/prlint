.PHONY: all venv install install-test requirements

# Update all requirements, test and lint project
all: install-test
	$(MAKE) -C prlint/ lint test

# Bootstrap virtualenv
venv:
	virtualenv venv --python=python3
	. venv/bin/activate && pip install -U pip

install:
	pip install -r requirements/base.txt

install-test:
	pip install -r requirements/test.txt

requirements:
	$(MAKE) -C requirements
