.PHONY: test lint isort

test:
	./manage.py test --settings=prlint.settings.test

lint:
	isort -rc --diff > isort.out
	if [ "$$(wc -l isort.out)" != "1 isort.out" ]; then cat isort.out; exit 1; fi
	flake8 prlint

# Update all import sorting
isort:
	isort -rc prlint/
