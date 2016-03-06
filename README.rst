Install
=======

Clone this repository.

Create a virtualenv containing Python3::

    virtualenv venv --python=python3

Activate and install requirements::

    . venv/bin/activate
    pip install -r requirements.txt

Testing
=======

While in virtualenv, add the testing requirements::

    pip install -r test-requirements.txt

Run tests with nose::

    nosetests
