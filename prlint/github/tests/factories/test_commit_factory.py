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
