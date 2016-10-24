from hypothesis.extra.django import TestCase

from ...factories import RepositoryFactory
from ...serializers import RepositoryPayloadSerializer, RepositorySerializer
from ..payload_factories import (
    PingPayloadFactory,
    PullRequestEventPayloadFactory,
)


class TestRepositoryPayloadSerializer(TestCase):

    def setUp(self):
        """
        Create valid and invalid repository payloads for stuffing inside a
        request data.
        """
        RepositoryFactory(remote_id=1234)
        self.valid_repository = {
            'id': 1234,
        }
        self.invalid_repository = {
            'id': 4321,
        }

    def test_set_up(self):
        """
        setUp: Valid repo payload is valid, invalid is invalid
        """
        self.assertTrue(RepositorySerializer(data=self.valid_repository).is_valid())
        self.assertFalse(RepositorySerializer(data=self.invalid_repository).is_valid())

    def test_happy(self):
        """
        RepositoryPayloadSerializer contains a valid Repository is valid
        """
        data = {
            'repository': self.valid_repository,
        }
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result)

    def test_unhappy(self):
        """
        RepositoryPayloadSerializer contains an invalid Repository is invalid
        """
        data = {
            'repository': self.invalid_repository,
        }
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('repository', serializer.errors)
        message = serializer.errors['repository']['id'][0]
        self.assertIn('id "4321" is not registered with prlint', message)

    def test_ping_factory_serializable(self):
        """
        RepositoryPayloadSerializer is valid with default PingPayloadFactory
        """
        repo = RepositoryFactory()
        data = PingPayloadFactory(repository__id=repo.remote_id)
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result, serializer.errors)

    def test_pull_request_factory_serializable(self):
        """
        RepositoryPayloadSerializer valid with PullRequestEventPayloadFactory
        """
        repo = RepositoryFactory()
        data = PullRequestEventPayloadFactory(repository__id=repo.remote_id)
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result, serializer.errors)
