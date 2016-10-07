import unittest

from ..payload_factories import PullRequestEventPayloadFactory


class TestPullRequestEventPayloadFactory(unittest.TestCase):

    def test_default(self):
        """
        PullRequestEventPayloadFactory generates default pull request payload
        """
        result = PullRequestEventPayloadFactory()

        expected_keys = ('action', 'number', 'pull_request')
        for key in expected_keys:
            self.assertIn(key, result)
