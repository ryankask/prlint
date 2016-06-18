import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from ...factories import RepositoryFactory
from ...models import PullRequest


class TestPullRequest(TestCase):

    def test_create(self):
        """
        PullRequest can be saved to database
        """
        repo = RepositoryFactory()
        pr = PullRequest(
            repository=repo,
        )

        result = pr.save()

        self.assertIsNone(result)
        self.assertEqual(PullRequest.objects.count(), 1)
        self.assertEqual(pr, PullRequest.objects.first())
        self.assertEqual(repo.pullrequest_set.count(), 1)

    def test_clean(self):
        """
        PullRequest model must be instantiated with title
        """
        pr = PullRequest(
            repository=RepositoryFactory(),
        )

        with self.assertRaises(ValidationError) as cm:
            pr.full_clean()

        self.assertEqual(list(cm.exception.error_dict.keys()), ['title'])

    def test_uuid_permanent(self):
        """
        PullRequest model instance can not have its uuid altered

        Trusts:
            test_signals: A helpful message is raised.
        """
        repo = PullRequest.objects.create(
            repository=RepositoryFactory(),
        )
        repo.uuid = uuid.uuid4()

        with self.assertRaises(ValidationError):
            repo.save()
