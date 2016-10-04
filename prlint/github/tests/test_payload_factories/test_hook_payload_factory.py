import unittest

from ..payload_factories import HookPayloadFactory


class TestHookPayloadFactory(unittest.TestCase):

    def test_default(self):
        """
        HookPayloadFactory generates default payload
        """
        result = HookPayloadFactory()

        self.assertEqual(result['config']['url'], 'http://noserver/__HOOK_URL__/')
        self.assertEqual(result['events'], ['pull_request'])

    def test_request_hook_url(self):
        """
        HookPayloadFactory passes config URL through to subfactory
        """
        result = HookPayloadFactory(config__url='__URL__')

        self.assertEqual(result['config']['url'], '__URL__')
