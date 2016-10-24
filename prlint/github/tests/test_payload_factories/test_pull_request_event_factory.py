import unittest

from ..payload_factories import PullRequestEventFactory
from .view_stubs import view


class TestPullRequestEventFactory(unittest.TestCase):

    def test_default_request(self):
        """
        PullRequestEventFactory generates request with expected URL
        """
        result = PullRequestEventFactory()

        self.assertEqual(result.get_raw_uri(), 'http://testserver/api/github/')

    def test_default(self):
        """
        PullRequestEventFactory generates pull request event payloads
        """
        request = PullRequestEventFactory()

        result = view(request)

        self.assertEqual(result.data['header_github_event'], 'pull_request')
        self.assertIn('action', result.data['request_data'])

    def test_set_repo_id(self):
        """
        PullRequestEventFactory passes through repository's remote ID
        """
        request = PullRequestEventFactory(repository__id='__REMOTE_ID__')

        result = view(request)

        self.assertEqual(result.data['request_data']['repository']['id'], '__REMOTE_ID__')
