import unittest

from nofixup.commit import Commit
from nofixup.exceptions import BadData


class TestValidate(unittest.TestCase):

    def test_bad_empty(self):
        """
        Commit was initialised with missing data, validation raises
        """
        commit = Commit('{}')

        with self.assertRaises(BadData):
            commit.validate()

    def test_valid(self):
        """
        Commit message is normal - commit is valid
        """
        data = '''
            {
                "commit": {
                    "message": "Add a test document"
                }
            }
        '''
        commit = Commit(data)

        result = commit.validate()

        self.assertEqual(result, True)

    def test_invalid(self):
        """
        Commit message starts with 'fixup! ' and is invalid
        """
        data = '''
            {
                "commit": {
                    "message": "fixup! Add new test document section"
                }
            }
        '''
        commit = Commit(data)

        result = commit.validate()

        self.assertEqual(result, False)
