from django.test import TestCase

from ...serializers import PingPayloadSerializer
from ..payload_factories import PingPayloadFactory


class TestPingPayloadSerializer(TestCase):

    def test_default(self):
        """
        PingPayloadSerializer validates default PingPayloadFactory data
        """
        data = PingPayloadFactory()
        serializer = PingPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertTrue(result, serializer.errors)

    def test_all_events(self):
        """
        PingPayloadSerializer is invalid with all '*' events
        """
        data = PingPayloadFactory(hook_events=['*'])
        serializer = PingPayloadSerializer(data=data)

        result = serializer.is_valid()

        self.assertFalse(result)
