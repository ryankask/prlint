from django.test import TestCase

from ..payload_factories import RepositoryPayloadFactory


class TestRepositoryPayloadFactory(TestCase):

    def test_default(self):
        """
        RepositoryPayloadFactory creates default payload
        """
        result = RepositoryPayloadFactory()

        self.assertGreater(result['id'], 999)
        self.assertGreater(result['name'], '')

    def test_no_id(self):
        """
        RepositoryPayloadFactory generates repo ID when None is passed
        """
        result = RepositoryPayloadFactory(repository_id=None)

        self.assertGreater(result['id'], 999)

    def test_with_id(self):
        """
        RepositoryPayloadFactory uses passed repo ID
        """
        result = RepositoryPayloadFactory(repository_id='__REPO_ID__')

        self.assertEqual(result['id'], '__REPO_ID__')
