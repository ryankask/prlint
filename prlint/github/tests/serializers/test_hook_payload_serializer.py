import unittest

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

    def test_no_events(self):
        """
        HookPayloadSerializer is invalid with empty list of events
        """
        data = {
            'events': [],
        }
        serializer = HookPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(list(serializer.errors), ['events'])

    def test_single(self):
        """
        HookPayloadSerializer is valid with "pull_request" event
        """
        data = {
            'events': ['*'],
        }
        serializer = HookPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result)
