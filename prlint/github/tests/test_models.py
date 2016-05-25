import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..factories import RepositoryFactory, UserFactory
from ..models import Repository


class TestModels(TestCase):

    def test_clean(self):
        """
        Repository model must have a name and full name
        """
        repo = Repository(
            remote_id=1,
            creator=UserFactory(),
        )

        with self.assertRaises(ValidationError) as cm:
            repo.full_clean()

        self.assertEqual(len(cm.exception.error_dict), 2)
        self.assertIn('name', cm.exception.error_dict.keys())
        self.assertIn('full_name', cm.exception.error_dict.keys())

    def test_uuid_permanent(self):
        """
        TODO Repository model instance can not have its uuid altered
        """
        repo = RepositoryFactory()
        original_id = repo.uuid
        repo.uuid = uuid.uuid4()
        repo.full_clean()

        result = repo.save()

        self.assertIsNone(result)
