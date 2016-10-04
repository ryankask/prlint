from .view_stubs import view
import unittest
from ..payload_factories import PingEventFactory


class TestPingEventFactory(unittest.TestCase):

    def test_default(self):
        """
        PingEventFactory generates ping event payloads
        """
        request = PingEventFactory()

        result = view(request)

        self.assertEqual(result.data['header_github_event'], 'ping')
