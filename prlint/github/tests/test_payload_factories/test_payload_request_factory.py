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
