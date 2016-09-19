from rest_framework import serializers


class HookPayloadSerializer(serializers.Serializer):
    """
    Serializes incoming JSON from Github that matches the Payload spec

    See https://developer.github.com/webhooks/#payloads
    """
    # repository = RepositorySerializer(

    events = serializers.ListField(child=serializers.CharField(
        min_length=1,
    ))

    def validate_events(self, value):
        """
        Must be at least 1 event
        """
        if len(value) < 1:
            raise serializers.ValidationError('No events passed')
        return value
