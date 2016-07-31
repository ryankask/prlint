from django.test import TestCase

from ...factories import WebhookPayloadFactory


class TestWebhookPayloadFactory(TestCase):

    def test_happy(self):
        """
        WebhookPayloadFactory creates a default payload
        """
        result = WebhookPayloadFactory()

        self.assertIsInstance(result, dict)
        self.assertGreater(result['zen'], '')
        self.assertIsInstance(result['hook_id'], int)
        self.assertGreater(result['hook_id'], 0)
        self.assertEqual(result['hook']['events'], ['pull_request'])

    def test_custom(self):
        result = WebhookPayloadFactory(
            hook_events=['a', 'b', 'c']
        )

        self.assertEqual(result['hook']['events'], ['a', 'b', 'c'])
