import unittest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..payload_factories import PayloadRequestFactory


@api_view(['POST'])
def view(request):
    """
    Testing stub view to return Request's data and GitHub event header.
    """
    return Response({
        'header_github_event': request.META.get('HTTP_X_GITHUB_EVENT', ''),
        'request_data': request.data,
    })


class TestURL(unittest.TestCase):

    def test_default(self):
        """
        PayloadRequestFactory sets github webhook URL by default
        """
        result = PayloadRequestFactory()

        self.assertEqual(result.get_full_path(), '/api/github/')

    def test_default_data(self):
        """
        PayloadRequestFactory default URL is included in payload
        """
        request = PayloadRequestFactory()

        result = view(request)

        expected_url = 'http://testserver/api/github/'
        self.assertEqual(result.data['request_data']['hook']['config']['url'], expected_url)
        self.assertEqual(result.data['header_github_event'], 'ping')
