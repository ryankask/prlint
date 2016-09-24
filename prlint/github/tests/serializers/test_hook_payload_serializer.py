import unittest

import hypothesis.strategies as st
from hypothesis import example, given

from ...serializers import HookPayloadSerializer


class TestHookPayloadSerializer(unittest.TestCase):

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

    @given(st.lists(st.text()).filter(lambda x: x != ['pull_request']))
    @example(['*'])
    @example([])
    def test_all_fail(self, events):
        """
        HookPayloadSerializer invalid for lists of strings that are not pull_request
        """
        data = {
            'events': events,
        }
        serializer = HookPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
