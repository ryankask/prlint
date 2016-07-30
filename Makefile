.PHONY: venv install install-test requirements test lint

venv:
	virtualenv venv --python=python3
	. venv/bin/activate && pip install pip==8.1.1  # Pin pip to pip-tools required version

install:
	pip install -r requirements/base.txt

install-test:
	pip install -r requirements/test.txt

requirements:
	$(MAKE) -C requirements

test:
	$(MAKE) -C prlint

lint:
	isort -rc --diff prlint/ > isort.out
	if [ "$$(wc -l isort.out)" != "1 isort.out" ]; then cat isort.out; exit 1; fi
	flake8 prlint/prlint
