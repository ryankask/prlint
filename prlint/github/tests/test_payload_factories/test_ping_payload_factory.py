from django.test import TestCase

from ..payload_factories import PingPayloadFactory


class TestPingPayloadFactory(TestCase):

    def test_happy(self):
        """
        PingPayloadFactory creates a default payload
        """
        result = PingPayloadFactory()

        self.assertIsInstance(result, dict)
        self.assertGreater(result['zen'], '')
        self.assertIsInstance(result['hook_id'], int)
        self.assertGreater(result['hook_id'], 0)
        self.assertEqual(result['hook']['events'], ['pull_request'])
        # self.assertGreater(result['repository']['id'], 999)

    def test_custom(self):
        """
        PingPayloadFactory can generate custom events
        """
        result = PingPayloadFactory(
            hook_events=['a', 'b', 'c']
        )

        self.assertEqual(result['hook']['events'], ['a', 'b', 'c'])
