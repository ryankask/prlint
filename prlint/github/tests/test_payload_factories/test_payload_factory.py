import unittest

from django.http import HttpRequest

from ..payload_factories import PayloadRequestFactory


class TestPayloadRequestFactory(unittest.TestCase):

    def test_default(self):
        """
        PayloadRequestFactory defaults to a request with pull_request event
        """
        result = PayloadRequestFactory()

        self.assertIsInstance(result, HttpRequest)
        self.assertEqual(result.META['HTTP_X_GITHUB_EVENT'], 'pull_request')
        data = result.POST
        self.assertEqual(data, {})
