import unittest

import hypothesis.strategies as st
from django.test import RequestFactory
from hypothesis import assume, example, given

from ...serializers import HeaderSerializer
from ..payload_factories import PayloadRequestFactory


class TestHeaderSerializer(unittest.TestCase):

    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.post('/api/github/')

    def test_default_missing(self):
        """
        HeaderSerializer is invalid given request with no X-GitHub-Event
        """
        serializer = HeaderSerializer(self.request)

        result = serializer.is_valid()

        self.assertFalse(result)

    @given(st.sampled_from(('ping', 'pull_request')))
    def test_valid(self, event):
        """
        HeaderSerializer is valid with pull_request or ping
        """
        self.request.META['HTTP_X_GITHUB_EVENT'] = event
        serializer = HeaderSerializer(self.request)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.event, event)

    @given(st.text())
    @example(' pull_request ')
    def test_invalid(self, event):
        """
        HeaderSerializer is invalid with event strings not pull_request or ping
        """
        assume(event not in ('pull_request', 'ping'))
        self.request.META['HTTP_X_GITHUB_EVENT'] = event
        serializer = HeaderSerializer(self.request)

        result = serializer.is_valid()

        self.assertFalse(result)

    def test_invalid_event_raises(self):
        """
        HeaderSerializer raises AssertionError when invalid and event is loaded
        """
        serializer = HeaderSerializer(self.request)

        with self.assertRaises(AssertionError):
            serializer.event

    @given(st.sampled_from(('ping', 'pull_request')))
    def test_request_factory_serializable(self, event):
        """
        HeaderSerializer is valid for Requests built by PayloadRequestFactory
        """
        request = PayloadRequestFactory({}, event)
        serializer = HeaderSerializer(request)

        result = serializer.is_valid()

        self.assertTrue(result, serializer.errors)
