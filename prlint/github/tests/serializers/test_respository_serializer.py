import hypothesis.strategies as st
from hypothesis import assume, example, given
from hypothesis.extra.django import TestCase

from ...factories import RepositoryFactory
from ...models import Repository
from ...serializers import RepositoryPayloadSerializer, RepositorySerializer


class TestRepositoryPayloadSerializer(TestCase):

    def setUp(self):
        """
        Create valid and invalid repository payloads for stuffing inside a
        request data.
        """
        RepositoryFactory(remote_id=1234)
        self.valid_repository = {
            'id': 1234,
        }
        self.invalid_repository = {
            'id': 4321,
        }

    def test_set_up(self):
        """
        setUp: Valid repo payload is valid, invalid is invalid
        """
        self.assertTrue(RepositorySerializer(data=self.valid_repository).is_valid())
        self.assertFalse(RepositorySerializer(data=self.invalid_repository).is_valid())

    def test_happy(self):
        """
        RepositoryPayloadSerializer contains a valid Repository is valid
        """
        data = {
            'repository': self.valid_repository,
        }
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result)

    def test_unhappy(self):
        """
        RepositoryPayloadSerializer contains an invalid Repository is invalid
        """
        data = {
            'repository': self.invalid_repository,
        }
        serializer = RepositoryPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('repository', serializer.errors)
        message = serializer.errors['repository']['id'][0]
        self.assertIn('id "4321" is not registered with prlint', message)


class TestRepositorySerializer(TestCase):

    def test_set_up(self):
        """
        setUp: No repositories in database
        """
        self.assertEqual(Repository.objects.count(), 0)

    @given(
        st.dictionaries(st.characters(), st.text()),
        st.integers(min_value=1000, max_value=999999),
    )
    def test_valid(self, data, repo_id):
        """
        RepositorySerializer is valid if Repository with provided ID is saved

        Constraints on repository ID match those of the factory.
        """
        assume('id' not in data)
        data['id'] = repo_id
        RepositoryFactory(remote_id=repo_id)
        serializer = RepositorySerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result)

    @given(st.characters())
    @example('')
    def test_invalid_not_int(self, repo_id):
        """
        RepositorySerializer is invalid with repository ID that's not an int
        """
        assume(not repo_id.isdigit())
        data = {'id': repo_id}
        serializer = RepositorySerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('valid integer', serializer.errors['id'][0])

    @given(st.integers())
    def test_invalid_out_of_range(self, repo_id):
        """
        RepositorySerializer is invalid if repository id is not in range

        Message options from DRF are "greater than or equal to" or "less than
        or equal to" so check for common "or equal to".
        """
        assume(1000 > repo_id or repo_id > 2**32)
        data = {'id': repo_id}
        serializer = RepositorySerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('or equal to', serializer.errors['id'][0])

    @given(
        st.dictionaries(st.characters(), st.text()),
        st.integers(min_value=1000, max_value=2**32),
    )
    def test_invalid_missing(self, data, repo_id):
        """
        RepositorySerializer is invalid if repository does not exist in db

        Given that 'id' is not a key in the data dictionary, set it to the
        provided value, or don't set it at all for the None example.
        """
        assume('id' not in data)
        data['id'] = repo_id
        serializer = RepositorySerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('id "{}" is not registered'.format(repo_id), str(serializer.errors))

    @given(st.dictionaries(st.characters(), st.text()))
    def test_invalid_no_id(self, data):
        """
        RepositorySerializer is invalid with no ID provided for repository
        """
        assume('id' not in data)
        serializer = RepositorySerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertIn('id', serializer.errors)
        self.assertIn('required', serializer.errors['id'][0])
