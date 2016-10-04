import unittest

from ..payload_factories import PingEventFactory
from .view_stubs import view


@unittest.skip('TODO: load a payload and test it')
class TestPingEventFactory(unittest.TestCase):

    def test_default(self):
        """
        PingEventFactory generates ping event payloads
        """
        request = PingEventFactory()

        result = view(request)

        self.assertEqual(result.data['header_github_event'], 'ping')

    def test_hook_events(self):
        """
        PingEventFactory sets hook events from kwarg
        """
        request = PingEventFactory(data__hook__events=['*'])

        result = view(request)

        self.assertEqual(result.data['request_data']['hook']['events'], ['*'])
