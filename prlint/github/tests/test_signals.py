from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import Mock

from ..factories import RepositoryFactory
from ..models import Repository
from ..signals import check_change_uuid


class TestSignals(TestCase):

    def test_happy_new(self):
        """
        check_change_uuid ignores unsaved Repository instance
        """
        repo = RepositoryFactory.build()

        result = check_change_uuid(Repository, repo)

        self.assertIsNone(result)

    def test_happy_same(self):
        """
        check_change_uuid ignores Repository instance where uuid is unchanged
        """
        repo = RepositoryFactory()

        result = check_change_uuid(Repository, repo)

        self.assertIsNone(result)

    def test_raises_changed(self):
        """
        check_change_uuid raises ValidationError if uuid has changed in inst
        """
        repo = RepositoryFactory()
        original_id = repo.uuid
        repo.uuid = '1234-4321'

        with self.assertRaises(ValidationError) as cm:
            check_change_uuid(Repository, repo)

        self.assertIn(str(original_id), cm.exception.message)
        self.assertIn(' 1234-4321', cm.exception.message)
