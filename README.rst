.. image:: https://circleci.com/gh/jamescooke/prlint.svg?style=svg
    :target: https://circleci.com/gh/jamescooke/prlint

Install
=======

Clone this repository.

Create a virtualenv containing Python3::

    make venv

Activate and install requirements::

    . venv/bin/activate
    make requirements

Testing
=======

While in virtualenv, add the testing requirements::

    make requirements-test

Run tests with Django's test runner which is configured to use Nose::

    make test

Check linting with ``flake8``::

    cd prlint
    make flake
