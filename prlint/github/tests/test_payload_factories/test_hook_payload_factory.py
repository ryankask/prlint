from django.test import RequestFactory, TestCase

from ..payload_factories import HookPayloadFactory


class TestHookPayloadFactory(TestCase):

    request_factory = RequestFactory()

    def test_default(self):
        """
        HookPayloadFactory generates default payload without request
        """
        result = HookPayloadFactory()

        self.assertEqual(result['config']['url'], 'http://noserver/__HOOK_URL__/')
        self.assertEqual(result['events'], ['pull_request'])

    def test_request(self):
        """
        HookPayloadFactory generates full URI when request is provided
        """
        request = self.request_factory.get('/')

        result = HookPayloadFactory(request=request)

        self.assertEqual(result['config']['url'], 'http://testserver/__HOOK_URL__/')

    def test_request_hook_url(self):
        """
        HookPayloadFactory uses request and hook_url to generate full URI
        """
        request = self.request_factory.get('/')

        result = HookPayloadFactory(request=request, hook_url='/github/')

        self.assertEqual(result['config']['url'], 'http://testserver/github/')
