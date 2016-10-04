import unittest

from ..payload_factories import PayloadRequestFactory
from .view_stubs import view


class TestPayloadRequestFactory(unittest.TestCase):

    def test_default(self):
        """
        PayloadRequestFactory wraps passed data in a request
        """
        request = PayloadRequestFactory(
            event='__EVENT__',
            data={'__KEY__': '__VALUE__'}
        )

        result = view(request)

        self.assertEqual(result.data['header_github_event'], '__EVENT__')
        self.assertEqual(result.data['request_data'], {'__KEY__': '__VALUE__'})

    def test_url(self):
        """
        PayloadRequestFactory accepts custom URL
        """
        result = PayloadRequestFactory(event='', data={}, url='/__TEST__/')

        self.assertEqual(result.get_full_path(), '/__TEST__/')


@unittest.skip('move to PingEventFactory')
class TestXPayloadRequestFactory(unittest.TestCase):

    def test_default_data(self):
        """
        PayloadRequestFactory default URL is included in payload
        """
        request = PayloadRequestFactory()

        result = view(request)

        expected_url = 'http://testserver/api/github/'
        self.assertEqual(result.data['request_data']['hook']['config']['url'], expected_url)
        self.assertGreater(result.data['request_data']['repository']['id'], 1000)
        self.assertEqual(result.data['header_github_event'], 'ping')

    def test_repository_id(self):
        """
        PayloadRequestFactory passes respository ID through to repo payload fac
        """
        request = PayloadRequestFactory(repository_id=999)

        result = view(request)

        self.assertEqual(result.data['request_data']['repository']['id'], 999)

    def test_event_header(self):
        """
        PayloadRequestFactory sets header event from kwarg
        """
        request = PayloadRequestFactory(header__event='commit')

        result = view(request)

        self.assertEqual(result.data['header_github_event'], 'commit')

    def test_hook_events(self):
        """
        PayloadRequestFactory sets hook events from kwarg
        """
        request = PayloadRequestFactory(hook_events=['*'])

        result = view(request)

        self.assertEqual(result.data['request_data']['hook']['events'], ['*'])
