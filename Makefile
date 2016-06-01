.PHONY: venv install install-test requirements test lint

venv:
	virtualenv venv --python=python3
	. venv/bin/activate && pip install pip==8.1.1  # Pin pip to pip-tools required version

install:
	pip install -r requirements/base.txt

install-test: install
	pip install -r requirements/test.txt

requirements:
	$(MAKE) -C requirements

test:
	$(MAKE) -C prlint

lint:
	flake8 prlint/prlint
