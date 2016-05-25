from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ...factories import RepositoryFactory


class TestFullCleanDjangoModelFactory(TestCase):
    """
    Assert that invalid Repository instances that could be created by factory
    are caught by full_clean called by FullCleanDjangoModelFactory.

    Trusts:
        test_repository_factory: Creating a Repository with the factory passes,
            therefore happy full_clean case is satisfied.
    """

    def test_missing_name(self):
        """
        FullCleanDjangoModelFactory accepts default state of RepositoryFactory
        """
        with self.assertRaises(ValidationError) as cm:
            RepositoryFactory(name=None)

        self.assertEqual(['name'], list(cm.exception.error_dict.keys()))
