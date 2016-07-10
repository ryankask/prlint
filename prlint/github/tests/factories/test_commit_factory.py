from django.test import TestCase

from ...factories import CommitFactory
from ...models import Commit


class TestCommitFactory(TestCase):

    def test_create_single(self):
        """
        CommitFactory creates single Commits
        """
        result = CommitFactory()

    def test_create_multi(self):
        """
        CommitFactory creates multiple instances with default values
        """
        result = CommitFactory.create_batch(3)

        self.assertEqual(set(Commit.objects.all()), set(result))

    def test_create_url(self):
        """
        CommitFactory builds a URL from the repo and sha of commit
        """
        commit = CommitFactory(
            sha='aaabbb1234',
            pull_request__repository__full_name='TESTUSER/TESTREPO'
        )

        result = commit.html_url

        self.assertEqual(result, 'https://github.com/TESTUSER/TESTREPO/commit/aaabbb1234')
