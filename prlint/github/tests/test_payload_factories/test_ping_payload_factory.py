from django.test import RequestFactory, TestCase

from ...serializers import RepositoryPayloadSerializer
from ..payload_factories import PingPayloadFactory


class TestPingPayloadFactory(TestCase):

    request_factory = RequestFactory()

    def test_default(self):
        """
        PingPayloadFactory creates a default payload
        """
        result = PingPayloadFactory()

        self.assertIsInstance(result, dict)
        self.assertGreater(result['zen'], '')
        self.assertIsInstance(result['hook_id'], int)
        self.assertGreater(result['hook_id'], 0)
        self.assertEqual(result['hook']['events'], ['pull_request'])
        self.assertEqual(result['hook']['config']['url'], 'http://noserver/__HOOK_URL__/')
        self.assertGreater(result['repository']['id'], 1000)

    def test_custom(self):
        """
        PingPayloadFactory can generate custom events
        """
        result = PingPayloadFactory(
            hook__events=['a', 'b', 'c']
        )

        self.assertEqual(result['hook']['events'], ['a', 'b', 'c'])

    def test_url(self):
        """
        PingPayloadFactory generates custom URLs
        """
        result = PingPayloadFactory(hook__config__url='http://testserver/github/')

        self.assertEqual(result['hook']['config']['url'], 'http://testserver/github/')

    def test_custom_repo(self):
        """
        PingPayloadFactory passes repository ID through to repo factory
        """
        result = PingPayloadFactory(repository__id=999)

        self.assertEqual(result['repository']['id'], 999)
