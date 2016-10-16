import unittest

from ..payload_factories import PullRequestPayloadFactory


class TestPullRequestPayloadFactory(unittest.TestCase):

    def test_default(self):
        """
        PullRequestPayloadFactory generates expected data by default
        """
        result = PullRequestPayloadFactory()

        expected_keys = ('id', 'number', 'state', 'commits_url', 'commits')
        for key in expected_keys:
            self.assertIn(key, result)
