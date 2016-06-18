from django.test import TestCase

from ...factories import PullRequestFactory
from ...models import PullRequest


class TestPullRequestFactory(TestCase):

    def test_create_single(self):
        """
        PullRequestFactory can create single Pull Request
        """
        result = PullRequestFactory()

        self.assertEqual(PullRequest.objects.count(), 1)
        created_pr = PullRequest.objects.first()
        self.assertEqual(created_pr, result)
        self.assertEqual(created_pr.body, '')
        self.assertGreater(created_pr.title, '')

    def test_create_multi(self):
        """
        PullRequestFactory can create multiple instances with default values
        """
        result = PullRequestFactory.create_batch(3)

        self.assertEqual(set(PullRequest.objects.all()), set(result))
