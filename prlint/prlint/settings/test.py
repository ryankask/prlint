from .base import *  # NOQA

INSTALLED_APPS += [
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nologcapture',
    '--with-doctest',
    '--with-yanc',
]
