from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from factory_djoy import UserFactory

from ...factories import RepositoryFactory
from ...models import Repository


class TestRespositoryFactory(TestCase):

    user_model = get_user_model()

    def test_create_single(self):
        """
        RepositoryFactory can make a single instance
        """
        result = RepositoryFactory()

        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(self.user_model.objects.count(), 1)
        created_repo = Repository.objects.first()
        self.assertGreater(created_repo.remote_id, 999)
        self.assertGreater(1000000, created_repo.remote_id)
        expected_end = '/{}'.format(created_repo.name)
        self.assertEndsWith(created_repo.full_name, expected_end)

    def test_create_single_existing(self):
        """
        RepositoryFactory fails if user already exists
        """
        UserFactory(username='user1')

        with self.assertRaises(IntegrityError):
            RepositoryFactory(creator__username='user1')

    def test_create_multi(self):
        """
        RepositoryFactory can make multiple instances with default values
        """
        RepositoryFactory.create_batch(2)

        self.assertEqual(Repository.objects.count(), 2)
        self.assertEqual(self.user_model.objects.count(), 2)
        repo_first = Repository.objects.first()
        repo_last = Repository.objects.last()
        for varname in ('creator', 'uuid', 'remote_id', 'name', 'full_name'):
            self.assertNotEqual(
                getattr(repo_first, varname),
                getattr(repo_last, varname),
                'Both users found to have same "{}" attribute'.format(varname)
            )

    # --- helpers ---

    def assertEndsWith(self, string, substring):
        message = '"{}" does not end with "{}"'.format(string, substring)
        self.assertEqual(string[-len(substring):], substring, message)
