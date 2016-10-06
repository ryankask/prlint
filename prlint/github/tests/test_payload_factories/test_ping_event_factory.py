import unittest

from ..payload_factories import PingEventFactory
from .view_stubs import view


class TestPingEventFactory(unittest.TestCase):

    def test_default_request(self):
        """
        PingEventFactory generates request with expected URL
        """
        result = PingEventFactory()

        self.assertEqual(result.get_raw_uri(), 'http://testserver/api/github/')

    def test_default(self):
        """
        PingEventFactory generates ping event payloads
        """
        request = PingEventFactory()

        result = view(request)

        expected_uri = 'http://testserver/api/github/'
        self.assertEqual(result.data['request_data']['hook']['config']['url'], expected_uri)
        self.assertEqual(result.data['header_github_event'], 'ping')
        self.assertEqual(result.data['request_data']['hook_id'], result.data['request_data']['hook']['id'])

    def test_hook_events(self):
        """
        PingEventFactory sets hook events from kwarg
        """
        request = PingEventFactory(hook__events=['*'])

        result = view(request)

        self.assertEqual(result.data['request_data']['hook']['events'], ['*'])

    def test_repository_id(self):
        """
        PingEventFactory passes respository ID through to repo payload fac
        """
        request = PingEventFactory(repository__id=999)

        result = view(request)

        self.assertEqual(result.data['request_data']['repository']['id'], 999)

    def test_passed_url(self):
        """
        PingEventFactory raises if passed a custom URI
        """
        with self.assertRaises(TypeError):
            PingEventFactory(hook__config__url='http://noserver/x/')
