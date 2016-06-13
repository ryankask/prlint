from django.test import TestCase

from ...models import PullRequest


class TestPullRequest(TestCase):

    def test_clean(self):
        """
        PullRequest model must be instantiated with 
        """
