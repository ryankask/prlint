from django.core.exceptions import ValidationError
from django.test import TestCase

from ...factories import PullRequestFactory
from ...models import Commit


class TestCommit(TestCase):

    def test_create(self):
        """
        Commit can be saved to database
        """
        commit = Commit(
            pull_request=PullRequestFactory(),
        )

        result = commit.save()

        self.assertIsNone(result)
        self.assertEqual(Commit.objects.count(), 1)
        self.assertEqual(commit, Commit.objects.first())

    def test_clean(self):
        """
        Commit requires sha, url and message at full_clean time
        """
        commit = Commit(
            pull_request=PullRequestFactory(),
        )

        with self.assertRaises(ValidationError) as cm:
            commit.full_clean()

        self.assertEqual(set(cm.exception.error_dict.keys()), set(['sha', 'html_url', 'message']))
