import hypothesis.strategies as st
from hypothesis import assume, example, given
from hypothesis.extra.django import TestCase

from ...factories import RepositoryFactory
from ...serializers import HookPayloadSerializer
from ..payload_factories import PingPayloadFactory


class TestHookPayloadSerializer(TestCase):

    def test_empty(self):
        """
        HookPayloadSerializer is invalid with empty data
        """
        serializer = HookPayloadSerializer(data={})

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(list(serializer.errors), ['events'])

    def test_pull_request_valid(self):
        """
        HookPayloadSerializer is valid with "pull_request" event
        """
        data = {
            'events': ['pull_request'],
        }
        serializer = HookPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result)

    @given(st.lists(st.text()))
    @example(['*'])
    @example([])
    def test_all_fail(self, events):
        """
        HookPayloadSerializer invalid for lists of strings that are not pull_request
        """
        assume(events != ['pull_request'])
        data = {
            'events': events,
        }
        serializer = HookPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)

    def test_ping_factory_serializable(self):
        """
        HookPayloadSerializer is valid with default PingPayloadFactory
        """
        repo = RepositoryFactory()
        data = PingPayloadFactory(repository_id=repo.remote_id)
        serializer = HookPayloadSerializer(data=data['hook'])

        result = serializer.is_valid()

        self.assertTrue(result, serializer.errors)
