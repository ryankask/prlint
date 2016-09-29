from django.test import RequestFactory, TestCase

from ..payload_factories import HookConfigPayloadFactory


class TestHookConfigPayloadFactory(TestCase):

    request_factory = RequestFactory()

    def test_request(self):
        """
        HookPayloadFactory generates full default URI if passed request
        """
        request = self.request_factory.get('/')

        result = HookConfigPayloadFactory(request=request)

        self.assertEqual(result['url'], 'http://testserver/__HOOK_URL__/')

    def test_request_url(self):
        """
        HookPayloadFactory generates full custom URI if passed request
        """
        request = self.request_factory.get('/')

        result = HookConfigPayloadFactory(request=request, hook_url='/github/')

        self.assertEqual(result['url'], 'http://testserver/github/')
