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

Run tests with nose::

    nosetests

Check linting with flake8::

    make flake8
