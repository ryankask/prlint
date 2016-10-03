import unittest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

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


class TestPayloadRequestFactory(unittest.TestCase):

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
