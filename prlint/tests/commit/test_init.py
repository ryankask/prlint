import unittest

from nofixup.commit import Commit


class TestInit(unittest.TestCase):

    def test_bad_empty(self):
        """
        Commit can't be initialised with no args
        """
        with self.assertRaises(TypeError):
            Commit()

    def test_bad_json_raises(self):
        """
        Commit initialisation will fail with data that's not JSON-like
        """
        with self.assertRaises(ValueError):
            Commit('hello World!')

    def test_happy(self):
        """
        Commit is initialised and data kept
        """
        json_str = '{"sha": "__TEST__"}'

        result = Commit(json_str)

        self.assertEqual(result.data['sha'], '__TEST__')
